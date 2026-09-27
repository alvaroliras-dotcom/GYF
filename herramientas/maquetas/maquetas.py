# -*- coding: utf-8 -*-
"""GYF · Composiciones de los casos (v2): capturas reales dentro de un portátil y un móvil dibujados en CSS,
con perspectiva, sombra suave, fondo de la marca y, a veces, un objeto 3D de la familia.
Se pintan en Chromium sin cabeza a 2× y salen en recursos/casos/ (1.600 px de ancho; rematar.py hace 800/1.600).
Uso (desde la raíz):  python3 herramientas/maquetas/maquetas.py [nombre ...]
Capturas de partida: /home/claude/gyf/casos/crudo/ (escritorio 800 px de ancho, móvil 750 × 1.624)."""
import os, sys, tempfile
from PIL import Image, ImageFilter

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
CRUDO = "/home/claude/gyf/casos/crudo"
OBJ = os.path.join(RAIZ, "herramientas", "objetos3d", "master")
SALIDA = os.path.join(RAIZ, "recursos", "casos")
TMP = os.path.join(tempfile.gettempdir(), "gyf-maquetas")

CSS = """
*{box-sizing:border-box;margin:0}
html,body{width:100%;height:100%;overflow:hidden}
.lienzo{position:relative;width:100vw;height:100vh;overflow:hidden}
.fondo{position:absolute;inset:0}
.escena{position:absolute;inset:0;perspective:2400px;perspective-origin:50% 40%}
/* ---- Portátil ---- */
.lap{position:absolute;transform-style:preserve-3d}
.lap .tapa{position:relative;border-radius:calc(var(--w)*.034);background:linear-gradient(160deg,#26262b,#0c0c0e 60%);
  box-shadow:0 0 0 calc(var(--w)*.0028) #9EA1A8,0 0 0 calc(var(--w)*.0045) #5c5f66,inset 0 0 0 calc(var(--w)*.002) #34343a;
  padding:calc(var(--w)*.034) calc(var(--w)*.024) calc(var(--w)*.03)}
.lap .cam{position:absolute;left:50%;top:calc(var(--w)*.013);width:calc(var(--w)*.008);height:calc(var(--w)*.008);border-radius:50%;background:#2b2d33;transform:translateX(-50%);box-shadow:inset 0 0 0 1px #3c4048}
.lap .pant{position:relative;aspect-ratio:1.6;overflow:hidden;border-radius:calc(var(--w)*.006);background:#fff}
.lap .pant img{width:100%;height:100%;object-fit:cover;object-position:top center;display:block}
.brillo{position:absolute;inset:0;background:linear-gradient(118deg,rgba(255,255,255,.14) 0%,rgba(255,255,255,.04) 34%,transparent 34.2%);pointer-events:none}
.lap .base{position:relative;margin:0 calc(var(--w)*-.075);height:calc(var(--w)*.032);border-radius:0 0 calc(var(--w)*.05) calc(var(--w)*.05)/0 0 calc(var(--w)*.026) calc(var(--w)*.026);
  background:linear-gradient(180deg,#f1f2f5 0%,#d6d8dd 30%,#b7b9bf 70%,#8d9097 100%);box-shadow:inset 0 1px 0 #fff}
.lap .base::before{content:"";position:absolute;left:50%;top:0;width:calc(var(--w)*.15);height:calc(var(--w)*.011);transform:translateX(-50%);
  border-radius:0 0 calc(var(--w)*.012) calc(var(--w)*.012);background:linear-gradient(180deg,#a9abb1,#c8cacf)}
.lap .suelo{position:absolute;left:-4%;right:-4%;bottom:calc(var(--w)*-.04);height:calc(var(--w)*.06);border-radius:50%;background:rgba(0,0,0,.55);filter:blur(calc(var(--w)*.03));z-index:-1}
/* ---- Móvil ---- */
.mov{position:absolute;aspect-ratio:1/2.05;border-radius:calc(var(--w)*.165);background:linear-gradient(145deg,#2d2d31,#101012);
  padding:calc(var(--w)*.042);box-shadow:0 0 0 calc(var(--w)*.012) #3d3e43,0 0 0 calc(var(--w)*.019) #16161a,inset 0 0 0 calc(var(--w)*.006) #4b4c52}
.mov .pant{position:relative;width:100%;height:100%;border-radius:calc(var(--w)*.125);overflow:hidden;background:#fff;display:flex;flex-direction:column}
.mov .pant img{width:100%;flex:1;min-height:0;object-fit:cover;object-position:top center;display:block}
.mov .barra{flex:none;height:calc(var(--w)*.15);display:flex;justify-content:space-between;align-items:center;padding:calc(var(--w)*.03) calc(var(--w)*.1) 0;font:600 calc(var(--w)*.05)/1 -apple-system,"Segoe UI",Roboto,sans-serif}
.mov .barra b{display:flex;gap:calc(var(--w)*.018);align-items:center}
.mov .barra b i{display:block;width:calc(var(--w)*.012);border-radius:1px;background:currentColor}
.mov .barra b u{display:block;width:calc(var(--w)*.075);height:calc(var(--w)*.036);border-radius:calc(var(--w)*.01);border:1.5px solid currentColor;margin-left:calc(var(--w)*.012);position:relative}
.mov .barra b u::after{content:"";position:absolute;inset:1.5px;right:28%;background:currentColor;border-radius:1px}
.mov .isla{position:absolute;left:50%;top:calc(var(--w)*.075);width:calc(var(--w)*.3);height:calc(var(--w)*.085);transform:translateX(-50%);border-radius:99px;background:#050506;z-index:2}
.mov .bot{position:absolute;width:calc(var(--w)*.022);border-radius:3px;background:linear-gradient(90deg,#1e1e22,#48494f)}
.sombra{box-shadow:0 60px 120px -30px rgba(20,6,14,.55),0 30px 60px -30px rgba(20,6,14,.5)}
.obj{position:absolute;display:block}
.marca{position:absolute;font:700 10px/1 sans-serif}
"""


CRUDO_HD = CRUDO + "-hd"          # capturas de escritorio a resolución real (si están, mandan)
_NITIDO = os.path.join(tempfile.gettempdir(), "maquetas-nitido")


def ruta(n):
    """Las capturas de escritorio salen en la pantalla del portátil a más tamaño del que tienen: si hay versión HD
    (crudo-hd/), se usa esa; si no, se amplía al doble con Lanczos y un enfoque suave para que no se vea borrosa."""
    hd = os.path.join(CRUDO_HD, n.rsplit(".", 1)[0] + ".png")
    if os.path.exists(hd):
        return "file://" + hd
    if n.startswith("dotti-busqueda") or "escritorio" in n:
        os.makedirs(_NITIDO, exist_ok=True)
        dest = os.path.join(_NITIDO, n.rsplit(".", 1)[0] + ".png")
        im = Image.open(os.path.join(CRUDO, n)).convert("RGB")
        im = im.resize((im.width * 2, im.height * 2), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=1.6, percent=110, threshold=2))
        im.save(dest)
        return "file://" + dest
    return "file://" + os.path.join(CRUDO, n)


def objeto(n):
    return "file://" + os.path.join(OBJ, n + ".png")


def recorte(n, caja, nombre):
    """Recorta una captura (x0, y0, x1, y1) a un archivo temporal y devuelve su URL."""
    os.makedirs(TMP, exist_ok=True)
    d = os.path.join(TMP, nombre)
    Image.open(os.path.join(CRUDO, n)).crop(caja).save(d, quality=95)
    return "file://" + d


def tapar(n, cajas, nombre):
    """Tapa zonas de una captura (p. ej. la foto de la cuenta de Google arriba a la derecha) con el color de su borde."""
    from PIL import ImageDraw
    os.makedirs(TMP, exist_ok=True)
    d = os.path.join(TMP, nombre)
    im = Image.open(os.path.join(CRUDO, n)).convert("RGB")
    dr = ImageDraw.Draw(im)
    for c in cajas:
        dr.rectangle(c, fill=im.getpixel((c[0] - 2, c[1] + 2)))
    im.save(d, quality=95)
    return "file://" + d


def desenfocado(n, radio, nombre, oscuro=0):
    os.makedirs(TMP, exist_ok=True)
    d = os.path.join(TMP, nombre)
    im = Image.open(os.path.join(CRUDO, n)).convert("RGB").filter(ImageFilter.GaussianBlur(radio))
    if oscuro:
        im = Image.blend(im, Image.new("RGB", im.size, (28, 18, 25)), oscuro)
    im.save(d, quality=92)
    return "file://" + d


def laptop(x, y, w, img, rot="", z=1, sombra=True):
    return (f'<div class="lap" style="--w:{w}px;left:{x}px;top:{y}px;width:{w}px;z-index:{z};transform:{rot}">'
            f'<div class="tapa{" sombra" if sombra else ""}"><i class="cam"></i><div class="pant"><img src="{img}"><i class="brillo"></i></div></div>'
            f'<div class="base"></div>{"<i class=suelo></i>" if sombra else ""}</div>')


def color_barra(img):
    """Color de la barra de estado: el de la primera fila de la captura; texto claro u oscuro según su luz."""
    im = Image.open(img.replace("file://", "")).convert("RGB")
    fila = im.crop((0, 0, im.width, 6)).resize((1, 1), Image.LANCZOS).getpixel((0, 0))
    luz = .299 * fila[0] + .587 * fila[1] + .114 * fila[2]
    return "#%02x%02x%02x" % fila, ("#111" if luz > 150 else "#fff")


def movil(x, y, w, img, rot="", z=2):
    h = w * 2.05
    fondo, tinta = color_barra(img)
    barra = (f'<div class="barra" style="background:{fondo};color:{tinta}"><span>9:41</span>'
             f'<b><i style="height:30%"></i><i style="height:45%"></i><i style="height:60%"></i><i style="height:75%"></i><u></u></b></div>')
    bots = (f'<i class="bot" style="left:calc(var(--w)*-.034);top:{h*.2:.0f}px;height:{h*.045:.0f}px"></i>'
            f'<i class="bot" style="left:calc(var(--w)*-.034);top:{h*.28:.0f}px;height:{h*.08:.0f}px"></i>'
            f'<i class="bot" style="left:calc(var(--w)*-.034);top:{h*.38:.0f}px;height:{h*.08:.0f}px"></i>'
            f'<i class="bot" style="right:calc(var(--w)*-.034);top:{h*.3:.0f}px;height:{h*.12:.0f}px"></i>')
    return (f'<div class="mov sombra" style="--w:{w}px;left:{x}px;top:{y}px;width:{w}px;z-index:{z};transform:{rot}">{bots}'
            f'<div class="pant">{barra}<img src="{img}"><i class="brillo"></i></div><i class="isla"></i></div>')


def obj(n, x, y, w, rot=0, z=3, extra=""):
    return f'<img class="obj" src="{objeto(n)}" style="left:{x}px;top:{y}px;width:{w}px;z-index:{z};transform:rotate({rot}deg);{extra}">'


# ---------- Fondos ----------
F_FUCSIA = "radial-gradient(120% 90% at 30% 20%,#FF2E97 0%,#E0067A 45%,#B10460 100%)"
F_BERENJENA = "radial-gradient(90% 70% at 70% 30%,#4A1F3B 0%,#2A1623 45%,#160C13 100%)"
F_CREMA = "radial-gradient(110% 90% at 50% 10%,#FFFFFF 0%,#F5F1EC 55%,#E9E1D8 100%)"
F_ROSA = "linear-gradient(160deg,#FFE3EF 0%,#F9C6DD 55%,#F2A9CA 100%)"
F_MALVA = "radial-gradient(100% 90% at 20% 10%,#F6E7EC 0%,#E9CFD8 50%,#D5B0BE 100%)"


def resplandor(x, y, r, color, op=.55):
    return f'<i style="position:absolute;left:{x - r}px;top:{y - r}px;width:{2*r}px;height:{2*r}px;border-radius:50%;background:{color};opacity:{op};filter:blur({r*.45:.0f}px)"></i>'


def simbolo_marca(x, y, h, color, op):
    """El & de la marca como marca de agua (trazado del SVG real)."""
    svg = open(os.path.join(RAIZ, "recursos", "marca", "simbolo-color.svg"), encoding="utf-8").read()
    import re
    svg = re.sub(r'fill="#[0-9A-Fa-f]{3,6}"', f'fill="{color}"', svg)
    svg = svg.replace("<svg ", f'<svg style="position:absolute;left:{x}px;top:{y}px;height:{h}px;width:auto;opacity:{op}" ', 1)
    return svg


# ---------- Composiciones ----------
# nombre de salida → (ancho CSS, alto CSS, fondo, piezas)
def composiciones():
    C = {}
    # --- Formato proyecto 16:10 (800 × 500 CSS → 1.600 × 1.000) ---
    C["diseno-web-alcorcon-caso-balgas"] = (800, 500, F_FUCSIA,
        simbolo_marca(470, -60, 640, "#FF5AAB", .35) + resplandor(620, 120, 160, "#FFD1E6", .35)
        + laptop(90, 92, 520, ruta("balgas-escritorio.jpg"), "rotateY(10deg) rotateX(3deg)")
        + movil(560, 150, 150, ruta("balgas-movil.jpg"), "rotate(-4deg)", 3)
        + obj("cursor", 680, 36, 110, -10, 1))
    C["diseno-web-alcorcon-caso-marcos-cerrajeros"] = (800, 500, F_BERENJENA,
        resplandor(560, 260, 230, "#E0067A", .55)
        + laptop(70, 108, 500, ruta("marcos-cerrajeros-escritorio.jpg"), "rotateY(14deg)")
        + movil(548, 88, 170, ruta("marcos-cerrajeros-movil.jpg"), "rotate(5deg)", 3)
        + obj("estrella-cromo", 20, 320, 150, -8, 4))
    C["diseno-web-arroyomolinos-caso-aquita"] = (800, 500, F_CREMA,
        resplandor(400, 470, 300, "#E6D9CB", .9)
        + laptop(130, 70, 540, ruta("aquita-escritorio.jpg"))
        + movil(600, 170, 138, ruta("aquita-movil.jpg"), "rotate(-3deg)", 3)
        + obj("chincheta", 26, 30, 170, 0, 0))
    C["diseno-web-alcorcon-caso-las-tejas"] = (800, 500, F_BERENJENA,
        resplandor(200, 120, 220, "#FF7AB8", .3)
        + laptop(210, 90, 520, ruta("las-tejas-escritorio.jpg"), "rotateY(-12deg)")
        + movil(90, 120, 160, ruta("las-tejas-movil.jpg"), "rotate(-5deg)", 3)
        + obj("bocadillo", 620, 330, 170, 0, 4))
    C["diseno-web-caso-solvento"] = (800, 500, F_MALVA,
        simbolo_marca(-60, 40, 520, "#FFFFFF", .45) + resplandor(560, 180, 220, "#FFFFFF", .5)
        + laptop(215, 82, 520, ruta("solvento-escritorio.jpg"), "rotateY(-16deg) rotateX(4deg)")
        + movil(95, 130, 158, ruta("solvento-movil.jpg"), "rotate(-3deg)", 3)
        + obj("abanico", 650, 24, 130, 8, 4))
    C["diseno-web-caso-rfg-andrade"] = (800, 500, F_ROSA,
        resplandor(400, 250, 260, "#FFFFFF", .45)
        + laptop(140, 76, 520, ruta("rfg-andrade-escritorio.jpg"), "rotateY(8deg)")
        + movil(590, 150, 140, ruta("rfg-andrade-movil.jpg"), "rotate(4deg)", 3)
        + obj("bocadillo", 34, 300, 130, -8, 4))
    panel = recorte("dotti-ficha-maps.jpg", (16, 8, 420, 1000), "dotti-panel.jpg")
    C["seo-local-caso-dotti-peluqueria"] = (800, 500, F_BERENJENA,
        resplandor(560, 200, 240, "#E0067A", .5)
        + laptop(60, 96, 520, tapar("dotti-busqueda-google.jpg", [(752, 0, 800, 34)], "dotti-busqueda.jpg"), "rotateY(12deg)")
        + movil(548, 70, 176, panel, "rotate(4deg)", 3)
        + obj("chincheta", 690, 300, 120, 10, 4) + obj("estrella", 470, 350, 110, -12, 4))
    # --- Formato galería de la portada ---
    # vertical 2:3 (500 × 750 → 1.000 × 1.500)
    C["diseno-web-alcorcon-caso-marcos-cerrajeros-movil"] = (500, 750, F_FUCSIA,
        simbolo_marca(40, 60, 640, "#FF5AAB", .3)
        + movil(135, 110, 230, ruta("marcos-cerrajeros-movil.jpg"), "rotate(-5deg)")
        + obj("lupa", 300, 510, 170, 6, 4))
    C["diseno-web-alcorcon-caso-las-tejas-movil"] = (500, 750, F_CREMA,
        resplandor(250, 700, 260, "#E6D9CB", .9)
        + movil(135, 95, 230, ruta("las-tejas-movil.jpg"), "rotate(4deg)")
        + obj("estrella", 24, 470, 160, -6, 4))
    C["seo-local-caso-dotti-peluqueria-movil"] = (500, 750, F_BERENJENA,
        resplandor(250, 360, 230, "#E0067A", .5)
        + movil(130, 100, 240, panel, "rotate(-4deg)")
        + obj("chincheta", 318, 60, 150, 10, 4) + obj("estrella", 40, 520, 140, -10, 4))
    # horizontal 3:2 (750 × 500 → 1.500 × 1.000): portátil de cerca, cortado por el borde
    C["diseno-web-arroyomolinos-caso-aquita-portatil"] = (750, 500, F_BERENJENA,
        resplandor(560, 120, 200, "#E0067A", .45)
        + laptop(150, 70, 640, ruta("aquita-escritorio.jpg"), "rotateY(-18deg) rotateX(5deg)")
        + obj("bocadillo", 14, 250, 170, -6, 4))
    C["diseno-web-caso-rfg-andrade-portatil"] = (750, 500, F_FUCSIA,
        simbolo_marca(-40, 20, 520, "#FF5AAB", .35)
        + laptop(80, 70, 660, ruta("rfg-andrade-escritorio.jpg"), "rotateY(16deg) rotateX(4deg)"))
    # grande 3:4 (600 × 800 → 1.200 × 1.600 → se guarda a 1.600 de ancho)
    C["diseno-web-alcorcon-caso-balgas-vertical"] = (600, 800, F_CREMA,
        resplandor(300, 760, 300, "#E6D9CB", .9)
        + laptop(40, 150, 520, ruta("balgas-escritorio.jpg"), "rotateY(8deg)")
        + movil(330, 330, 190, ruta("balgas-movil.jpg"), "rotate(4deg)", 3)
        + obj("cursor", 40, 450, 150, -12, 4))
    C["diseno-web-caso-solvento-vertical"] = (600, 800, F_MALVA,
        simbolo_marca(180, 330, 520, "#FFFFFF", .5)
        + laptop(60, 120, 500, ruta("solvento-escritorio.jpg"), "rotateY(-10deg)")
        + movil(90, 300, 200, ruta("solvento-movil.jpg"), "rotate(-4deg)", 3)
        + obj("abanico", 390, 550, 170, -6, 4))
    # --- Tarjetas de servicio de la home (4:3, 800 × 600 → 1.600 × 1.200), sin objeto: el de la tarjeta va encima ---
    busq = tapar("dotti-busqueda-google.jpg", [(752, 0, 800, 34)], "dotti-busqueda.jpg")
    C["servicio-seo-local-ficha-dotti"] = (800, 600, F_FUCSIA,
        simbolo_marca(420, -40, 700, "#FF5AAB", .3)
        + laptop(40, 150, 520, busq, "rotateY(14deg)", 1)
        + movil(470, 70, 200, panel, "rotate(5deg)", 3))
    C["servicio-auditoria-aquita"] = (800, 600, F_CREMA,
        resplandor(400, 560, 320, "#E6D9CB", .9)
        + laptop(60, 70, 600, ruta("aquita-escritorio.jpg"), "rotateY(-16deg) rotateX(5deg)"))
    C["servicio-diseno-web-las-tejas"] = (800, 600, F_BERENJENA,
        resplandor(560, 220, 260, "#E0067A", .45)
        + laptop(200, 110, 560, ruta("las-tejas-escritorio.jpg"), "rotateY(-12deg)")
        + movil(70, 90, 190, ruta("las-tejas-movil.jpg"), "rotate(-4deg)", 3))
    C["servicio-google-ads-balgas"] = (800, 600, F_ROSA,
        resplandor(300, 300, 280, "#FFFFFF", .5)
        + laptop(250, 120, 520, ruta("balgas-escritorio.jpg"), "rotateY(-10deg)")
        + movil(90, 70, 210, ruta("balgas-movil.jpg"), "rotate(-5deg)", 3))
    C["servicio-diseno-grafico-solvento"] = (800, 600, F_MALVA,
        simbolo_marca(-80, 60, 640, "#FFFFFF", .45)
        + laptop(250, 110, 540, ruta("solvento-escritorio.jpg"), "rotateY(-14deg) rotateX(3deg)", 1)
        + movil(90, 80, 200, ruta("solvento-movil.jpg"), "rotate(-6deg)", 3))
    C["servicio-redaccion-rfg-andrade"] = (800, 600, F_FUCSIA,
        resplandor(600, 120, 220, "#FFD1E6", .3)
        + laptop(90, 90, 620, ruta("rfg-andrade-escritorio.jpg"), "rotateY(12deg) rotateX(4deg)"))
    C["servicio-analitica-marcos"] = (800, 600, F_CREMA,
        resplandor(400, 560, 320, "#E6D9CB", .9)
        + laptop(60, 120, 540, ruta("marcos-cerrajeros-escritorio.jpg"), "rotateY(12deg)")
        + movil(540, 80, 190, ruta("marcos-cerrajeros-movil.jpg"), "rotate(4deg)", 3))
    return C


def main(nombres):
    from playwright.sync_api import sync_playwright
    os.makedirs(SALIDA, exist_ok=True); os.makedirs(TMP, exist_ok=True)
    C = composiciones()
    with sync_playwright() as p:
        b = p.chromium.launch()
        for n in (nombres or list(C)):
            w, h, fondo, piezas = C[n]
            Z = 3   # Chromium rasteriza las capas en 3D a 1 px por px CSS (ignora el device_scale_factor): se agranda con zoom y se reduce
            pg = b.new_page(viewport={"width": w * Z, "height": h * Z}, device_scale_factor=1)
            html = (f"<!doctype html><html><head><meta charset=utf-8><style>{CSS} html{{zoom:{Z}}}</style></head><body>"
                    f'<div class="lienzo"><div class="fondo" style="background:{fondo}"></div><div class="escena">{piezas}</div></div></body></html>')
            f = os.path.join(TMP, n + ".html"); open(f, "w", encoding="utf-8").write(html)
            pg.goto("file://" + f); pg.wait_for_timeout(250)
            tmp = os.path.join(TMP, n + ".png"); pg.screenshot(path=tmp)
            im = Image.open(tmp).convert("RGB")
            if im.width != 1600:
                im = im.resize((1600, round(im.height * 1600 / im.width)), Image.LANCZOS)
            im.save(os.path.join(SALIDA, n + ".jpg"), quality=90)
            pg.close()
            print(n, im.size)
        b.close()


if __name__ == "__main__":
    main(sys.argv[1:])
