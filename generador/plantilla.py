# -*- coding: utf-8 -*-
"""GYF-Rayo · Plantilla común: <head>, cabecera con menú a pantalla completa, pie de tarjetas y piezas
reutilizables (botón que rueda letra a letra, cintas, iconos del sprite, fotos).
Un cambio aquí llega a todas las páginas (paso 48)."""
import html, json, os, re
import config as C
from config import (VERSION, DOMINIO, GTM_ID, NEGOCIO as N, MENU, LEGALES, CREDITO, MARCA, URLS, COLOR_TEMA,
                    FICHA, FUENTES_PRECARGA, SERVICIOS_HOME, MUNICIPIOS, texto)

A = lambda s: html.escape(str(s), quote=True)
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------- Sprite: iconos (recursos/iconos/sprite.svg, estilo C) + el símbolo de la marca ----------
_SP = open(os.path.join(RAIZ, "recursos", "iconos", "sprite.svg"), encoding="utf-8").read()
SIMBOLOS = {m.group(1): m.group(0) for m in re.finditer(r'<symbol id="i-([a-z0-9-]+)".*?</symbol>', _SP, re.S)}

_SVG = open(os.path.join(RAIZ, "recursos", "marca", MARCA["simbolo"]), encoding="utf-8").read()
_SVG = re.sub(r"<metadata>.*?</metadata>", "", _SVG, flags=re.S)
_CUERPO = re.search(r"<svg[^>]*>(.*)</svg>", _SVG, re.S).group(1)
VB = re.search(r'viewBox="([^"]+)"', _SVG).group(1)
# El <svg> que usa el símbolo va en 0 0 ancho alto: el <symbol> ya trae su viewBox (con origen donde sea)
VB0 = "0 0 {} {}".format(*VB.split()[2:4])
_MONO = re.sub(r'fill="#[0-9A-Fa-f]{3,6}"', 'fill="currentColor"', _CUERPO)
if "fill=" not in _MONO:
    _MONO = f'<g fill="currentColor">{_MONO}</g>'


# ---------- v4 · El logotipo como elemento gráfico: GORDO, & y FLACO en tres <symbol> (se animan por separado) ----------
_LG = open(os.path.join(RAIZ, "recursos", "marca", "logo-horizontal-color.svg"), encoding="utf-8").read()
LG_VB = re.search(r'viewBox="([^"]+)"', _LG).group(1)
_LG_P = [re.sub(r"(\d+\.\d)\d+", r"\1", d) for d in re.findall(r'<path[^>]* d="([^"]+)"', _LG)]
_LG_PARTES = {"gordo": _LG_P[0:5], "simbolo": _LG_P[10:12], "flaco": _LG_P[5:10]}
LG_SIMBOLOS = "".join(f'<symbol id="lg-{k}" viewBox="{LG_VB}">' + "".join(f'<path d="{d}"/>' for d in v) + "</symbol>"
                      for k, v in _LG_PARTES.items())


def logotipo(clase=""):
    """El logotipo completo en tres piezas (lg__gordo, lg__simbolo (el monograma G+F), lg__flaco) para moverlas por separado.
    Color con fill/stroke desde el CSS. Decorativo: aria-hidden."""
    ancho, alto = LG_VB.split()[2:4]   # el <use> de un <symbol> ocupa 0 0 100% 100%: el <svg> va en origen 0
    return (f'<svg class="lg {clase}" viewBox="0 0 {ancho} {alto}" aria-hidden="true" focusable="false">'
            + "".join(f'<use class="lg__{k}" href="#lg-{k}"/>' for k in ("gordo", "simbolo", "flaco")) + "</svg>")


def sprite(html_pagina):
    """Solo los símbolos que usa la página (se inserta al abrir <body>)."""
    usados = sorted(set(re.findall(r'href="#i-([a-z0-9-]+)"', html_pagina)))
    faltan = [u for u in usados if u not in SIMBOLOS]
    if faltan:
        raise SystemExit(f"plantilla: iconos que no están en recursos/iconos/sprite.svg: {faltan}")
    cuerpo = "".join(SIMBOLOS[u] for u in usados)
    return (f'<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">'
            f'<symbol id="simbolo-c" viewBox="{VB}">{_CUERPO}</symbol><symbol id="simbolo-m" viewBox="{VB}">{_MONO}</symbol>'
            f'{LG_SIMBOLOS if "#lg-" in html_pagina else ""}{cuerpo}</svg>')


def ico(nombre, clase=""):
    """Icono del sprite (trazo en currentColor + un acento .a/.al que pinta var(--ico-acento))."""
    return f'<svg class="ico {clase}" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><use href="#i-{nombre}"/></svg>'


def simbolo(clase="", color=False):
    """El símbolo de la marca. color=False lo pinta de un solo color (currentColor): viñetas y separadores."""
    return f'<svg class="simbolo {clase}" viewBox="{VB0}" aria-hidden="true" focusable="false"><use href="#simbolo-{"c" if color else "m"}"/></svg>'


# ---------- Botón: el texto rueda letra a letra (R13) ----------
def _letras(t):
    return "".join(f'<span style="--i:{k}">{"&nbsp;" if c == " " else html.escape(c)}</span>' for k, c in enumerate(t))


def txt_boton(t):
    return (f'<span class="sr">{html.escape(t)}</span><span class="btn__txt" aria-hidden="true">'
            f'<span class="btn__a">{_letras(t)}</span><span class="btn__b">{_letras(t)}</span></span>')


def boton(t, href, clase="", icono="flecha-diagonal", extra=""):
    ic = f'<span class="btn__ico">{ico(icono)}{ico(icono)}</span>' if icono else ""
    pre = ""
    if icono in ("contacto", "whatsapp-generico"):   # el icono de llamar/WhatsApp va delante y quieto
        pre, ic = ico(icono, "btn__pre"), ""
    return f'<a class="btn {clase}" href="{A(href)}"{extra}>{pre}{txt_boton(t)}{ic}</a>'


def boton_form(t, clase="btn--acento"):
    return f'<button class="btn {clase}" type="submit">{txt_boton(t)}<span class="btn__ico">{ico("flecha-diagonal")}{ico("flecha-diagonal")}</span></button>'


def btn_llamar(clase="btn--acento", t=None, extra=""):
    return boton(t or f"Llamar al {N['telefono']}", f"tel:{N['telefono_e164']}", clase + " tel", "contacto", extra)


CTX = {"pueblo": None}   # en las landings de municipio, todos los WhatsApp llevan el pueblo


def wa_url(pueblo=None):
    from urllib.parse import quote
    pueblo = pueblo or CTX["pueblo"]
    t = texto("whatsapp_saludo") + (texto("whatsapp_pueblo", pueblo=pueblo) if pueblo else "") + ": "
    return f"https://wa.me/{N['whatsapp']}?text={quote(t)}"


def btn_whatsapp(clase="btn--linea", pueblo=None):
    return boton("WhatsApp", wa_url(pueblo), clase, "whatsapp-generico", ' rel="noopener" target="_blank"')


# ---------- Imágenes (las genera rematar.py: 800 y 1600, JPG y WebP) ----------
def medida(archivo):
    from PIL import Image
    for d in ("fotos", "casos"):
        r = os.path.join(RAIZ, "recursos", d, archivo)
        if os.path.exists(r):
            with Image.open(r) as im:
                return im.width, im.height
    return 1600, 1067


def foto(archivo, alt, sizes="(max-width: 900px) 100vw, 50vw", prioridad=False, clase=""):
    base = archivo.rsplit(".", 1)[0]
    w, h = medida(archivo)
    alto = round(1600 * h / w)
    carga = 'fetchpriority="high"' if prioridad else 'loading="lazy" decoding="async"'
    return (f'<picture class="{clase}"><source type="image/webp" srcset="/img/{base}-800.webp 800w, /img/{base}-1600.webp 1600w" sizes="{sizes}">'
            f'<img src="/img/{base}-1600.jpg" srcset="/img/{base}-800.jpg 800w, /img/{base}-1600.jpg 1600w" sizes="{sizes}" '
            f'width="1600" height="{alto}" alt="{A(alt)}" {carga}></picture>')


# ---------- v2 · Objetos 3D de la marca (los genera rematar.py en /img/obj/: 400, 800 y 1.200, WebP con alfa) ----------
def objeto(nombre, sizes="(max-width: 900px) 60vw, 420px", clase="", alt="", prioridad=False):
    carga = 'fetchpriority="high"' if prioridad else 'loading="lazy" decoding="async"'
    return (f'<img class="obj3d {clase}" src="/img/obj/{nombre}-800.webp" srcset="/img/obj/{nombre}-400.webp 400w, '
            f'/img/obj/{nombre}-800.webp 800w, /img/obj/{nombre}-1200.webp 1200w" sizes="{sizes}" width="800" height="800" alt="{A(alt)}" {carga}>')


# ---------- <head> ----------
def og_ruta(url):
    """Imagen para redes de cada página (la genera rematar.py en /og/). La 404 usa la general."""
    if url == "/404/":
        return "/og-image.jpg"
    return "/og/" + ("inicio" if url == "/" else url.strip("/").replace("/", "-")) + ".jpg"


def cabeza(p, schema, robots="index, follow", precarga=None):
    """precarga: (srcset, sizes) de la imagen LCP (el objeto de portada en la home)."""
    url = DOMINIO + p["url"]
    pre = ""
    if precarga:
        pre = f'<link rel="preload" as="image" type="image/webp" imagesrcset="{precarga[0]}" imagesizes="{precarga[1]}" fetchpriority="high">'
    fuentes = "".join(f'<link rel="preload" href="/fuentes/{f}" as="font" type="font/woff2" crossorigin>' for f in FUENTES_PRECARGA)
    return f"""<!doctype html>
<html lang="es" data-gtm="{GTM_ID}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{A(p['title'])}</title>
<meta name="description" content="{A(p['meta'])}">
<meta name="robots" content="{robots}">
{"" if p["url"] == "/404/" else f'<link rel="canonical" href="{url}">'}
<meta name="theme-color" content="{COLOR_TEMA}">
<meta property="og:type" content="website">
<meta property="og:locale" content="es_ES">
<meta property="og:site_name" content="{A(N['nombre'])}">
<meta property="og:title" content="{A(p['title'])}">
<meta property="og:description" content="{A(p['meta'])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{DOMINIO}{og_ruta(p['url'])}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{A(p['h1'])}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
{fuentes}
{pre}
<script>document.documentElement.classList.add("js")</script>
<link rel="stylesheet" href="/css/estilo.css?v={VERSION}">
<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False, separators=(",", ":"))}</script>
</head>
"""


# ---------- Cabecera y menú a pantalla completa (R4 variación B + R34 sin Flip) ----------
def _menu(actual):
    grandes, cols = [], []
    for k, (nombre, dest) in enumerate(MENU):
        if isinstance(dest, list):
            if not dest:
                continue
            li = "".join(f'<li><a href="{u}"{" aria-current=page" if u == actual else ""}>{n}</a></li>' for n, u in dest)
            cols.append(f'<div class="menu__col"><p class="menu__h">{nombre}</p><ul>{li}</ul></div>')
        else:
            cur = ' aria-current="page"' if dest == actual else ""
            grandes.append(f'<li style="--i:{len(grandes)}"><a href="{dest}"{cur}><span>{nombre}</span></a></li>')
    return "".join(grandes), "".join(cols)


def cabecera(actual):
    grandes, cols = _menu(actual)
    logo = f'<img src="/marca/{MARCA["logo"]}" alt="{A(texto("logo_alt"))}" width="{MARCA["logo_ancho"]}" height="{MARCA["logo_alto"]}">'
    logo_b = MARCA.get("logo_blanco") or MARCA["logo"]
    return f"""<body>
<!--SPRITE-->
<div class="cortina" aria-hidden="true" data-cortina><svg class="cortina__sim" viewBox="{VB0}"><use href="#simbolo-m"/></svg></div>
<a class="saltar" href="#contenido">Saltar al contenido</a>
<header class="cab" data-cab>
 <div class="contenedor cab__in">
  <a class="cab__logo" href="/" aria-label="{A(N['nombre'])}: inicio">{logo}</a>
  <div class="cab__der">
   {btn_llamar("btn--acento btn--cab", N['telefono'], ' data-zona="cabecera"')}
   <a class="cab__circulo tel" href="tel:{N['telefono_e164']}" aria-label="Llamar al {N['telefono']}" data-zona="cabecera">{ico("contacto")}</a>
   <button class="cab__burger" type="button" aria-label="Abrir menú" aria-expanded="false" aria-controls="menu"><span></span><span></span></button>
  </div>
 </div>
</header>
<div class="menu" id="menu" aria-hidden="true" role="dialog" aria-label="Menú" data-menu>
 <div class="contenedor menu__in">
  <div class="menu__top"><img class="menu__logo" src="/marca/{logo_b}" alt="" width="{MARCA['logo_ancho']}" height="{MARCA['logo_alto']}"><button class="menu__cerrar" type="button" aria-label="Cerrar menú">{ico("cerrar")}</button></div>
  <nav class="menu__nav" aria-label="Principal"><ul class="menu__grandes">{grandes}</ul><div class="menu__cols">{cols}</div></nav>
  <div class="menu__contacto">
   <p class="estado" data-estado><i></i><span>{N['horario_corto']}</span></p>
   <a class="menu__tel tel" href="tel:{N['telefono_e164']}">{N['telefono']}</a>
   <a class="menu__mail" href="mailto:{N['email']}">{N['email']}</a>
   <div class="acciones">{btn_whatsapp("btn--linea-claro")}</div>
  </div>
 </div>
</div>
<main id="contenido">
"""


# ---------- Cintas (R14): pista con dos grupos iguales para que el bucle no tenga costura ----------
def cinta(palabras, clase="", sentido=-1):
    sep = simbolo("cinta__sep")
    grupo = "".join(f"<span>{A(x)}</span>{sep}" for x in list(palabras) * 2)
    return (f'<div class="cinta {clase}" aria-hidden="true"><div class="cinta__pista" data-cinta="{sentido}">'
            f'<div class="cinta__grupo">{grupo}</div><div class="cinta__grupo">{grupo}</div></div></div>')


# ---------- Estado abierto / cerrado y nota de Google (piezas de la base GYF) ----------
def estado(clase=""):
    return f'<p class="estado {clase}" data-estado><i></i><span>{N["horario_corto"]}</span></p>'


def nota(clase="", enlace=None):
    cuerpo = (f'<strong data-nota>{N["valoracion"]}</strong><span class="estrellas" aria-hidden="true">★★★★★</span>'
              + (f'<span><span data-resenas>{N["resenas"]}</span> reseñas en Google</span>' if getattr(C, "NOTA_CON_NUMERO", True)
                 else f'<span>en Google<span data-resenas hidden>{N["resenas"]}</span></span>'))
    if enlace:
        return f'<a class="nota {clase}" href="{A(enlace)}"{" rel=noopener target=_blank" if enlace.startswith("http") else ""}>{cuerpo}</a>'
    return f'<p class="nota {clase}">{cuerpo}</p>'


# ---------- Pie (v2, el de Rayo): el logotipo gigante a sangre que baja con el scroll (R17) y tarjetas de color ----------
def pie():
    serv = [(n, u) for n, u in (MENU[1][1] if isinstance(MENU[1][1], list) else [])]
    base = [] if N["localidad"] in [n for _, n in MUNICIPIOS] else [(N["localidad"], "/")]
    zona = base + [(n, u) for u, n in MUNICIPIOS] if URLS["municipio"] else []
    grandes = [(n, d) for n, d in MENU if not isinstance(d, list)]
    lst = lambda L: "".join(f'<li><a href="{u}">{n}</a></li>' for n, u in L)
    leg = "".join(f'<li><a href="{u}">{n}</a></li>' for n, u in LEGALES)
    abre, cierra = N["abre"].lstrip("0"), N["cierra"].lstrip("0")
    return f"""</main>
<footer class="pie">
 <div class="contenedor">
  <div class="pie__nombre" aria-hidden="true" data-pie-nombre>{logotipo("pie__lg")}</div>
  <div class="pie__tarjetas">
   <div class="pie__t pie__t--menu rv">
    <p class="pie__titular">{texto("pie_titular")}</p>
    <ul class="pie__grandes">{lst(grandes)}</ul>
   </div>
   <div class="pie__t pie__t--contacto rv">
    {estado("estado--claro")}
    <a class="pie__tel tel" href="tel:{N['telefono_e164']}" data-zona="pie">{N['telefono']}</a>
    <a class="pie__mail" href="mailto:{N['email']}">{N['email']}</a>
    <p class="pie__dir"><a href="{FICHA}" rel="noopener" target="_blank">{N['calle']}, {N['cp']} {N['localidad']} ({N['provincia']})</a></p>
    <div class="acciones">{btn_whatsapp("btn--blanco btn--peq")}</div>
   </div>
   <div class="pie__t pie__t--horario rv">
    <span class="pie__sim" aria-hidden="true">{objeto("simbolo-cerca", "(max-width: 900px) 60vw, 360px")}</span>
    <p class="pie__h">Horario</p>
    <p class="pie__horas"><strong>{abre}<em>—</em>{cierra}</strong><span>{N['dias_texto']}</span></p>
    <p class="pie__nota">{texto("llms_horario_extra")}</p>
   </div>
   <div class="pie__t pie__t--listas rv">
    <div><p class="pie__h">Servicios</p><ul>{lst(serv)}</ul></div>
    {f'<div class="pie__zonas"><p class="pie__h">Zonas</p><ul>{lst(zona)}</ul></div>' if zona else ""}
   </div>
  </div>
  <div class="pie__legal">
   <span>© <span data-anio>2026</span> {N['razon_social']}</span>
   <ul>{leg}<li><a href="#" data-cookies-config>Configurar cookies</a></li></ul>
   {f'<span class="pie__credito">Diseño y SEO: <a href="{CREDITO[1]}" target="_blank" rel="noopener">{CREDITO[0]}</a></span>' if CREDITO else ""}
  </div>
 </div>
</footer>
<a class="subir" href="#contenido" aria-label="Volver arriba" data-subir>{ico("flecha-diagonal")}</a>
<nav class="barra-movil" aria-label="Contacto rápido">{btn_llamar("btn--acento", "Llamar")}{btn_whatsapp("btn--linea")}</nav>
<div class="cookies" id="cookies" role="dialog" aria-label="Aviso de cookies">
 <p>Usamos cookies propias y de Google para medir las visitas y saber qué anuncios funcionan. Solo se activan si las acepta. <a href="/politica-de-cookies/">Política de cookies</a>.</p>
 <div class="acciones"><button class="btn btn--oscuro btn--peq" type="button" data-cookies="si">{txt_boton("Aceptar")}</button><button class="btn btn--linea btn--peq" type="button" data-cookies="no">{txt_boton("Rechazar")}</button></div>
</div>
<script src="/js/main.js?v={VERSION}" defer></script>
</body>
</html>
"""
