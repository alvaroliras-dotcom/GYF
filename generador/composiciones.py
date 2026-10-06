# -*- coding: utf-8 -*-
"""GYF · composiciones del portfolio: la web real de cada cliente (captura + móvil) sobre el color de su marca, sin el
fondo rosa de las maquetas. Genera recursos/trabajos/tarjeta2-<slug>.jpg (4:5) y recursos/escaparate/escaparate2-<slug>.jpg (2:1).
Uso: python3 generador/composiciones.py   (después, build.py y rematar.py)"""
import os
from PIL import Image, ImageDraw, ImageFilter
R = os.path.join(os.path.dirname(__file__), "..", "recursos")
T = os.path.join(R, "trabajos")
COL = {"balgas": "#16213d", "marcos-cerrajeros": "#1d1712", "aquita": "#c9dfbd", "las-tejas": "#14100a", "rfg-andrade": "#e6dfd2",
       "maribel-yebenes": "#e6d8d1", "jif-2026": "#0f4a4b", "psicorazon": "#b98a6a", "dotti-peluqueria": "#dde4ee"}


def abrir(n):
    p = os.path.join(T, n)
    return Image.open(p).convert("RGB") if os.path.exists(p) else None


def redondear(im, r):
    m = Image.new("L", im.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, im.width - 1, im.height - 1), r, fill=255)
    o = im.convert("RGBA"); o.putalpha(m); return o


def sombra(lienzo, caja, r, opac=90, desp=26, desen=40):
    x0, y0, x1, y1 = caja
    s = Image.new("RGBA", lienzo.size, (0, 0, 0, 0))
    ImageDraw.Draw(s).rounded_rectangle((x0, y0 + desp, x1, y1 + desp), r, fill=(0, 0, 0, opac))
    lienzo.alpha_composite(s.filter(ImageFilter.GaussianBlur(desen)))


def ventana(img, ancho):
    h = round(img.height * ancho / img.width)
    pant = img.resize((ancho, h), Image.LANCZOS)
    barra = max(34, ancho // 36)
    w = Image.new("RGB", (ancho, h + barra), (240, 238, 235))
    w.paste(pant, (0, barra))
    d = ImageDraw.Draw(w)
    for k, c in enumerate(((237, 106, 94), (245, 191, 79), (97, 197, 84))):
        d.ellipse((barra * 0.55 + k * barra * 0.55, barra * 0.3, barra * 0.55 + k * barra * 0.55 + barra * 0.4, barra * 0.7), fill=c)
    return redondear(w, max(12, ancho // 70))


def telefono(img, ancho):
    h = round(img.height * ancho / img.width)
    b = max(10, ancho // 28)
    p = img.resize((ancho, h), Image.LANCZOS)
    m = Image.new("RGB", (ancho + 2 * b, h + 2 * b), (22, 22, 24))
    m.paste(p, (b, b))
    return redondear(m, ancho // 5)


def poner(lienzo, im, x, y, sombra_r=None):
    if sombra_r:
        sombra(lienzo, (x, y, x + im.width, y + im.height), sombra_r)
    lienzo.alpha_composite(im, (x, y))


def componer(slug, W, H):
    web = abrir(f"web-{slug}.jpg") or abrir(f"mapa-{slug}.jpg")
    mov = abrir(f"movil-{slug}.jpg")
    c = Image.new("RGBA", (W, H), COL[slug])
    if not mov and H > W and slug == "psicorazon":   # web que es una foto: la misma foto desenfocada de fondo
        cw = round(web.height * W / H); x0 = round(web.width * 0.20)
        fondo = web.crop((x0, 0, x0 + cw, web.height)).resize((W, H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(38))
        c = Image.blend(fondo, Image.new("RGB", (W, H), "#3a2a20"), 0.25).convert("RGBA")
    if not mov:   # sin móvil: la ventana sola, grande y centrada
        v = ventana(web, round(W * (0.90 if H > W else 0.74))); poner(c, v, (W - v.width) // 2, (H - v.height) // 2, 30)
    elif H > W:   # tarjeta vertical: escritorio arriba, móvil abajo a la derecha
        v = ventana(web, round(W * 0.84)); x = (W - v.width) // 2; y = round(H * 0.14)
        poner(c, v, x, y, 26)
        if mov:
            t = telefono(mov, round(W * 0.23)); poner(c, t, x + v.width - t.width + 30, y + v.height - round(t.height * 0.16), 60)
    else:       # hero horizontal
        v = ventana(web, round(W * 0.66)); x = round(W * 0.09); y = (H - v.height) // 2
        poner(c, v, x, y, 30)
        if mov:
            t = telefono(mov, round(H * 0.27)); poner(c, t, x + v.width - round(t.width * 0.35), y + v.height - round(t.height * 0.66), 60)
    return c.convert("RGB")


if __name__ == "__main__":
    for s in COL:
        v = "4" if s == "psicorazon" else ("3" if s == "dotti-peluqueria" else "2")   # el número cambia cuando la composición cambia (la caché guarda un año)
        componer(s, 1600, 2000).save(os.path.join(T, f"tarjeta{v}-{s}.jpg"), quality=90)
        componer(s, 2400, 1200).save(os.path.join(R, "escaparate", f"escaparate{v}-{s}.jpg"), quality=90)
        print("ok", s)
