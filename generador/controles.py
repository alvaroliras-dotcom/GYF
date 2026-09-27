# -*- coding: utf-8 -*-
"""GYF-Rayo · Controles a máquina (fase 08) sobre sitio/. Uso: python3 generador/controles.py
Sale con código 1 si hay errores. Los avisos no bloquean."""
import csv, json, os, re, sys
from html.parser import HTMLParser

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import DOMINIO, NEGOCIO, LEGALES
SITIO = os.path.join(RAIZ, "sitio")
err, avi = [], []


class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.h1 = 0; s.links = []; s.imgs = []; s.title = ""; s._t = False; s.meta = {}; s.ld = []; s._ld = False; s.canon = None; s.ids = set()
    def handle_starttag(s, tag, a):
        a = dict(a)
        if "id" in a: s.ids.add(a["id"])
        if tag == "h1": s.h1 += 1
        if tag == "a" and a.get("href"): s.links.append(a["href"])
        if tag == "img": s.imgs.append(a)
        if tag == "title": s._t = True
        if tag == "meta" and a.get("name"): s.meta[a["name"]] = a.get("content", "")
        if tag == "link" and a.get("rel") == "canonical": s.canon = a.get("href")
        if tag == "script" and a.get("type") == "application/ld+json": s._ld = True
    def handle_endtag(s, tag):
        if tag == "title": s._t = False
        if tag == "script": s._ld = False
    def handle_data(s, d):
        if s._t: s.title += d
        if s._ld: s.ld.append(d)


paginas = {}
for r, _, fs in os.walk(SITIO):
    for f in fs:
        if f.endswith(".html"):
            ruta = os.path.join(r, f)
            url = "/" + os.path.relpath(ruta, SITIO).replace("index.html", "").replace(os.sep, "/")
            url = url if url.endswith("/") or url.endswith(".html") else url + "/"
            paginas[url] = ruta

existe = lambda u: u in paginas or os.path.exists(os.path.join(SITIO, u.lstrip("/").split("?")[0].split("#")[0]))
titulos, metas = {}, {}
for url, ruta in sorted(paginas.items()):
    h = open(ruta, encoding="utf-8").read()
    p = P(); p.feed(h)
    idx = "noindex" not in p.meta.get("robots", "")
    if p.h1 != 1: err.append(f"{url}: {p.h1} H1")
    if re.search(r"\[LINK|🔗|🆕|\]\(/", h): err.append(f"{url}: restos de markdown o marcas del contrato")
    for l in p.links:
        if l.startswith("/") and not existe(l.split("#")[0].split("?")[0] or "/"):
            err.append(f"{url}: enlace roto {l}")
        if l.startswith("/") and not l.endswith("/") and "." not in l.split("/")[-1] and "#" not in l and "?" not in l:
            avi.append(f"{url}: enlace sin barra final {l}")
    for im in p.imgs:
        if "alt" not in im: err.append(f"{url}: imagen sin alt {im.get('src')}")
        src = im.get("src", "")
        if src.startswith("/") and not existe(src.split("?")[0]): err.append(f"{url}: imagen que no existe {src}")
    for d in p.ld:
        try: json.loads(d)
        except Exception as e: err.append(f"{url}: JSON-LD inválido ({e})")
    if idx and url.endswith("/"):
        t, m = p.title.strip(), p.meta.get("description", "")
        if not 30 <= len(t) <= 65: avi.append(f"{url}: title de {len(t)} caracteres")
        if not 120 <= len(m) <= 160: avi.append(f"{url}: meta de {len(m)} caracteres")
        if p.canon != DOMINIO + url: err.append(f"{url}: canónica {p.canon}")
        titulos.setdefault(t, []).append(url); metas.setdefault(m, []).append(url)
    if f"tel:{NEGOCIO['telefono_e164']}" not in h: err.append(f"{url}: sin enlace de llamada")
    # Controles de texto (auditoría v6): notas de maqueta, subtítulos vacíos, enlaces que se pierden
    cuerpo = re.sub(r"<script.*?</script>|<style.*?</style>", "", h, flags=re.S)
    sin_op = re.sub(r'<ul class="op-lista".*?</ul>', "", cuerpo, flags=re.S)  # las reseñas reales no se tocan
    txt = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", sin_op))
    for pat, que in [(r"\((Formulario|Widget|Foto|Imagen|Mapa|Nota)\b", "nota de maqueta entre paréntesis"),
                     (r"\ben contacta con nosotros\b", "«en contacta con nosotros»"),
                     (r"[a-záéíóúñ,] Contacta con nosotros", "«Contacta» con mayúscula a mitad de frase"),
                     (r"a la hora que sea|24 ?h(oras)?\b(?! no)", "promesa de horario que no es verdad")]:
        if re.search(pat, txt) and not (que.startswith("promesa") and url in [u for _, u in LEGALES]) and not (que.startswith("promesa") and re.search(r"no (hacemos|atendemos|damos)[^.]{0,40}24", txt)):
            err.append(f"{url}: {que}")
    if re.search(r"<p><strong>[^<]{3,40}</strong></p>\s*<p><strong>[^<]{3,40}</strong></p>", cuerpo):
        err.append(f"{url}: dos subtítulos seguidos sin contenido")
    # Restos de Markdown: tablas sin convertir y citas «>» pegadas a un párrafo
    if "|---" in cuerpo or re.search(r"\|\s*:?-{3,}:?\s*\|", cuerpo):
        err.append(f"{url}: tabla de Markdown sin convertir (|---|)")
    if re.search(r"<p\b[^>]*>(?:(?!</p>).)*&gt;", cuerpo, flags=re.S):
        err.append(f"{url}: «&gt;» dentro de un párrafo (cita de Markdown sin convertir)")
    # Declaración de ~60 palabras (el resto de la entrada baja al primer bloque)
    for d in re.findall(r'<p class="declara__txt[^"]*">(.*?)</p>', cuerpo, flags=re.S):
        w = len(re.sub(r"<[^>]+>", " ", d).split())
        if w > 70: avi.append(f"{url}: declaración de {w} palabras (máximo ~60)")
    fotos_pag = re.findall(r'<img src="/img/([a-z0-9-]+)-1600\.jpg"', cuerpo.split('<footer')[0])
    rep = {x for x in fotos_pag if fotos_pag.count(x) > 1 and 'sitem__mini' not in cuerpo}
    if rep: avi.append(f"{url}: foto repetida en la página {sorted(rep)}")

for t, us in titulos.items():
    if len(us) > 1: err.append(f"title duplicado en {us}")
for m, us in metas.items():
    if len(us) > 1: err.append(f"meta duplicada en {us}")

# Contrato de enlaces (paso 23): cada enlace editorial previsto tiene que estar en su página
faltan = 0
ruta_c = os.path.join(RAIZ, "generador", "contrato_enlaces.csv")
if os.path.exists(ruta_c):
    for row in csv.DictReader(open(ruta_c, encoding="utf-8-sig"), delimiter=";"):
        o, d = row["origen"], row["destino"]
        if o in paginas and d.startswith("/"):
            if f'href="{d}"' not in open(paginas[o], encoding="utf-8").read():
                faltan += 1; avi.append(f"contrato: falta {o} → {d}")

# Sitemap
sm = open(os.path.join(SITIO, "sitemap.xml"), encoding="utf-8").read()
for u in re.findall(rf"<loc>{re.escape(DOMINIO)}([^<]+)</loc>", sm):
    if u not in paginas: err.append(f"sitemap: {u} no existe")

# Datos de ejemplo del tema que se hayan quedado sin cambiar
_r = json.load(open(os.path.join(RAIZ, "contenido", "resenas.json"), encoding="utf-8"))
if "_nota" in _r or not _r.get("opiniones"): avi.append("resenas.json: son los datos de EJEMPLO (sin reseñas reales)")
if any(o.get("marcador") for o in _r.get("opiniones", [])): avi.append("resenas.json: hay opiniones MARCADOR (sustituir por las reales de la ficha)")
from config import CASOS, OBJETO_PORTADA
_sin = [c[0] for c in CASOS if not c[2]]
if _sin: avi.append(f"CASOS sin captura real (sale el marcador de maqueta): {', '.join(_sin)}")
if not os.path.exists(os.path.join(SITIO, "img", OBJETO_PORTADA["imagen"].rsplit(".", 1)[0] + "-840.webp")): err.append("falta la imagen fija del objeto de portada")
for k, v in [("DOMINIO", DOMINIO), ("teléfono", NEGOCIO["telefono_e164"]), ("CID", NEGOCIO["cid"])]:
    if "ejemplo" in v or "600000000" in v or set(v) <= {"0"}: avi.append(f"config.py: {k} sigue siendo el de EJEMPLO")
# Paso 26 · noindex solo en la vista previa (vercel.json), nunca en producción (salvo la 404)
for url, ruta in paginas.items():
    h = open(ruta, encoding="utf-8").read()
    if url != "/404.html" and re.search(r'name="robots" content="[^"]*noindex', h):
        err.append(f"{url}: lleva noindex (en producción no puede)")
    m = re.search(r'property="og:image" content="([^"]+)"', h)
    if not m or not existe(m.group(1).replace(DOMINIO, "")):
        err.append(f"{url}: sin imagen para redes (og:image) o no existe")
vj = os.path.join(SITIO, "vercel.json")
if not os.path.exists(vj) or "noindex" not in open(vj).read():
    err.append("vercel.json: falta el noindex de la vista previa")
# Paso 26 · 301: todas las URLs viejas de la arquitectura están en el .htaccess, con destino que existe
from config import REDIRECCIONES, REDIRECCIONES_302
ht = open(os.path.join(SITIO, ".htaccess"), encoding="utf-8").read()
for a_, b_ in REDIRECCIONES + REDIRECCIONES_302:
    if not re.search(r"RewriteRule \^" + re.escape(a_).replace("\\-", "-").replace("/", "/") , ht.replace("\\-", "-")):
        err.append(f".htaccess: falta la redirección de /{a_}/")
    if b_ not in paginas:
        err.append(f".htaccess: /{a_}/ → {b_}, que no existe")
# El nombre del titular solo en los legales (la web es de la marca)
for url, ruta in paginas.items():
    if url in [u for _, u in LEGALES] or url == "/contacto/":
        continue
    if re.search(r"Liras|Torrente|53109681", open(ruta, encoding="utf-8").read()):
        err.append(f"{url}: nombra al titular fuera de los legales")
# Pendientes que dependen de Álvaro
if NEGOCIO.get("festivos_locales_pendientes"):
    avi.append("festivos: faltan los dos locales de Alcorcón (confirmar en el BOCM y añadirlos a NEGOCIO['festivos'])")
if any('data-marcador="logos"' in open(r, encoding="utf-8").read() for r in paginas.values()):
    avi.append("logos de clientes: sale el MARCADOR (faltan los logotipos en recursos/clientes/)")

print(f"Páginas HTML: {len(paginas)}")
print(f"ERRORES: {len(err)}"); [print("  ✗", e) for e in err[:80]]
print(f"AVISOS: {len(avi)}"); [print("  ·", a) for a in avi[:80]]
sys.exit(1 if err else 0)
