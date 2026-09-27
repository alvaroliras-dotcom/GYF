# -*- coding: utf-8 -*-
"""Tira de fotogramas del desplazamiento de la home (v2), CON movimiento: 12 (o N) pantallas a 1.440 × 900 tomadas
mientras se baja con la rueda, montadas en una hoja. Y, si se pide, un vídeo corto (MP4) con ffmpeg.
Uso:  python3 herramientas/tira_v2.py --salida ../08-WEB/capturas-v2 [--fotogramas 12] [--video]"""
import argparse, functools, http.server, os, re, socketserver, subprocess, threading
from PIL import Image, ImageDraw, ImageFont

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser()
ap.add_argument("--salida", default=os.path.join(RAIZ, "capturas", "v2"))
ap.add_argument("--ruta", default="/")
ap.add_argument("--fotogramas", type=int, default=12)
ap.add_argument("--video", action="store_true")
ap.add_argument("--ancho", type=int, default=1440)
ap.add_argument("--puerto", type=int, default=8772)
a = ap.parse_args()
os.makedirs(a.salida, exist_ok=True)
clave = re.search(r'COOKIES_CLAVE\s*=\s*"([^"]+)"', open(os.path.join(RAIZ, "generador", "config.py"), encoding="utf-8").read()).group(1)


class Silencioso(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *x):
        pass


socketserver.TCPServer.allow_reuse_address = True
srv = socketserver.ThreadingTCPServer(("127.0.0.1", a.puerto), functools.partial(Silencioso, directory=os.path.join(RAIZ, "sitio")))
threading.Thread(target=srv.serve_forever, daemon=True).start()
from playwright.sync_api import sync_playwright

movil = a.ancho < 900
alto_v = 844 if movil else 900
tmp = os.path.join(a.salida, "_fotogramas"); os.makedirs(tmp, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(args=["--use-gl=swiftshader", "--enable-webgl", "--ignore-gpu-blocklist"])
    ctx = b.new_context(viewport={"width": a.ancho, "height": alto_v}, is_mobile=movil, has_touch=movil,
                        record_video_dir=tmp if a.video else None, record_video_size={"width": a.ancho // 2, "height": alto_v // 2} if a.video else None)
    ctx.add_init_script(f"try{{localStorage.setItem('{clave}','no')}}catch(e){{}}")
    pg = ctx.new_page()
    pg.goto(f"http://127.0.0.1:{a.puerto}{a.ruta}", wait_until="commit")
    fotos = []
    pg.wait_for_selector("[data-cortina]", state="attached")
    pg.wait_for_timeout(120); pg.screenshot(path=os.path.join(tmp, "f00.png"), animations="allow"); fotos.append("f00.png")   # la cortinilla
    pg.wait_for_load_state("load"); pg.wait_for_timeout(2600)
    total = pg.evaluate("document.documentElement.scrollHeight") - alto_v
    n = a.fotogramas - 1
    pasos = 26                   # movimientos de rueda entre fotograma y fotograma
    for i in range(1, n + 1):
        destino = total * i / n
        y = pg.evaluate("scrollY")
        for k in range(pasos):
            pg.mouse.wheel(0, (destino - y) / pasos); pg.wait_for_timeout(45)
        pg.wait_for_timeout(1100)
        nombre = f"f{i:02d}.png"; pg.screenshot(path=os.path.join(tmp, nombre)); fotos.append(nombre)
    ctx.close(); b.close()
srv.shutdown()

# Hoja: 3 columnas, cada fotograma a 1/3 (480 × 300) con su número
cols = 3 if not movil else 6
w = 480 if not movil else 195
h = round(w * alto_v / a.ancho)
filas = (len(fotos) + cols - 1) // cols
hoja = Image.new("RGB", (cols * (w + 16) + 16, filas * (h + 44) + 16), "#1C1219")
d = ImageDraw.Draw(hoja)
try:
    f = ImageFont.truetype(os.path.join(RAIZ, "recursos", "og", "outfit-600.ttf"), 18)
except Exception:
    f = None
for i, n in enumerate(fotos):
    im = Image.open(os.path.join(tmp, n)).convert("RGB").resize((w, h), Image.LANCZOS)
    x, y = 16 + (i % cols) * (w + 16), 16 + (i // cols) * (h + 44)
    hoja.paste(im, (x, y + 28))
    d.text((x, y + 2), f"{i + 1:02d}" + (" · cortinilla de entrada" if i == 0 else ""), fill="#FF7AB8", font=f)
sal = os.path.join(a.salida, f"_TIRA-{'MOVIL' if movil else 'HOME'}-desplazamiento.jpg")
hoja.save(sal, quality=86)
print("tira:", sal, hoja.size)
if a.video:
    webm = [x for x in os.listdir(tmp) if x.endswith(".webm")]
    if webm:
        mp4 = os.path.join(a.salida, f"_VIDEO-{'MOVIL' if movil else 'HOME'}-desplazamiento.mp4")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", os.path.join(tmp, webm[0]), "-c:v", "libx264", "-pix_fmt", "yuv420p",
                        "-crf", "26", "-movflags", "+faststart", mp4], check=False)
        print("vídeo:", mp4)
