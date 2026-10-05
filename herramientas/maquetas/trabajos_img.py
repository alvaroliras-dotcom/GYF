# -*- coding: utf-8 -*-
"""GYF · v5.12 · Imágenes del portfolio (recursos/trabajos/): capturas limpias para el navegador y el móvil dibujados
en CSS de cada ficha, y la tarjeta 4:5 de la rejilla de /trabajos/ (maqueta propia, con el móvil en primer plano).
Uso (desde la raíz):  GYF_CRUDO=<.../03-FOTOS/06-CASOS/crudo> python3 herramientas/maquetas/trabajos_img.py"""
import os, sys
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import escaparate as E  # noqa: E402
from maquetas import CRUDO, RAIZ, objeto, F_FUCSIA, F_BERENJENA, F_CREMA, F_ROSA, F_MALVA  # noqa: E402

HD = CRUDO + "-hd"
SALIDA = os.path.join(RAIZ, "recursos", "trabajos")

# Capturas de escritorio (crudo-hd) y su recorte: la columna de la web, sin barras ni avisos
WEB = {"balgas": ("balgas-escritorio.png", None), "marcos-cerrajeros": ("marcos-cerrajeros-escritorio.png", None),
       "aquita": ("aquita-escritorio.png", None), "las-tejas": ("las-tejas-escritorio.png", None),
       "solvento": ("solvento-v2-escritorio.png", (0, 0, 1904, 919)), "rfg-andrade": ("rfg-andrade-escritorio.png", None),
       "vinos-gallegos-pousada": ("vinos-pousada-escritorio.png", (0, 0, 1904, 919)), "jif-2026": ("jif-2026-escritorio.png", None),
       "psicorazon": ("psicorazon-escritorio.png", None), "maribel-yebenes": ("maribel-yebenes-escritorio.png", None),
       "delfinia-piscinas": ("delfinia-escritorio.png", (298, 0, 1608, 840))}
MOVIL = {"balgas": "balgas-movil.jpg", "marcos-cerrajeros": "marcos-cerrajeros-movil.jpg", "aquita": "aquita-movil.jpg",
         "las-tejas": "las-tejas-movil.jpg", "solvento": "solvento-v2-movil.jpg", "rfg-andrade": "rfg-andrade-movil.jpg",
         "jif-2026": "jif-2026-movil.jpg", "maribel-yebenes": "maribel-yebenes-movil.jpg"}
# Ficha en Google Maps (capturas de Álvaro, 1.920 × 919): recortes del panel de arriba abajo (sin lo que solo ve el dueño)
MAPA = {"marcos-cerrajeros": ("maps-marcos-cerrajeros.png", None), "dotti-peluqueria": ("maps-dotti.png", None),
        "las-tejas": ("maps-las-tejas.png", None),
        "balgas": ("maps-balgas.png", [(72, 255, 474, 372), (72, 466, 474, 514), (72, 656, 474, 919)])}


def guarda(im, nombre, q=90):
    os.makedirs(SALIDA, exist_ok=True)
    im.convert("RGB").save(os.path.join(SALIDA, nombre), quality=q)
    print(nombre, im.size)


def mapa_limpio(archivo, panel):
    im = Image.open(os.path.join(CRUDO, archivo)).convert("RGB")
    dr = ImageDraw.Draw(im)
    dr.rectangle((1855, 8, 1915, 58), fill=im.getpixel((1850, 70)))          # la foto de la cuenta de Google
    if panel:
        trozos = [im.crop(c) for c in panel]
        dr.rectangle((72, panel[0][1], 480, 919), fill=(255, 255, 255))
        y = panel[0][1]
        for t in trozos:
            im.paste(t, (72, y)); y += t.height
    return im.crop((72, 0, 1920, 919))       # sin la barra lateral (historial de búsquedas)


def main():
    for slug, (f, caja) in WEB.items():
        im = Image.open(os.path.join(HD, f)).convert("RGB")
        guarda(im.crop(caja) if caja else im, f"web-{slug}.jpg")
    for slug, f in MOVIL.items():
        guarda(Image.open(os.path.join(CRUDO, f)), f"movil-{slug}.jpg")
    for slug, (f, panel) in MAPA.items():
        guarda(mapa_limpio(f, panel), f"mapa-{slug}.jpg")
    tarjetas()


# ---------- Tarjetas 4:5 de la rejilla (800 × 1.000 CSS a 2×). El centro aguanta un recorte a 1:1 ----------
def tarjetas():
    from playwright.sync_api import sync_playwright
    T = {}
    def disp(slug):
        return "file://" + os.path.join(SALIDA, f"web-{slug}.jpg")
    def mov(slug):
        return "file://" + os.path.join(SALIDA, f"movil-{slug}.jpg")
    def con_movil(slug, fondo, extra="", dom=""):
        return (fondo, E.resplandor(400, 520, 360, "#FFFFFF", .25) + extra
                + E.portatil(-260, 210, 900, disp(slug), dom, z=1)
                + E.movil(380, 160, 330, mov(slug), z=3))
    T["balgas"] = (F_CREMA, E.portatil(-260, 210, 900, disp("balgas"), "reparacioncalderasbalgas.es", z=1)
                   + E.movil(380, 160, 330, dentro=E.mm("balgas"), z=3) + E.obj("cursor", 40, 60, 140, -10, 4))
    T["marcos-cerrajeros"] = (F_BERENJENA, E.resplandor(560, 520, 340, "#E0067A", .45)
                              + E.portatil(-260, 210, 900, disp("marcos-cerrajeros"), "marcoscerrajeros.es", z=1)
                              + E.movil(380, 160, 330, dentro=E.mm("marcos"), z=3))
    T["aquita"] = con_movil("aquita", F_ROSA, E.obj("chincheta", 40, 60, 150, -6, 4), "aquita.es")
    T["las-tejas"] = con_movil("las-tejas", F_BERENJENA, E.resplandor(300, 300, 300, "#FF7AB8", .28), "restaurantelastejas.es")
    T["solvento"] = con_movil("solvento", F_MALVA, "", "solvento.es")
    T["rfg-andrade"] = con_movil("rfg-andrade", F_FUCSIA, E.simbolo_marca(300, -60, 760, "#FF5AAB", .3), "rfgandrade.es")
    T["jif-2026"] = con_movil("jif-2026", F_BERENJENA, "", "jif26.es")
    T["maribel-yebenes"] = con_movil("maribel-yebenes", F_CREMA, E.obj("estrella-cromo", 40, 60, 150, -8, 4), "maribelyebenes.com")
    T["dotti-peluqueria"] = (F_BERENJENA, E.resplandor(400, 500, 360, "#E0067A", .45)
                             + E.movil(205, 120, 390, dentro=E.mm("dotti"), z=3) + E.obj("chincheta", 600, 700, 150, 10, 4))
    # Sin captura de móvil: la web en grande, de cerca y cortada por el borde
    def cerca(slug, fondo, dom, extra=""):
        return (fondo, extra + E.portatil(-140, 250, 1180, disp(slug), dom, z=1))
    T["vinos-gallegos-pousada"] = cerca("vinos-gallegos-pousada", F_CREMA, "vinospousada.es", E.obj("abanico", 560, 70, 150, 8, 4))
    T["psicorazon"] = cerca("psicorazon", F_ROSA, "psicorazon.com", E.obj("bocadillo", 60, 70, 150, -8, 4))
    T["delfinia-piscinas"] = cerca("delfinia-piscinas", F_MALVA, "delfiniapiscinas.com", E.obj("estrella", 580, 80, 140, 10, 4))
    css = E.CSS.replace("width:1200px;height:675px", "width:800px;height:1000px")
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 800, "height": 1000}, device_scale_factor=2)
        for slug, (fondo, piezas) in T.items():
            html = (f"<!doctype html><html><head><meta charset=utf-8><style>{css}</style></head><body>"
                    f'<div class="lienzo" style="width:800px;height:1000px"><div class="fondo" style="background:{fondo}"></div>{piezas}</div></body></html>')
            f = os.path.join(E.TMP, f"tarjeta-{slug}.html"); os.makedirs(E.TMP, exist_ok=True)
            open(f, "w", encoding="utf-8").write(html)
            pg.goto("file://" + f); pg.wait_for_load_state("networkidle"); pg.wait_for_timeout(150)
            tmp = os.path.join(E.TMP, f"tarjeta-{slug}.png"); pg.screenshot(path=tmp)
            im = Image.open(tmp).convert("RGB").resize((1600, 2000), Image.LANCZOS)
            guarda(im, f"tarjeta-{slug}.jpg")
        b.close()


if __name__ == "__main__":
    main()
