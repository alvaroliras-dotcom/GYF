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
                    CTA_H2, CTA_ULTIMO, ZONA_H2, HORARIO_H2, CTA_EXTRA, texto,
                    CASOS_ETQ, OBJETO_URL, OBJETO_MUNICIPIO, CASO_URL, IMG_SERVICIO, OBJETOS_CIFRAS, QUIEN_H2,
                    PIEZAS_VIVAS, PIEZAS_ETQ, CASOS_H2, SERVICIOS_HOME as _SH, OBJETOS_FUCSIA, FOTOS, LOGOTIPO_FOTO)
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
        "alternateName": getattr(C, "ALTERNATE_NAME", N["nombre"]),
        "url": DOMINIO + "/", "telephone": N["telefono_e164"], "email": N["email"],
        "logo": DOMINIO + "/android-chrome-512x512.png", "image": DOMINIO + "/og-image.jpg",
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
    ss = getattr(C, "SERVICIO_SCHEMA", {})
    if ss:   # v5 · catálogo de servicios del negocio
        d["hasOfferCatalog"] = {"@type": "OfferCatalog", "name": "Servicios", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "@id": DOMINIO + u + "#servicio", "name": n}} for u, (n, _) in ss.items()]}
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


FAQ_MARCADAS = set()


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
        ss = getattr(C, "SERVICIO_SCHEMA", {})
        if p["url"] in ss:   # v5 · servicio: nombre y tipo propios; zona: los 11 municipios
            nom, tipo = ss[p["url"]]
            area = [{"@type": "City", "name": a} for a in [BASE] + [v for k, v in PUEBLO.items() if v != BASE]]
            g.append({"@type": "Service", "@id": url + "#servicio", "name": nom, "serviceType": tipo, "provider": {"@id": NEG_ID},
                      "url": url, "areaServed": area, "description": p["meta"]})
        else:                # municipio o página de la marca
            pb = PUEBLO.get(p["url"], BASE)
            g.append({"@type": "Service", "@id": url + "#servicio", "name": f"SEO local y marketing online para negocios de {pb}",
                      "serviceType": "SEO local", "provider": {"@id": NEG_ID}, "url": url,
                      "areaServed": {"@type": "City", "name": pb}, "description": p["meta"]})
    # v5: cada pregunta se marca en una sola página (la primera que la trae); en las demás se ve, pero no va al schema
    faq_propia = [(q, a) for q, a in p["faq"] if q.strip().lower() not in FAQ_MARCADAS]
    FAQ_MARCADAS.update(q.strip().lower() for q, _ in faq_propia)
    if faq_propia:
        g.append({"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", inline(a))}}
            for q, a in faq_propia]})
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


CTX_PAG = {"home": False}
TONOS_APIL = ["oscuro", "acento", "claro", "oscuro", "acento", "claro", "oscuro"]
CASO_POR_NOMBRE = {c[0]: c for c in CASOS}


def foto_caso(nombre, sizes, clase="", grande=True):
    c = CASO_POR_NOMBRE.get(nombre)
    if not c:
        return ""
    return T.foto(c[5] if grande else c[2], f"{c[0]}: {c[1]}", sizes, clase=clase)


FOTOS_DIR = os.path.join(RAIZ, "recursos", "fotos")


def archivo_foto(nombre):
    """El archivo real de una foto en recursos/fotos/ con ese nombre (acepta .jpg, .jpeg, .png o .webp), o None."""
    base = nombre.rsplit(".", 1)[0]
    for ext in (".jpg", ".jpeg", ".png", ".webp"):
        if os.path.exists(os.path.join(FOTOS_DIR, base + ext)):
            return base + ext
    return None


FOTOS_PENDIENTES = set()


def foto_hueco(clave, sizes, clase="", prioridad=False):
    """v3 · Hueco de foto integrado en el diseño: encuadre (aspect-ratio), tratamiento (duotono o viñeta) y, mientras
    no llega la foto, un marcador de la marca (degradado con el símbolo grande recortado). Basta con soltar el archivo
    en recursos/fotos/ con el nombre de config.FOTOS y regenerar."""
    f = FOTOS.get(clave)
    if not f:
        return ""
    real = archivo_foto(f["archivo"])
    if real:
        cuerpo = T.foto(real, f["alt"], sizes, prioridad, clase="fotohueco__img")
        aria = ""
    else:
        FOTOS_PENDIENTES.add(f["archivo"])
        cuerpo = f'<span class="fotohueco__marca">{T.simbolo("fotohueco__sim")}</span>'
        aria = ' aria-hidden="true"'
    return (f'<figure class="fotohueco fotohueco--{f["trat"]}{"" if real else " fotohueco--vacio"} {clase}" style="--ar:{f["formato"]}"'
            f' data-foto="{A(f["archivo"])}"{aria}>{cuerpo}</figure>')


def apiladas_html(items):
    """v2 · Servicios en tarjetas apiladas de Rayo (R7): berenjena, fucsia, blanca… Se pegan arriba al hacer
    scroll (position: sticky, sin JS) y la de debajo encoge un poco cuando llega la siguiente (GSAP).
    Cada tarjeta: icono, título, número, el texto del servicio con su enlace, etiquetas, un caso real y su objeto 3D."""
    out = []
    for i, (tit, cuerpo) in enumerate(items):
        m = URL_1.search(cuerpo)
        u = m.group(1) if m else None
        tono = TONOS_APIL[i % len(TONOS_APIL)]
        ic = T.ico(ICONO_URL[u]) if u in ICONO_URL else T.simbolo()
        etq = "".join(f"<li>{esc(e)}</li>" for e in ETQ_URL.get(u, []))
        caso = T.foto(IMG_SERVICIO[u][0], IMG_SERVICIO[u][1], "(max-width: 900px) 90vw, 46vw", clase="apil__foto") if u in IMG_SERVICIO else ""
        obj = T.objeto(OBJETO_URL[u], "(max-width: 900px) 40vw, 300px", "apil__obj") if u in OBJETO_URL else ""
        tit_h = f'<a href="{u}">{inline(tit.rstrip(".:"))}</a>' if u else inline(tit.rstrip(".:"))
        out.append(f"""<li class="apil apil--{tono}" style="--i:{i}" data-apil>
 <div class="apil__in">
  <div class="apil__txt">
   <div class="apil__cab"><span class="apil__ico">{ic}</span><span class="apil__num" aria-hidden="true">/{i + 1:02d}</span></div>
   <h3 class="apil__tit">{tit_h}</h3>
   <p class="apil__p">{inline(cuerpo)}</p>
   {f'<ul class="apil__etq">{etq}</ul>' if etq else ""}
  </div>
  <div class="apil__vis">{foto_hueco(u, "(max-width: 900px) 40vw, 22vw", "apil__fh")}<div class="apil__caso">{caso}</div>{obj}</div>
 </div>
</li>""")
    return f'<ol class="apiladas">{"".join(out)}</ol>'


def filas_html(items, clase=""):
    """«**Título.** texto» seguidos (3 o más) → filas de Rayo con línea, icono y «/ 01» (R27: las demás se apagan).
    En la home (v2), tarjetas apiladas."""
    if CTX_PAG["home"]:
        return apiladas_html(items)
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


NOMBRE_ITEM = re.compile(r"^\*\*(.+?)\*\*,\s*(.+)$")


def rejilla_nombres(items):
    """v5 · Listas «**Nombre**, qué hace» que son el equipo de agentes o una muestra de trabajos: en rejilla.
    Agentes: objeto 3D de su oficio y nombre (decisión de Álvaro: sin caras). Trabajos: miniatura del caso si la hay."""
    ms = [NOMBRE_ITEM.match(x) for x in items]
    if not all(ms) or len(ms) < 3:
        return ""
    ag = getattr(C, "AGENTES_OBJETO", {})
    if all(m.group(1) in ag for m in ms):
        li = "".join(f'<li class="agente rv"><span class="agente__obj" aria-hidden="true">{T.objeto(ag[m.group(1)], "160px")}</span>'
                     f'<strong class="agente__n">{esc(m.group(1))}</strong><span class="agente__t">{inline(m.group(2).rstrip("."))}</span></li>' for m in ms)
        return f'<ul class="agentes">{li}</ul>'
    alias = getattr(C, "MUESTRA_CASO", {})
    casos = [CASO_POR_NOMBRE.get(alias.get(m.group(1), m.group(1))) for m in ms]
    if sum(1 for c in casos if c) * 2 < len(ms):
        return ""
    li = []
    for m, c in zip(ms, casos):
        mf = getattr(C, "MUESTRA_FOTO", {}).get(m.group(1))   # v5.7: maqueta propia de una muestra que no está en la galería
        if not c and mf and os.path.exists(os.path.join(RAIZ, "recursos", "casos", mf[0])):
            c = (m.group(1), mf[1], mf[0])
        mini = (T.foto(c[2], f"{m.group(1)}: {c[1]}", "(max-width: 700px) 44vw, 240px", clase="muestra__foto") if c
                else f'<span class="muestra__obj" aria-hidden="true">{T.objeto(getattr(C, "MUESTRA_OBJETO", {}).get(m.group(1), "estrella-cromo"), "160px")}</span>')
        li.append(f'<li class="muestra rv{"" if c else " muestra--sin"}">{mini}<strong>{esc(m.group(1))}</strong><span>{inline(m.group(2))}</span></li>')
    return f'<ul class="muestras">{"".join(li)}</ul>'


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
            elif (rej := rejilla_nombres(c)):
                pon(rej, True)
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


def ver_de(tit):
    """v5.7 · Texto del enlace de cada caso: «Ver la web» o, si no tiene web, «Ver la ficha»."""
    return getattr(C, "CASOS_VER_CASO", {}).get(tit, CASOS_VER)


def caso_html(c, i):
    tit, sub, img, url, fmt = c[:5]
    fmt = fmt if fmt in FORMATOS_OK else "v"
    cuerpo = T.foto(img, f"{tit}: {sub}", "(max-width: 900px) 70vw, 34vw", clase="caso__foto")
    ojo = f'<span class="caso__ojo" aria-hidden="true">{T.ico("flecha-diagonal")}{esc(ver_de(tit))}</span>' if url else ""
    pie = f'<p class="caso__pie"><strong>{esc(tit)}</strong> {esc(sub)}</p>'
    dentro = f'<div class="caso__marco">{cuerpo}{ojo}</div>{pie}'
    if url:
        ext = ' rel="noopener" target="_blank"' if url.startswith("http") else ""
        dentro = f'<a href="{A(url)}"{ext}>{dentro}</a>'
    return f'<li class="caso caso--{fmt} caso--{i}" data-vel="{(.9, 1.15, .95, 1.2, 1.05, .9, 1.12)[i % 7]}">{dentro}</li>'


def portada_home(p):
    """Portada A de Rayo: H1 arriba a la izquierda, cinta gigante que acelera con el scroll (R14) con el objeto
    encima (R28 / 3D), servicios en dos columnas abajo a la izquierda y tarjeta de conversión abajo a la derecha.
    Debajo, la galería de casos que sube por encima de la portada fija (R5, solo ordenador)."""
    etiqueta, corta = etiqueta_y_entrada(p)
    serv = "".join(f'<li><a href="{u}">{T.ico(ic)}<span>{esc(t)}</span></a></li>' for t, _, u, ic, _, _ in SERVICIOS_HOME)
    extra = f'<a class="tarjeta__extra" href="#pedir-auditoria">{esc(CTA_EXTRA[0])} {T.ico("flecha-diagonal")}</a>' if CTA_EXTRA else ""
    tarjeta = f"""<aside class="tarjeta" aria-label="Contacto" data-sale>
     <span class="tarjeta__obj" aria-hidden="true">{T.objeto("estrella", "96px", "flota-lenta")}</span>
     {T.estado()}
     {T.nota("tarjeta__nota", "#opiniones" if OPINIONES else FICHA)}
     <a class="tarjeta__ir" href="#te-llamamos" data-zona="tarjeta_portada"><span>{texto("tarjeta_titulo")}</span><strong>{texto("tarjeta_ir")} ↓</strong></a>
     {extra}
    </aside>"""
    # v5.9 (portada B, Álvaro 28/09): titular enorme con la parte clave en fucsia; la cinta sale de la portada y abre
    # la galería. Fuera la chincheta y la estrella sueltas. v5.9.1: abajo, una fila hasta el borde de la pantalla con
    # el texto y los botones, la G+F 3D en el centro, los servicios y la tarjeta (todo cabe en la primera pantalla).
    h1_home = esc(p['h1'])
    ac = getattr(C, "H1_ACENTO", "")
    if ac and ac in p['h1']:
        h1_home = esc(p['h1']).replace(esc(ac), f'<span class="h1-home__acento">{esc(ac)}</span>', 1)
    galeria = ""
    # v5.2: la galería de portada no repite los casos que se cuentan en «Lo más reciente»
    gal = [c for c in CASOS if c[0] not in getattr(C, "CASOS_RECIENTES", [])][:7] or CASOS[:7]
    gal = gal + list(getattr(C, "GALERIA_EXTRA", []))   # v5.8: la galería enseña también los trabajos de la muestra
    if CASOS:
        # v5.7 (Álvaro 03/10): las tarjetas pequeñas se quitan (los trabajos van en grande en el escaparate de
        # «Lo más reciente»); la cinta gigante se queda
        lista = (f'<ul class="galeria__lista galeria__lista--{len(gal)}">{"".join(caso_html(c, i) for i, c in enumerate(gal))}</ul>'
                 if getattr(C, "GALERIA_PORTADA", True) else "")
        galeria = (f'<section class="galeria{"" if lista else " galeria--solo-cinta"}" aria-label="Trabajos recientes" data-galeria>'
                   f'<div class="galeria__cinta">{T.cinta(CINTA_PORTADA, "cinta--gigante")}</div>{lista}</section>')
    return f"""<div class="hero{' hero--galeria' if galeria else ''}" data-hero>
<section class="portada-a" data-portada>
 <div class="contenedor portada-a__top" data-sale>
  <p class="etiqueta">{T.simbolo("etiqueta__sim")}{etiqueta}</p>
  <div class="h1-caja"><h1 class="h1-home">{h1_home}</h1></div>
 </div>
 <div class="contenedor portada-a__pie">
  <div class="portada-a__texto" data-sale>
   <p class="portada-a__corta">{corta}</p>
   <div class="acciones">{T.btn_llamar(extra=' data-zona="portada_boton"')}{T.btn_whatsapp("btn--linea")}</div>
   {T.nota("portada-a__nota", "#opiniones" if OPINIONES else FICHA)}
   <p class="portada-a__gratis">{T.ico("check")}{esc(texto("portada_gratis"))}</p>
  </div>
  <div class="portada-a__centro">{objeto_html()}</div>
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
    if t == "home" and extra:   # v5.17: en la portada, la auditoría tiene su sección y el botón baja a ella
        extra = T.boton(CTA_EXTRA[0], "#pedir-auditoria", "btn--linea")
    if u == URLS.get("auditoria", "/auditoria-seo-local/"):   # v5.1: en la auditoría, lo primero es pedirla
        acciones_portada = (T.boton(texto("aud_boton"), "#pedir-auditoria", "btn--acento", "flecha-diagonal", ' data-zona="portada_auditoria"')
                            + T.btn_whatsapp("btn--linea", t=texto("whatsapp_auditoria"), rotulo="Pedirla por WhatsApp")
                            + T.btn_llamar("btn--linea", extra=' data-zona="portada_boton"'))
    else:
        acciones_portada = T.btn_llamar(extra=' data-zona="portada_boton"') + T.btn_whatsapp("btn--linea", pueblo=pb) + extra
    # v2 · Tarjeta visual a la derecha: el objeto 3D del servicio sobre fucsia, o el pueblo con la chincheta sobre berenjena
    if t == "municipio":
        # v5: foto propia de cada municipio (config.FOTOS «municipio-<slug>») si ya está en recursos/fotos; si no, la común
        clave_m = "municipio-" + u.replace(URLS["municipio"], "").strip("/")
        if not (FOTOS.get(clave_m) and archivo_foto(FOTOS[clave_m]["archivo"])):
            clave_m = "municipio"
        vis = (f'<div class="cab-int__vis cab-int__vis--oscuro" aria-hidden="true">{foto_hueco(clave_m, "(max-width: 1000px) 92vw, 36vw", "cab-int__fh")}'
               f'{T.objeto(OBJETO_MUNICIPIO, "(max-width: 1000px) 50vw, 340px", "cab-int__obj flota-lenta", prioridad=True)}</div>')
    elif u in OBJETO_URL:
        # los objetos casi todo fucsia van sobre berenjena; los de cromo o crema, sobre fucsia
        tono = "oscuro" if OBJETO_URL[u] in OBJETOS_FUCSIA else "acento"
        vis = (f'<div class="cab-int__vis cab-int__vis--{tono}" aria-hidden="true">{foto_hueco(u, "(max-width: 1000px) 92vw, 36vw", "cab-int__fh")}'
               f'{T.objeto(OBJETO_URL[u], "(max-width: 1000px) 50vw, 340px", "cab-int__obj flota-lenta", prioridad=True)}</div>')
    else:
        vis = ""
    return f"""<section class="cab-int{' cab-int--vis' if vis else ''}">
 <div class="contenedor">
  {migas_html(u)}
  <div class="cab-int__grid">
   <p class="etiqueta cab-int__etq">{T.simbolo("etiqueta__sim")}{etiqueta}</p>
   <div class="cab-int__txt">
    <h1 class="h1-int{' h1-int--largo' if len(p['h1']) > 44 else ''}"><span class="h1__pildora" aria-hidden="true">{pild}</span>{esc(p['h1'])}</h1>
    <p class="cab-int__corta">{corta}</p>
    <div class="acciones">{acciones_portada}</div>
   </div>
   {vis}
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
 {f'<div class="contenedor foto-sangre rv">{foto_hueco("portada", "(max-width: 900px) 100vw, 92vw")}</div>' if p["url"] == "/" else ""}
</section>
"""


def bloque_home(sec, n):
    """Sección de la home con la anatomía de «Company»: H2 a la izquierda (5/12, segunda mitad en gris que se
    enciende), entradilla y texto a la derecha; filas, pasos, tablas y enlaces a ancho completo debajo.
    v2: la de los pasos va en franja berenjena de lado a lado; «Dónde trabajamos» en franja fucsia con la cinta
    y los municipios; «¿Quién hay detrás…?» con tres piezas que giran; «Lo más reciente» con los casos clavados."""
    h = sec["h2"]
    if QUIEN_H2 and h.startswith(QUIEN_H2):
        return quien_html(sec)
    if CASOS_H2 and h.startswith(CASOS_H2):
        return proyectos_html(sec)
    estr = []
    cuerpo = render_bloques(sec["bl"], estr)
    partes = re.split(r"(?<=</p>)\n", cuerpo, maxsplit=1)
    primero = partes[0].replace("<p>", '<p class="entradilla">', 1) if partes[0].startswith("<p>") else partes[0]
    resto = partes[1] if len(partes) > 1 else ""
    zona = ZONA_H2 and h.startswith(ZONA_H2)
    oscuro = any(t == "ol" for t, _ in sec["bl"])
    clase, deco, tras = "seccion blq", "", ""
    if oscuro:
        clase = "franja franja--oscuro blq"
        deco = f'<span class="franja__obj franja__obj--pasos" aria-hidden="true">{T.objeto("bocadillo", "(max-width: 900px) 40vw, 320px", "flota-lenta")}</span>' + marca_agua()
    elif zona:
        clase = "franja franja--acento blq"
        deco = f'<span class="franja__obj franja__obj--zona" aria-hidden="true">{T.objeto("chincheta", "(max-width: 900px) 36vw, 260px", "flota-lenta")}</span>'
        tras = zona_html()
    return f"""<section class="{clase}" id="{slug(h)}">
 {deco}
 <div class="contenedor">
  <div class="blq__cab">
   <div class="blq__tit"><h2 class="{h2c(h)}">{h2_gris(h)}</h2>{foto_hueco("zonas", "(max-width: 1000px) 92vw, 36vw", "blq__foto rv") if zona else ""}</div>
   <div class="blq__txt prosa rv">{primero}{resto}</div>
  </div>
  {foto_hueco("pasos", "(max-width: 900px) 100vw, 92vw", "franja__foto rv") if oscuro else ""}
  {"".join(estr) if not zona else ""}
 </div>
 {tras}
</section>
"""


def parrafos(sec):
    return [c for t, c in sec["bl"] if t == "p"]


def quien_html(sec):
    """v2 · «¿Quién hay detrás…?»: H2 y primer párrafo arriba; los párrafos 2, 3 y 4 (interlocutor, profesionales,
    agentes de IA) en tres tarjetas altas con una pieza 3D que gira en vivo en ordenador (imagen fija de respaldo);
    el resto del texto debajo. El texto es el de contenido/, sin tocar."""
    ps = parrafos(sec)
    if len(ps) < 4:
        return bloque_generico(sec)
    tonos = ["oscuro", "acento", "claro"]
    tarj = []
    for i, (pz, img, giro, mats) in enumerate(PIEZAS_VIVAS[:3]):
        tarj.append(f"""<li class="pieza pieza--{tonos[i]} rv" data-pieza="{pz}" data-giro="{giro}" data-mats="{mats}">
   <div class="pieza__vis" aria-hidden="true">{T.objeto(img, "(max-width: 900px) 70vw, 360px", "pieza__img")}<div class="pieza__lienzo" data-lienzo></div></div>
   <p class="pieza__etq"><span>{i + 1:02d}</span>{esc(PIEZAS_ETQ[i])}</p>
   <p class="pieza__txt">{inline(ps[i + 1])}</p>
  </li>""")
    resto = "".join(f"<p>{inline(x)}</p>" for x in ps[4:])
    return f"""<section class="seccion blq quien" id="{slug(sec['h2'])}">
 <div class="contenedor">
  <h2 class="{h2c(sec['h2'])} quien__h2">{h2_gris(sec['h2'])}</h2>
  <div class="quien__cab">
   {foto_hueco("quien", "(max-width: 1000px) 92vw, 36vw", "quien__foto rv")}
   <div class="prosa rv"><p class="entradilla">{inline(ps[0])}</p>{resto}</div>
  </div>
  <ul class="piezas" data-piezas>{"".join(tarj)}</ul>
 </div>
</section>
"""


def bloque_generico(sec):
    estr = []
    cuerpo = render_bloques(sec["bl"], estr)
    return f"""<section class="seccion blq" id="{slug(sec['h2'])}"><div class="contenedor"><div class="blq__cab"><h2 class="{h2c(sec['h2'])}">{h2_gris(sec['h2'])}</h2>
   <div class="blq__txt prosa rv">{cuerpo}</div></div>{"".join(estr)}</div></section>"""


ESC_SIZES = "(max-width: 1099px) 94vw, 72vw"


def escaparate_html(sec):
    """v5.7 · «Lo más reciente» como escaparate (Álvaro 03/10: «tarjetas más grandes que saltan solas a la
    siguiente, y si pinchas, también»). Una pila de tarjetas grandes con la maqueta 16:9 de cada trabajo
    (herramientas/maquetas/escaparate.py: portátil o sobremesa con el dominio real + móvil; en las fichas, el mapa).
    Pasa sola cada 6 s, se pausa con su botón, al salir de pantalla y con «reducir movimiento»; al pinchar la tarjeta
    salta a la siguiente. Sin JavaScript es una tira horizontal con desplazamiento. Todos los textos van en el HTML."""
    ps = parrafos(sec)
    txt = "".join(f"<p>{inline(x)}</p>" for x in ps)
    orden = list(getattr(C, "CASOS_RECIENTES", [])) + [c[0] for c in CASOS if c[0] not in getattr(C, "CASOS_RECIENTES", [])]
    lista_c = [CASO_POR_NOMBRE[n] for n in orden if n in CASO_POR_NOMBRE and n in C.ESCAPARATE]
    lista_c += [tuple(e) + (None,) for e in getattr(C, "GALERIA_EXTRA", []) if e[0] in C.ESCAPARATE]
    total = len(lista_c)
    items = []
    for i, c in enumerate(lista_c):
        tit, sub, _, url, _, _ = c
        archivo, alt = C.ESCAPARATE[tit]
        muni, partida = getattr(C, "CASO_DETALLE", {}).get(tit, (None, None))
        etq = "".join(f"<li>{esc(e)}</li>" for e in CASOS_ETQ.get(tit, []))
        foto = T.foto(archivo, alt, ESC_SIZES, clase="esc__foto")
        ver = ""
        if url:
            ext = ' rel="noopener" target="_blank"' if url.startswith("http") else ""
            txt_ver = getattr(C, "CASOS_VER_CASO", {}).get(tit, CASOS_VER)
            from trabajos import TRABAJOS as _TR
            _t = next((x for x in _TR if x["nombre"] == tit), None)
            if _t:   # v5.11: la tarjeta lleva a la ficha del trabajo; la web del cliente se enlaza desde la ficha
                url, ext, txt_ver = f"/trabajos/{_t['slug']}/", "", "Ver el trabajo"
            ver = f'<a class="esc__ver" href="{A(url)}"{ext} data-zona="escaparate_ver">{esc(txt_ver)}{T.ico("flecha-diagonal")}<span class="sr"> de {esc(tit)}{" (se abre en otra pestaña)" if ext else ""}</span></a>'
        items.append(f"""<li class="esc__item" data-esc-item aria-roledescription="diapositiva" aria-label="{i + 1} de {total}: {A(tit)}">
   <article class="esc__tarjeta">
    <div class="esc__marco">{foto}<ul class="esc__etq">{etq}</ul></div>
    <div class="esc__info">
     <p class="esc__num" aria-hidden="true">{i + 1:02d}<span>/{total:02d}</span></p>
     <div class="esc__nombre"><h3 class="esc__tit">{esc(tit)}</h3><p class="esc__sub">{esc(sub)}{f" · {esc(muni)}" if muni else ""}</p></div>
     {f'<p class="esc__res">{esc(partida)}</p>' if partida else '<p class="esc__res"></p>'}
     {ver}
    </div>
   </article>
  </li>""")
    pausa = ('<svg class="ico esc__i-pausa" viewBox="0 0 24 24" aria-hidden="true"><rect x="6.5" y="5" width="3.6" height="14" rx="1.2" fill="currentColor"/><rect x="13.9" y="5" width="3.6" height="14" rx="1.2" fill="currentColor"/></svg>'
             '<svg class="ico esc__i-play" viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5.6v12.8a1 1 0 0 0 1.5.86l10.2-6.4a1 1 0 0 0 0-1.72L9.5 4.74A1 1 0 0 0 8 5.6z" fill="currentColor"/></svg>')
    return f"""<section class="seccion escaparate" id="casos">
 <div class="contenedor">
  <div class="escaparate__cab">
   <h2 class="h2 enciende">{h2_gris(sec['h2'])}</h2>
   <div class="prosa">{txt}</div>
  </div>
  <div class="esc" data-esc role="region" aria-roledescription="carrusel" aria-label="Trabajos recientes">
   <ol class="esc__pila" data-esc-pila aria-live="off">
  {"".join(items)}
   </ol>
   <div class="esc__mando" data-esc-mando hidden>
    <button class="esc__btn esc__btn--ant" type="button" data-esc-ant aria-label="Trabajo anterior">{T.ico("flecha-derecha")}</button>
    <p class="esc__cuenta" aria-hidden="true"><b data-esc-n>01</b> / {total:02d}</p>
    <div class="esc__nombres" aria-hidden="true">{"".join(f'<span>{esc(c[0])}</span>' for c in lista_c)}</div>
    <span class="esc__progreso" aria-hidden="true"><i data-esc-barra></i></span>
    <button class="esc__btn esc__btn--pausa" type="button" data-esc-pausa aria-label="Pausar el pase de trabajos" aria-pressed="false">{pausa}</button>
    <button class="esc__btn esc__btn--sig" type="button" data-esc-sig aria-label="Siguiente trabajo">{T.ico("flecha-derecha")}</button>
   </div>
  </div>
 </div>
</section>
"""


def proyectos_html(sec):
    """«Lo más reciente»: desde v5.7 es el escaparate si hay maquetas (C.ESCAPARATE); si no, la lista de v2."""
    if getattr(C, "ESCAPARATE", None):
        return escaparate_html(sec)
    ps = parrafos(sec)
    txt = "".join(f"<p>{inline(x)}</p>" for x in ps)
    items = []
    destacados = getattr(C, "CASOS_RECIENTES", None)   # v5: tres casos destripados, no la galería repetida
    lista_c = [CASO_POR_NOMBRE[n] for n in destacados if n in CASO_POR_NOMBRE] if destacados else CASOS
    for i, c in enumerate(lista_c):
        tit, sub, _, url, _, grande = c
        etq = "".join(f"<li>{esc(e)}</li>" for e in CASOS_ETQ.get(tit, []))
        foto = T.foto(grande, f"{tit}: {sub}", "(max-width: 1000px) 92vw, 58vw", clase="proy__foto")
        marco = f'<div class="proy__marco">{foto}{f"<ul class=proy__etq>{etq}</ul>" if etq else ""}</div>'
        muni, partida = getattr(C, "CASO_DETALLE", {}).get(tit, (None, None))
        pie = (f'<p class="proy__tit"><strong>{esc(tit)}</strong> {esc(sub)}{f" · {esc(muni)}" if muni else ""}'
               f'{f"<span class=proy__partida>{esc(partida)}</span>" if partida else ""}</p>')
        if url:
            ext = ' rel="noopener" target="_blank"' if url.startswith("http") else ""
            cuerpo = f'<a href="{A(url)}"{ext}>{marco}{pie}<span class="proy__ir" aria-hidden="true">{T.ico("flecha-diagonal")}</span></a>'
        else:
            cuerpo = marco + pie
        items.append(f'<li class="proy rv">{cuerpo}</li>')
    return f"""<section class="seccion proyectos" id="casos">
 <div class="contenedor proyectos__in">
  <div class="proyectos__cab">
   <h2 class="h2 enciende">{h2_gris(sec['h2'])}</h2>
   <div class="prosa">{txt}</div>
  </div>
  <ol class="proyectos__lista">{"".join(items)}</ol>
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
        b = T.boton(bt[0], bt[1], {0: "btn--blanco btn--peq", 2: "btn--linea-claro btn--peq"}.get(i, "btn--linea btn--peq")) if bt else ""
        ob = OBJETOS_CIFRAS[i] if i < len(OBJETOS_CIFRAS) else None
        deco = (f'<span class="cifra__obj" aria-hidden="true">{T.objeto(ob, "(max-width: 900px) 46vw, 340px")}</span>' if ob
                else f'<span class="cifra__deco" aria-hidden="true">{T.ico(ic)}</span>')
        # v5: la nota y el año no se cuentan desde cero (una nota no «sube»); solo las cifras con «+»
        cuenta = f' data-cuenta="{A(val)}"' if suf == "+" else ""
        tarj.append(f'<div class="cifra cifra--{i} rv"><p class="cifra__n"><span{cuenta}{fuente}>{esc(val)}</span>{esc(suf)}</p>'
                    f'<p class="cifra__t">{esc(txt)}</p>{b}{deco}</div>')
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
    n = n - n % 12 if n >= 24 or n % 12 == 0 else (n - n % 6 if n >= 6 else n - n % 2)   # 22 → 18, 24 → 24
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
        col = ""
        if os.path.exists(os.path.join(RAIZ, "recursos", "clientes-color", f)):
            os.makedirs(os.path.join(SITIO, "img", "clientes-color"), exist_ok=True)
            shutil.copy(os.path.join(RAIZ, "recursos", "clientes-color", f), os.path.join(SITIO, "img", "clientes-color", f))
            col = f'<img class="logo__color" src="/img/clientes-color/{A(f)}" alt="" width="{w}" height="{h}" loading="lazy" decoding="async">'
        li.append(f'<li class="logo{" logo--alto" if w / max(h, 1) < 1.8 else ""}{"" if col else " logo--sin-color"}"><span class="logo__caja"><img class="logo__gris" src="/img/clientes/{A(f)}" alt="{A(n)}" width="{w}" height="{h}" loading="lazy" decoding="async">{col}</span></li>')
    return (f'<section class="seccion logos-sec" aria-label="{tit}"><div class="contenedor">'
            f'<p class="etiqueta">{T.simbolo("etiqueta__sim")}{tit}</p><ul class="logos{"" if len(li) % 12 == 0 else " logos--seis"}" data-logos>{"".join(li)}</ul></div></section>')


def logotipo_foto():
    """v4 · El logotipo a todo el ancho con una foto dentro de las letras (máscara CSS con el propio SVG de la marca)
    y el trazo fucsia encima; con el scroll, la foto se desplaza dentro de las letras y el monograma G+F gira hasta su sitio."""
    f = FOTOS.get(LOGOTIPO_FOTO)
    real = archivo_foto(f["archivo"]) if f else None
    if not real:
        return ""
    return f"""<section class="lgfoto" aria-label="{esc(N['nombre'])}">
 <div class="contenedor">
  <div class="lgfoto__caja" data-lgfoto>
   <div class="lgfoto__mascara">{T.foto(real, "", "(max-width: 900px) 100vw, 92vw", clase="lgfoto__img")}</div>
   {T.logotipo("lgfoto__trazo")}
  </div>
  <p class="lgfoto__pie etiqueta">{T.simbolo("etiqueta__sim")}{esc(texto("lgfoto_pie"))}</p>
 </div>
</section>
"""


def marca_agua():
    """v4 · El logotipo en trazo, enorme y cortado, de fondo en las franjas oscuras (se desliza con el scroll)."""
    return f'<span class="marca-agua" aria-hidden="true" data-marca-agua>{T.logotipo("lg--trazo")}</span>'


def cinta_tarjetas():
    """v2 · Cinta de tarjetas de la home B de Rayo (R15): dos filas que corren en sentido contrario, con los objetos
    3D sobre fondos de la marca y tarjetas de texto en fucsia y berenjena. Decorativa (aria-hidden)."""
    objs = ["simbolo-cromo", "simbolo-despiece-crema", "chincheta", "simbolo-cristal", "simbolos-grupo", "estrella", "simbolo-bicolor",
            "lupa", "simbolo-fucsia-perfil", "cursor", "simbolo-crema", "bocadillo", "simbolo-berenjena", "barras"]
    palabras = list(CINTA_PORTADA) + ["Ficha de Google", "Reseñas reales", "Webs rápidas", "Anuncios en Maps"]
    def fila(ini, sentido):
        items = []
        for k in range(7):
            if k % 3 == 1:
                w = palabras[(ini + k) % len(palabras)]
                items.append(f'<span class="ct ct--txt ct--{("acento", "oscuro")[(ini + k) % 2]}"><b>{esc(w)}</b>{T.simbolo("ct__sim")}</span>')
            else:
                o = objs[(ini * 7 + k) % len(objs)]
                if o in OBJETOS_FUCSIA or o == "simbolo-bicolor":
                    tono = ("oscuro", "crema")[(ini + k) % 2]
                elif o in ("simbolo-crema", "simbolo-despiece-crema", "bocadillo"):
                    tono = ("oscuro", "acento")[(ini + k) % 2]
                elif o in ("simbolo-berenjena",):
                    tono = ("acento", "claro")[(ini + k) % 2]
                else:
                    tono = ("acento", "oscuro", "claro")[(ini + k) % 3]
                items.append(f'<span class="ct ct--{tono}">{T.objeto(o, "(max-width: 900px) 40vw, 260px", "ct__obj")}</span>')
        grupo = "".join(items)
        return (f'<div class="cinta cinta--tarjetas"><div class="cinta__pista" data-cinta="{sentido}"><div class="cinta__grupo">{grupo}</div>'
                f'<div class="cinta__grupo">{grupo}</div></div></div>')
    return f'<div class="cinta-tarj" aria-hidden="true">{fila(0, -1)}{fila(1, 1)}</div>'


def zona_html():
    """Dentro de la franja fucsia (v2): la cinta fina de municipios (R14, peso 300, en blanco) y los enlaces."""
    nombres = CINTA_SECUNDARIA or ([BASE] + [n for _, n in MUNICIPIOS if n != BASE])
    li = "".join(f'<li class="rv"><a href="{u}">{esc(MUNICIPIO_ANCLA.format(pueblo=n))}{T.ico("flecha-diagonal")}</a></li>' for u, n in MUNICIPIOS)
    return (f'<div class="cinta-sec">{T.cinta(nombres, "cinta--fina", 1)}</div>'
            + (f'<div class="contenedor"><ul class="enlaces enlaces--zonas" aria-label="{A(texto("zona_titulo"))}">{li}</ul></div>' if li else ""))


def horario_html(sec):
    """v2 · Horario: título y texto a la izquierda; a la derecha una tarjeta berenjena con las horas en grande,
    el estado en vivo y un objeto 3D que se sale por arriba."""
    txt = render_bloques(sec["bl"])
    return f"""<section class="seccion horario-sec" id="{slug(sec['h2'])}">
 <div class="contenedor">
  <div class="horario">
   <div class="horario__cab"><h2 class="h2 enciende">{h2_gris(sec['h2'])}</h2>
    <div class="horario__txt prosa">{txt}<p><a class="horario__tel tel" href="tel:{N['telefono_e164']}">{T.ico("contacto")}{N['telefono']}</a></p></div></div>
   <div class="horario__tarjeta rv">
    <span class="horario__obj" aria-hidden="true">{T.objeto("simbolo-despiece-crema", "(max-width: 900px) 44vw, 300px", "flota-lenta")}</span>
    {T.estado("estado--claro")}
    <p class="horario__grande"><span>{N['dias_texto']}</span><strong>{N['abre'].lstrip('0')}<em>—</em>{N['cierra'].lstrip('0')}</strong></p>
   </div>
  </div>
 </div>
</section>
"""


MAPA_EMBED = f"https://maps.google.com/maps?cid={N['cid']}&z=16&hl=es&output=embed"


def mapa(sec=None):
    """v5 · Con `sec` (el bloque «Horario y oficina» de la home) funde horario y mapa en una sola sección."""
    if sec:
        cab = (f'<p class="etiqueta">{T.simbolo("etiqueta__sim")}Dónde estamos</p><h2 class="h2-lect" id="{slug(sec["h2"])}">{inline(sec["h2"])}</h2>'
               f'<div class="mapa__horas">{T.estado()}</div>'
               f'<div class="prosa">{render_bloques(sec["bl"])}</div>')
    else:
        cab = f'<p class="etiqueta">{T.simbolo("etiqueta__sim")}Dónde estamos</p><h2 class="h2-lect">{texto("mapa_titular")}</h2>'
    txt_mapa = "" if sec else f'<p>{texto("mapa_texto")}</p>'
    return f"""<section class="seccion mapa-sec{' mapa-sec--horario' if sec else ''}" aria-label="Dónde estamos">
 <div class="contenedor">
  <div class="mapa">
   <div class="mapa__info">
    {cab}
    <p class="mapa__dir">{N['calle']}<br>{N['cp']} {N['localidad']} ({N['provincia']})</p>
    {txt_mapa}
    <div class="acciones">{T.boton("Ver en Google Maps", FICHA, "btn--linea", "flecha-diagonal", ' rel="noopener" target="_blank"')}</div>
   </div>
   <div class="mapa__marco"><iframe src="{MAPA_EMBED}" title="Mapa: {A(N['nombre'])}, {A(N['calle'])}, {A(N['localidad'])}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe></div>
  </div>
 </div>
</section>
"""


def tarjeta_opinion(o):
    serv = esc(o.get("servicio") or getattr(C, "OPINION_ETIQUETA", {}).get(o["nombre"], "")) + (f' · {esc(o["lugar"])}' if o.get("lugar") else "")
    marca = " op--marcador" if o.get("marcador") else ""
    return (f'<li class="op{marca}"><span class="estrellas" aria-label="5 estrellas">★★★★★</span>'
            f'<p class="op__tit">{esc(o["titulo"])}</p><div class="op__cuerpo"><p class="op__txt">«{esc(o["texto"])}»</p></div>'
            f'<button type="button" class="op__mas" data-op-mas hidden>Leer más</button>'
            f'<div class="op__pie"><span class="op__ini" aria-hidden="true">{esc(o["nombre"][:1])}</span>'
            f'<span class="op__quien"><strong>{esc(o["nombre"])}</strong><span>{serv or "Opinión publicada en Google"}</span></span></div></li>')


def lista_opiniones(url):
    """v5 · N1: cada página ordena las reseñas por lo que le toca. Home: todas; interiores: tres y el resto en Google."""
    por_nombre = {o["nombre"]: o for o in OPINIONES}
    orden = getattr(C, "OPINION_ORDEN", {}).get(url)
    munis = [u for u, _ in MUNICIPIOS]
    if orden is None and url in munis:
        rot = getattr(C, "OPINION_MUNICIPIO", [])
        orden = rot[munis.index(url) % len(rot)] if rot else None
    if orden is None:
        return OPINIONES[:3] if url != "/" else OPINIONES
    return [por_nombre[n] for n in orden if n in por_nombre]


def opiniones(pb=None, titulo=None, texto_op="", url="/"):
    """Opiniones de la home B de Rayo: título, texto y sello de Google a la izquierda (en el sitio de Clutch),
    carrusel de tarjetas blancas a la derecha con flechas y contador (R33 sin automático). Sello que gira con el scroll (R25)."""
    lista = lista_opiniones(url)
    titulo = titulo or esc(texto("opiniones_titular"))
    texto_op = f'<p>{texto_op}</p>' if texto_op else ""
    sello_t = esc(texto("opiniones_sello"))
    sello = (f'<a class="sello" href="{FICHA}" rel="noopener" target="_blank"><span class="sr">Ver las reseñas en Google</span>'
             f'<svg class="sello__aro" viewBox="0 0 200 200" aria-hidden="true" data-gira><defs><path id="aro" d="M100,100 m-78,0 a78,78 0 1,1 156,0 a78,78 0 1,1 -156,0"/></defs>'
             f'<text><textPath href="#aro" textLength="486" lengthAdjust="spacingAndGlyphs">{sello_t}{sello_t}</textPath></text></svg>{T.simbolo("sello__sim")}</a>')
    carrusel = ""
    if lista:
        carrusel = f"""<div class="op-carril">
   <ul class="op-lista" data-opiniones tabindex="0" aria-label="Reseñas">{"".join(tarjeta_opinion(o) for o in lista)}</ul>
   <div class="op-ctrl"><button type="button" class="redondo" data-op="-1" aria-label="Reseña anterior">←</button><span class="op-cuenta" data-op-cuenta>1 / {len(lista)}</span><button type="button" class="redondo" data-op="1" aria-label="Reseña siguiente">→</button></div>
  </div>"""
    return f"""<section class="franja franja--oscuro opiniones-sec" id="opiniones" aria-label="Opiniones de clientes en Google">
 {marca_agua()}
 <div class="contenedor opiniones">
  <div class="opiniones__cab">
   <p class="etiqueta">{T.simbolo("etiqueta__sim")}{esc(texto("opiniones_etiqueta"))}</p>
   <h2 class="h2 enciende">{titulo}</h2>
   {texto_op}
   <div class="opiniones__nota">{T.nota("nota--grande", FICHA)}{sello}</div>
   <span class="opiniones__obj" aria-hidden="true">{T.objeto("estrella", "(max-width: 900px) 30vw, 200px", "flota-lenta")}</span>
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


def aud_ir():
    """v5.2 · En la página de la auditoría, la banda final no trae otro formulario: manda al de la página."""
    return ('<div class="aud-ir"><p class="aud-ir__t">El formulario está un poco más arriba.</p>'
            + T.boton(texto("aud_boton"), "#pedir-auditoria", "btn--acento", "flecha-diagonal", ' data-zona="banda_auditoria"') + '</div>')


def cita_banda(url, salto=0):
    """v5.1 · Una frase real de la reseña que abre esa página, junto al formulario (la primera frase entera, sin recortar)."""
    citas = {**getattr(C, "OPINION_CITA", {}), **getattr(C, "OPINION_CITA_PAGINA", {}).get(url, {})}
    for o in lista_opiniones(url)[salto:]:
        t = re.sub(r"\s+", " ", o["texto"]).strip().strip("“”\"")
        elegida = citas.get(o["nombre"])
        m = re.match(r"(.{25,170}?[.!])(\s|$)", t) if not elegida else re.match(r"(.+)", elegida)
        if elegida and elegida.strip("… ") not in t:   # la cita tiene que ser literal (se admiten puntos suspensivos)
            m = None
        if m:
            et = getattr(C, "OPINION_ETIQUETA", {}).get(o["nombre"], "")
            return (f'<figure class="banda__op"><span class="estrellas" aria-label="5 estrellas">★★★★★</span><blockquote>«{esc(m.group(1))}»</blockquote>'
                    f'<figcaption>{esc(o["nombre"])}{f" · {esc(et)}" if et else ""} · en Google</figcaption></figure>')
    return ""


def banda(url, titulo=None, texto_b=None):
    titulo = titulo or esc(BANDA_TIT.get(url) or texto("banda_titulo"))
    texto_b = texto_b or esc(texto("banda_texto"))
    extra = f'<a class="banda__extra" href="{"#pedir-auditoria" if url == "/" else CTA_EXTRA[1]}">{esc(CTA_EXTRA[0])} {T.ico("flecha-diagonal")}</a>' if CTA_EXTRA and not CTA_EXTRA[1].startswith(url if url != "/" else "#") else ""
    obj = (f'<span class="banda__objeto" aria-hidden="true">{T.objeto("simbolo-despiece", "(max-width: 1000px) 40vw, 380px", "flota-lenta")}</span>'
           if OBJETO_PORTADA.get("en_banda") else "")
    return f"""<section class="banda-sec" aria-label="Contacto">
 <div class="contenedor">
  <div class="banda" data-abre>
   <span class="banda__fondo" aria-hidden="true"><img src="/img/obj/banda-fondo.webp" alt="" width="1440" height="900" loading="lazy" decoding="async">{foto_hueco("banda", "100vw", "banda__foto")}</span>
   {obj}
   <div class="banda__txt">
    <p class="etiqueta etiqueta--claro">{T.simbolo("etiqueta__sim")}{esc("Auditoría gratuita" if url == "/auditoria-seo-local/" else texto("banda_etiqueta"))}</p>
    <h2 class="banda__tit">{titulo}</h2>
    <p class="banda__p">{texto_b}</p>
    {T.estado("estado--claro")}
    <div class="acciones">{T.btn_llamar("btn--acento btn--grande", extra=' data-zona="banda"')}{T.btn_whatsapp("btn--linea-claro")}</div>
    {extra}
    {cita_banda(url)}
   </div>
   <div class="banda__form">{llamada(url) if url != "/auditoria-seo-local/" else aud_ir()}</div>
  </div>
 </div>
</section>
"""


# ---------- Páginas interiores: columna de lectura con índice clavado ----------
def lectura(p, entrada, resto, secs_normales, ul=None):
    """Columna de lectura (720 px) con el índice clavado a la izquierda en tarjeta blanca y la tarjeta de
    llamada debajo (variación A de páginas interiores)."""
    ind, blq = [], []
    for k, s in enumerate(secs_normales, 1):
        sid = slug(s["h2"])
        ind.append(f'<li><a href="#{sid}">{esc(plano(s["h2"]))}</a></li>')
        blq.append(f'<section class="lectura__blq" id="{sid}"><h2 class="h2-lect h2-lect--n rv">{inline(s["h2"])}</h2><div class="prosa rv">{render_bloques(s["bl"])}</div></section>')
    # v2 · Un caso real dentro de la columna (la «foto dentro del texto» del artículo de Rayo), tras el segundo bloque
    c = caso_de(p["url"])
    if c and blq and p["url"] not in [x[2] for x in SERVICIOS_HOME]:   # v5: en los servicios el caso va a sangre, fuera de la columna
        muni, partida = getattr(C, "CASO_DETALLE", {}).get(c[0], (None, None))
        pb_pag = next((n for u, n in MUNICIPIOS if u == p["url"]), None)
        etq = "Caso real" if not pb_pag else ("Caso real en " + pb_pag if muni == pb_pag else "El caso más cercano")
        donde = f' · {esc(muni)}' if muni else ""
        mas = f'<span class="lectura__partida">{esc(partida)}</span>' if partida else ""
        fig = (f'<figure class="lectura__caso rv">{T.foto(c[5], f"{c[0]}: {c[1]}", "(max-width: 1200px) 92vw, 720px", clase="lectura__foto")}'
               f'<figcaption><span class="lectura__etq">{esc(etq)}</span><strong>{esc(c[0])}</strong> {esc(c[1])}{donde}{mas}</figcaption></figure>')
        blq.insert(min(2, len(blq)), fig)
    if True:  # opiniones sale siempre (con reseñas o con la nota de la ficha)
        ind.append('<li><a href="#opiniones">Opiniones</a></li>')
    if p["faq"]:
        ind.append('<li><a href="#preguntas">Preguntas frecuentes</a></li>')
    extra = f'<a class="mini__extra" href="{CTA_EXTRA[1]}">{esc(CTA_EXTRA[0])} {T.ico("flecha-diagonal")}</a>' if CTA_EXTRA and not CTA_EXTRA[1].startswith(p["url"]) else ""
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


def caso_de(url):
    """Caso que acompaña a una página interior: el de config.CASO_URL o, en los municipios, uno por turno."""
    if url in CASO_URL:
        return CASO_POR_NOMBRE.get(CASO_URL[url])
    for nombre, cats in getattr(C, "CASOS_CATEGORIAS", {}).items():   # v4: primer caso con esa categoría
        if url in cats and nombre in CASO_POR_NOMBRE:
            return CASO_POR_NOMBRE[nombre]
    munis = [u for u, _ in MUNICIPIOS]
    if url in munis:
        return CASOS[munis.index(url) % len(CASOS)]
    return None


def caso_sangre(url):
    """v5 · Gesto de las páginas de servicio: el caso real a sangre, con su municipio y su punto de partida."""
    c = caso_de(url)
    if not c:
        return ""
    muni, partida = getattr(C, "CASO_DETALLE", {}).get(c[0], (None, None))
    ir = ""
    if c[3]:
        ext = ' rel="noopener" target="_blank"' if c[3].startswith("http") else ""
        ir = f'<a class="sangre__ir" href="{A(c[3])}"{ext}>{esc(ver_de(c[0]))} {T.ico("flecha-diagonal")}</a>'
    etq = "".join(f"<li>{esc(e)}</li>" for e in CASOS_ETQ.get(c[0], []))
    return f"""<section class="sangre" aria-label="Caso real: {A(c[0])}">
 {T.foto(c[5], f"{c[0]}: {c[1]}", "100vw", clase="sangre__foto")}
 <div class="contenedor sangre__pie">
  <p class="etiqueta">{T.simbolo("etiqueta__sim")}Caso real{f" · {esc(muni)}" if muni else ""}</p>
  <p class="sangre__tit"><strong>{esc(c[0])}</strong> {esc(c[1])}</p>
  {f'<p class="sangre__partida">{esc(partida)}</p>' if partida else ""}
  {f'<ul class="sangre__etq">{etq}</ul>' if etq else ""}
  {ir}
 </div>
</section>
"""


def zona_municipio(url, pb):
    """v5 · Gesto de las páginas de municipio: su mapa, y los municipios vecinos donde también trabajamos."""
    from urllib.parse import quote
    nom = dict(MUNICIPIOS)
    slug_m = url.replace(URLS["municipio"], "").strip("/")
    vecinos = [(URLS["municipio"] + v + "/", nom[URLS["municipio"] + v + "/"]) for v in getattr(C, "VECINOS", {}).get(slug_m, [])
               if URLS["municipio"] + v + "/" in nom]
    enl = "".join(f'<li><a href="{u}">{esc(MUNICIPIO_ANCLA.format(pueblo=n))}{T.ico("flecha-diagonal")}</a></li>' for u, n in vecinos)
    src = f"https://maps.google.com/maps?q={quote(pb + ', Madrid')}&z=13&hl=es&output=embed"
    return f"""<section class="seccion zona" aria-labelledby="zona-tit">
 <div class="contenedor zona__in">
  <div class="zona__txt">
   <p class="etiqueta">{T.simbolo("etiqueta__sim")}La zona</p>
   <h2 class="h2" id="zona-tit">{esc(pb)}, desde {esc(BASE)}</h2>
   <p>Nuestra oficina está en {esc(BASE)} y vamos a verle a su negocio en {esc(pb)}. También trabajamos al lado:</p>
   <ul class="enlaces">{enl}<li><a href="/">Agencia SEO en {esc(BASE)}{T.ico("flecha-diagonal")}</a></li></ul>
  </div>
  <div class="zona__mapa"><iframe src="{src}" title="Mapa de {A(pb)}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
 </div>
</section>
"""


def otros_servicios(url, pb=None):
    """v2 · Franja berenjena con los servicios en tarjetas (icono, objeto 3D, texto corto); al pasar el ratón se
    rellenan de fucsia desde abajo. En un servicio salen los otros seis; en un municipio, los siete."""
    li = []
    for t, txt, u, ic, _, _ in SERVICIOS_HOME:
        if u == url:
            continue
        ob = T.objeto(OBJETO_URL[u], "180px", "otro__obj") if u in OBJETO_URL else ""
        li.append(f'<li class="rv"><a class="otro" href="{u}"><span class="otro__ico">{T.ico(ic)}</span><span class="otro__tit">{esc(t)}</span>'
                  f'<span class="otro__txt">{esc(txt)}</span>{ob}<span class="otro__ir" aria-hidden="true">{T.ico("flecha-diagonal")}</span></a></li>')
    tit = SERVICIOS_TITULO if not pb else f"{SERVICIOS_TITULO} en {pb}"
    return f"""<section class="seccion otros" aria-labelledby="otros-tit">
 <div class="contenedor">
  <div class="otros__cab"><p class="etiqueta">{T.simbolo("etiqueta__sim")}Servicios</p><h2 class="h2" id="otros-tit">{esc(tit)}</h2></div>
  <ul class="otros__lista otros__lista--{len(li)}">{"".join(li)}</ul>
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
 <label>Municipio <span class="opcional">(opcional)</span><input type="text" name="municipio" autocomplete="address-level2" maxlength="60" placeholder="{A(texto('form_municipio_ph'))}"></label>
 <label>{texto("form_mensaje_label")} <span class="opcional">(opcional)</span><textarea name="mensaje" maxlength="2000" placeholder="{A(texto('form_mensaje_ph'))}"></textarea></label>
 <label class="trampa" aria-hidden="true">Web<input type="text" name="web" tabindex="-1" autocomplete="off"></label>
 <input type="hidden" name="t" value="">
 {privacidad("privacidad_form")}
 <div class="acciones">{T.boton_form(texto("form_boton"))}</div>
</form>"""


def auditoria_form():
    """v5 · Formulario propio para pedir la auditoría gratis (lo tenía la web vieja en /auditoria-gratis/#formulario):
    qué revisar (ficha, web o las dos), nombre, teléfono y la web o el nombre del negocio. Evento solicitud_auditoria."""
    pts = "".join(f"<li>{T.ico('check')}<span>{esc(x)}</span></li>" for x in texto("aud_puntos").split("|"))
    return f"""<section class="audform" id="pedir-auditoria" aria-labelledby="audform-tit">
 <div class="contenedor audform__grid">
  <div class="audform__txt rv">
   <p class="etiqueta">{T.simbolo("etiqueta__sim")}Auditoría gratuita</p>
   <h2 class="h2" id="audform-tit">{esc(texto("aud_titular"))}</h2>
   <p>{esc(texto("aud_texto"))}</p>
   <ul class="audform__puntos">{pts}</ul>
   <div class="audform__op">{cita_banda("/auditoria-seo-local/", 1)}</div>
  </div>
  <form class="formulario audform__form rv" action="/enviar.php" method="post" aria-label="Pedir la auditoría gratuita">
   <div class="aviso aviso--ok" id="aud-ok" hidden>{esc(texto("aud_ok"))}</div>
   <div class="aviso aviso--error" id="aud-error" hidden>No se ha podido enviar. Llámenos al {N['telefono']} o inténtelo de nuevo.</div>
   <fieldset class="audform__que"><legend>¿Qué quiere que revisemos?</legend>
    <label><input type="radio" name="revisar" value="Ficha de Google"> Mi ficha de Google</label>
    <label><input type="radio" name="revisar" value="Web"> Mi web</label>
    <label><input type="radio" name="revisar" value="Ficha y web" checked> Las dos</label>
   </fieldset>
   <div class="fila-form">
    <label>Nombre<input type="text" name="nombre" autocomplete="name" required maxlength="80"></label>
    <label>Teléfono<input type="tel" name="telefono" autocomplete="tel" inputmode="tel" required pattern="[0-9 +()\\-]{{9,20}}" maxlength="20"></label>
   </div>
   <label>Su web o el nombre de su negocio <span class="opcional">(opcional)</span><input type="text" name="negocio" maxlength="160" placeholder="{A(texto('aud_negocio_ph'))}"></label>
   <label class="trampa" aria-hidden="true">Web<input type="text" name="web" tabindex="-1" autocomplete="off"></label>
   <input type="hidden" name="t" value=""><input type="hidden" name="tipo" value="auditoria"><input type="hidden" name="pagina" value="/auditoria-seo-local/"><input type="hidden" name="origen" value="" data-origen>
   {privacidad("privacidad_form")}
   <div class="acciones">{T.boton_form(texto("aud_boton"))}{T.btn_whatsapp("btn--linea", t=texto("whatsapp_auditoria"), rotulo="Pedirla por WhatsApp")}</div>
  </form>
 </div>
</section>
"""


def contacto_cuerpo(p, intro):
    ps = [c for t, c in intro if t == "p"]
    txt = "".join(f"<p>{inline(x)}</p>" for x in ps)
    extra = f'<p><strong>{esc(CTA_EXTRA[0])}:</strong> <a href="{CTA_EXTRA[1]}">{esc(nombre(CTA_EXTRA[1]))}</a></p>' if CTA_EXTRA and CTA_EXTRA[1] != p["url"] else ""
    return f"""<section class="seccion contacto">
 <div class="contenedor contacto__grid">
  <div class="contacto__datos">
   <span class="contacto__obj" aria-hidden="true">{T.objeto("chincheta", "(max-width: 900px) 34vw, 220px", "flota-lenta")}</span>
   <div class="prosa rv">{txt}</div>
   <a class="contacto__tel tel" href="tel:{N['telefono_e164']}" data-zona="contacto">{N['telefono']}</a>
   {T.estado("estado--claro")}
   <address class="prosa">
    <p><strong>Horario:</strong> {N['horario_texto']}.</p>   <!-- v5.2: lo de fuera de horario ya lo dice el texto de la página -->
    <p><strong>Correo:</strong> <a href="mailto:{N['email']}">{N['email']}</a></p>
    <p><strong>Dirección:</strong> <a href="{FICHA}" rel="noopener" target="_blank">{N['calle']}, {N['cp']} {N['localidad']}</a></p>
    {extra}
   </address>
   <div class="acciones">{T.btn_whatsapp("btn--linea-claro")}</div>
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
    CTX_PAG["home"] = t == "home"
    puesto_op = False
    if t == "home":
        cuerpo.append(portada_home(p))
        dec, resto = reparte_intro(intro)
        cuerpo.append(manifiesto(p, dec, ul))
        cuerpo.append(auditoria_form())   # v5.18: el gancho arriba (Álvaro): la auditoría gratuita, justo tras la portada y el manifiesto
        if resto and normales:
            normales[0]["bl"] = resto + normales[0]["bl"]
        hay_filas = any(sum(1 for tt, c in s["bl"] if tt == "p" and FILA.match(c)) >= 3 for s in normales)
        if SERVICIOS_SECCION and not hay_filas:
            cuerpo.append(servicios_seccion())
        puesto_mapa = False
        for n, s in enumerate(normales, 1):
            if s["h2"].startswith(HORARIO_H2):
                cuerpo.append(mapa(s)); puesto_mapa = True   # v5: horario y mapa en una sola sección
            else:
                cuerpo.append(bloque_home(s, n))
                if QUIEN_H2 and s["h2"].startswith(QUIEN_H2) and not puesto_op:   # v5.1: opiniones antes de los casos
                    cuerpo.append(opiniones(pb, *(op or (None, "")), url=p["url"])); puesto_op = True
            if n == CIFRAS_EN.get("home"):
                cuerpo.append(cifras())
                cuerpo.append(logos_html())
                # v5: fuera la cinta de tarjetas en la home (monograma repetido y 700 px de más)
                cuerpo.append(logotipo_foto())
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
        if p["url"] == URLS.get("auditoria", "/auditoria-seo-local/"):
            cuerpo.append(auditoria_form())
        dec, resto = reparte_intro(intro)
        cuerpo.append(lectura(p, dec, resto, normales, ul))
        if CIFRAS_EN.get(t):
            cuerpo.append(cifras())
        if t == "servicio":
            cuerpo.append(caso_sangre(p["url"]))
        if t == "municipio":
            cuerpo.append(zona_municipio(p["url"], pb))
        if t in ("servicio", "municipio"):
            cuerpo.append(otros_servicios(p["url"], pb))
    if not puesto_op:
        cuerpo.append(opiniones(pb, *(op or (None, "")), url=p["url"]))
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
    # sitio/ se rehace entero, salvo /img y /og (rematar.py solo regenera las imágenes cuyo original ha cambiado)
    guarda = os.path.join(RAIZ, ".img-cache")
    if os.path.isdir(guarda):
        shutil.rmtree(guarda)
    os.makedirs(guarda)
    for d in ("img", "og"):
        if os.path.isdir(os.path.join(SITIO, d)):
            shutil.move(os.path.join(SITIO, d), os.path.join(guarda, d))
    if os.path.isdir(SITIO):
        shutil.rmtree(SITIO)
    os.makedirs(SITIO)
    for d in os.listdir(guarda):
        shutil.move(os.path.join(guarda, d), os.path.join(SITIO, d))
    urls = []
    for p in PAGINAS:
        p["mod"] = fecha_mod(p["ruta"])
        escribir(p["url"], pagina(p))
        if CONTACTO_INDEXABLE or datos.tipo_de(p["url"]) != "contacto":
            urls.append((p["url"], p["mod"]))
    for url, tit, md in legales():
        escribir(url, pagina_legal(url, tit, md))
        urls.append((url, fecha_mod(os.path.join(RAIZ, "contenido", "legales", "legales.md"))))
    # v5.11 · Portfolio (/trabajos/ y una ficha por trabajo): generador/portfolio.py + trabajos.py
    import portfolio
    for url, h in portfolio.paginas():
        escribir(url, montar(h))
        urls.append((url, fecha_mod(os.path.join(RAIZ, "generador", "trabajos.py"))))
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
