# -*- coding: utf-8 -*-
"""GYF · Versión en su color original de cada logotipo de cliente (v2), para el paso de gris a color al pasar el ratón.
Parte de /home/claude/gyf/logos-clientes/originales/ y deja en recursos/clientes-color/ un archivo con el MISMO nombre
que su versión gris de recursos/clientes/ (SVG con el viewBox ya recortado, o PNG de 120 px de alto recortado).
Los logotipos que solo existen a una tinta (Balgas, Marcos Cerrajeros…) pasan del gris a su tinta original.
Uso (desde la raíz):  python3 herramientas/logos_color.py"""
import os, re
from PIL import Image, ImageChops

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORIG = "/home/claude/gyf/logos-clientes/originales"
GRIS = os.path.join(RAIZ, "recursos", "clientes")
DEST = os.path.join(RAIZ, "recursos", "clientes-color")
ALTO = 120

# SVG: el gris tiene el viewBox recortado; se cambia el gris por la tinta o el color del original
SVG_TINTA = {"balgas.svg": "#161616", "marcos-cerrajeros.svg": "#161616", "solvento.svg": "#00747A", "asesoria-mayo.svg": "#1C1219"}
# PNG: archivo original y cómo quitarle el fondo
PNG = {"aquita.png": ("aquita__logo-aquita.png", "blanco"), "ele-room.png": ("ele-room__logo.png", None),
       "expertise.png": ("expertise__logo-grande-negro-expertise.png", None), "ines-ingenieros.png": ("ines-ingenieros__logoines.bmp", "blanco"),
       "las-tejas.png": ("las-tejas__logo-las-tejas-NEGRO.png", None), "psicorazon.png": ("psicorazon__logoblack.png", None),
       "vinos-gallegos-pousada.png": ("vinos-gallegos-pousada__logo_gallego.png", None)}


def sin_blanco(im):
    """Fondo blanco → transparente conservando el color (desmultiplica sobre blanco)."""
    im = im.convert("RGB")
    px = im.load(); w, h = im.size
    out = Image.new("RGBA", im.size)
    po = out.load()
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            a = 255 - min(r, g, b)
            if a < 8:
                po[x, y] = (0, 0, 0, 0); continue
            k = 255 / a
            po[x, y] = (max(0, min(255, round(255 - (255 - r) * k))), max(0, min(255, round(255 - (255 - g) * k))),
                        max(0, min(255, round(255 - (255 - b) * k))), a)
    return out


def recorta_y_escala(im):
    bb = im.split()[-1].point(lambda v: 255 if v > 10 else 0).getbbox()
    im = im.crop(bb)
    return im.resize((max(1, round(im.width * ALTO / im.height)), ALTO), Image.LANCZOS)


def jif():
    """JIF 2026: el SVG original a color, pintado con Chromium y recortado."""
    from playwright.sync_api import sync_playwright
    svg = open(os.path.join(ORIG, "jif-2026__LOGO-JIF26-SOLO.svg"), encoding="utf-8").read()
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 595, "height": 842}, device_scale_factor=2)
        pg.set_content(f"<html><body style='margin:0;background:transparent'>{svg}</body></html>")
        pg.screenshot(path="/tmp/jif-color.png", omit_background=True)
        b.close()
    return recorta_y_escala(Image.open("/tmp/jif-color.png").convert("RGBA"))


def main():
    os.makedirs(DEST, exist_ok=True)
    for f, tinta in SVG_TINTA.items():
        s = open(os.path.join(GRIS, f), encoding="utf-8").read()
        s = re.sub(r"#8A8484", tinta, s, flags=re.I)
        open(os.path.join(DEST, f), "w", encoding="utf-8").write(s)
    for f, (o, fondo) in PNG.items():
        im = Image.open(os.path.join(ORIG, o))
        im = sin_blanco(im) if fondo == "blanco" else im.convert("RGBA")
        recorta_y_escala(im).save(os.path.join(DEST, f), optimize=True)
    jif().save(os.path.join(DEST, "jif-2026.png"), optimize=True)
    faltan = [f for f in os.listdir(GRIS) if f.lower().endswith((".svg", ".png")) and not os.path.exists(os.path.join(DEST, f))]
    print("logos_color:", len(os.listdir(DEST)), "archivos", "· faltan:", faltan or "ninguno")


if __name__ == "__main__":
    main()
