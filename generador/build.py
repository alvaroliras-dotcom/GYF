# -*- coding: utf-8 -*-
"""GYF-Rayo · Genera sitio/ entero a partir de contenido/. Orden: build.py → rematar.py → controles.py.
Uso:  python3 generador/build.py && python3 generador/rematar.py && python3 generador/controles.py

Piezas de Rayo (003 de la biblioteca, FICHA.md) sobre la base GYF (schema, sitemap, llms.txt, tarjeta de
llamada, estado en vivo, reseñas desde resenas.json, FAQ, mapa por CID, cookies y GTM).
Dónde está cada efecto: MAPA-DEL-TEMA.md."""
import html, json, math, os, re, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import datos
from datos import inline, esc
A = lambda x: html.escape(str(x), quote=True)
from config import (DOMINIO, NEGOCIO as N, SERVICIOS_HOME, SERVICIOS_SECCION, SERVICIOS_TITULO, SERVICIOS_TEXTO,
                    OPINIONES, URLS, PREFIJOS_MUNICIPIO, NOMBRE_CORTO, MUNICIPIOS, MUNICIPIO_ANCLA, CONTACTO_INDEXABLE,
                    LEGALES, CONTACTO_YA, BANDA_TIT, LLMS_PRINCIPALES, LLMS_MARCAS, TEXTOS, FICHA, MARCA, OBJETO_PORTADA,
                    CASOS, CASOS_VER, CINTA_PORTADA, CINTA_SECUNDARIA, CIFRAS, CIFRAS_EN, PASOS_ICONOS, ICONO_URL,
                    CTA_H2, CTA_ULTIMO, ZONA_H2, HORARIO_H2, CTA_EXTRA, texto)
import plantilla as T
import config as C

RAIZ = datos.RAIZ
SITIO = os.path.join(RAIZ, "sitio")
PAGINAS = datos.todas()
POR_URL = {p["url"]: p for p in PAGINAS}

# ---------- Municipios: los de config (MUNICIPIOS) y, si hay hub, los enlaces del hub ----------
PUEBLO = dict(MUNICIPIOS)
_PREF = "|".join(re.escape(x) for x in PREFIJOS_MUNICIPIO) or "(?!)"
if URLS.get("hub"):
    for t, b in POR_URL.get(URLS["hub"], {"bloques": []})["bloques"]:
        if t == "ul":
            for it in b:
                m = re.match(rf"\[(?:LINK )?(?:{_PREF}) ([^\]]+)\]\(({re.escape(URLS['municipio'])}[^)]+)\)", it)
                if m:
                    PUEBLO.setdefault(m.group(2), m.group(1))
BASE = N["localidad"]
NOMBRE_CORTO = dict(NOMBRE_CORTO)
ES_CTA = re.compile(CTA_H2, re.I)
ES_WIDGET = lambda c: c.startswith("(Widget de reseñas") or c.strip() == "[[RESEÑAS]]"


def nombre(url):
    return NOMBRE_CORTO.get(url) or PUEBLO.get(url) or url.strip("/")


def migas(url):
    if url == "/":
        return []
    cad = [("/", "Inicio")]
    if datos.tipo_de(url) == "municipio" and URLS.get("hub") and URLS["hub"] in POR_URL:
        cad.append((URLS["hub"], nombre(URLS["hub"])))
    else:
        partes = url.strip("/").split("/")
        for i in range(1, len(partes)):
            u = "/" + "/".join(partes[:i]) + "/"
            if u in POR_URL:
                cad.append((u, nombre(u)))
    cad.append((url, nombre(url)))
    return cad


def migas_html(url):
    c = migas(url)
    if not c:
        return ""
    li = [f'<li><a href="{u}">{esc(n)}</a></li>' if i < len(c) - 1 else f'<li aria-current="page">{esc(n)}</li>' for i, (u, n) in enumerate(c)]
    return f'<nav class="migas" aria-label="Migas de pan"><ol>{"".join(li)}</ol></nav>'


# ---------- Schema ----------
NEG_ID = DOMINIO + "/#negocio"


def negocio_schema():
    area = [BASE] + [v for k, v in PUEBLO.items() if v != BASE]
    d = {
        "@type": N["schema_tipo"], "@id": NEG_ID, "name": N["nombre_largo"],   # el nombre de la ficha (manda)
        "alternateName": N["nombre"],
        "url": DOMINIO + "/", "telephone": N["telefono_e164"], "email": N["email"],
        "logo": DOMINIO + "/marca/" + MARCA["simbolo"], "image": DOMINIO + "/og-image.jpg",
        "address": {"@type": "PostalAddress", "streetAddress": N["calle"], "postalCode": N["cp"],
                    "addressLocality": N["localidad"], "addressRegion": N["region"], "addressCountry": "ES"},
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": N["dias_schema"],
                                       "opens": N["abre"], "closes": N["cierra"]}],
        "areaServed": [{"@type": "City", "name": a, "containedInPlace": {"@type": "AdministrativeArea", "name": "Comunidad de Madrid"}}
                       for a in area],
        "aggregateRating": {"@type": "AggregateRating", "ratingValue": N["valoracion"].replace(",", "."),
                            "reviewCount": int(N["resenas"]), "bestRating": "5", "worstRating": "1"},
        "geo": {"@type": "GeoCoordinates", "latitude": N["lat"], "longitude": N["lng"]},
        "hasMap": FICHA, "sameAs": C.SAME_AS,
        "knowsAbout": N["knows_about"],
    }
    if N.get("precio"):
        d["priceRange"] = N["precio"]
    if N.get("pago"):
        d["paymentAccepted"] = N["pago"]
    if N.get("fundacion"):
        d["foundingDate"] = str(N["fundacion"])
    if int(N["resenas"]) == 0 or not getattr(C, "SCHEMA_VALORACION", True):
        del d["aggregateRating"]
    pe = N.get("persona")
    if pe:
        d["founder"] = {"@type": "Person", "@id": DOMINIO + "/#" + pe["id"], "name": pe["nombre"], "jobTitle": pe["cargo"],
                        "worksFor": {"@id": NEG_ID},
                        "hasCredential": [{"@type": "EducationalOccupationalCredential", "name": n, "identifier": i}
                                          for n, i in pe.get("credenciales", [])]}
    return d


def schema_de(p):
    url = DOMINIO + p["url"]
    g = [negocio_schema(),
         {"@type": "WebPage", "@id": url + "#pagina", "url": url, "name": p["title"], "description": p["meta"],
          "inLanguage": "es", "isPartOf": {"@id": DOMINIO + "/#web"}, "about": {"@id": NEG_ID},
          **({"dateModified": p["mod"]} if p.get("mod") else {})},
         {"@type": "WebSite", "@id": DOMINIO + "/#web", "url": DOMINIO + "/", "name": N["nombre"], "inLanguage": "es",
          "publisher": {"@id": NEG_ID}}]
    c = migas(p["url"])
    if c:
        g.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": DOMINIO + u} for i, (u, n) in enumerate(c)]})
    t = datos.tipo_de(p["url"])
    if t in ("servicio", "marca", "municipio"):
        g.append({"@type": "Service", "name": p["h1"], "serviceType": N["servicio_tipo"], "provider": {"@id": NEG_ID},
                  "url": url, "areaServed": {"@type": "City", "name": PUEBLO.get(p["url"], BASE)}})
    if p["faq"]:
        g.append({"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", inline(a))}}
            for q, a in p["faq"]]})
    return {"@context": "https://schema.org", "@graph": g}


# ---------- Utilidades de texto ----------
def plano(txt):
    return re.sub(r"<[^>]+>", "", inline(txt))


def palabras(txt):
    return len(plano(re.sub(r"\[(?:LINK )?([^\]]+)\]\([^)]+\)", r"\1", txt)).split())


def slug(t):
    import unicodedata
    s = unicodedata.normalize("NFKD", plano(t)).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")[:48] or "seccion"


def h2_gris(t):
    """R11 · Rayo: la segunda mitad del titular va en gris y se enciende palabra a palabra con el scroll.
    Sin JS o con movimiento reducido se ve entero en negro."""
    w = plano(t).split()
    if len(w) < 3:
        return esc(plano(t))
    k = max(1, math.ceil(len(w) * .5))
    return f'{esc(" ".join(w[:k]))} <span class="gris">{esc(" ".join(w[k:]))}</span>'


def h2c(t):
    """Clase del H2 de sección: los titulares largos (preguntas) van arriba a lo ancho, a menor tamaño."""
    return "h2 enciende" + (" h2--largo" if len(plano(t)) > 32 else "")


def secciones(bl):
    intro, secs, act = [], [], None
    for b in bl:
        if b[0] == "h2":
            act = {"h2": b[1], "bl": []}; secs.append(act)
        elif act is None:
            intro.append(b)
        else:
            act["bl"].append(b)
    return intro, secs


# ---------- Bloques de texto → HTML ----------
SOLO_ENLACE = re.compile(r"^\s*\[(?:LINK )?[^\]]+\]\([^)]+\)\s*(🔗|🆕)?\s*$")
FILA = re.compile(r"^\*\*(.+?)\*\*\s*(.+)$")
URL_1 = re.compile(r"\]\((/[^)]*)\)")
ETQ_URL = {u: e for _, _, u, _, e, _ in SERVICIOS_HOME}


def filas_html(items, clase=""):
    """«**Título.** texto» seguidos (3 o más) → filas de Rayo con línea, icono y «/ 01» (R27: las demás se apagan)."""
    out = []
    for i, (tit, cuerpo) in enumerate(items, 1):
        m = URL_1.search(cuerpo)
        u = m.group(1) if m else None
        ic = T.ico(ICONO_URL[u]) if u in ICONO_URL else T.simbolo()
        etq = "".join(f"<li>{esc(e)}</li>" for e in ETQ_URL.get(u, []))
        out.append(f'<li class="fila rv"><span class="fila__ico">{ic}</span><h3 class="fila__tit">{inline(tit.rstrip(".:"))}</h3>'
                   f'<div class="fila__txt"><p>{inline(cuerpo)}</p></div>'
                   f'{f"<ul class=fila__etq>{etq}</ul>" if etq else ""}<span class="fila__num" aria-hidden="true">/ {i:02d}</span></li>')
    return f'<ol class="filas {clase}">{"".join(out)}</ol>'


def pasos_html(items):
    out = []
    for i, it in enumerate(items):
        ic = T.ico(PASOS_ICONOS[i]) if i < len(PASOS_ICONOS) else ""
        out.append(f'<li class="paso rv"><span class="paso__n">{i + 1:02d}</span><span class="paso__ico">{ic}</span><span class="paso__txt">{inline(it)}</span></li>')
    return f'<ol class="pasos">{"".join(out)}</ol>'


def tabla_html(cab, filas):
    th = "".join(f'<th scope="col">{inline(h)}</th>' for h in cab)
    trs = []
    for f in filas:
        f = (f + [""] * len(cab))[:len(cab)]
        trs.append("<tr>" + "".join(f'<td data-col="{A(plano(h))}">{inline(c)}</td>' for h, c in zip(cab, f)) + "</tr>")
    return f'<div class="tabla rv"><table class="tabla-datos"><thead><tr>{th}</tr></thead><tbody>{"".join(trs)}</tbody></table></div>'


def render_bloques(bl, estructura=None):
    """Markdown en bloques → HTML. estructura (lista) recibe lo que va a ancho completo en la home."""
    out, i, tras = [], 0, [False]
    def pon(h, estr=False):
        """En la home, lo estructurado va a ancho completo; lo que viene detrás de ello, también (conserva el orden)."""
        if estructura is not None and (estr or tras[0]):
            estructura.append(h if estr else f'<div class="prosa blq__tras rv">{h}</div>'); tras[0] = True
        else:
            out.append(h)
    while i < len(bl):
        t, c = bl[i]
        if t == "p":
            if ES_WIDGET(c) or c.startswith("(Formulario") or c.strip() in ("[[FORMULARIO]]", "[[MAPA]]"):
                i += 1; continue
            grupo = []
            while i < len(bl) and bl[i][0] == "p" and FILA.match(bl[i][1]):
                m = FILA.match(bl[i][1]); grupo.append((m.group(1), m.group(2))); i += 1
            if len(grupo) >= 3:
                pon(filas_html(grupo), True); continue
            for tit, cu in grupo:
                pon(f"<p><strong>{inline(tit)}</strong> {inline(cu)}</p>")
            if grupo:
                continue
            pon(f"<p>{inline(c)}</p>")
        elif t in ("h3", "h4"):
            pon(f"<{t}>{inline(c)}</{t}>")
        elif t == "ul":
            if all(SOLO_ENLACE.match(x) for x in c):
                items = []
                for x in c:
                    m = re.search(r"\[(?:LINK )?([^\]]+)\]\(([^)]+)\)", x)
                    items.append(f'<li><a href="{m.group(2)}">{esc(m.group(1))}{T.ico("flecha-diagonal")}</a></li>')
                pon(f'<ul class="enlaces">{"".join(items)}</ul>', True)
            else:
                vin = T.simbolo("vineta")
                pon('<ul class="lista">' + "".join(f"<li>{vin}<span>{inline(x)}</span></li>" for x in c) + "</ul>")
        elif t == "ol":
            pon(pasos_html(c), True)
        elif t == "tabla":
            pon(tabla_html(*c), True)
        i += 1
    return re.sub(r" {2,}", " ", "\n".join(out))


# ---------- Piezas de Rayo ----------
def pueblo_de(url):
    return PUEBLO.get(url, BASE)


def etiqueta_y_entrada(p):
    pb = pueblo_de(p["url"])
    muni = datos.tipo_de(p["url"]) == "municipio"
    et = esc(p.get("etiqueta") or texto("etiqueta_portada", pueblo=pb))
    en = inline(p["entrada_corta"]) if p.get("entrada_corta") else esc(texto("corta_municipio" if muni else "corta", pueblo=pb))
    return et, en


def objeto_html(clase="objeto", lcp=True):
    """Objeto de portada (R28 flota; «3d»: módulo three.js diferido encima de la imagen fija, que es el LCP)."""
    o = OBJETO_PORTADA
    b = o["imagen"].rsplit(".", 1)[0]
    carga = 'fetchpriority="high"' if lcp else 'loading="lazy" decoding="async"'
    img = (f'<picture><source type="image/webp" srcset="/img/{b}-420.webp 420w, /img/{b}-840.webp 840w" sizes="{OBJ_SIZES}">'
           f'<img src="/img/{b}-840.png" width="{o["ancho"]}" height="{o["alto"]}" alt="{A(o["alt"])}" {carga}></picture>')
    extra = ""
    if o["tipo"] == "3d" and lcp:
        extra = f' data-objeto3d="/marca/{o["svg_3d"]}"' + (f' data-color="{o["color_3d"]}"' if o.get("color_unico") else "")
    elif o["tipo"] == "video" and lcp and o.get("video_webm"):
        mov = f'<source src="/objeto/{o["video_mov"]}" type=\'video/mp4; codecs="hvc1"\'>' if o.get("video_mov") else ""
        img = (f'<video class="objeto__video" autoplay muted loop playsinline poster="/img/{b}-840.png" width="{o["ancho"]}" height="{o["alto"]}" aria-hidden="true">'
               f'{mov}<source src="/objeto/{o["video_webm"]}" type="video/webm"></video>') + img
    lienzo = '<div class="objeto__lienzo" aria-hidden="true"></div>' if extra and "objeto3d" in extra else ""
    return f'<div class="{clase}" data-objeto{extra}><div class="objeto__flota">{img}{lienzo}</div></div>'


OBJ_SIZES = "(min-width: 1600px) 500px, (min-width: 768px) 380px, 230px"
FORMATOS_OK = {"v", "h", "g"}


def caso_html(c, i):
    tit, sub, img, url, fmt = c
    fmt = fmt if fmt in FORMATOS_OK else "v"
    if img:
        cuerpo = T.foto(img, f"{tit}: {sub}", "(max-width: 900px) 80vw, 34vw", clase="caso__foto")
    else:  # marcador de maqueta: la captura real va en recursos/casos/ (maqueta de dispositivo)
        disp = "movil" if fmt == "v" else "portatil"
        cuerpo = (f'<div class="caso__maqueta caso__maqueta--{disp} tono-{i % 3}"><span class="caso__disp"><b>{esc(tit)}</b>'
                  f'<em>Captura real pendiente</em></span></div>')
    ojo = f'<span class="caso__ojo" aria-hidden="true">{T.ico("flecha-diagonal")}{esc(CASOS_VER)}</span>' if url else ""
    pie = f'<p class="caso__pie"><strong>{esc(tit)}</strong> {esc(sub)}</p>'
    dentro = f'<div class="caso__marco">{cuerpo}{ojo}</div>{pie}'
    if url:
        ext = ' rel="noopener" target="_blank"' if url.startswith("http") else ""
        dentro = f'<a href="{A(url)}"{ext}>{dentro}</a>'
    return f'<li class="caso caso--{fmt} caso--{i}">{dentro}</li>'


def portada_home(p):
    """Portada A de Rayo: H1 arriba a la izquierda, cinta gigante que acelera con el scroll (R14) con el objeto
    encima (R28 / 3D), servicios en dos columnas abajo a la izquierda y tarjeta de conversión abajo a la derecha.
    Debajo, la galería de casos que sube por encima de la portada fija (R5, solo ordenador)."""
    etiqueta, corta = etiqueta_y_entrada(p)
    serv = "".join(f'<li><a href="{u}">{T.ico(ic)}<span>{esc(t)}</span></a></li>' for t, _, u, ic, _, _ in SERVICIOS_HOME)
    extra = f'<a class="tarjeta__extra" href="{CTA_EXTRA[1]}">{esc(CTA_EXTRA[0])} {T.ico("flecha-diagonal")}</a>' if CTA_EXTRA else ""
    tarjeta = f"""<aside class="tarjeta" aria-label="Contacto" data-sale>
     {T.estado()}
     {T.nota("tarjeta__nota", "#opiniones" if OPINIONES else FICHA)}
     <a class="tarjeta__ir" href="#te-llamamos" data-zona="tarjeta_portada"><span>{texto("tarjeta_titulo")}</span><strong>{texto("tarjeta_ir")} ↓</strong></a>
     {extra}
    </aside>"""
    galeria = ""
    if CASOS:
        galeria = (f'<section class="galeria" aria-labelledby="galeria-tit" data-galeria><h2 class="sr" id="galeria-tit">Trabajos</h2>'
                   f'<ul class="galeria__lista">{"".join(caso_html(c, i) for i, c in enumerate(CASOS[:7]))}</ul></section>')
    return f"""<div class="hero{' hero--galeria' if galeria else ''}" data-hero>
<section class="portada-a" data-portada>
 <div class="contenedor portada-a__top" data-sale>
  <p class="etiqueta">{T.simbolo("etiqueta__sim")}{etiqueta}</p>
  <h1 class="h1-home">{esc(p['h1'])}</h1>
  <p class="portada-a__corta">{corta}</p>
  <div class="acciones">{T.btn_llamar(extra=' data-zona="portada_boton"')}{T.btn_whatsapp("btn--linea")}</div>
 </div>
 <div class="portada-a__centro">
  {T.cinta(CINTA_PORTADA, "cinta--gigante")}
  {objeto_html()}
 </div>
 <div class="contenedor portada-a__pie">
  <nav class="portada-a__serv" aria-label="Servicios" data-sale><ul>{serv}</ul></nav>
  {tarjeta}
 </div>
</section>
{galeria}
</div>
"""


def portada_interior(p, t):
    """Cabecera interior de `services`: etiqueta a la izquierda, H1 a la derecha con la miniatura en píldora
    delante (icono del servicio o del municipio sobre el acento) y la llamada pegada al H1."""
    etiqueta, corta = etiqueta_y_entrada(p)
    u = p["url"]
    ic = ICONO_URL.get(u)
    if not ic and t == "municipio":
        s = u.replace(URLS["municipio"], "").strip("/")
        ic = s if s in T.SIMBOLOS else "ubicacion"
    pild = T.ico(ic) if ic and ic in T.SIMBOLOS else T.simbolo()
    pb = pueblo_de(u) if t == "municipio" else None
    extra = T.boton(CTA_EXTRA[0], CTA_EXTRA[1], "btn--linea") if CTA_EXTRA and CTA_EXTRA[1] != u and t != "contacto" else ""
    return f"""<section class="cab-int">
 <div class="contenedor">
  {migas_html(u)}
  <div class="cab-int__grid">
   <p class="etiqueta cab-int__etq">{T.simbolo("etiqueta__sim")}{etiqueta}</p>
   <div class="cab-int__txt">
    <h1 class="h1-int{' h1-int--largo' if len(p['h1']) > 44 else ''}"><span class="h1__pildora" aria-hidden="true">{pild}</span>{esc(p['h1'])}</h1>
    <p class="cab-int__corta">{corta}</p>
    <div class="acciones">{T.btn_llamar(extra=' data-zona="portada_boton"')}{T.btn_whatsapp("btn--linea", pueblo=pb)}{extra}</div>
   </div>
  </div>
 </div>
</section>
"""


DECLARA_MAX = 60


def reparte_intro(intro):
    ps = [c for t, c in intro if t == "p"]
    ps = [x for x in ps if len(plano(re.sub(r"\[(?:LINK )?[^\]]+\]\([^)]+\)", "", x)).strip(" ·.,")) > 30]
    dec, total = [], 0
    for i, x in enumerate(ps):
        w = palabras(x)
        if i == 0 or total + w <= DECLARA_MAX + 5:
            dec.append(x); total += w
        else:
            return dec, [("p", y) for y in ps[i:]]
    return dec, []


def ventajas_html(ul):
    items = []
    for it in ul:
        m = re.match(r"\*\*(.+?)\*\*[,.:]?\s*(.*)", it)
        if m:
            items.append(f'<li class="rv">{T.ico("check")}<strong>{inline(m.group(1))}</strong><span>{inline(m.group(2))}</span></li>')
        else:
            items.append(f'<li class="rv">{T.ico("check")}<span>{inline(it)}</span></li>')
    return f'<ul class="ventajas">{"".join(items)}</ul>'


def manifiesto(p, ps, ul):
    """Manifiesto de la home B de Rayo: «+ Quiénes somos» a la izquierda y la declaración grande a la derecha,
    que se enciende palabra a palabra (R11); debajo, las ventajas del texto."""
    if not ps:
        return ""
    txt = " ".join(inline(x) for x in ps)
    boton = T.boton(nombre(URLS["empresa"]), URLS["empresa"], "btn--linea") if URLS["empresa"] in POR_URL and p["url"] != URLS["empresa"] else ""
    return f"""<section class="seccion manifiesto">
 <div class="contenedor manifiesto__in">
  <p class="etiqueta">{T.simbolo("etiqueta__sim")}{esc(texto("declara_etiqueta"))}</p>
  <div>
   <p class="manifiesto__txt enciende">{txt}</p>
   {ventajas_html(ul) if ul else ""}
   <div class="acciones">{boton}</div>
  </div>
 </div>
</section>
"""


def bloque_home(sec, n):
    """Sección de la home con la anatomía de «Company»: H2 a la izquierda (5/12, segunda mitad en gris que se
    enciende), entradilla y texto a la derecha; filas, pasos, tablas y enlaces a ancho completo debajo."""
    estr = []
    cuerpo = render_bloques(sec["bl"], estr)
    partes = re.split(r"(?<=</p>)\n", cuerpo, maxsplit=1)
    primero = partes[0].replace("<p>", '<p class="entradilla">', 1) if partes[0].startswith("<p>") else partes[0]
    resto = partes[1] if len(partes) > 1 else ""
    return f"""<section class="seccion blq" id="{slug(sec['h2'])}">
 <div class="contenedor">
  <div class="blq__cab">
   <h2 class="{h2c(sec['h2'])}">{h2_gris(sec['h2'])}</h2>
   <div class="blq__txt prosa rv">{primero}{resto}</div>
  </div>
  {"".join(estr)}
 </div>
</section>
"""


def servicios_seccion():
    """Filas de servicios desde config (si el texto de la home no las trae ya): variación B de `services`
    (nombre grande, texto, etiquetas; R27) y, con foto, la foto que sigue al cursor (R23)."""
    out = []
    for i, (t, txt, u, ic, etq, foto_s) in enumerate(SERVICIOS_HOME, 1):
        e = "".join(f"<li>{esc(x)}</li>" for x in etq)
        f = f'<span class="fila__foto" aria-hidden="true">{T.foto(foto_s, "", "(max-width: 900px) 90vw, 280px")}</span>' if foto_s else ""
        out.append(f'<li class="fila fila--enlace rv{" con-foto" if foto_s else ""}"><a href="{u}"><span class="fila__ico">{T.ico(ic)}</span>'
                   f'<h3 class="fila__tit">{esc(t)}</h3><span class="fila__txt"><span>{esc(txt)}</span></span>'
                   f'{f"<ul class=fila__etq>{e}</ul>" if e else ""}<span class="fila__num" aria-hidden="true">/ {i:02d}</span>{f}</a></li>')
    return f"""<section class="seccion blq servicios" id="servicios">
 <div class="contenedor">
  <div class="blq__cab"><h2 class="{h2c(SERVICIOS_TITULO)}">{h2_gris(SERVICIOS_TITULO)}</h2><div class="blq__txt prosa rv"><p class="entradilla">{esc(SERVICIOS_TEXTO)}</p></div></div>
  <ol class="filas filas--serv" data-sigue>{"".join(out)}</ol>
  <div class="cursor-foto" aria-hidden="true" data-cursor-foto></div>
 </div>
</section>
"""


MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]


def valor_cifra(v):
    if v == "{valoracion}":
        return N["valoracion"], ' data-fuente="valoracion"'
    if v == "{resenas}":
        return N["resenas"], ' data-fuente="resenas"'
    return v.format(anios=N["anios"], anios_marca=N["anios_marca"]), ""


def cifras():
    """Cifras en mosaico 2 + 2 de anchos cruzados (Rayo `mxd-stats-cards`), la primera en el acento.
    Sin objetos 3D: un icono grande de trazo en la esquina. Cuentan al entrar (R32, sin odómetro)."""
    import datetime
    hoy = datetime.date.today()
    fecha = f'<time datetime="{hoy:%Y-%m}">{MESES[hoy.month - 1]} de {hoy.year}</time>'
    tarj = []
    for i, (v, suf, txt, bt, ic) in enumerate(CIFRAS[:4]):
        val, fuente = valor_cifra(v)
        b = T.boton(bt[0], bt[1], "btn--linea btn--peq" if i else "btn--blanco btn--peq") if bt else ""
        tarj.append(f'<div class="cifra cifra--{i} rv"><p class="cifra__n"><span data-cuenta="{A(val)}"{fuente}>{esc(val)}</span>{esc(suf)}</p>'
                    f'<p class="cifra__t">{esc(txt)}</p>{b}<span class="cifra__deco" aria-hidden="true">{T.ico(ic)}</span></div>')
    return f"""<section class="seccion cifras-sec" aria-label="{A(texto('cifras_etiqueta'))}">
 <div class="contenedor">
  <div class="blq__cab"><h2 class="h2 enciende">{h2_gris(texto("cifras_titulo"))}</h2><div class="blq__txt"><p class="cifras__fecha">{texto("cifras_fecha", fecha=fecha)}</p></div></div>
  <div class="cifras">{"".join(tarj)}</div>
 </div>
</section>
"""


# ---------- Tira de logotipos de clientes (en gris; a color al pasar el ratón) ----------
LOGOS_EXT = (".svg", ".png", ".webp")


def _logos():
    """Lee recursos/clientes/ (si está vacía y existe config.LOGOS_ORIGEN, copia de ahí antes).
    logos.json opcional: [{"archivo": "balgas.svg", "nombre": "Balgas"}] para orden y nombre."""
    dest = os.path.join(RAIZ, "recursos", "clientes")
    orig = getattr(C, "LOGOS_ORIGEN", None)
    if orig and os.path.isdir(orig):
        os.makedirs(dest, exist_ok=True)
        for f in os.listdir(orig):
            if (f.lower().endswith(LOGOS_EXT) and not f.startswith("_")) or f == "logos.json":
                shutil.copy(os.path.join(orig, f), os.path.join(dest, f))
    if not os.path.isdir(dest):
        return []
    js = os.path.join(dest, "logos.json")
    if os.path.exists(js):
        lista = [(x["archivo"], x["nombre"]) for x in json.load(open(js, encoding="utf-8"))
                 if os.path.exists(os.path.join(dest, x["archivo"]))]
    else:
        nombres = getattr(C, "LOGOS_NOMBRES", {})
        lista = [(f, nombres.get(f.rsplit(".", 1)[0]) or re.sub(r"[-_]+", " ", f.rsplit(".", 1)[0]).strip().title())
                 for f in sorted(os.listdir(dest)) if f.lower().endswith(LOGOS_EXT) and not f.startswith("_")]
    # Rejilla sin huérfanos (3 columnas en móvil, 4 en tableta, 6 en ordenador): múltiplo de 12, o de 6, o par
    n = len(lista)
    n = n - n % 12 if n >= 12 else (n - n % 6 if n >= 6 else n - n % 2)
    return lista[:n]


LOGOS = _logos()


def logos_html():
    tit = esc(getattr(C, "LOGOS_TITULO", "Clientes"))
    if not LOGOS:   # MARCADOR de maqueta: controles.py avisa mientras salga
        cajas = "".join(f'<li class="logo logo--marcador"><span>Logotipo {i}</span></li>' for i in range(1, 7))
        return (f'<section class="seccion logos-sec" aria-label="{tit}" data-marcador="logos"><div class="contenedor">'
                f'<p class="etiqueta">{T.simbolo("etiqueta__sim")}{tit}</p><ul class="logos">{cajas}</ul></div></section>')
    os.makedirs(os.path.join(SITIO, "img", "clientes"), exist_ok=True)
    li = []
    for f, n in LOGOS:
        shutil.copy(os.path.join(RAIZ, "recursos", "clientes", f), os.path.join(SITIO, "img", "clientes", f))
        w, h = 200, 80
        if not f.lower().endswith(".svg"):
            from PIL import Image
            with Image.open(os.path.join(RAIZ, "recursos", "clientes", f)) as im:
                w, h = im.width, im.height
        else:
            vb = re.search(r'viewBox="[\d.\-]+ [\d.\-]+ ([\d.]+) ([\d.]+)"', open(os.path.join(RAIZ, "recursos", "clientes", f), encoding="utf-8", errors="ignore").read())
            if vb:
                w, h = round(float(vb.group(1))), round(float(vb.group(2)))
        li.append(f'<li class="logo{" logo--alto" if w / max(h, 1) < 1.8 else ""}"><img src="/img/clientes/{A(f)}" alt="{A(n)}" width="{w}" height="{h}" loading="lazy" decoding="async"></li>')
    return (f'<section class="seccion logos-sec" aria-label="{tit}"><div class="contenedor">'
            f'<p class="etiqueta">{T.simbolo("etiqueta__sim")}{tit}</p><ul class="logos{"" if len(li) % 12 == 0 else " logos--seis"}">{"".join(li)}</ul></div></section>')


def zona_html():
    """Cinta secundaria fina a la derecha (R14, peso 300) y la lista de enlaces a los municipios."""
    nombres = CINTA_SECUNDARIA or ([BASE] + [n for _, n in MUNICIPIOS if n != BASE])
    li = "".join(f'<li class="rv"><a href="{u}">{esc(MUNICIPIO_ANCLA.format(pueblo=n))}{T.ico("flecha-diagonal")}</a></li>' for u, n in MUNICIPIOS)
    return (f'<div class="cinta-sec">{T.cinta(nombres, "cinta--fina", 1)}</div>'
            + (f'<section class="seccion zonas-sec" aria-label="{A(texto("zona_titulo"))}"><div class="contenedor"><ul class="enlaces enlaces--zonas">{li}</ul></div></section>' if li else ""))


def horario_html(sec):
    txt = render_bloques(sec["bl"])
    return f"""<section class="seccion horario-sec" id="{slug(sec['h2'])}">
 <div class="contenedor">
  <div class="horario">
   <div class="horario__cab"><h2 class="h2 enciende">{h2_gris(sec['h2'])}</h2>{T.estado()}</div>
   <p class="horario__grande"><span>{N['dias_texto']}</span><strong>{N['abre'].lstrip('0')}<em>—</em>{N['cierra'].lstrip('0')}</strong></p>
   <div class="horario__txt prosa">{txt}<p><a class="horario__tel tel" href="tel:{N['telefono_e164']}">{T.ico("contacto")}{N['telefono']}</a></p></div>
  </div>
 </div>
</section>
"""


MAPA_EMBED = f"https://maps.google.com/maps?cid={N['cid']}&z=16&hl=es&output=embed"


def mapa():
    return f"""<section class="seccion mapa-sec" aria-label="Dónde estamos">
 <div class="contenedor">
  <div class="mapa">
   <div class="mapa__info">
    <p class="etiqueta">{T.simbolo("etiqueta__sim")}Dónde estamos</p>
    <h2 class="h2-lect">{texto("mapa_titular")}</h2>
    <p class="mapa__dir">{N['calle']}<br>{N['cp']} {N['localidad']} ({N['provincia']})</p>
    <p>{texto("mapa_texto")}</p>
    <div class="acciones">{T.boton("Ver en Google Maps", FICHA, "btn--linea", "flecha-diagonal", ' rel="noopener" target="_blank"')}</div>
   </div>
   <div class="mapa__marco"><iframe src="{MAPA_EMBED}" title="Mapa: {A(N['nombre'])}, {A(N['calle'])}, {A(N['localidad'])}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe></div>
  </div>
 </div>
</section>
"""


def tarjeta_opinion(o):
    serv = esc(o.get("servicio", "")) + (f' · {esc(o["lugar"])}' if o.get("lugar") else "")
    marca = " op--marcador" if o.get("marcador") else ""
    return (f'<li class="op{marca}"><span class="estrellas" aria-label="5 estrellas">★★★★★</span>'
            f'<p class="op__tit">{esc(o["titulo"])}</p><p class="op__txt">«{esc(o["texto"])}»</p>'
            f'<div class="op__pie"><span class="op__ini" aria-hidden="true">{esc(o["nombre"][:1])}</span>'
            f'<span class="op__quien"><strong>{esc(o["nombre"])}</strong><span>{serv or "Opinión publicada en Google"}</span></span></div></li>')


def opiniones(pb=None, titulo=None, texto_op=""):
    """Opiniones de la home B de Rayo: título, texto y sello de Google a la izquierda (en el sitio de Clutch),
    carrusel de tarjetas blancas a la derecha con flechas y contador (R33 sin automático). Sello que gira con el scroll (R25)."""
    lista = sorted(OPINIONES, key=lambda o: 0 if pb and o.get("lugar") == pb else 1)
    titulo = titulo or esc(texto("opiniones_titular"))
    texto_op = f'<p>{texto_op}</p>' if texto_op else ""
    sello_t = esc(texto("opiniones_sello"))
    sello = (f'<a class="sello" href="{FICHA}" rel="noopener" target="_blank" aria-label="Ver las reseñas en Google">'
             f'<svg class="sello__aro" viewBox="0 0 200 200" aria-hidden="true" data-gira><defs><path id="aro" d="M100,100 m-78,0 a78,78 0 1,1 156,0 a78,78 0 1,1 -156,0"/></defs>'
             f'<text><textPath href="#aro" textLength="486" lengthAdjust="spacingAndGlyphs">{sello_t}{sello_t}</textPath></text></svg>{T.simbolo("sello__sim")}</a>')
    carrusel = ""
    if lista:
        carrusel = f"""<div class="op-carril">
   <ul class="op-lista" data-opiniones tabindex="0" aria-label="Reseñas">{"".join(tarjeta_opinion(o) for o in lista)}</ul>
   <div class="op-ctrl"><button type="button" class="redondo" data-op="-1" aria-label="Reseña anterior">←</button><span class="op-cuenta" data-op-cuenta>1 / {len(lista)}</span><button type="button" class="redondo" data-op="1" aria-label="Reseña siguiente">→</button></div>
  </div>"""
    return f"""<section class="seccion opiniones-sec" id="opiniones" aria-label="Opiniones de clientes en Google">
 <div class="contenedor opiniones">
  <div class="opiniones__cab">
   <p class="etiqueta">{T.simbolo("etiqueta__sim")}{esc(texto("opiniones_etiqueta"))}</p>
   <h2 class="h2 enciende">{titulo}</h2>
   {texto_op}
   <div class="opiniones__nota">{T.nota("nota--grande", FICHA)}{sello}</div>
   <div class="acciones">{T.boton("Ver todas en Google", FICHA, "btn--linea", "flecha-diagonal", ' rel="noopener" target="_blank"')}</div>
  </div>
  {carrusel}
 </div>
</section>
"""


def faq_html(faq):
    if not faq:
        return ""
    items = "".join(f'<details class="rv" name="faq"{" open" if i == 1 else ""}><summary><span>{esc(q)}</span><i aria-hidden="true"></i></summary>'
                    f'<div class="faq__resp"><p>{inline(a)}</p></div></details>' for i, (q, a) in enumerate(faq, 1))
    return f"""<section class="seccion faq-sec" id="preguntas">
 <div class="contenedor faq">
  <div class="faq__cab">
   <p class="etiqueta">{T.simbolo("etiqueta__sim")}{esc(texto("faq_etiqueta"))}</p>
   <h2 class="h2 enciende">{h2_gris(texto("faq_titulo"))}</h2>
   <a class="faq__tel tel" href="tel:{N['telefono_e164']}"><span>{esc(texto("faq_cta"))}</span><strong>{N['telefono']}</strong></a>
  </div>
  <div class="faq__lista">{items}</div>
 </div>
</section>
"""


# ---------- Tarjeta «Le llamamos» (base GYF) y banda final que se abre (R21) ----------
URL_PRIVACIDAD = next((u for n, u in LEGALES if "privacidad" in n.lower()), "/politica-de-privacidad/")


def privacidad(clave):
    return f'<p class="casilla casilla--info">{texto(clave)} <a href="{URL_PRIVACIDAD}">Política de privacidad</a>.</p>'


def llamada(url):
    return f"""<div class="llamada" id="te-llamamos">
 <p class="llamada__tit">{texto("llamada_titulo")}</p>
 <p class="llamada__txt" data-promesa>{texto("llamada_promesa")}</p>
 <div class="aviso aviso--ok" data-llamada-ok hidden>{texto("llamada_ok")}</div>
 <div class="aviso aviso--error" data-llamada-error hidden>No se ha podido enviar. Llámenos al {N['telefono']}.</div>
 <form class="llamada__form" action="/enviar.php" method="post">
  <input type="hidden" name="tipo" value="llamada"><input type="hidden" name="pagina" value="{url}"><input type="hidden" name="t" value="">
  <label class="trampa" aria-hidden="true">Web<input type="text" name="web" tabindex="-1" autocomplete="off"></label>
  <label>Nombre<input type="text" name="nombre" autocomplete="name" required maxlength="80"></label>
  <label>Teléfono<input type="tel" name="telefono" autocomplete="tel" inputmode="tel" required pattern="[0-9 +()\\-]{{9,20}}" maxlength="20"></label>
  {privacidad("privacidad_llamada")}
  {T.boton_form(texto("llamada_boton"))}
 </form>
</div>"""


def banda(url, titulo=None, texto_b=None):
    titulo = titulo or esc(BANDA_TIT.get(url) or texto("banda_titulo"))
    texto_b = texto_b or esc(texto("banda_texto"))
    extra = f'<a class="banda__extra" href="{CTA_EXTRA[1]}">{esc(CTA_EXTRA[0])} {T.ico("flecha-diagonal")}</a>' if CTA_EXTRA and CTA_EXTRA[1] != url else ""
    obj = objeto_html("banda__objeto", lcp=False) if OBJETO_PORTADA.get("en_banda") else ""
    return f"""<section class="banda-sec" aria-label="Contacto">
 <div class="contenedor">
  <div class="banda" data-abre>
   <span class="banda__fondo" aria-hidden="true"></span>
   {obj}
   <div class="banda__txt">
    <p class="etiqueta etiqueta--claro">{T.simbolo("etiqueta__sim")}{esc(texto("banda_etiqueta"))}</p>
    <h2 class="banda__tit">{titulo}</h2>
    <p class="banda__p">{texto_b}</p>
    {T.estado("estado--claro")}
    <div class="acciones">{T.btn_llamar("btn--acento btn--grande", extra=' data-zona="banda"')}{T.btn_whatsapp("btn--linea-claro")}</div>
    {extra}
   </div>
   <div class="banda__form">{llamada(url)}</div>
  </div>
 </div>
</section>
"""


# ---------- Páginas interiores: columna de lectura con índice clavado ----------
def lectura(p, entrada, resto, secs_normales, ul=None):
    """Columna de lectura (720 px) con el índice clavado a la izquierda en tarjeta blanca y la tarjeta de
    llamada debajo (variación A de páginas interiores)."""
    ind, blq = [], []
    for s in secs_normales:
        sid = slug(s["h2"])
        ind.append(f'<li><a href="#{sid}">{esc(plano(s["h2"]))}</a></li>')
        blq.append(f'<section class="lectura__blq" id="{sid}"><h2 class="h2-lect rv">{inline(s["h2"])}</h2><div class="prosa rv">{render_bloques(s["bl"])}</div></section>')
    if True:  # opiniones sale siempre (con reseñas o con la nota de la ficha)
        ind.append('<li><a href="#opiniones">Opiniones</a></li>')
    if p["faq"]:
        ind.append('<li><a href="#preguntas">Preguntas frecuentes</a></li>')
    extra = f'<a class="mini__extra" href="{CTA_EXTRA[1]}">{esc(CTA_EXTRA[0])} {T.ico("flecha-diagonal")}</a>' if CTA_EXTRA and CTA_EXTRA[1] != p["url"] else ""
    lista = "".join(ind)
    ent = f'<p class="lectura__entrada rv">{" ".join(inline(x) for x in entrada)}</p>' if entrada else ""
    return f"""<section class="lectura">
 <div class="contenedor lectura__in">
  <aside class="lectura__lado" aria-label="{A(texto('indice_titulo'))}">
   <details class="indice" data-indice open><summary>{esc(texto("indice_titulo"))}</summary><ol>{lista}</ol></details>
   <div class="mini">
    <p class="mini__tit">{esc(texto("indice_llamar"))}</p>
    {T.estado()}
    {T.btn_llamar("btn--acento btn--peq", N['telefono'], ' data-zona="indice"')}
    {T.btn_whatsapp("btn--linea btn--peq")}
    {extra}
   </div>
  </aside>
  <div class="lectura__col">
   {ent}
   <div class="prosa rv">{render_bloques(resto)}</div>
   {ventajas_html(ul) if ul else ""}
   {"".join(blq)}
  </div>
 </div>
</section>
"""


# ---------- Contacto ----------
def formulario():
    return f"""<form class="formulario rv" action="/enviar.php" method="post" aria-label="Escríbanos">
 <div class="aviso aviso--ok" id="form-ok" hidden>{texto("form_ok")}</div>
 <div class="aviso aviso--error" id="form-error" hidden>No se ha podido enviar. Llámenos al {N['telefono']} o inténtelo de nuevo.</div>
 <p class="formulario__confianza">{texto("form_confianza")}</p>
 <div class="fila-form">
  <label>Nombre<input type="text" name="nombre" autocomplete="name" required maxlength="80"></label>
  <label>Teléfono<input type="tel" name="telefono" autocomplete="tel" inputmode="tel" required pattern="[0-9 +()\\-]{{9,20}}" maxlength="20"></label>
 </div>
 <label>Municipio<input type="text" name="municipio" autocomplete="address-level2" maxlength="60" placeholder="{A(texto('form_municipio_ph'))}"></label>
 <label>{texto("form_mensaje_label")} <span class="opcional">(opcional)</span><textarea name="mensaje" maxlength="2000" placeholder="{A(texto('form_mensaje_ph'))}"></textarea></label>
 <label class="trampa" aria-hidden="true">Web<input type="text" name="web" tabindex="-1" autocomplete="off"></label>
 <input type="hidden" name="t" value="">
 {privacidad("privacidad_form")}
 <div class="acciones">{T.boton_form(texto("form_boton"))}</div>
</form>"""


def contacto_cuerpo(p, intro):
    ps = [c for t, c in intro if t == "p"]
    txt = "".join(f"<p>{inline(x)}</p>" for x in ps)
    extra = f'<p><strong>{esc(CTA_EXTRA[0])}:</strong> <a href="{CTA_EXTRA[1]}">{esc(nombre(CTA_EXTRA[1]))}</a></p>' if CTA_EXTRA and CTA_EXTRA[1] != p["url"] else ""
    return f"""<section class="seccion contacto">
 <div class="contenedor contacto__grid">
  <div class="contacto__datos">
   <div class="prosa rv">{txt}</div>
   <a class="contacto__tel tel" href="tel:{N['telefono_e164']}" data-zona="contacto">{N['telefono']}</a>
   {T.estado()}
   <address class="prosa">
    <p><strong>Horario:</strong> {N['horario_texto']}. {texto('contacto_horario_extra')}</p>
    <p><strong>Correo:</strong> <a href="mailto:{N['email']}">{N['email']}</a></p>
    <p><strong>Dirección:</strong> <a href="{FICHA}" rel="noopener" target="_blank">{N['calle']}, {N['cp']} {N['localidad']}</a></p>
    {extra}
   </address>
   <div class="acciones">{T.btn_whatsapp("btn--linea")}</div>
  </div>
  <div class="contacto__form">{formulario()}</div>
 </div>
</section>
"""


# ---------- Página ----------
def es_widget(s):
    return any(tt == "p" and ES_WIDGET(c) for tt, c in s["bl"])


def pagina(p):
    t = datos.tipo_de(p["url"])
    intro, secs = secciones(p["bloques"])
    pb = pueblo_de(p["url"]) if t == "municipio" else None
    T.CTX["pueblo"] = pb
    cuerpo, op, cta = [], None, None
    uls = [c for tt, c in intro if tt == "ul"]
    ul = uls[0] if uls else None
    normales = []
    for k, s in enumerate(secs):
        if ES_CTA.match(s["h2"]) or (CTA_ULTIMO and k == len(secs) - 1 and not es_widget(s)):
            ps = [c for tt, c in s["bl"] if tt == "p"]
            cta = (inline(s["h2"]), " ".join(inline(x) for x in ps) or None)
        elif es_widget(s):
            ps = [c for tt, c in s["bl"] if tt == "p" and not c.startswith("(") and not c.startswith("[[")]
            op = op or (inline(s["h2"]), " ".join(inline(x) for x in ps))
        elif t == "contacto" and s["h2"] in CONTACTO_YA:
            continue
        else:
            normales.append(s)
    if t == "home":
        cuerpo.append(portada_home(p))
        dec, resto = reparte_intro(intro)
        cuerpo.append(manifiesto(p, dec, ul))
        if resto and normales:
            normales[0]["bl"] = resto + normales[0]["bl"]
        hay_filas = any(sum(1 for tt, c in s["bl"] if tt == "p" and FILA.match(c)) >= 3 for s in normales)
        if SERVICIOS_SECCION and not hay_filas:
            cuerpo.append(servicios_seccion())
        puesto_mapa = False
        for n, s in enumerate(normales, 1):
            if s["h2"].startswith(HORARIO_H2):
                cuerpo.append(horario_html(s)); cuerpo.append(mapa()); puesto_mapa = True
            else:
                cuerpo.append(bloque_home(s, n))
                if ZONA_H2 and s["h2"].startswith(ZONA_H2):
                    cuerpo.append(zona_html())
            if n == CIFRAS_EN.get("home"):
                cuerpo.append(cifras())
                cuerpo.append(logos_html())
        if not puesto_mapa:
            cuerpo.append(mapa())
    elif t == "contacto":
        cuerpo.append(portada_interior(p, t))
        cuerpo.append(contacto_cuerpo(p, intro))
        cuerpo.append(mapa())
        if normales:
            cuerpo.append(lectura(p, [], [], normales))
    else:
        cuerpo.append(portada_interior(p, t))
        dec, resto = reparte_intro(intro)
        cuerpo.append(lectura(p, dec, resto, normales, ul))
        if CIFRAS_EN.get(t):
            cuerpo.append(cifras())
    cuerpo.append(opiniones(pb, *(op or (None, ""))))
    cuerpo.append(faq_html(p["faq"]))
    if t != "contacto":
        cuerpo.append(banda(p["url"], *(cta or (None, None))))
    robots = "noindex, follow" if (t == "contacto" and not CONTACTO_INDEXABLE) else "index, follow"
    pre = None
    if t == "home":
        b = OBJETO_PORTADA["imagen"].rsplit(".", 1)[0]
        pre = (f"/img/{b}-420.webp 420w, /img/{b}-840.webp 840w", OBJ_SIZES)
    return montar(T.cabeza(p, schema_de(p), robots, precarga=pre) + T.cabecera(p["url"]) + "".join(cuerpo) + T.pie())


def montar(h):
    """El sprite de la página (solo los iconos que usa) se inserta al abrir <body>."""
    return h.replace("<!--SPRITE-->", T.sprite(h), 1)


# ---------- Legales y 404 ----------
def legales():
    txt = open(os.path.join(RAIZ, "contenido", "legales", "legales.md"), encoding="utf-8").read()
    res = []
    for m in re.finditer(r"^## (/[^\n]+/)\n(.*?)(?=^## /|\Z)", txt, re.S | re.M):
        url, cuerpo = m.group(1).strip(), m.group(2).strip()
        lineas = cuerpo.split("\n")
        res.append((url, lineas[0].strip(), "\n".join(lineas[1:]).strip().replace("\n---", "")))
    return res


META_LEGAL = {
    "/aviso-legal/": "Aviso legal de elgordoyelflaco.es: datos del titular de El Gordo y el Flaco, agencia SEO en Alcorcón, condiciones de uso y propiedad intelectual.",
    "/politica-de-privacidad/": "Política de privacidad de El Gordo y el Flaco: qué datos recogen los formularios de la web, para qué se usan y cómo ejercer sus derechos.",
    "/politica-de-cookies/": "Política de cookies de elgordoyelflaco.es: qué cookies son técnicas, cuáles se activan solo si las acepta y cómo cambiar su decisión.",
}


def pagina_legal(url, titulo, md):
    T.CTX["pueblo"] = None
    p = {"url": url, "title": f"{titulo} | {N['nombre']}", "meta": META_LEGAL.get(url, f"{titulo} de {DOMINIO.split('//')[1]}."), "h1": titulo}
    NOMBRE_CORTO[url] = titulo
    bl = []
    for par in re.split(r"\n\s*\n", md):
        par = par.strip()
        if not par:
            continue
        bl.append(("h2l", par) if (len(par) < 90 and not par.endswith(".") and "\n" not in par) else ("p", par))
    def parrafo(c):
        lineas = [x for x in c.split("\n") if x.strip()]
        if lineas and all(re.match(r"^\s*[-*]\s+", x) for x in lineas):   # lista de guiones → <ul>
            return "<ul>" + "".join("<li>" + inline(re.sub(r"^\s*[-*]\s+", "", x)) + "</li>" for x in lineas) + "</ul>"
        return "".join(f"<p>{inline(x)}</p>" for x in lineas)
    htmlc = "".join(f'<h2 class="h2-lect">{esc(c)}</h2>' if t == "h2l" else parrafo(c) for t, c in bl)
    schema = {"@context": "https://schema.org", "@graph": [negocio_schema(), {"@type": "WebPage", "url": DOMINIO + url, "name": titulo,
                                                                          "dateModified": fecha_mod(os.path.join(RAIZ, "contenido", "legales", "legales.md"))}]}
    # Indexables: en producción ninguna página lleva noindex (regla 10); el noindex es solo de la vista previa
    return montar(T.cabeza(p, schema, "index, follow") + T.cabecera(url) + f"""<section class="cab-int cab-int--legal"><div class="contenedor">{migas_html(url)}<h1 class="h1-int">{esc(titulo)}</h1></div></section>
<section class="seccion"><div class="contenedor"><div class="prosa legal">{htmlc}</div></div></section>""" + T.pie())


def pagina_404():
    T.CTX["pueblo"] = None
    p = {"url": "/404/", "title": f"Página no encontrada | {N['nombre']}", "meta": "Esta página no existe.", "h1": "Esta página no existe"}
    schema = {"@context": "https://schema.org", "@graph": [negocio_schema()]}
    return montar(T.cabeza(p, schema, "noindex, follow") + T.cabecera("") + f"""<section class="cab-int"><div class="contenedor"><p class="etiqueta">{T.simbolo("etiqueta__sim")}Error 404</p><h1 class="h1-int">Esta página no existe</h1>
<p class="cab-int__corta">{texto("error_texto")}</p>
<div class="acciones">{T.btn_llamar()}{T.boton("Ir al inicio", "/", "btn--linea")}</div></div></section>""" + T.pie())


def fecha_mod(ruta):
    import datetime, subprocess
    hoy = datetime.date.today().isoformat()
    try:
        r = subprocess.run(["git", "status", "--porcelain", "--", ruta], cwd=RAIZ, capture_output=True, text=True, timeout=20)
        if r.returncode == 0:
            if r.stdout.strip():
                return hoy
            f = subprocess.run(["git", "log", "-1", "--format=%cs", "--", ruta], cwd=RAIZ, capture_output=True, text=True, timeout=20).stdout.strip()
            if f:
                return f
    except Exception:
        pass
    try:
        return datetime.date.fromtimestamp(os.path.getmtime(ruta)).isoformat()
    except OSError:
        return hoy


def escribir(url, contenido):
    ruta = os.path.join(SITIO, url.strip("/"), "index.html") if url != "/" else os.path.join(SITIO, "index.html")
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    open(ruta, "w", encoding="utf-8").write(contenido)


def main():
    if os.path.isdir(SITIO):
        shutil.rmtree(SITIO)
    os.makedirs(SITIO)
    urls = []
    for p in PAGINAS:
        p["mod"] = fecha_mod(p["ruta"])
        escribir(p["url"], pagina(p))
        if CONTACTO_INDEXABLE or datos.tipo_de(p["url"]) != "contacto":
            urls.append((p["url"], p["mod"]))
    for url, tit, md in legales():
        escribir(url, pagina_legal(url, tit, md))
        urls.append((url, fecha_mod(os.path.join(RAIZ, "contenido", "legales", "legales.md"))))
    open(os.path.join(SITIO, "404.html"), "w", encoding="utf-8").write(pagina_404())
    sm = "".join(f"<url><loc>{DOMINIO}{u}</loc><lastmod>{f}</lastmod></url>" for u, f in urls)
    open(os.path.join(SITIO, "sitemap.xml"), "w", encoding="utf-8").write(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>\n')
    open(os.path.join(SITIO, "robots.txt"), "w", encoding="utf-8").write(
        f"User-agent: *\nAllow: /\nDisallow: /enviar.php\n\nSitemap: {DOMINIO}/sitemap.xml\n")
    datos_neg = [f"- Nombre: {N['nombre']} ({N['razon_social']}).",
                 f"- Dirección: {N['calle']}, {N['cp']} {N['localidad']} ({N['provincia']}).",
                 f"- Teléfono: {N['telefono']} · Correo: {N['email']} · Ficha de Google: {FICHA}",
                 f"- Horario: {N['horario_texto']}. {texto('llms_horario_extra')}".rstrip(),
                 *TEXTOS["llms_datos"]]
    if N.get("pago"):
        datos_neg.append(f"- Pago: {N['pago']}.")
    llms = [texto("llms_titulo"), "",
            f"> {texto('llms_resumen')} {N['horario_texto']}. Teléfono {N['telefono']}. {N['valoracion']} en Google" + (f" con {N['resenas']} reseñas." if getattr(C, "NOTA_CON_NUMERO", True) else "."), "",
            "## Datos del negocio", *datos_neg]
    no_hace = [x for x in TEXTOS.get("llms_no_hace", []) if x]
    if not N.get("cambia_equipos") and TEXTOS.get("llms_no_instala"):
        no_hace.append(TEXTOS["llms_no_instala"])
    if no_hace:
        llms += ["", f"## Lo que {N['nombre']} no hace", *no_hace]
    llms += ["", "## Páginas principales"]
    llms += [f"- [{nombre(u)}]({DOMINIO}{u}): {POR_URL[u]['meta']}" for u in LLMS_PRINCIPALES if u in POR_URL]
    marcas = [u for u in LLMS_MARCAS if u in POR_URL]
    if marcas:
        llms += ["", "## Marcas"] + [f"- [{nombre(u)}]({DOMINIO}{u}): {POR_URL[u]['meta']}" for u in marcas]
    if PUEBLO:
        llms += ["", "## Municipios"] + [f"- [{v}]({DOMINIO}{k})" for k, v in PUEBLO.items() if k in POR_URL]
    open(os.path.join(SITIO, "llms.txt"), "w", encoding="utf-8").write("\n".join(llms) + "\n")
    print(f"build: {len(PAGINAS)} páginas + {len(legales())} legales + 404 · sitemap con {len(urls)} URLs")


if __name__ == "__main__":
    main()
