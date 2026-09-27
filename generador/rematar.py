# -*- coding: utf-8 -*-
"""GYF-Rayo · Rematar (paso 52): siempre el ÚLTIMO del build.
Copia recursos, genera imágenes 800/1600 en JPG y WebP, une y minifica el CSS,
y deja los archivos de servidor (.htaccess, enviar.php, favicons, manifest)."""
import os, re, shutil, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import (VERSION, NEGOCIO as N, DOMINIO, MARCA, COOKIES_CLAVE, HOST_PRODUCCION, COLOR_TEMA, REDIRECCIONES,
                    REDIRECCIONES_302, GONE_410, GONE_410_PATRONES, URLS, OBJETO_PORTADA, OG, texto)
import json

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = lambda *p: os.path.join(RAIZ, *p)
S = lambda *p: os.path.join(RAIZ, "sitio", *p)


def css():
    base = open(R("base", "css", "base.css"), encoding="utf-8").read()
    tema = open(R("cliente", "css", "tema.css"), encoding="utf-8").read()
    v2 = R("cliente", "css", "v2.css")
    if os.path.exists(v2):   # v2: color, cajas, objetos 3D y movimiento (va detrás de base y tema: manda)
        tema += "\n" + open(v2, encoding="utf-8").read()
    v3 = R("cliente", "css", "v3.css")
    if os.path.exists(v3):   # v3: el símbolo G+F manda y los huecos de foto (la última)
        tema += "\n" + open(v3, encoding="utf-8").read()
    v4 = R("cliente", "css", "v4.css")
    if os.path.exists(v4):   # v4: fotos artísticas y el logotipo como elemento gráfico
        tema += "\n" + open(v4, encoding="utf-8").read()
    # el tema va DESPUÉS de la base para que sus variables manden; las @font-face, arriba
    fuentes = "".join(re.findall(r"@font-face\{[^}]+\}", tema))
    tema = re.sub(r"@font-face\{[^}]+\}", "", tema)
    todo = fuentes + base + tema
    todo = re.sub(r"/\*.*?\*/", "", todo, flags=re.S)
    todo = re.sub(r"\s+", " ", todo)
    todo = re.sub(r"\s*([{}:;,>])\s*", r"\1", todo)
    todo = todo.replace(";}", "}")
    # restaurar espacios necesarios en selectores/valores que la regla anterior pudo tocar
    todo = re.sub(r"@media\(", "@media (", todo)
    todo = todo.replace(")and(", ") and (").replace("and(", "and (")
    os.makedirs(S("css"), exist_ok=True)
    open(S("css", "estilo.css"), "w", encoding="utf-8").write(todo)
    return len(todo)


def al_dia(origen, salidas):
    """True si todas las salidas existen y son más nuevas que el original (no hace falta regenerarlas)."""
    t = os.path.getmtime(origen)
    return all(os.path.exists(s) and os.path.getmtime(s) >= t for s in salidas)


def imagenes():
    """Fotos y casos (JPG/PNG/WebP) → 800 y 1600 en JPG y WebP. El objeto de portada (con alfa) → 420 y 840
    en WebP con alfa y 840 en PNG (respaldo)."""
    os.makedirs(S("img"), exist_ok=True)
    n = 0
    for carpeta in ("fotos", "casos"):
        d = R("recursos", carpeta)
        if not os.path.isdir(d):
            continue
        for f in sorted(os.listdir(d)):
            if not f.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                continue
            b = f.rsplit(".", 1)[0]
            if al_dia(os.path.join(d, f), [S("img", f"{b}-{w}.{e}") for w in (800, 1600) for e in ("jpg", "webp")]):
                n += 1; continue
            im = Image.open(os.path.join(d, f)).convert("RGB")
            for w in (800, 1600):
                v = im if im.width == w else im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
                v.save(S("img", f"{b}-{w}.jpg"), "JPEG", quality=80 if w == 1600 else 78, optimize=True, progressive=True)
                v.save(S("img", f"{b}-{w}.webp"), "WEBP", quality=76, method=6)
            n += 1
    o = R("recursos", "objeto", OBJETO_PORTADA["imagen"])
    if os.path.exists(o):
        im = Image.open(o).convert("RGBA")
        b = OBJETO_PORTADA["imagen"].rsplit(".", 1)[0]
        for w in (420, 840):
            v = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
            v.save(S("img", f"{b}-{w}.webp"), "WEBP", quality=82, method=6)
        im.resize((840, round(im.height * 840 / im.width)), Image.LANCZOS).save(S("img", f"{b}-840.png"), "PNG", optimize=True)
    else:
        sys.exit(f"rematar: falta el objeto de portada recursos/objeto/{OBJETO_PORTADA['imagen']} (herramientas/objeto3d/foto_fija.py lo genera)")
    for k in ("video_webm", "video_mov"):
        if OBJETO_PORTADA.get(k):
            os.makedirs(S("objeto"), exist_ok=True)
            shutil.copy(R("recursos", "objeto", OBJETO_PORTADA[k]), S("objeto", OBJETO_PORTADA[k]))
    return n


OBJ_MASTER = R("herramientas", "objetos3d", "master")
OBJ_ANCHOS = (400, 800, 1200)


def objetos():
    """v2 · Familia de objetos 3D (máster PNG 1.600 con alfa) → WebP con alfa a 400, 800 y 1.200 en /img/obj/.
    Además, un fondo desenfocado para la banda final (el símbolo de cromo muy de cerca, oscuro y fuera de foco)."""
    from PIL import ImageFilter, ImageEnhance
    if not os.path.isdir(OBJ_MASTER):
        sys.exit("rematar: faltan los objetos 3D (python3 herramientas/objetos3d/generar.py)")
    os.makedirs(S("img", "obj"), exist_ok=True)
    vivos = {f[:-4] for f in os.listdir(OBJ_MASTER) if f.endswith(".png")}
    for f in os.listdir(S("img", "obj")):
        if f != "banda-fondo.webp" and f.rsplit("-", 1)[0] not in vivos:
            os.remove(S("img", "obj", f))
    n = 0
    for f in sorted(os.listdir(OBJ_MASTER)):
        if not f.endswith(".png"):
            continue
        b = f[:-4]
        if al_dia(os.path.join(OBJ_MASTER, f), [S("img", "obj", f"{b}-{w}.webp") for w in OBJ_ANCHOS]):
            n += 1; continue
        im = Image.open(os.path.join(OBJ_MASTER, f)).convert("RGBA")
        for w in OBJ_ANCHOS:
            im.resize((w, w), Image.LANCZOS).save(S("img", "obj", f"{b}-{w}.webp"), "WEBP", quality=80, method=6)
        n += 1
    g = Image.open(os.path.join(OBJ_MASTER, "simbolo-cerca-cromo.png")).convert("RGBA").resize((900, 900), Image.LANCZOS)
    fondo = Image.new("RGBA", (1440, 900), (0, 0, 0, 0))
    fondo.alpha_composite(g, (620, 60))
    fondo = fondo.filter(ImageFilter.GaussianBlur(16))
    fondo = ImageEnhance.Brightness(fondo).enhance(.7)
    fondo.save(S("img", "obj", "banda-fondo.webp"), "WEBP", quality=70, method=6)
    return n


def copiar():
    shutil.copytree(R("recursos", "fuentes"), S("fuentes"), dirs_exist_ok=True)
    for f in os.listdir(S("fuentes")):
        m = re.match(r"(.+)-latin-(\d+)-normal\.woff2", f)
        if m:
            os.replace(S("fuentes", f), S("fuentes", f"{m.group(1)}-{m.group(2)}.woff2"))
    os.makedirs(S("marca"), exist_ok=True)
    for f in os.listdir(R("recursos", "marca")):
        if f.endswith(".svg"):
            shutil.copy(R("recursos", "marca", f), S("marca", f))
    shutil.copy(R("recursos", "favicon", "favicon.svg"), S("favicon.svg"))
    favicons()
    # el manifest sale de config.py (nombre y color), no se copia a mano
    open(S("site.webmanifest"), "w", encoding="utf-8").write(json.dumps({
        "name": N["nombre"], "short_name": N["nombre"][:12],
        "icons": [{"src": "/android-chrome-192x192.png", "sizes": "192x192", "type": "image/png"},
                  {"src": "/android-chrome-512x512.png", "sizes": "512x512", "type": "image/png"}],
        "theme_color": COLOR_TEMA, "background_color": COLOR_TEMA, "display": "standalone"}, ensure_ascii=False))
    os.makedirs(S("js"), exist_ok=True)
    js()
    shutil.copytree(R("cliente", "js", "vendor"), S("js", "vendor"), dirs_exist_ok=True)
    shutil.copy(R("contenido", "resenas.json"), S("resenas.json"))


# ---------- Favicons desde el símbolo fucsia (recursos/og/simbolo-fucsia.png) ----------
def _simbolo_en(lado, margen, fondo=None):
    sim = Image.open(R("recursos", "og", "simbolo-fucsia.png")).convert("RGBA")
    caja = lado - 2 * margen
    esc = min(caja / sim.width, caja / sim.height)
    s = sim.resize((max(1, round(sim.width * esc)), max(1, round(sim.height * esc))), Image.LANCZOS)
    lienzo = Image.new("RGBA", (lado, lado), fondo or (0, 0, 0, 0))
    lienzo.alpha_composite(s, ((lado - s.width) // 2, (lado - s.height) // 2))
    return lienzo


def favicons():
    crema = Image.new("RGBA", (1, 1), COLOR_TEMA).getpixel((0, 0))
    for n, lado, margen, fondo in [("favicon-16x16.png", 16, 1, None), ("favicon-32x32.png", 32, 2, None),
                                   ("favicon-48x48.png", 48, 3, None), ("apple-touch-icon.png", 180, 34, crema),
                                   ("android-chrome-192x192.png", 192, 36, crema), ("android-chrome-512x512.png", 512, 96, crema)]:
        _simbolo_en(lado, margen, fondo).save(S(n), "PNG", optimize=True)
    _simbolo_en(48, 3).save(S("favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])


# ---------- Imagen para redes (Open Graph) por página: 1200 × 630, crema, H1 en Outfit y símbolo fucsia ----------
def _partir(draw, txt, fuente, ancho):
    lineas, act = [], ""
    for w in txt.split():
        prueba = (act + " " + w).strip()
        if draw.textlength(prueba, font=fuente) <= ancho or not act:
            act = prueba
        else:
            lineas.append(act); act = w
    return lineas + ([act] if act else [])


def og_imagen(h1, destino, etiqueta):
    from PIL import ImageDraw, ImageFont
    W, H = 1200, 630
    im = Image.new("RGBA", (W, H), OG["fondo"])
    d = ImageDraw.Draw(im)
    sim = _simbolo_en(470, 0)
    im.alpha_composite(sim, (W - 470 + 40, (H - 470) // 2 + 30))   # el símbolo sale por la derecha, cortado
    ancho = 760
    for tam in (84, 76, 68, 60, 54, 48):
        f = ImageFont.truetype(R("recursos", "og", "outfit-600.ttf"), tam)
        lineas = _partir(d, h1, f, ancho)
        if len(lineas) <= 4:
            break
    fe = ImageFont.truetype(R("recursos", "og", "outfit-400.ttf"), 30)
    fm = ImageFont.truetype(R("recursos", "og", "outfit-600.ttf"), 30)
    x, y = 72, 70
    d.rounded_rectangle((x, y + 6, x + 14, y + 20), 3, fill=OG["acento"])
    d.text((x + 28, y), etiqueta, font=fe, fill=OG["gris"])
    alto = tam * 1.08
    y0 = (H - alto * len(lineas)) / 2 + 10
    for i, l in enumerate(lineas):
        d.text((x, y0 + i * alto), l, font=f, fill=OG["texto"])
    d.text((x, H - 100), N["nombre"], font=fm, fill=OG["texto"])
    d.text((x, H - 62), f"{N['telefono']} · {N['localidad']}", font=fe, fill=OG["gris"])
    im.convert("RGB").save(destino, "JPEG", quality=86, optimize=True, progressive=True)


def og_todas():
    """Una por página indexable (la de la home también es /og-image.jpg, la del schema)."""
    import datos
    from config import TEXTOS
    os.makedirs(S("og"), exist_ok=True)
    n = 0
    for p in datos.todas():
        nombre = "inicio" if p["url"] == "/" else p["url"].strip("/").replace("/", "-")
        etq = p.get("etiqueta") or ("Agencia SEO · " + N["localidad"])
        og_imagen(p["h1"], S("og", f"{nombre}.jpg"), etq)
        n += 1
    for url, tit in [("/aviso-legal/", "Aviso legal"), ("/politica-de-privacidad/", "Política de privacidad"),
                     ("/politica-de-cookies/", "Política de cookies")]:
        og_imagen(tit, S("og", url.strip("/") + ".jpg"), N["nombre"]); n += 1
    shutil.copy(S("og", "inicio.jpg"), S("og-image.jpg"))
    return n


HTACCESS = r"""# __NOMBRE__ · servidor Apache (hosting Plesk del cliente)
Options -Indexes
DirectoryIndex index.html
AddType font/woff2 .woff2
AddType application/manifest+json .webmanifest
AddCharset utf-8 .txt

# Nada de copias, volcados ni registros a la vista
<FilesMatch "\.(zip|sql|bak|old|log|sh|ini|env|git.*|md|py|csv)$">
  Require all denied
</FilesMatch>
ErrorDocument 404 /404.html
ErrorDocument 410 /404.html

<IfModule mod_rewrite.c>
RewriteEngine On
# ORDEN (paso 26): primero las reglas de ruta, con destino ABSOLUTO (https y sin www), y después las de host.
# Así http://www.…/servicios/seo-local llega en UN salto a __DOMINIO__/seo-local/, nunca en cadena.

# 1 · Redirecciones del cambio de web (nuria2/arquitectura.md §c.1)
__REDIRECCIONES__
# 2 · Temporales (302): URLs reservadas que volverán a servir 200 (el día que exista /trabajos/, se quitan)
__REDIRECCIONES_302__
# 3 · 410: ya no existen y no vuelven (restos de WordPress, adjuntos, categorías, error-404 y cookies viejas)
RewriteRule ^(wp-admin|wp-content|wp-includes|wp-json)(/.*)?$ - [G,L]
RewriteRule ^(wp-login\.php|xmlrpc\.php|wp-cron\.php|feed/?|comments/feed/?)$ - [G,L]
RewriteRule ^(author|category|tag|page)(/.*)?$ - [G,L]
RewriteCond %{QUERY_STRING} (^|&)(p|page_id|attachment_id|cat|author)=[0-9]+ [NC]
RewriteRule ^(index\.php)?$ - [G,L]
__GONE__
# 4 · Sitemaps viejos de WordPress / Yoast / Rank Math → el nuevo
RewriteRule ^(sitemap_index\.xml|wp-sitemap\.xml|[a-z0-9_-]+-sitemap[0-9]*\.xml)$ __DOMINIO__/sitemap.xml [L,R=301]
# 5 · Barra final en las URLs de carpeta (absoluta: arregla también host y https en el mismo salto)
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_URI} !(\.[a-z0-9]{2,5})$ [NC]
RewriteCond %{REQUEST_URI} !/$
RewriteRule ^(.*)$ __DOMINIO__/$1/ [L,R=301]
# 6 · Host: sin www (paso 18)
RewriteCond %{HTTP_HOST} ^www\. [NC]
RewriteRule ^ __DOMINIO__%{REQUEST_URI} [L,R=301]
# 7 · A https. Solo si ni Apache ni el proxy de Plesk (nginx delante) dicen que ya es https:
# así no entra en bucle detrás de un proxy (lo que tiró la web de Marcos).
RewriteCond %{HTTPS} off
RewriteCond %{HTTP:X-Forwarded-Proto} !https [NC]
RewriteCond %{HTTP:X-Forwarded-SSL} !on [NC]
RewriteRule ^ __DOMINIO__%{REQUEST_URI} [L,R=301]
</IfModule>

<IfModule mod_deflate.c>
AddOutputFilterByType DEFLATE text/html text/css application/javascript image/svg+xml application/json text/xml application/xml
</IfModule>

<IfModule mod_expires.c>
ExpiresActive On
ExpiresByType text/html "access plus 0 seconds"
ExpiresByType text/css "access plus 1 year"
ExpiresByType application/javascript "access plus 1 year"
ExpiresByType image/jpeg "access plus 1 year"
ExpiresByType image/webp "access plus 1 year"
ExpiresByType image/svg+xml "access plus 1 year"
ExpiresByType font/woff2 "access plus 1 year"
ExpiresByType image/png "access plus 1 year"
ExpiresByType image/x-icon "access plus 1 year"
ExpiresByType image/vnd.microsoft.icon "access plus 1 year"
ExpiresByType application/manifest+json "access plus 1 week"
ExpiresByType application/json "access plus 0 seconds"
ExpiresByType application/xml "access plus 1 hour"
ExpiresByType text/xml "access plus 1 hour"
</IfModule>

<IfModule mod_headers.c>
Header always set X-Content-Type-Options "nosniff"
Header always set Referrer-Policy "strict-origin-when-cross-origin"
Header always set X-Frame-Options "SAMEORIGIN"
</IfModule>
"""

ENVIAR = r"""<?php
/* __NOMBRE__ · formularios de la web: «Que me llaman» (tarjeta de la portada) y contacto.
   Antispam: trampa + tiempo en la página + sin enlaces en el mensaje. Sin captcha. El mensaje es opcional.
   «t» lo rellena main.js al enviar: milisegundos que lleva la página abierta (performance.now()),
   así no depende del reloj del servidor ni del del móvil. Válido entre 3 s y 24 h. */
header('X-Robots-Tag: noindex');
if ($_SERVER['REQUEST_METHOD'] !== 'POST') { header('Location: __CONTACTO__'); exit; }
$c = function ($k, $max) { return trim(mb_substr(strip_tags($_POST[$k] ?? ''), 0, $max)); };
$tipo = ($_POST['tipo'] ?? '') === 'llamada' ? 'llamada' : 'contacto';
$pagina = $c('pagina', 120);
if (!preg_match('#^/[a-z0-9\-/]*$#', $pagina) || strpos($pagina, '//') !== false) { $pagina = '/'; }
$nombre = $c('nombre', 80); $telefono = $c('telefono', 20); $municipio = $c('municipio', 60); $mensaje = $c('mensaje', 2000);
$trampa = $_POST['web'] ?? ''; $t = (int)($_POST['t'] ?? 0);
$motivo = '';
if ($trampa !== '') { $motivo = 'trampa'; }
elseif ($t < 3000 || $t > 86400000) { $motivo = 'tiempo'; }
elseif ($nombre === '' || !preg_match('/^[0-9 +()\-]{9,20}$/', $telefono)) { $motivo = 'datos'; }
elseif (preg_match_all('#https?://#i', $mensaje) > 0) { $motivo = 'enlaces'; }
$ok = $motivo === '';
if ($tipo === 'llamada') { $vuelta = $pagina; $clave = 'llamada'; $ancla = '#te-llamamos'; $ancla_ko = '#te-llamamos'; }
else { $vuelta = '__CONTACTO__'; $clave = 'enviado'; $ancla = '#form-ok'; $ancla_ko = '#form-error'; }
if (!$ok) { header('Location: ' . $vuelta . '?' . $clave . '=0&motivo=' . $motivo . $ancla_ko); exit; }
$para = '__EMAIL__';
if ($tipo === 'llamada') {
  $asunto = '=?UTF-8?B?' . base64_encode('QUE ME LLAMEN · ' . $nombre . ' · ' . $telefono) . '?=';
  $cuerpo = "Petición de llamada desde la web.\n\nNombre: $nombre\nTeléfono: $telefono\nPágina: __DOMINIO__$pagina\n";
} else {
  $asunto = '=?UTF-8?B?' . base64_encode('Web __NOMBRE__: ' . $nombre . ($municipio ? ' (' . $municipio . ')' : '')) . '?=';
  $cuerpo = "Nombre: $nombre\nTeléfono: $telefono\nMunicipio: $municipio\n\n$mensaje\n\n-- Enviado desde __HOST____CONTACTO__";
}
$cab = "From: Web __NOMBRE__ <web@__HOST_SIN_WWW__>\r\nContent-Type: text/plain; charset=UTF-8\r\n";
$enviado = @mail($para, $asunto, $cuerpo, $cab);
header('Location: ' . $vuelta . '?' . $clave . '=' . ($enviado ? '1' . $ancla : '0&motivo=envio' . $ancla_ko));
"""


def _ruta_re(a):
    """Ruta vieja → patrón de RewriteRule que casa con y sin barra final (solo se escapan los caracteres de regex)."""
    return "^" + re.sub(r"([.+*?()\[\]{}|^$\\])", r"\\\1", a.strip("/")) + "/?$"


def servidor():
    host = DOMINIO.split("//")[1]
    red = "\n".join(f"RewriteRule {_ruta_re(a)} {DOMINIO}{b} [L,R=301]" for a, b in REDIRECCIONES) or "# (ninguna)"
    red2 = "\n".join(f"RewriteRule {_ruta_re(a)} {DOMINIO}{b} [L,R=302]" for a, b in REDIRECCIONES_302) or "# (ninguna)"
    gone = "\n".join([f"RewriteRule {_ruta_re(a)} - [G,L]" for a in GONE_410] + [f"RewriteRule {p} - [G,L]" for p in GONE_410_PATRONES])
    sust = {"__NOMBRE__": N["nombre"], "__HOST_SIN_WWW__": host.removeprefix("www."),
            "__HOST__": host, "__CONTACTO__": URLS["contacto"], "__REDIRECCIONES_302__": red2, "__REDIRECCIONES__": red,
            "__GONE__": gone or "# (ninguna)", "__EMAIL__": N["email"], "__DOMINIO__": DOMINIO}
    h, e = HTACCESS, ENVIAR
    for k, v in sust.items():
        h, e = h.replace(k, v), e.replace(k, v)
    if host.startswith("www."):  # dominio con www: se fuerza el www en lugar de quitarlo
        h = h.replace("# 6 · Host: sin www (paso 18)\nRewriteCond %{HTTP_HOST} ^www\\. [NC]", "# 6 · Host: con www (paso 18)\nRewriteCond %{HTTP_HOST} !^www\\. [NC]")
    open(S(".htaccess"), "w").write(h)
    open(S("enviar.php"), "w").write(e)
    # Vista previa (Vercel): noindex en TODO lo que sirve Vercel. vercel.json solo lo lee Vercel; en el hosting
    # de producción (Apache) no hace nada, así que producción nunca lleva el noindex (regla 10).
    open(S("vercel.json"), "w").write(json.dumps({
        "cleanUrls": False, "trailingSlash": True,
        "headers": [{"source": "/(.*)", "headers": [{"key": "X-Robots-Tag", "value": "noindex, nofollow"}]}]}, indent=1))


DIAS_N = {"Sunday": 0, "Monday": 1, "Tuesday": 2, "Wednesday": 3, "Thursday": 4, "Friday": 5, "Saturday": 6}


def js():
    """main.js del cliente con sus datos (horario, festivos, dominio, clave de cookies, textos del estado)."""
    N_ = N
    hosts = "|".join(re.escape(h) for h in HOST_PRODUCCION).replace("\\", "\\\\")
    sust = {"__HOSTS_RE__": hosts, "__COOKIES__": COOKIES_CLAVE, "__TZ__": N_["zona_horaria"],
            "__FESTIVOS__": json.dumps(N_["festivos"]), "__PASCUA__": json.dumps(N_.get("festivos_pascua", [])),
            "__DIAS_N__": json.dumps([DIAS_N[d] for d in N_["dias_schema"]]),
            "__ABRE_H__": str(int(N_["abre"][:2])), "__CIERRA_H__": str(int(N_["cierra"][:2])),
            "__ESTADO_ABIERTO__": json.dumps(texto("estado_abierto"), ensure_ascii=False),
            "__ESTADO_FUERA__": json.dumps(texto("estado_fuera"), ensure_ascii=False),
            "__PROMESA_ABIERTO__": json.dumps(texto("promesa_abierto"), ensure_ascii=False),
            "__PROMESA_ANTES__": json.dumps(texto("promesa_antes"), ensure_ascii=False),
            "__PROMESA_SIGUIENTE__": json.dumps(texto("promesa_siguiente", dia="{dia}"), ensure_ascii=False)}
    j = open(R("cliente", "js", "main.js"), encoding="utf-8").read()
    for k, v in sust.items():
        j = j.replace(k, v)
    faltan = re.findall(r"__[A-Z_]+__", j)
    if faltan:
        sys.exit(f"main.js: marcadores sin rellenar {faltan}")
    open(S("js", "main.js"), "w", encoding="utf-8").write(j)


def main():
    copiar()
    n = imagenes()
    no = objetos()
    k = css()
    servidor()
    o = og_todas()
    print(f"rematar: {n} fotos × 4 variantes · {no} objetos 3D × 3 · {o} imágenes para redes · estilo.css {k/1024:.1f} KB · v{VERSION}")


if __name__ == "__main__":
    if sys.argv[1:] == ["rapido"]:   # solo CSS y JS (para iterar el diseño; la entrega siempre con el rematar completo)
        copiar(); servidor(); shutil.copy(S("og", "inicio.jpg"), S("og-image.jpg"))
        print(f"rematar rápido (sin regenerar imágenes ni imágenes para redes): estilo.css {css()/1024:.1f} KB")
    else:
        main()
