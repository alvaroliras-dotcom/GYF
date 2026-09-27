# -*- coding: utf-8 -*-
"""Control a máquina en el navegador (paso 29) · autónomo: sirve sitio/ con http.server en un hilo del mismo
proceso (los servidores en segundo plano mueren en la sesión) y lanza Chromium con Playwright para Python.
Uso (desde la raíz del repositorio):  python3 herramientas/control29.py [--salida capturas/v1] [--anchos 390,768,1024,1280,1440] / /seo-local/ …
Comprueba por página y ancho: desborde horizontal, errores de JS, primera pantalla y página entera, texto que se
queda invisible tras recorrer la página, y en móvil el aviso de cookies en la PRIMERA visita (no puede tapar el
botón de llamar). Además, una vez: menú a pantalla completa y la vuelta de los formularios (éxito y error)."""
import argparse, functools, http.server, os, re, socketserver, threading
from playwright.sync_api import sync_playwright

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser()
ap.add_argument("rutas", nargs="*", default=["/", "/seo-local/", "/agencia-seo-getafe/", "/contacto/", "/quienes-somos/"])
ap.add_argument("--salida", default=os.path.join(RAIZ, "capturas"))
ap.add_argument("--anchos", default="390,768,1024,1280,1440")
ap.add_argument("--puerto", type=int, default=8765)
ap.add_argument("--sin-entera", action="store_true")
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
problemas = []

INVISIBLE = """() => { const r = [];
  document.querySelectorAll('main p, main h1, main h2, main h3, main li, footer p').forEach(e => {
    const s = getComputedStyle(e), b = e.getBoundingClientRect();
    if (!e.textContent.trim() || b.width === 0 || e.closest('[hidden],details:not([open]),.cookies,.menu,.sr,.trampa,[aria-hidden=true]')) return;
    if (parseFloat(s.opacity) < 0.05 || s.visibility === 'hidden') r.push(e.tagName + ': ' + e.textContent.trim().slice(0, 50));
  }); return r.slice(0, 8); }"""

SOLAPE = """() => { const c = document.querySelector('#cookies'); if (!c || getComputedStyle(c).display === 'none' || !c.getBoundingClientRect().height) return 'sin aviso';
  const rc = c.getBoundingClientRect(); const tapados = [];
  document.querySelectorAll('a.btn.tel, .barra-movil a, .cab__circulo').forEach(e => { const r = e.getBoundingClientRect();
    if (!r.width || r.bottom < 0 || r.top > innerHeight || getComputedStyle(e).visibility === 'hidden') return;
    const x = Math.min(r.right, rc.right) - Math.max(r.left, rc.left), y = Math.min(r.bottom, rc.bottom) - Math.max(r.top, rc.top);
    if (x > 4 && y > 4) tapados.push((e.textContent.trim() || e.getAttribute('aria-label') || '').slice(0, 30)); });
  const visibles = [...document.querySelectorAll('a.btn.tel, .barra-movil a, .cab__circulo')].filter(e => { const r = e.getBoundingClientRect();
    return r.width && r.top >= 0 && r.bottom <= innerHeight; }).length;
  return JSON.stringify({aviso: [Math.round(rc.top), Math.round(rc.bottom)], tapados, llamadas_visibles: visibles}); }"""

with sync_playwright() as p:
    b = p.chromium.launch(args=["--use-gl=swiftshader", "--enable-webgl", "--ignore-gpu-blocklist"])
    for ruta in a.rutas:
        nombre = ruta.strip("/").replace("/", "_") or "home"
        for w in [int(x) for x in a.anchos.split(",")]:
            movil = w < 900
            ctx = b.new_context(viewport={"width": w, "height": ALTO.get(w, 900)}, device_scale_factor=1, is_mobile=movil, has_touch=movil)
            pg = ctx.new_page(); errores = []
            pg.on("pageerror", lambda e: errores.append(str(e)))
            pg.on("console", lambda m: errores.append(m.text) if m.type == "error" and "maps.google" not in m.text
                  and "google.com" not in m.text and "net::ERR" not in m.text else None)
            # 1 · Primera visita, sin decidir las cookies: el aviso no tapa la llamada (móvil)
            pg.goto(BASE + ruta, wait_until="load"); pg.wait_for_timeout(2500)
            if movil:
                pg.screenshot(path=f"{a.salida}/{nombre}-{w}-primera-visita.png")
                sol = pg.evaluate(SOLAPE)
                if '"tapados": []' not in sol.replace('"tapados":[]', '"tapados": []') and sol != "sin aviso":
                    problemas.append(f"{ruta} @{w}: el aviso de cookies tapa {sol}")
                print(f"{ruta} @{w}: cookies {sol}")
            # 2 · Con las cookies decididas: primera pantalla y página entera
            pg.evaluate(f"try{{localStorage.setItem('{clave}','no')}}catch(e){{}}")
            pg.reload(wait_until="load"); pg.wait_for_timeout(3000)
            pg.screenshot(path=f"{a.salida}/{nombre}-{w}.png")
            alto = pg.evaluate("document.documentElement.scrollHeight")
            for y in range(0, alto, 400):
                pg.evaluate(f"window.scrollTo(0,{y})"); pg.wait_for_timeout(70)
            pg.wait_for_timeout(900)
            inv = pg.evaluate(INVISIBLE)
            pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(700)
            if not a.sin_entera:
                pg.screenshot(path=f"{a.salida}/{nombre}-{w}-entera.png", full_page=True)
            desb = pg.evaluate("""() => { const W = document.documentElement.clientWidth; const r = [];
                document.querySelectorAll('body *').forEach(e => { const b = e.getBoundingClientRect();
                  if (b.right > W + 1 && b.width > 0 && !e.closest('.cinta,.galeria,.op-lista,.menu,[aria-hidden=true],.cursor-foto,.sr,.fotohueco')) r.push(e.className || e.tagName); });
                return {pagina: document.documentElement.scrollWidth > W, piezas: [...new Set(r)].slice(0, 6)}; }""")
            linea = f"{ruta} @{w}: desborde {'SÍ' if desb['pagina'] else 'no'}{(' ' + str(desb['piezas'])) if desb['piezas'] else ''} · invisibles {inv or 'ninguno'} · JS {'; '.join(errores) or 'sin errores'}"
            print(linea)
            if desb["pagina"] or desb["piezas"] or inv or errores:
                problemas.append(linea)
            ctx.close()
    # 3 · Menú y vuelta de los formularios (una vez, en móvil y en ordenador)
    for w in (390, 1440):
        ctx = b.new_context(viewport={"width": w, "height": ALTO[w]}, is_mobile=w < 900, has_touch=w < 900)
        ctx.add_init_script(f"try{{localStorage.setItem('{clave}','no')}}catch(e){{}}")
        pg = ctx.new_page()
        pg.goto(BASE + "/", wait_until="load"); pg.wait_for_timeout(1500)
        pg.click(".cab__burger"); pg.wait_for_timeout(1200)
        pg.screenshot(path=f"{a.salida}/menu-{w}.png")
        abierto = pg.evaluate("document.querySelector('#menu').getAttribute('aria-hidden')")
        print(f"menú @{w}: aria-hidden={abierto}")
        if abierto != "false":
            problemas.append(f"menú @{w}: no se abre")
        for url, sel_ok, sel_form in [("/seo-local/?llamada=1#te-llamamos", "[data-llamada-ok]", ".llamada__form input[name=nombre]"),
                                      ("/seo-local/?llamada=0&motivo=datos#te-llamamos", "[data-llamada-error]", None),
                                      ("/contacto/?enviado=1#form-ok", "#form-ok", ".formulario input[name=nombre]"),
                                      ("/contacto/?enviado=0&motivo=envio#form-error", "#form-error", None)]:
            pg.goto(BASE + url, wait_until="load"); pg.wait_for_timeout(1200)
            vis = pg.evaluate(f"(() => {{ const e = document.querySelector('{sel_ok}'); return !!e && !e.hidden && e.getBoundingClientRect().height > 0; }})()")
            form = pg.evaluate(f"(() => {{ const e = document.querySelector('{sel_form}'); return !!e && !e.hidden && e.getBoundingClientRect().height > 0; }})()") if sel_form else None
            nom = re.sub(r"[^a-z0-9]+", "-", url)[1:40]
            pg.screenshot(path=f"{a.salida}/vuelta-{nom}-{w}.png")
            print(f"vuelta {url} @{w}: aviso visible={vis}" + (f" · formulario a la vista={form}" if sel_form else ""))
            if not vis or form:
                problemas.append(f"vuelta {url} @{w}: aviso visible={vis}, formulario a la vista={form}")
        ctx.close()
    b.close()
srv.shutdown()
print("\nPROBLEMAS:", len(problemas))
for x in problemas:
    print("  ·", x)
