# -*- coding: utf-8 -*-
"""Capturas de la v2: página entera a 1.440 y 390 (y los anchos que se pidan) tras recorrerla despacio, para que
salten las apariciones, los titulares y los contadores. Sirve sitio/ en un hilo del mismo proceso.
Uso:  python3 herramientas/capturas_v2.py --salida ../08-WEB/capturas-v2 / /seo-local/ /agencia-seo-getafe/ /contacto/
Informa de errores de JS y de desborde horizontal."""
import argparse, functools, http.server, os, re, socketserver, threading, time
from playwright.sync_api import sync_playwright

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser()
ap.add_argument("rutas", nargs="*", default=["/", "/seo-local/", "/agencia-seo-getafe/", "/contacto/"])
ap.add_argument("--salida", default=os.path.join(RAIZ, "capturas", "v2"))
ap.add_argument("--anchos", default="1440,390")
ap.add_argument("--puerto", type=int, default=8771)
ap.add_argument("--primera", action="store_true", help="también la primera pantalla")
ap.add_argument("--movimiento", action="store_true", help="con movimiento (por defecto, movimiento reducido: la página entera sale quieta y completa)")
a = ap.parse_args()
os.makedirs(a.salida, exist_ok=True)
clave = re.search(r'COOKIES_CLAVE\s*=\s*"([^"]+)"', open(os.path.join(RAIZ, "generador", "config.py"), encoding="utf-8").read()).group(1)


class Silencioso(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *x):
        pass


socketserver.TCPServer.allow_reuse_address = True
srv = socketserver.ThreadingTCPServer(("127.0.0.1", a.puerto), functools.partial(Silencioso, directory=os.path.join(RAIZ, "sitio")))
threading.Thread(target=srv.serve_forever, daemon=True).start()
BASE = f"http://127.0.0.1:{a.puerto}"
ALTO = {390: 844, 768: 1024, 1024: 768, 1280: 800, 1440: 900}

with sync_playwright() as p:
    b = p.chromium.launch(args=["--use-gl=swiftshader", "--enable-webgl", "--ignore-gpu-blocklist"])
    for ruta in a.rutas:
        nombre = ruta.strip("/").replace("/", "_") or "home"
        for w in [int(x) for x in a.anchos.split(",")]:
            movil = w < 900
            ctx = b.new_context(viewport={"width": w, "height": ALTO.get(w, 900)}, device_scale_factor=1, is_mobile=movil, has_touch=movil,
                                reduced_motion="no-preference" if a.movimiento else "reduce")
            ctx.add_init_script(f"try{{localStorage.setItem('{clave}','no')}}catch(e){{}}")
            pg = ctx.new_page(); errores = []
            pg.on("pageerror", lambda e: errores.append(str(e)))
            pg.goto(BASE + ruta, wait_until="load"); pg.wait_for_timeout(1400)
            if a.primera:
                pg.screenshot(path=os.path.join(a.salida, f"{nombre}-{w}.png"))
            alto = pg.evaluate("document.documentElement.scrollHeight")
            y = 0
            while y < alto:
                y += 380
                pg.evaluate(f"window.scrollTo(0,{y})"); pg.wait_for_timeout(90)
                alto = pg.evaluate("document.documentElement.scrollHeight")
            pg.wait_for_timeout(900)
            pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(700)
            ancho = pg.evaluate("document.documentElement.scrollWidth")
            pg.add_style_tag(content=".barra-movil,.subir{display:none!important}")   # fijos: en la página entera salen a mitad
            pg.screenshot(path=os.path.join(a.salida, f"{nombre}-{w}-entera.png"), full_page=True)
            print(f"{ruta} {w}: alto {alto} · desborde {'SÍ ' + str(ancho) if ancho > w else 'no'} · errores JS {errores or 'ninguno'}")
            ctx.close()
    b.close()
srv.shutdown()
