# -*- coding: utf-8 -*-
"""Genera sitio/ entero a partir de contenido/. Orden: build.py y después rematar.py (siempre el último).
Uso:  python3 generador/build.py && python3 generador/rematar.py"""
import html, json, os, re, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import datos
from datos import inline, esc
from config import DOMINIO, NEGOCIO as N, SERVICIOS_HOME, OPINIONES
import plantilla as T

RAIZ = datos.RAIZ
SITIO = os.path.join(RAIZ, "sitio")
FOTOS = datos.fotos_por_url()
PAGINAS = datos.todas()
POR_URL = {p["url"]: p for p in PAGINAS}

# ---------- Nombres cortos de municipio (del hub) ----------
PUEBLO = {}
for t, b in POR_URL["/reparacion-de-calderas-madrid/"]["bloques"]:
    if t == "ul":
        for it in b:
            m = re.match(r"\[LINK (?:Reparación calderas|Servicio técnico de calderas) ([^\]]+)\]\((/reparacion-calderas-[^)]+)\)", it)
            if m:
                PUEBLO[m.group(2)] = m.group(1)

NOMBRE_CORTO = {
    "/": "Inicio",
    "/reparacion-de-calderas-madrid/": "Zona de trabajo",
    "/reparacion-de-calderas-madrid-2/": "Mantenimiento de calderas",
    "/reparacion-de-calentadores-en-madrid/": "Calentadores",
    "/reparacion-de-termos-electronicos-en-madrid/": "Termos eléctricos",
    "/productos-o-calderas/": "Calderas por marca",
    "/productos-o-calderas/calderas-de-condensacion/": "Condensación",
    "/productos-o-calderas/calderas-de-gasoil/": "Gasoil",
    "/productos-o-calderas/calderas-de-condensacion/saunier-duval/": "Saunier Duval",
    "/productos-o-calderas/calderas-de-condensacion/baxi/": "Baxi",
    "/productos-o-calderas/calderas-de-condensacion/vaillant/": "Vaillant",
    "/productos-o-calderas/calderas-de-gasoil/domusa/": "Domusa",
    "/productos-o-calderas/calderas-de-gasoil/baxi/": "Baxi gasoil",
    "/quienes-somos/": "Quiénes somos",
    "/contacto/": "Contacto",
}


def nombre(url):
    return NOMBRE_CORTO.get(url) or PUEBLO.get(url) or url.strip("/")


def migas(url):
    if url == "/":
        return []
    cad = [("/", "Inicio")]
    if datos.tipo_de(url) == "municipio":
        cad.append(("/reparacion-de-calderas-madrid/", "Zona de trabajo"))
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
    li = []
    for i, (u, n) in enumerate(c):
        li.append(f'<li><a href="{u}">{esc(n)}</a></li>' if i < len(c) - 1 else f'<li aria-current="page">{esc(n)}</li>')
    return f'<nav class="migas" aria-label="Migas de pan"><ol>{"".join(li)}</ol></nav>'


# ---------- Schema ----------
NEG_ID = DOMINIO + "/#negocio"


def negocio_schema():
    area = ["Alcorcón"] + [v for k, v in PUEBLO.items() if v != "Alcorcón"]
    return {
        "@type": "HVACBusiness", "@id": NEG_ID, "name": "Balgas",
        "alternateName": "Balgas Mantenimiento y Reparación de Calderas",
        "legalName": "BALGAS MANTENIMIENTO Y REPARACIÓN DE CALDERAS, S.L.",
        "url": DOMINIO + "/", "telephone": N["telefono_e164"], "email": N["email"],
        "logo": DOMINIO + "/marca/balgas-simbolo-color.svg", "image": DOMINIO + "/og-image.jpg",
        "address": {"@type": "PostalAddress", "streetAddress": N["calle"], "postalCode": N["cp"],
                    "addressLocality": N["localidad"], "addressRegion": "Madrid", "addressCountry": "ES"},
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification",
                                       "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                                       "opens": "09:00", "closes": "20:00"}],
        "areaServed": [{"@type": "City", "name": a} for a in area] + [{"@type": "AdministrativeArea", "name": f"Madrid ({d})"} for d in ("Latina", "Carabanchel", "Usera", "Villaverde")],
        "aggregateRating": {"@type": "AggregateRating", "ratingValue": N["valoracion"].replace(",", "."),
                            "reviewCount": int(N["resenas"]), "bestRating": "5", "worstRating": "1"},
        "geo": {"@type": "GeoCoordinates", "latitude": 40.3282739, "longitude": -3.8346282},
        "hasMap": "https://maps.google.com/?cid=10173824761497024545",
        "sameAs": ["https://maps.google.com/?cid=10173824761497024545"],
        "founder": {"@type": "Person", "@id": DOMINIO + "/#sergio", "name": "Sergio", "jobTitle": "Técnico de calderas e instalador de gas",
                    "worksFor": {"@id": NEG_ID},
                    "hasCredential": [
                        {"@type": "EducationalOccupationalCredential", "name": "Instalador de gas autorizado", "identifier": "IGA nº 1442 (registro 202026)"},
                        {"@type": "EducationalOccupationalCredential", "name": "Carné de mantenedor-reparador de calefacción y ACS", "identifier": "APMR CA-03174"}]},
        "paymentAccepted": "Cualquier medio de pago",
        "foundingDate": "2019",  # «desde hace 7 años, como Balgas» (Sergio, 2026)
        "knowsAbout": ["Reparación de calderas", "Mantenimiento de calderas", "Calderas de condensación",
                       "Calderas de gasoil", "Calentadores", "Termos eléctricos"],
    }


def schema_de(p):
    url = DOMINIO + p["url"]
    g = [negocio_schema(),
         {"@type": "WebPage", "@id": url + "#pagina", "url": url, "name": p["title"], "description": p["meta"],
          "inLanguage": "es", "isPartOf": {"@id": DOMINIO + "/#web"}, "about": {"@id": NEG_ID},
          **({"dateModified": p["mod"]} if p.get("mod") else {})},
         {"@type": "WebSite", "@id": DOMINIO + "/#web", "url": DOMINIO + "/", "name": "Balgas", "inLanguage": "es",
          "publisher": {"@id": NEG_ID}}]
    c = migas(p["url"])
    if c:
        g.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": DOMINIO + u} for i, (u, n) in enumerate(c)]})
    t = datos.tipo_de(p["url"])
    if t in ("servicio", "marca", "municipio"):
        s = {"@type": "Service", "name": p["h1"], "serviceType": "Reparación y mantenimiento de calderas",
             "provider": {"@id": NEG_ID}, "url": url}
        s["areaServed"] = {"@type": "City", "name": PUEBLO.get(p["url"], "Alcorcón")}
        g.append(s)
    if p["faq"]:
        g.append({"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", inline(a))}}
            for q, a in p["faq"]]})
    return {"@context": "https://schema.org", "@graph": g}


# ---------- Bloques de texto ----------
FICHA = "https://maps.google.com/?cid=10173824761497024545"  # ficha de Google de Balgas (por su CID)
MAPS = FICHA
RESENAS = (f'<div class="resenas"><span class="resenas__n" data-nota>{N["valoracion"]}</span><span class="resenas__t">'
           f'<span class="sello__estrellas" aria-hidden="true">★★★★★</span><strong style="color:var(--c-oscuro)"><span data-resenas>{N["resenas"]}</span> reseñas en Google</strong>'
           f'<span>Valoración media en la ficha de Balgas</span></span>'
           f'<a class="btn btn--linea btn--peq" href="{MAPS}" rel="noopener" target="_blank"><span class="btn__txt"><span>Leer las reseñas</span><span aria-hidden="true">Leer las reseñas</span></span></a></div>')
SOLO_ENLACE = re.compile(r"^\s*\[(?:LINK )?[^\]]+\]\([^)]+\)\s*(🔗|🆕)?\s*$")


def render_bloques(bl):
    out = []
    for t, c in bl:
        if t == "p":
            if c.startswith("(Widget de reseñas"):
                out.append(RESENAS)
                continue
            if c.startswith("(Formulario"):
                continue
            out.append(f"<p>{inline(c)}</p>")
        elif t == "h3":
            out.append(f"<h3>{inline(c)}</h3>")
        elif t == "h4":
            out.append(f"<h4>{inline(c)}</h4>")
        elif t == "ul":
            if all(SOLO_ENLACE.match(i) for i in c):
                items = []
                for i in c:
                    m = re.search(r"\[(?:LINK )?([^\]]+)\]\(([^)]+)\)", i)
                    txt = re.sub(r"^(Reparación calderas|Servicio técnico de calderas) (en )?", "", m.group(1))
                    items.append(f'<li><a href="{m.group(2)}" title="{html.escape(m.group(1))}">{esc(txt)}</a></li>')
                out.append(f'<ul class="chips">{"".join(items)}</ul>')
            else:
                out.append("<ul>" + "".join(f"<li>{inline(i)}</li>" for i in c) + "</ul>")
        elif t == "ol":
            out.append('<ol class="pasos">' + "".join(f"<li>{inline(i)}</li>" for i in c) + "</ol>")
        elif t == "tabla":
            out.append(tabla_html(*c))
    return re.sub(r" {2,}", " ", "\n".join(out))


def tabla_html(cab, filas):
    """Tabla de Markdown → <table>. Cada celda lleva su cabecera en data-col (el CSS la usa en el móvil)."""
    th = "".join(f'<th scope="col">{inline(h)}</th>' for h in cab)
    trs = []
    for f in filas:
        f = (f + [""] * len(cab))[:len(cab)]
        trs.append("<tr>" + "".join(f'<td data-col="{T.A(plano(h))}">{inline(c)}</td>' for h, c in zip(cab, f)) + "</tr>")
    return f'<div class="tabla"><table class="tabla-datos"><thead><tr>{th}</tr></thead><tbody>{"".join(trs)}</tbody></table></div>'


def palabras(txt):
    return len(plano(re.sub(r"\[(?:LINK )?([^\]]+)\]\([^)]+\)", r"\1", txt)).split())


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


ES_CTA = re.compile(r"^(Pide (cita|presupuesto)|Llámanos|Llama |Contacta|Solicita|¿Necesitas|Cuéntanos)", re.I)


def plano(txt):
    return re.sub(r"<[^>]+>", "", inline(txt))


# ---------- Piezas de página ----------
# Fotos de apoyo (se reparten por página sin repetir la de la portada)
POOL = [(img, tit) for tit, _, _, img in SERVICIOS_HOME] + [
    ("reparacion-calderas-domicilio-alcorcon.jpg", "Reparación de calderas a domicilio"),
    ("tecnico-calderas-herramientas-alcorcon.jpg", "Técnico de calderas con sus herramientas"),
]
# Más fotos de apoyo (v10), con el alt del plan de fotos: así la home y las páginas largas no repiten foto.
_ALT = {f["archivo"]: f["alt"] for fs in FOTOS.values() for f in fs}
POOL += [(f, _ALT[f]) for f in ("reparacion-calderas-domusa-alcorcon.jpg", "tecnico-calderas-alcorcon-quienes-somos.jpg",
                                  "reparacion-calderas-villamantilla.jpg", "reparacion-calderas-villamanta.jpg") if f in _ALT]


USADAS = set()  # fotos ya puestas en la página que se está generando (no se repiten)


def pool(url, n, evitar=None):
    h = sum(ord(c) for c in url)
    L = [x for x in POOL if x[0] != evitar and x[0] not in USADAS] or [x for x in POOL if x[0] != evitar]
    res = []
    for k in range(len(L) * 3):
        x = L[(h + k * 3) % len(L)]
        if x not in res:
            res.append(x)
        if len(res) == n:
            break
    USADAS.update(x[0] for x in res)
    return res


def pueblo_de(url):
    return PUEBLO.get(url, "Alcorcón")


def llamada(url):
    """Tarjeta «Que me llamen» (contrato 9): sin estado ni nota, que ya están en el cristal de la portada.
    [data-promesa] lo rellena main.js según la hora."""
    return f"""<aside class="llamada" id="te-llamamos" aria-label="Te llamamos">
 <p class="llamada__tit">Déjanos tu nombre y tu teléfono</p>
 <p class="llamada__txt" data-promesa>Te llamamos lo antes posible.</p>
 <div class="aviso aviso--ok" data-llamada-ok hidden>Recibido. De lunes a viernes, de 9:00 a 20:00, te llamamos en menos de una hora; si es fuera de ese horario, en cuanto empecemos.</div>
 <div class="aviso aviso--error" data-llamada-error hidden>No se ha podido enviar. Llámanos al {N['telefono']}.</div>
 <form class="llamada__form" action="/enviar.php" method="post">
  <input type="hidden" name="tipo" value="llamada"><input type="hidden" name="pagina" value="{url}"><input type="hidden" name="t" value="">
  <label class="trampa" aria-hidden="true">Web<input type="text" name="web" tabindex="-1" autocomplete="off"></label>
  <label>Nombre<input type="text" name="nombre" autocomplete="name" required maxlength="80"></label>
  <label>Teléfono<input type="tel" name="telefono" autocomplete="tel" inputmode="tel" required pattern="[0-9 +()\\-]{{9,20}}" maxlength="20"></label>
  <p class="casilla casilla--info">Usamos tus datos solo para llamarte. <a href="/politica-de-privacidad/">Política de privacidad</a>.</p>
  <button class="btn btn--acento" type="submit"><span class="btn__txt"><span>Que me llamen</span><span aria-hidden="true">Que me llamen</span></span>{T.ICONO['flecha']}</button>
 </form>
 <p class="llamada__pie">¿Prefieres hablar ya? Llama al <a class="tel" href="tel:{N['telefono_e164']}">{N['telefono']}</a></p>
</aside>"""


def etiqueta_y_entrada(p):
    """Etiqueta (encima del H1) y entrada corta (bajo el H1): del .md si vienen; si no, las de por defecto (contrato 1)."""
    pb = pueblo_de(p["url"])
    if datos.tipo_de(p["url"]) == "municipio":
        et = f"Servicio técnico de calderas · {pb}"
        en = f"En Balgas reparamos calderas a domicilio en {pb}. Visita gratis y presupuesto antes de tocar nada."
    else:
        et = "Servicio técnico de calderas · Alcorcón"
        en = "Balgas repara calderas a domicilio en Alcorcón y alrededores. Visita gratis y presupuesto antes de tocar nada."
    et = esc(p.get("etiqueta") or et)
    en = inline(p["entrada_corta"]) if p.get("entrada_corta") else esc(en)
    return et, en


def portada(p, intro, foto_p, sello=True):
    """Portada como la de Orisa (O4): la foto llena el marco (F1 sigue al ratón, F2 zoom de entrada),
    titular grande encima, tarjeta de cristal, pegatina, texto vertical y los servicios en el borde de abajo.
    En el móvil: primero la foto con la nota de Google, luego el titular, una línea y Llamar."""
    pb = pueblo_de(p["url"])
    ft = ""
    if foto_p:
        ft = f'<div class="portada__fondo zoom" data-raton>{T.foto(foto_p["archivo"], foto_p["alt"], "100vw", prioridad=True)}</div>'
    peg = (f'<a class="pegatina" data-zona="pegatina" href="tel:{N["telefono_e164"]}"><span class="pegatina__in"><span class="sr">Visita gratis. Llamar al {N["telefono"]}</span>'
           f'<svg class="pegatina__aro" viewBox="0 0 200 200" aria-hidden="true"><defs><path id="aro" d="M100,100 m-74,0 a74,74 0 1,1 148,0 a74,74 0 1,1 -148,0"/></defs>'
           f'<text><textPath href="#aro">VISITA GRATIS · 1 AÑO DE GARANTÍA · {pb.upper()} · </textPath></text></svg>'
           f'{T.llama("pegatina__llama", False)}</span></a>')
    nota = (f'<a class="portada__nota" href="#opiniones">'
            f'<strong data-nota>{N["valoracion"]}</strong><span class="estrellas" aria-hidden="true">★★★★★</span>'
            f'<span><span data-resenas>{N["resenas"]}</span> reseñas en Google</span></a>')
    etiqueta, corta = etiqueta_y_entrada(p)
    cristal = f"""<aside class="portada__cristal" aria-label="Te llamamos">
     <p class="cristal__estado" data-estado><i></i><span>{N['horario_corto']}</span></p>
     <p class="cristal__nota"><strong data-nota>{N["valoracion"]}</strong><span class="estrellas" aria-hidden="true">★★★★★</span><span><span data-resenas>{N["resenas"]}</span> reseñas en Google</span></p>
     <p class="cristal__tit">¿Te llamamos nosotros?</p>
     <a class="cristal__ir" href="#te-llamamos">Déjanos tu teléfono <span aria-hidden="true">↓</span></a>
    </aside>"""
    serv = "".join(f'<li><a href="{u}">{t} <span aria-hidden="true">→</span></a></li>' for t, _, u, _ in SERVICIOS_HOME if u != p["url"])
    return f"""<section class="portada portada--foto">
 <div class="portada__marco" data-marco>
  {ft}
  <span class="portada__velo" aria-hidden="true"></span>
  {nota if ft else ""}
  {peg}
  <div class="contenedor portada__in">
   {migas_html(p['url'])}
   <div class="portada__cuerpo">
    <div class="portada__texto">
     <span class="etiqueta">{etiqueta}</span>
     <h1 class="h1{' h1--largo' if len(p['h1']) > 44 else ''}">{esc(p['h1'])}</h1>
     <p class="entrada-corta">{corta}</p>
     <div class="acciones">{T.btn_llamar(extra=' data-zona="portada_boton"')}{T.btn_whatsapp("btn--linea btn--wa", pueblo=pb if datos.tipo_de(p["url"]) == "municipio" else None)}</div>
     <div class="portada__datos">{T.corchete(N["horario_corto"])}{T.corchete("1 año de garantía en la reparación")}</div>
    </div>
    {cristal}
   </div>
   <ul class="portada__servicios">{serv}</ul>
  </div>
  <p class="portada__vertical" aria-hidden="true">[ {N['horario_corto']} · {N['telefono']} ]</p>
 </div>
</section>
<section class="seccion llamada-sec" aria-label="Te llamamos"><div class="contenedor">{llamada(p['url'])}</div></section>
"""


def resalta(html_txt, url):
    pb = pueblo_de(url)
    return re.sub(rf"\b({re.escape(pb)})\b", r'<em class="clave">\1</em>', html_txt, count=2)


DECLARA_MAX = 60  # palabras (contrato 2): el primer párrafo siempre; los siguientes, solo si caben


def reparte_intro(intro):
    """Párrafos de entrada → (los de la declaración, los que bajan al principio del primer bloque)."""
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


def corchete_declara(p):
    t = datos.tipo_de(p["url"])
    if t == "empresa":
        return "IGA nº 1442"
    if t == "marca":
        return "Repuestos originales"
    return f"{N['anios']} años en el oficio"


def declaracion(p, ps, foto_p):
    """Texto grande que se «enciende» con el scroll (O7) y dos fotos que se cruzan (F2 + F3, zoom morph F7)."""
    if not ps:
        return ""
    txt = resalta(" ".join(inline(x) for x in ps), p["url"])
    a, b = pool(p["url"], 2, foto_p["archivo"] if foto_p else None)
    return f"""<section class="seccion declara">
 <div class="contenedor">
  <div class="declara__cab"><span class="etiqueta">Balgas · {esc(pueblo_de(p['url']))}</span>{T.corchete(corchete_declara(p))}</div>
  <p class="declara__txt anim-enciende">{txt}</p>
  <div class="declara__fotos">
   <div class="declara__f1 zoom morph" data-velocidad="0.85">{T.foto(a[0], a[1], "(max-width: 900px) 60vw, 34vw")}</div>
   <div class="declara__f2 zoom morph" data-velocidad="1.15">{T.foto(b[0], b[1], "(max-width: 900px) 50vw, 26vw")}</div>
   {T.llama("declara__forma", False)}
  </div>
 </div>
</section>
"""


def ventajas(ul):
    """Mosaico (O23) con inclinación 3D al pasar el ratón (F9)."""
    items = []
    for n, it in enumerate(ul, 1):
        m = re.match(r"\*\*(.+?)\*\*[,.:]?\s*(.*)", it)
        cab = f'<span class="ventaja__num">[{n:02d}]</span>{T.llama("ventaja__llama", False)}'
        if m:
            items.append(f'<li class="ventaja inclina">{cab}<strong>{inline(m.group(1))}</strong><span>{inline(m.group(2))}</span></li>')
        else:
            items.append(f'<li class="ventaja inclina">{cab}<span>{inline(it)}</span></li>')
    return f'<section class="seccion seccion--gris ventajas-sec" aria-label="Por qué Balgas"><div class="contenedor"><ul class="ventajas">{"".join(items)}</ul></div></section>'


def horario(sec, n):
    """Horario como faldón: el horario y el teléfono en grande, el texto debajo."""
    solo_tel = re.compile(r"\*\*\[[^\]]+\]\(tel:[^)]+\)\s*(🔗|🆕)?\*\*")
    txt = render_bloques([b for b in sec["bl"] if not (b[0] == "p" and solo_tel.fullmatch(b[1].strip()))])
    return f"""<section class="seccion horario-sec">
 <div class="contenedor">
  <div class="horario">
   <div class="horario__cab"><span class="bloque__num">[{n:02d}]</span><h2 class="h2">{inline(sec['h2'])}</h2><span class="pildora-estado pildora-estado--claro" data-estado><i></i><span>{N['horario_corto']}</span></span></div>
   <div class="horario__datos">
    <p class="horario__grande"><span>Lunes a viernes</span><strong>9:00 <em>—</em> 20:00</strong></p>
    <a class="horario__tel tel" href="tel:{N['telefono_e164']}">{T.ICONO['tel']}{N['telefono']}</a>
   </div>
   <div class="prosa horario__txt">{txt}</div>
  </div>
 </div>
</section>
"""


def bloque(sec, n, gris):
    if sec["h2"].startswith("Horario"):
        return horario(sec, n)
    # El texto que se enciende (anim-enciende) solo en el H2 del primer bloque (contrato 13); el resto entra con .rv
    anim = "anim-enciende" if n == 1 else "rv"
    return f"""<section class="seccion{' seccion--gris seccion--trama' if gris else ''}">
 <div class="contenedor bloque">
  <div class="bloque__cab"><span class="bloque__num">[{n:02d}]</span><h2 class="h2 {anim}">{inline(sec['h2'])}</h2></div>
  <div class="prosa rv">{render_bloques(sec['bl'])}</div>
 </div>
</section>
"""


def foto_libre(clave):
    """Una foto de la bolsa que aún no salga en la página, o None (pool() repetiría si no queda ninguna)."""
    libres = [x for x in POOL if x[0] not in USADAS]
    return pool(clave, 1)[0] if libres else None


def bloque_partido(sec, n, fp, izq=False):
    """Bloque con foto y texto partido (Jean Paul, ronda 2). El CSS (B) lo pone en dos columnas y alterna el lado."""
    return f"""<section class="seccion bloque--partido{' bloque--izq' if izq else ''}">
 <div class="contenedor bloque">
  <div class="bloque__foto zoom">{T.foto(fp[0], fp[1], "(max-width: 900px) 100vw, 40vw")}</div>
  <div class="bloque__texto">
   <div class="bloque__cab"><span class="bloque__num">[{n:02d}]</span><h2 class="h2 rv">{inline(sec['h2'])}</h2></div>
   <div class="prosa rv">{render_bloques(sec['bl'])}</div>
  </div>
 </div>
</section>
"""


def faq_html(faq, url="/", titulo="Preguntas frecuentes", foto_f=None):
    if not faq:
        return ""
    items = "".join(f'<details class="rv" name="faq"{" open" if i == 1 else ""}><summary><b>{i:02d}</b><span>{esc(q)}</span><i aria-hidden="true"></i></summary><div class="faq__resp"><p>{inline(a)}</p></div></details>' for i, (q, a) in enumerate(faq, 1))
    f = foto_f or pool(url + "faq", 1)[0]
    return f"""<section class="seccion seccion--gris faq-sec" id="preguntas">
 <div class="contenedor faq">
  <div class="faq__cab">
   <span class="etiqueta">Dudas habituales</span><h2 class="h2 anim-enciende">{titulo}</h2>
   <div class="faq__visual">
    <div class="faq__foto zoom" data-velocidad="0.9">{T.foto(f[0], f[1], "(max-width: 900px) 100vw, 38vw")}</div>
    <a class="faq__cta" href="tel:{N['telefono_e164']}">{T.llama("faq__llama", False)}<span>¿No está tu pregunta?</span><strong>{N['telefono']}</strong><em>Te lo contamos por teléfono</em></a>
   </div>
  </div>
  <div class="faq__lista">{items}</div>
 </div>
</section>
"""


G_ICONO = '<svg class="op__g" viewBox="0 0 24 24" aria-hidden="true"><path fill="#4285F4" d="M23.5 12.3c0-.8-.1-1.6-.2-2.3H12v4.5h6.5a5.6 5.6 0 0 1-2.4 3.7v3h3.9c2.2-2.1 3.5-5.2 3.5-8.9z"/><path fill="#34A853" d="M12 24c3.2 0 6-1.1 8-2.9l-3.9-3c-1.1.7-2.5 1.2-4.1 1.2-3.1 0-5.8-2.1-6.7-5H1.3v3.1A12 12 0 0 0 12 24z"/><path fill="#FBBC05" d="M5.3 14.3a7.2 7.2 0 0 1 0-4.6V6.6H1.3a12 12 0 0 0 0 10.8z"/><path fill="#EA4335" d="M12 4.8c1.8 0 3.3.6 4.6 1.8l3.4-3.4A12 12 0 0 0 1.3 6.6l4 3.1c.9-2.9 3.6-4.9 6.7-4.9z"/></svg>'


def tarjeta_opinion(o):
    lugar = f'<span class="op__lugar">{esc(o["lugar"])}</span>' if o.get("lugar") else ""
    ini = esc(o["nombre"][:1])
    serv = esc(o.get("servicio", "")) + (f' · {esc(o["lugar"])}' if o.get("lugar") else "")
    return (f'<li class="op inclina rv"><span class="op__brillo" aria-hidden="true"></span>'
            f'<span class="estrellas" aria-label="5 estrellas">★★★★★</span>'
            f'<p class="op__serv">Servicio: {serv}</p>'
            f'<p class="op__tit">{esc(o["titulo"])}</p><p class="op__txt">«{esc(o["texto"])}»</p>'
            f'<div class="op__cab"><span class="op__ini" aria-hidden="true">{ini}</span>'
            f'<span class="op__quien"><strong>{esc(o["nombre"])}</strong><span class="op__lugar">Opinión publicada en Google</span></span>{G_ICONO}</div></li>')


def opiniones(pb=None, titulo=None, texto=""):
    """Reseñas reales de la ficha en tarjetas oscuras con profundidad (O24). Salen de resenas.json.
    En la landing de un pueblo, primero la reseña de ese pueblo si la hay. Si la página tiene su propio
    bloque de opiniones (el del widget), su H2 y su texto van aquí: un solo bloque de opiniones, no dos."""
    if not OPINIONES:
        return ""
    lista = sorted(OPINIONES, key=lambda o: 0 if pb and o.get("lugar") == pb else 1)
    titulo = titulo or "Lo que dicen los clientes de Balgas"
    texto = f'<p class="op-cab__txt">{texto}</p>' if texto else ""
    return f"""<section class="seccion seccion--oscura opiniones-sec" id="opiniones" aria-label="Opiniones de clientes en Google">
 <span class="cifras__resplandor" aria-hidden="true"></span>
 <div class="contenedor">
  <div class="op-cab">
   <div><span class="etiqueta">Opiniones reales en Google</span><h2 class="h2 anim-lineas">{titulo}</h2>{texto}</div>
   <div class="acciones op-cab__acciones">{T.boton("Ver todas las opiniones", MAPS, "btn--linea", None, ' rel="noopener" target="_blank"')}{T.btn_llamar("btn--acento", "Llamar")}</div>
  </div>
  <div class="op-carril">
   <ul class="op-lista" data-opiniones tabindex="0" aria-label="Reseñas">{"".join(tarjeta_opinion(o) for o in lista)}</ul>
  </div>
  <div class="op-pie">
   <p class="op-resumen"><span class="op-resumen__nota"><strong data-nota>{N['valoracion']}</strong><span class="estrellas" aria-hidden="true">★★★★★</span></span><span><span data-resenas>{N['resenas']}</span> opiniones de clientes que nos llamaron por una avería, una revisión o un calentador — <a href="{MAPS}" rel="noopener" target="_blank">verlas en Google</a></span></p>
   <div class="op-flechas"><button type="button" class="op-flecha" data-op="-1" aria-label="Reseña anterior">←</button><button type="button" class="op-flecha" data-op="1" aria-label="Reseña siguiente">→</button></div>
  </div>
 </div>
</section>
"""


def servicios_home():
    """Lista gigante con foto fija que cambia (O14 + F4)."""
    fotos, items = [], []
    for i, (tit, txt, url, img) in enumerate(SERVICIOS_HOME):
        fotos.append(f'<div class="slista__img{" activa" if i == 0 else ""}" data-i="{i}">{T.foto(img, tit + " en Alcorcón", "(max-width: 900px) 0px, 36vw")}</div>')
        items.append(f"""<li><a class="sitem{' activa' if i == 0 else ''}" href="{url}" data-i="{i}">
  <span class="sitem__num" aria-hidden="true">[{i + 1:02d}]</span>
  <span class="sitem__cuerpo"><span class="sitem__tit">{tit}</span><span class="sitem__txt">{txt}</span></span>
  <span class="sitem__mini">{T.foto(img, "", "180px")}</span>
 </a></li>""")
    return f"""<section class="seccion servicios-sec">
 <div class="contenedor">
  <div class="cab-seccion"><div><span class="etiqueta">Servicios</span><h2 class="h2 anim-enciende">Qué reparamos en tu casa</h2></div><p>Calderas, calentadores y termos de todas las marcas, en Alcorcón y los municipios de alrededor. {T.corchete("Todas las marcas")}</p></div>
  <div class="slista">
   <div class="slista__fija" aria-hidden="true">{"".join(fotos)}</div>
   <ol class="slista__items">{"".join(items)}</ol>
  </div>
 </div>
</section>
"""


MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]


def cifras_titulo(p):
    t, pb = datos.tipo_de(p["url"]), pueblo_de(p["url"])
    if t == "home":
        return f"{N['valoracion']} en Google y {N['anios']} años en el oficio"
    if t == "empresa":
        return f"{N['anios']} años en el oficio; {N['anios_balgas']} como Balgas"
    if t == "municipio":
        return f"Quién va a tu casa en {esc(pb)}, en cifras"
    if t == "marca":
        return "Un técnico para todas las marcas, en cifras"
    return "El técnico que va a tu casa, en cifras"


def cifras(p):
    """Faldón de cifras con contadores que ruedan (O22). H2 según el tipo de página y fecha visible de los datos."""
    import datetime
    hoy = datetime.date.today()
    return f"""<section class="seccion seccion--oscura cifras-sec" aria-label="Balgas en cifras">
 <span class="cifras__resplandor" aria-hidden="true"></span>
 <div class="contenedor">
  <div class="cab-seccion"><div><span class="etiqueta">Balgas en cifras</span><h2 class="h2 anim-lineas">{cifras_titulo(p)}</h2></div><p class="cifras__fecha" style="color:rgba(255,255,255,.72)">Datos de la ficha de Google, actualizados en <time datetime="{hoy:%Y-%m}">{MESES[hoy.month - 1]} de {hoy.year}</time>.</p></div>
  <div class="cifras">
   <div class="cifra"><span class="cifra__n"><span class="odo" data-odo="{N['valoracion']}" data-fuente="valoracion">{N['valoracion']}</span></span><span class="cifra__t">de valoración media en Google</span></div>
   <div class="cifra"><span class="cifra__n"><span class="odo" data-odo="{N['resenas']}" data-fuente="resenas">{N['resenas']}</span></span><span class="cifra__t">reseñas de clientes en Google</span></div>
   <div class="cifra"><span class="cifra__n"><span class="odo" data-odo="{N['anios']}">{N['anios']}</span></span><span class="cifra__t">años en el oficio; {N['anios_balgas']} como Balgas</span></div>
   <div class="cifra"><span class="cifra__n"><span class="odo" data-odo="1">1</span></span><span class="cifra__t">año de garantía sobre la avería reparada</span></div>
  </div>
 </div>
</section>
"""


# ---------- Marcas que reparamos: logos en gris que se encienden a color al pasar el ratón (ficha 14c) ----------
MARCAS_LOGOS = [
    ("saunier-duval", "Saunier Duval", "/productos-o-calderas/calderas-de-condensacion/saunier-duval/", 221),
    ("baxi", "Baxi", "/productos-o-calderas/calderas-de-condensacion/baxi/", 391),
    ("vaillant", "Vaillant", "/productos-o-calderas/calderas-de-condensacion/vaillant/", 501),
    ("domusa", "Domusa", "/productos-o-calderas/calderas-de-gasoil/domusa/", 393),
    ("junkers", "Junkers", None, 424),
    ("ferroli", "Ferroli", None, 240),
    ("ariston", "Ariston", None, 493),
    ("hermann", "Hermann", None, 513),
]


def marcas_logos():
    items = []
    for k, n, u, w in MARCAS_LOGOS:
        alta = ' class="alta"' if w / 120 < 1.9 else ""
        img = f'<img{alta} src="/img/marcas/{k}.webp" alt="{n}" width="{w}" height="120" loading="lazy" decoding="async">'
        items.append(f'<li><a class="marca-logo" href="{u}" title="Reparación de calderas {n}">{img}</a></li>' if u
                     else f'<li><span class="marca-logo">{img}</span></li>')
    return f"""<section class="seccion marcas-sec" aria-label="Marcas que reparamos">
 <div class="contenedor">
  <div class="marcas-cab"><span class="etiqueta">Marcas que reparamos</span><p>Reparamos todas las marcas. Estas son las que más vemos.</p></div>
  <ul class="marcas-logos">{"".join(items)}</ul>
 </div>
</section>
"""


def figura(foto_p, pb="Alcorcón", desenfoque=False):
    """Foto grande con desenfoque y texto al pasar el ratón (F6)."""
    return f"""<section class="contenedor figura-sec"><figure class="figura zoom{' desenfoca' if desenfoque else ''}">{T.foto(foto_p['archivo'], foto_p['alt'], '100vw')}<figcaption>{T.corchete('A domicilio')}<span>{esc(pb) if pb != "Alcorcón" else "Alcorcón y los municipios de alrededor"}</span></figcaption></figure></section>"""


# ---------- Mapa (dónde está Balgas: C. del Mestizaje, 3, Alcorcón) ----------
MAPA_EMBED = "https://maps.google.com/maps?cid=10173824761497024545&z=16&hl=es&output=embed"


def mapa():
    return f"""<section class="seccion mapa-sec" aria-label="Dónde estamos">
 <div class="contenedor">
  <div class="mapa">
   <div class="mapa__info">
    <span class="etiqueta">Dónde estamos</span>
    <h2 class="h2">Nuestra base, en Alcorcón</h2>
    <p class="mapa__dir">{N['calle']}<br>{N['cp']} {N['localidad']} ({N['provincia']})</p>
    <p>Trabajamos siempre a domicilio: desde aquí vamos a tu casa en Alcorcón y en los municipios de alrededor.</p>
    <div class="acciones">{T.btn_llamar("btn--acento", "Llamar ahora")}{T.boton("Ver en Google Maps", MAPS, "btn--linea", None, ' rel="noopener" target="_blank"')}</div>
   </div>
   <div class="mapa__marco"><iframe src="{MAPA_EMBED}" title="Mapa: Balgas, C. del Mestizaje 3, Alcorcón" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe></div>
  </div>
 </div>
</section>
"""


# ---------- Contacto ----------
def formulario():
    return f"""<form class="formulario rv rv-d1" action="/enviar.php" method="post" aria-label="Pedir presupuesto">
 <div class="aviso aviso--ok" id="form-ok" hidden>Mensaje enviado. De lunes a viernes, de 9:00 a 20:00, te llamamos en menos de una hora; si es fuera de ese horario, en cuanto empecemos.</div>
 <div class="aviso aviso--error" id="form-error" hidden>No se ha podido enviar. Llámanos al {N['telefono']} o inténtalo de nuevo.</div>
 <p class="formulario__confianza">Visita gratis, presupuesto sin compromiso y 1 año de garantía en la reparación. Te llamamos de lunes a viernes, de 9:00 a 20:00. Ayuda que nos digas qué aparato es, la marca y qué hace.</p>
 <div class="fila">
  <label>Nombre<input type="text" name="nombre" autocomplete="name" required maxlength="80"></label>
  <label>Teléfono<input type="tel" name="telefono" autocomplete="tel" inputmode="tel" required pattern="[0-9 +()\\-]{{9,20}}" maxlength="20"></label>
 </div>
 <label>Municipio<input type="text" name="municipio" autocomplete="address-level2" maxlength="60" placeholder="Alcorcón, Móstoles…"></label>
 <label>¿Qué le pasa? <span class="opcional">(opcional)</span><textarea name="mensaje" maxlength="2000" placeholder="Marca, modelo si lo sabes y qué hace (código de error, pierde presión, no enciende…)"></textarea></label>
 <label class="trampa" aria-hidden="true">Web<input type="text" name="web" tabindex="-1" autocomplete="off"></label>
 <input type="hidden" name="t" value="">
 <p class="casilla casilla--info">Usamos tus datos solo para contestarte. <a href="/politica-de-privacidad/">Política de privacidad</a>.</p>
 <div class="acciones"><button class="btn btn--acento" type="submit"><span class="btn__txt"><span>Pedir presupuesto</span><span aria-hidden="true">Pedir presupuesto</span></span></button><span style="font-size:.875rem;color:var(--c-suave)">O llama al <a class="tel" href="tel:{N['telefono_e164']}">{N['telefono']}</a></span></div>
</form>"""


def portada_contacto(p, intro):
    ps = [c for t, c in intro if t == "p"]
    entrada = inline(p["entrada_corta"]) if p.get("entrada_corta") else (inline(ps[0]) if ps else "")
    etq = f'<span class="etiqueta">{esc(p["etiqueta"])}</span>' if p.get("etiqueta") else ""
    return f"""<section class="portada">
 <div class="contenedor">
  {migas_html(p['url'])}
  <div class="portada__grid" style="align-items:start">
   <div class="rv">
    {etq}<h1 class="h1">{esc(p['h1'])}</h1>
    <p class="entrada">{entrada}</p>
    <a class="banda__tel tel" style="color:var(--c-oscuro)" href="tel:{N['telefono_e164']}">{N['telefono']}</a>
    <div class="acciones" style="margin-bottom:2rem">{T.btn_llamar("btn--acento", "Llamar ahora")}{T.btn_whatsapp()}</div>
    <address class="prosa" style="font-style:normal">
     <p><strong>Horario de trabajo:</strong> {N['horario_texto']}. El teléfono lo cogemos también fuera de horario y en festivos.</p>
     <p><strong>Correo:</strong> <a href="mailto:{N['email']}">{N['email']}</a></p>
     <p><strong>Dirección:</strong> {N['calle']}, {N['cp']} {N['localidad']}. Trabajamos siempre a domicilio.</p>
    </address>
   </div>
   {formulario()}
  </div>
 </div>
</section>
"""


# ---------- Página ----------
CONTACTO_YA = {"Teléfono", "Horario", "Email", "Pide presupuesto por escrito", "Opiniones en Google"}
BANDA_TIT = {
    "/reparacion-de-calentadores-en-madrid/": "¿Tu calentador no enciende o se apaga? Cuéntanos qué hace.",
    "/reparacion-de-termos-electronicos-en-madrid/": "¿Tu termo no calienta o gotea? Cuéntanos qué hace.",
    "/reparacion-de-calderas-madrid-2/": "¿Toca la revisión de tu caldera? Te damos cita.",
}
def es_widget(s):
    return any(tt == "p" and c.startswith("(Widget de reseñas") for tt, c in s["bl"])


def pagina(p):
    t = datos.tipo_de(p["url"])
    intro, secs = secciones(p["bloques"])
    fotos = FOTOS.get(p["url"], [])
    f0 = fotos[0] if fotos else None
    robots = "index, follow"  # v11: Contacto también se indexa (NAP, mapa y formulario)
    USADAS.clear()
    USADAS.update(f["archivo"] for f in fotos)
    if t == "home":
        USADAS.update(img for _, _, _, img in SERVICIOS_HOME)  # ya salen en la lista de servicios
    pb = pueblo_de(p["url"]) if t == "municipio" else None
    T.CTX["pueblo"] = pb
    # Foto a sangre (Jean Paul N6): se reserva ANTES de repartir las fotos de la declaración
    fig = None
    if t in ("home", "municipio", "servicio", "marca"):
        if len(fotos) > 1:
            fig = fotos[1]
        else:
            x = pool(p["url"] + "figura", 1)[0]
            fig = {"archivo": x[0], "alt": x[1]}
    # La foto del FAQ y la de la banda también se reservan antes: los bloques partidos solo usan fotos libres
    foto_faq = pool(p["url"] + "faq", 1)[0] if p["faq"] else None
    foto_banda = pool(p["url"] + "banda", 1)[0] if t != "contacto" else None
    # Secciones que salen como bloque normal (ni llamada a la acción, ni las de contacto que ya están arriba, ni la de opiniones)
    normal = lambda s: not ES_CTA.match(s["h2"]) and not (t == "contacto" and s["h2"] in CONTACTO_YA) and not es_widget(s)
    cuerpo = []
    if t == "contacto":
        cuerpo.append(portada_contacto(p, intro))
        cuerpo.append(mapa())
        largos = [c for tt, c in intro if tt == "p"]
        resto = [("p", c) for c in (largos if p.get("entrada_corta") else largos[1:])]
    else:
        cuerpo.append(portada(p, intro, f0))
        dec, resto = reparte_intro(intro)
        cuerpo.append(declaracion(p, dec, f0))
        uls = [c for tt, c in intro if tt == "ul"]
        if uls:
            cuerpo.append(ventajas(uls[0]))
    # Los párrafos de entrada que no caben en la declaración abren el primer bloque (contrato 2)
    if resto:
        for s in secs:
            if normal(s) and not s["h2"].startswith("Horario"):
                s["bl"] = resto + s["bl"]
                break
    if t == "home":
        cuerpo.append(servicios_home())
        cuerpo.append(marcas_logos())
    if p["url"] == "/productos-o-calderas/":
        cuerpo.append(marcas_logos())
    k = sum(1 for s in secs if normal(s))
    con_cifras = t in ("municipio", "servicio", "marca") and len(secs) > 5 and k >= 3
    if t == "home":
        pos_fig = 5 if k >= 5 else k
    else:
        pos_fig = 6 if k >= 7 else (k - 1 if k >= 4 else k)
        if con_cifras and pos_fig == 3:
            pos_fig = 4 if k >= 4 else 3
    n, gris, tiene_cta, puesto_op, puesto_mapa = 0, False, False, False, False
    partidos = []
    for i, s in enumerate(secs):
        if t == "contacto" and s["h2"] in CONTACTO_YA:
            continue  # ya están en la portada de contacto (teléfono, horario, correo y formulario)
        if ES_CTA.match(s["h2"]):
            ps = [c for tt, c in s["bl"] if tt == "p"]
            cuerpo.append(T.cinta())
            fb = foto_banda or pool(p["url"] + "banda", 1)[0]; foto_banda = None
            cuerpo.append(T.banda(inline(s["h2"]), " ".join(inline(x) for x in ps) or None, foto_banda=fb))
            tiene_cta = True
            continue
        if es_widget(s):
            if not puesto_op:
                ps = [c for tt, c in s["bl"] if tt == "p" and not c.startswith("(")]
                cuerpo.append(opiniones(pb, inline(s["h2"]), " ".join(inline(x) for x in ps)))
                puesto_op = True; gris = False
            continue
        n += 1
        # 1 de cada 3 bloques normales ([02], [05], [08]…) con foto y texto partido, solo con una foto libre
        fp = None
        if t in ("municipio", "servicio", "marca") and n % 3 == 2 and not s["h2"].startswith("Horario"):
            fp = foto_libre(p["url"] + f"partido{n}")
        if fp:
            cuerpo.append(bloque_partido(s, n, fp, izq=(n // 3) % 2 == 1)); gris = False
            partidos.append(n)
            if n == pos_fig:  # que la foto a sangre no vaya pegada a un bloque con foto
                pos_fig = n + 1  # si era el último bloque, la figura va tras el bucle
            continue
        cuerpo.append(bloque(s, n, gris))
        gris = not gris
        if t == "home" and s["h2"].startswith("Horario"):
            cuerpo.append(mapa()); puesto_mapa = True; gris = False
        if t == "home" and n == 3:
            cuerpo.append(cifras(p))
            gris = False
        if t == "empresa" and n == 1:
            cuerpo.append(cifras(p))
            gris = False
        # landings, servicios y marcas: una pieza distinta cada pocas pantallas para romper el muro de bloques
        if con_cifras and n == 3:
            cuerpo.append(cifras(p)); gris = False
        if fig and n == pos_fig:
            cuerpo.append(figura(fig, pueblo_de(p["url"]), desenfoque=(t == "home"))); gris = False; fig = None
    if fig and pos_fig > n and partidos and partidos[-1] == n:
        cuerpo.append(figura(fig, pueblo_de(p["url"]), desenfoque=(t == "home"))); fig = None
    # Dirección y mapa: en la home (junto al horario) y al cierre de la landing de Alcorcón (Matías 1)
    if (t == "home" and not puesto_mapa) or p["url"] == "/reparacion-calderas-alcorcon/":
        cuerpo.append(mapa())
    if not puesto_op:
        cuerpo.append(opiniones(pb))
    cuerpo.append(faq_html(p["faq"], p["url"], foto_f=foto_faq))
    if not tiene_cta and t != "contacto":
        cuerpo.append(T.cinta())
        cuerpo.append(T.banda(BANDA_TIT.get(p["url"]), foto_banda=foto_banda or pool(p["url"] + "banda", 1)[0]))
    return T.cabeza(p, schema_de(p), robots, precarga=f0["archivo"] if (f0 and t != "contacto") else None) + T.cabecera(p["url"]) + "".join(cuerpo) + T.pie()


# ---------- Legales ----------
def legales():
    txt = open(os.path.join(RAIZ, "contenido", "legales", "legales.md"), encoding="utf-8").read()
    res = []
    for m in re.finditer(r"^## (/[^\n]+/)\n(.*?)(?=^## /|\Z)", txt, re.S | re.M):
        url, cuerpo = m.group(1).strip(), m.group(2).strip()
        lineas = [l for l in cuerpo.split("\n")]
        titulo = lineas[0].strip()
        resto = "\n".join(lineas[1:]).strip().replace("\n---", "")
        res.append((url, titulo, resto))
    return res


def pagina_legal(url, titulo, md):
    T.CTX["pueblo"] = None
    p = {"url": url, "title": f"{titulo} | Balgas", "meta": f"{titulo} de reparacioncalderasbalgas.es.", "h1": titulo}
    NOMBRE_CORTO[url] = titulo
    bl = []
    for par in re.split(r"\n\s*\n", md):
        par = par.strip()
        if not par:
            continue
        if len(par) < 90 and not par.endswith(".") and "\n" not in par:
            bl.append(("h2l", par))
        else:
            bl.append(("p", par))
    htmlc = "".join(f'<h2 class="h3" style="margin:2.2rem 0 .8rem">{esc(c)}</h2>' if t == "h2l" else
                    "".join(f"<p>{inline(x)}</p>" for x in c.split("\n") if x.strip()) for t, c in bl)
    schema = {"@context": "https://schema.org", "@graph": [negocio_schema(), {"@type": "WebPage", "url": DOMINIO + url, "name": titulo,
                                                                          "dateModified": fecha_mod(os.path.join(RAIZ, "contenido", "legales", "legales.md"))}]}
    return T.cabeza(p, schema, "noindex, follow") + T.cabecera(url) + f"""<section class="portada"><div class="contenedor">{migas_html(url)}<h1 class="h1" style="font-size:clamp(2rem,1.4rem + 2.6vw,3.5rem)">{esc(titulo)}</h1></div></section>
<section class="seccion" style="padding-top:0"><div class="contenedor"><div class="prosa">{htmlc}</div></div></section>""" + T.pie()


def pagina_404():
    T.CTX["pueblo"] = None
    p = {"url": "/404/", "title": "Página no encontrada | Balgas", "meta": "Esta página no existe.", "h1": "Esta página no existe"}
    schema = {"@context": "https://schema.org", "@graph": [negocio_schema()]}
    return T.cabeza(p, schema, "noindex, follow") + T.cabecera("") + f"""<section class="portada"><div class="contenedor"><span class="etiqueta">Error 404</span><h1 class="h1">Esta página no existe</h1>
<p class="entrada">Puede que el enlace esté mal o que la página haya cambiado de sitio. Si tu caldera tiene un problema, llámanos y lo vemos.</p>
<div class="acciones">{T.btn_llamar()}{T.boton("Ir al inicio", "/", "btn--linea")}{T.boton("Zona de trabajo", "/reparacion-de-calderas-madrid/", "btn--linea")}</div></div></section>""" + T.pie()


def fecha_mod(ruta):
    """Fecha real de la última modificación de un texto (Bruno N2): la del último commit git que lo tocó,
    o la de hoy si tiene cambios sin commit (o si git no lo conoce)."""
    import datetime, subprocess
    hoy = datetime.date.today().isoformat()
    try:
        sucio = subprocess.run(["git", "status", "--porcelain", "--", ruta], cwd=RAIZ, capture_output=True, text=True, timeout=20).stdout.strip()
        if sucio:
            return hoy
        f = subprocess.run(["git", "log", "-1", "--format=%cs", "--", ruta], cwd=RAIZ, capture_output=True, text=True, timeout=20).stdout.strip()
        return f or hoy
    except Exception:
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
        urls.append((p["url"], p["mod"]))
    for url, tit, md in legales():
        escribir(url, pagina_legal(url, tit, md))
    open(os.path.join(SITIO, "404.html"), "w", encoding="utf-8").write(pagina_404())
    # sitemap y robots
    sm = "".join(f"<url><loc>{DOMINIO}{u}</loc><lastmod>{f}</lastmod></url>" for u, f in urls)
    open(os.path.join(SITIO, "sitemap.xml"), "w", encoding="utf-8").write(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>\n')
    open(os.path.join(SITIO, "robots.txt"), "w", encoding="utf-8").write(
        f"User-agent: *\nAllow: /\nDisallow: /enviar.php\n\nSitemap: {DOMINIO}/sitemap.xml\n")
    # llms.txt: resumen para asistentes de IA (datos de la ficha, lo que hace y lo que no, y todas las páginas)
    principales = ["/", "/reparacion-de-calderas-madrid/", "/reparacion-de-calderas-madrid-2/", "/reparacion-de-calentadores-en-madrid/",
                   "/reparacion-de-termos-electronicos-en-madrid/", "/productos-o-calderas/",
                   "/productos-o-calderas/calderas-de-condensacion/", "/productos-o-calderas/calderas-de-gasoil/",
                   "/quienes-somos/", "/contacto/"]
    marcas = ["/productos-o-calderas/calderas-de-condensacion/saunier-duval/", "/productos-o-calderas/calderas-de-condensacion/baxi/",
              "/productos-o-calderas/calderas-de-condensacion/vaillant/", "/productos-o-calderas/calderas-de-gasoil/domusa/",
              "/productos-o-calderas/calderas-de-gasoil/baxi/"]
    llms = [f"# Balgas · Reparación de calderas en Alcorcón", "",
            f"> Balgas repara y mantiene calderas de gas y de gasoil (también de condensación), calentadores y termos eléctricos, "
            f"a domicilio, en Alcorcón, el sur y el oeste de Madrid y La Sagra (Toledo). "
            f"{N['horario_texto']}. Teléfono {N['telefono']}. {N['valoracion']} en Google con {N['resenas']} reseñas.", "",
            "## Datos del negocio",
            f"- Nombre: Balgas ({N['razon_social']}).",
            f"- Dirección: {N['calle']}, {N['cp']} {N['localidad']} ({N['provincia']}). No atiende en local: trabaja siempre a domicilio.",
            f"- Teléfono: {N['telefono']} · Correo: {N['email']} · Ficha de Google: {FICHA}",
            f"- Horario: {N['horario_texto']}. El teléfono se coge también fuera de horario, pero no hay servicio en fin de semana.",
            f"- Técnico: Sergio, {N['anios']} años en el oficio ({N['anios_balgas']} como Balgas), instalador de gas autorizado (IGA nº 1442, registro 202026) y carné APMR CA-03174.",
            "- Visita gratis, presupuesto sin compromiso antes de reparar y 1 año de garantía sobre la avería reparada. Repuestos originales.",
            "- Todas las marcas (Saunier Duval, Baxi, Vaillant, Junkers, Ferroli, Domusa, Ariston, Hermann…). Si la caldera sigue en la garantía del fabricante, primero se llama a la marca.",
            "- Cambia la caldera solo cuando repararla sale muy caro y es lo mejor para el cliente; siempre intenta reparar primero al mejor coste posible.",
            "- También cambia termos y calentadores cuando ya no compensa repararlos.",
            "- Sin contratos de mantenimiento; si el cliente lo pide, cada año le llama o le escribe por WhatsApp para recordarle la revisión (sin compromiso).",
            "- Corrige los defectos de la inspección periódica de gas (obligatoria cada 5 años). La inspección en sí recomienda hacerla con la compañía de gas, que sale más barata.",
            "- Pago: cualquier medio de pago.",
            "", "## Lo que Balgas no hace",
            "- Urgencias 24 horas.",
            "- Servicio en fines de semana.",
            "- Calefacción central de edificios ni comunidades de vecinos.",
            "- Instalaciones industriales.",
            "- No da precios cerrados ni plazo de cita por la web: el presupuesto se da en la visita y la cita, por teléfono.",
            "", "## Páginas principales"]
    llms += [f"- [{nombre(u)}]({DOMINIO}{u}): {POR_URL[u]['meta']}" for u in principales if u in POR_URL]
    llms += ["", "## Marcas"] + [f"- [{nombre(u)}]({DOMINIO}{u}): {POR_URL[u]['meta']}" for u in marcas if u in POR_URL]
    llms += ["", "## Municipios"] + [f"- [{v}]({DOMINIO}{k})" for k, v in PUEBLO.items()]
    open(os.path.join(SITIO, "llms.txt"), "w", encoding="utf-8").write("\n".join(llms) + "\n")
    print(f"build: {len(PAGINAS)} páginas + {len(legales())} legales + 404 · sitemap con {len(urls)} URLs")


if __name__ == "__main__":
    main()
