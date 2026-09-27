# -*- coding: utf-8 -*-
"""Capturas de control (paso 29) con Playwright para Python: primera pantalla y página entera a 390, 1.024 y
1.440 px, desborde horizontal y errores de consola. Lanza Chromium con SwiftShader (WebGL sin GPU).
Uso (desde la raíz, con la web servida por servir.sh):
  python3 herramientas/capturas.py [--base http://localhost:8765] [--salida capturas] [--anchos 390,1024,1440] / /contacto/ …
Antes de la página entera recorre la página para que salten las apariciones y los contadores."""
import argparse, os, re, sys
from playwright.sync_api import sync_playwright

ap = argparse.ArgumentParser()
ap.add_argument("rutas", nargs="*", default=["/"])
ap.add_argument("--base", default="http://localhost:8765")
ap.add_argument("--salida", default="capturas")
ap.add_argument("--anchos", default="390,1024,1440")
ap.add_argument("--solo-primera", action="store_true")
a = ap.parse_args()
os.makedirs(a.salida, exist_ok=True)
try:
    clave = re.search(r'COOKIES_CLAVE\s*=\s*"([^"]+)"', open("generador/config.py", encoding="utf-8").read()).group(1)
except Exception:
    clave = "cookies"
ALTO = {390: 844, 768: 1024, 1024: 768, 1280: 800, 1440: 900}
with sync_playwright() as p:
    b = p.chromium.launch(args=["--use-gl=swiftshader", "--enable-webgl", "--ignore-gpu-blocklist"])
    for ruta in a.rutas:
        nombre = ruta.strip("/").replace("/", "_") or "home"
        for w in [int(x) for x in a.anchos.split(",")]:
            movil = w < 900
            ctx = b.new_context(viewport={"width": w, "height": ALTO.get(w, 900)}, device_scale_factor=1,
                                is_mobile=movil, has_touch=movil)
            ctx.add_init_script(f"try{{localStorage.setItem('{clave}','no')}}catch(e){{}}")
            pg = ctx.new_page(); errores = []
            pg.on("pageerror", lambda e: errores.append(str(e)))
            pg.on("console", lambda m: errores.append(m.text) if m.type == "error" and "maps.google" not in m.text and "net::" not in m.text else None)
            pg.goto(a.base + ruta, wait_until="load"); pg.wait_for_timeout(4000)
            pg.screenshot(path=f"{a.salida}/{nombre}-{w}.png")
            if not a.solo_primera:
                alto = pg.evaluate("document.documentElement.scrollHeight")
                for y in range(0, alto, 500):
                    pg.evaluate(f"window.scrollTo(0,{y})"); pg.wait_for_timeout(90)
                pg.wait_for_timeout(600)
                pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(700)
                pg.screenshot(path=f"{a.salida}/{nombre}-{w}-entera.png", full_page=True)
            desb = pg.evaluate("document.documentElement.scrollWidth") > w
            print(f"{ruta} @{w}: desborde {'SÍ' if desb else 'no'} · errores JS: {'; '.join(errores) or 'ninguno'}")
            ctx.close()
    b.close()
