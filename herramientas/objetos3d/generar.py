# -*- coding: utf-8 -*-
"""GYF · Genera la familia de objetos 3D de la marca (v2).
Uso (desde la raíz del repositorio):  python3 herramientas/objetos3d/generar.py [nombre ...]
1. Compila escultor.js con esbuild (three de node_modules, enlazado desde simbolo3d/).
2. Pinta cada pieza del CATÁLOGO en Chromium sin cabeza (SwiftShader: no hace falta GPU) a 2.400 px.
3. Recorta al contenido, deja un 7 % de margen y guarda el máster PNG con alfa a 1.600 px en
   herramientas/objetos3d/master/ (de ahí lo lee rematar.py).
Las versiones web (WebP con alfa 400/800/1200) y las de tarjeta de color las hace rematar.py."""
import base64, io, os, subprocess, sys, time
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
MASTER = os.path.join(AQUI, "master")

# nombre: forma, materiales, giro (x, y, z en radianes), resolución de la malla
CATALOGO = {
    # --- v3 · El símbolo G+F manda: familia de 12 (poses, cortes y materiales distintos) ---
    "simbolo-fucsia":        dict(forma="simbolo", mats=["fucsia"], giro=[-.16, -.5, -.06]),
    "simbolo-cromo":         dict(forma="simbolo", mats=["cromo"], giro=[-.18, .5, .06]),
    "simbolo-berenjena":     dict(forma="simbolo", mats=["berenjena"], giro=[.12, -.55, -.08]),
    "simbolo-fucsia-perfil": dict(forma="simbolo", mats=["fucsia"], giro=[-.25, 1.05, .12]),
    "simbolo-crema":         dict(forma="simbolo", mats=["crema-mate"], giro=[.3, .35, .22]),
    "simbolo-cristal":       dict(forma="simbolo", mats=["cristal-fucsia"], giro=[-.1, -.3, -.15]),
    "simbolo-bicolor":       dict(forma="simbolo", mats=["berenjena", "fucsia"], giro=[-1.0, .25, .35]),
    "simbolo-despiece":      dict(forma="simbolo", mats=["fucsia", "cromo"], giro=[-.12, .45, 0],
                                  despiece=[[-.28, -.2, .45, 0, -.25, -.12], [.3, .22, -.4, 0, .3, .1]]),
    "simbolo-despiece-crema": dict(forma="simbolo", mats=["crema-mate", "fucsia"], giro=[.18, -.6, .1],
                                  despiece=[[-.55, -.1, .35, .25, .45, .2], [.4, .12, -.3, -.15, -.25, -.18]]),
    "simbolo-cerca":         dict(forma="simbolo", mats=["fucsia"], giro=[-.35, .7, .3], cerca=True, zoom=.46),
    "simbolo-cerca-cromo":   dict(forma="simbolo", mats=["cromo"], giro=[.25, -.8, -.25], cerca=True, zoom=.5),
    "simbolos-grupo":        dict(forma="grupo", giro=[0, 0, 0], grupo=[
                                  [0, 0, 0, 1, -.15, .45, 0, "fucsia"], [1.5, .95, -.6, .5, .4, -.7, .3, "cromo"],
                                  [-1.35, -.9, .3, .55, -.3, .9, -.4, "berenjena"], [1.2, -1.05, .5, .42, .2, .2, .6, "crema-mate"],
                                  [-1.2, 1.15, -.4, .38, .5, -.4, -.3, "cromo", "fucsia"]]),
    # --- Objetos del oficio (se quedan donde refuerzan la tarjeta) ---
    "chincheta":          dict(forma="chincheta", mats=["fucsia"], giro=[-.12, .5, .08]),
    "estrella":           dict(forma="estrella", mats=["fucsia"], giro=[-.2, .45, -.12]),
    "estrella-cromo":     dict(forma="estrella", mats=["cromo"], giro=[.25, -.5, .2]),
    "lupa":               dict(forma="lupa", mats=["cromo", "fucsia"], giro=[-.2, .55, 0]),
    "cursor":             dict(forma="cursor", mats=["fucsia"], giro=[-.25, .55, .15]),
    "bocadillo":          dict(forma="bocadillo", mats=["crema", "fucsia"], giro=[-.15, .45, .05]),
    "barras":             dict(forma="barras", giro=[-.28, .62, 0]),
    "abanico":            dict(forma="abanico", giro=[-.2, .4, .1]),
}
# Retirados en la v3 (abstractos sin significado): jaula, nudo, cinta, anillos, píldoras, esferas, giroide.
# Las formas siguen en escultor.js por si hacen falta en otra web.


def compilar():
    out = os.path.join(AQUI, "escultor.bundle.js")
    fuentes = [os.path.join(AQUI, f) for f in ("escultor.js", "estudio.js")]
    if os.path.exists(out) and os.path.getmtime(out) > max(os.path.getmtime(f) for f in fuentes):
        return out
    subprocess.run(["npx", "--yes", "esbuild", "escultor.js", "--bundle", "--format=iife", "--global-name=Escultor",
                    "--target=es2020", "--outfile=escultor.bundle.js", "--log-level=warning"], cwd=AQUI, check=True)
    return out


def recortar(im, margen=.07, lado=1600):
    """Recorta al contenido (alfa > 6) y centra en un cuadrado con margen."""
    a = im.split()[-1].point(lambda v: 255 if v > 6 else 0)
    bb = a.getbbox()
    im = im.crop(bb)
    w, h = im.size
    L = round(max(w, h) * (1 + 2 * margen))
    c = Image.new("RGBA", (L, L), (0, 0, 0, 0))
    c.alpha_composite(im, ((L - w) // 2, (L - h) // 2))
    return c.resize((lado, lado), Image.LANCZOS)


def main(nombres):
    from playwright.sync_api import sync_playwright
    os.makedirs(MASTER, exist_ok=True)
    js = compilar()
    svg = open(os.path.join(RAIZ, "recursos", "marca", "simbolo-3d.svg"), encoding="utf-8").read()
    with sync_playwright() as p:
        b = p.chromium.launch(args=["--use-gl=swiftshader", "--enable-webgl", "--ignore-gpu-blocklist"])
        pg = b.new_page(viewport={"width": 600, "height": 600})
        pg.set_content("<html><body style='margin:0;background:transparent'></body></html>")
        pg.add_script_tag(path=js)
        for n in nombres:
            cfg = dict(CATALOGO[n]); cfg.setdefault("res", 170)
            t0 = time.time()
            url = pg.evaluate("async (c) => await Escultor.render(c)", {**cfg, "svg": svg, "tam": 2400})
            im = Image.open(io.BytesIO(base64.b64decode(url.split(",", 1)[1]))).convert("RGBA")
            m = im.resize((1600, 1600), Image.LANCZOS) if cfg.get("cerca") else recortar(im)
            m.save(os.path.join(MASTER, f"{n}.png"), optimize=True)
            print(f"{n}: {time.time() - t0:.1f} s")
        b.close()


if __name__ == "__main__":
    main(sys.argv[1:] or list(CATALOGO))
