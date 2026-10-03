# -*- coding: utf-8 -*-
"""GYF · v5.7 · Maquetas grandes del escaparate de casos (la sección «Lo más reciente» de la home).
Dispositivos de frente, sin perspectiva (así se lee el trabajo y Chromium no rasteriza capas 3D a 1×):
portátil 16:9 o pantalla de sobremesa con barra de navegador y el dominio real, más un móvil delante.
En los casos de ficha de Google el móvil enseña el mapa con la ficha abierta.
Lienzo 1.200 × 675 CSS a 2× → 2.400 × 1.350 en recursos/escaparate/ (rematar.py hace 800/1.200/1.600/2.400).
Uso (desde la raíz):  python3 herramientas/maquetas/escaparate.py [nombre ...]"""
import os, sys, tempfile
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from maquetas import ruta, objeto, color_barra, resplandor, simbolo_marca, CRUDO, RAIZ, F_FUCSIA, F_BERENJENA, F_CREMA, F_ROSA, F_MALVA  # noqa: E402

SALIDA = os.path.join(RAIZ, "recursos", "escaparate")
TMP = os.path.join(tempfile.gettempdir(), "gyf-escaparate")
W, H = 1200, 675

CSS = """
*{box-sizing:border-box;margin:0}
html,body{width:1200px;height:675px;overflow:hidden;-webkit-font-smoothing:antialiased}
.lienzo{position:relative;width:1200px;height:675px;overflow:hidden}
.fondo{position:absolute;inset:0}
.suelo{position:absolute;border-radius:50%;background:rgba(18,6,13,.5);filter:blur(22px)}
/* ---- navegador dentro de la pantalla ---- */
.nav{display:flex;align-items:center;gap:7px;height:var(--b);padding:0 calc(var(--b)*.45);background:linear-gradient(#f3f3f5,#e7e7ea);border-bottom:1px solid #d3d3d8;flex:none}
.nav i{width:calc(var(--b)*.3);height:calc(var(--b)*.3);border-radius:50%;background:#d0d0d5;flex:none}
.nav i:nth-child(1){background:#ff5f57}.nav i:nth-child(2){background:#febc2e}.nav i:nth-child(3){background:#28c840}
.nav span{flex:1;display:flex;justify-content:center}
.nav em{font:500 calc(var(--b)*.4)/1 -apple-system,"SF Pro Text","Segoe UI",Roboto,sans-serif;font-style:normal;color:#3a3a40;background:#fff;border-radius:7px;
  padding:calc(var(--b)*.17) calc(var(--b)*1.4);display:flex;align-items:center;gap:6px;box-shadow:0 0 0 1px #d9d9de;min-width:40%;justify-content:center}
.nav em svg{width:calc(var(--b)*.32);height:calc(var(--b)*.32)}
.pant{position:relative;display:flex;flex-direction:column;overflow:hidden;background:#fff}
.pant > img{display:block;width:100%;height:auto}
.reflejo{position:absolute;inset:0;background:linear-gradient(115deg,rgba(255,255,255,.10) 0%,rgba(255,255,255,.03) 38%,transparent 38.2%);pointer-events:none}
/* ---- portátil ---- */
.lap{position:absolute}
.lap .tapa{position:relative;border-radius:18px 18px 6px 6px;background:#0d0d0f;padding:15px 15px 20px;
  box-shadow:0 0 0 1.5px #a7aab1,0 0 0 3px #4d5057,0 40px 70px -30px rgba(18,6,13,.55)}
.lap .tapa::after{content:"";position:absolute;left:50%;top:6px;width:5px;height:5px;border-radius:50%;background:#26282d;transform:translateX(-50%)}
.lap .pant{border-radius:4px}
.lap .base{position:relative;height:20px;margin:0 -64px;border-radius:2px 2px 26px 26px/2px 2px 12px 12px;
  background:linear-gradient(180deg,#f4f5f7 0%,#dcdee2 35%,#b9bcc2 75%,#8f9298 100%);box-shadow:inset 0 1px 0 #fff,0 18px 30px -14px rgba(18,6,13,.6)}
.lap .base::before{content:"";position:absolute;left:50%;top:0;width:130px;height:8px;transform:translateX(-50%);border-radius:0 0 10px 10px;background:linear-gradient(180deg,#a3a6ac,#cbcdd2)}
/* ---- pantalla de sobremesa ---- */
.mon{position:absolute}
.mon .marco{position:relative;border-radius:16px 16px 0 0;background:#0b0b0d;padding:13px;box-shadow:0 0 0 1.5px #b9bcc2}
.mon .pant{border-radius:3px}
.mon .barbilla{height:54px;border-radius:0 0 16px 16px;background:linear-gradient(180deg,#eceef1,#d3d6db 70%,#c2c5cb);box-shadow:0 0 0 1.5px #b9bcc2,0 40px 70px -30px rgba(18,6,13,.5)}
.mon .cuello{width:150px;height:74px;margin:0 auto;background:linear-gradient(90deg,#b6b9bf,#e8eaed 45%,#c9ccd1 70%,#9fa2a8);clip-path:polygon(8% 0,92% 0,100% 100%,0 100%)}
.mon .pie{width:250px;height:12px;margin:0 auto;border-radius:3px 3px 8px 8px;background:linear-gradient(180deg,#e9ebee,#b3b6bc);box-shadow:0 14px 22px -8px rgba(18,6,13,.55)}
/* ---- móvil ---- */
.mov{position:absolute;border-radius:40px;background:linear-gradient(145deg,#303035,#0e0e10);padding:9px;
  box-shadow:0 0 0 2.5px #4a4b51,0 0 0 4px #17171a,inset 0 0 0 1.5px #55565c,0 50px 80px -28px rgba(18,6,13,.65),0 22px 36px -18px rgba(18,6,13,.5)}
.mov .pant{width:100%;height:100%;border-radius:32px}
.mov .pant > img{flex:1;min-height:0;height:auto;object-fit:cover;object-position:top center}
.mov .isla{position:absolute;left:50%;top:19px;width:30%;height:23px;transform:translateX(-50%);border-radius:99px;background:#050506;z-index:3}
.mov .bot{position:absolute;width:4px;border-radius:2px;background:linear-gradient(90deg,#1e1e22,#4a4b51)}
.barra{flex:none;height:44px;display:flex;justify-content:space-between;align-items:center;padding:6px 24px 0 30px;font:600 14px/1 -apple-system,"SF Pro Text","Segoe UI",Roboto,sans-serif;position:relative;z-index:2}
.barra b{display:flex;gap:3px;align-items:flex-end;height:11px}
.barra b i{display:block;width:3px;border-radius:1px;background:currentColor}
.barra b u{display:block;width:22px;height:11px;border-radius:3.5px;border:1.4px solid currentColor;margin-left:5px;position:relative;opacity:.9}
.barra b u::after{content:"";position:absolute;inset:1.4px;right:25%;background:currentColor;border-radius:1px}
/* ---- mapa en el móvil (ficha de Google) ---- */
.mapa{position:relative;flex:none;height:46%;overflow:hidden;margin-top:-44px}
.mapa img{position:absolute;display:block}
.pin{position:absolute;width:30px;height:42px;transform:translate(-50%,-100%);filter:drop-shadow(0 4px 4px rgba(0,0,0,.35))}
.hoja{position:relative;flex:1;margin-top:-16px;background:#fff;border-radius:18px 18px 0 0;overflow:hidden;box-shadow:0 -6px 18px rgba(0,0,0,.18)}
.hoja::before{content:"";position:absolute;left:50%;top:7px;width:36px;height:4px;border-radius:2px;background:#d5d5da;transform:translateX(-50%);z-index:2}
.hoja img{display:block;width:100%}
.obj{position:absolute;display:block;filter:drop-shadow(0 26px 30px rgba(18,6,13,.35))}
"""

CANDADO = '<svg viewBox="0 0 16 16"><path fill="#6b6b72" d="M4 7V5a4 4 0 1 1 8 0v2h.5A1.5 1.5 0 0 1 14 8.5v5A1.5 1.5 0 0 1 12.5 15h-9A1.5 1.5 0 0 1 2 13.5v-5A1.5 1.5 0 0 1 3.5 7H4zm2 0h4V5a2 2 0 1 0-4 0v2z"/></svg>'


def tam(img):
    with Image.open(img.replace("file://", "")) as im:
        return im.width, im.height


def navegador(dominio, b):
    return f'<div class="nav" style="--b:{b}px"><i></i><i></i><i></i><span><em>{CANDADO}{dominio}</em></span><i style="opacity:0"></i><i style="opacity:0"></i><i style="opacity:0"></i></div>'


def pantalla(img, dominio, w):
    """Pantalla de ordenador: barra de navegador + captura a todo el ancho (alto según la captura)."""
    b = round(w * .036)
    iw, ih = tam(img)
    return w * ih / iw + b, (f'<div class="pant" style="width:{w}px">{navegador(dominio, b) if dominio else ""}'
                            f'<img src="{img}"><i class="reflejo"></i></div>')


def portatil(x, y, w, img, dominio, z=1):
    _, p = pantalla(img, dominio, w - 30)
    return f'<div class="lap" style="left:{x}px;top:{y}px;width:{w}px;z-index:{z}"><div class="tapa">{p}</div><div class="base"></div></div>'


def sobremesa(x, y, w, img, dominio, z=1):
    _, p = pantalla(img, dominio, w - 26)
    return (f'<div class="mon" style="left:{x}px;top:{y}px;width:{w}px;z-index:{z}"><div class="marco">{p}</div>'
            f'<div class="barbilla"></div><div class="cuello"></div><div class="pie"></div></div>')


def barra_estado(fondo, tinta):
    return (f'<div class="barra" style="background:{fondo};color:{tinta}"><span>9:41</span>'
            f'<b><i style="height:35%"></i><i style="height:55%"></i><i style="height:75%"></i><i style="height:100%"></i><u></u></b></div>')


def movil(x, y, w, img=None, dentro=None, z=3, giro=0):
    h = round(w * 2.06)
    if dentro is None:
        fondo, tinta = color_barra(img)
        dentro = barra_estado(fondo, tinta) + f'<img src="{img}">'
    bots = (f'<i class="bot" style="left:-6px;top:{h*.2:.0f}px;height:{h*.05:.0f}px"></i>'
            f'<i class="bot" style="left:-6px;top:{h*.29:.0f}px;height:{h*.085:.0f}px"></i>'
            f'<i class="bot" style="left:-6px;top:{h*.4:.0f}px;height:{h*.085:.0f}px"></i>'
            f'<i class="bot" style="right:-6px;top:{h*.31:.0f}px;height:{h*.12:.0f}px"></i>')
    return (f'<div class="mov" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;z-index:{z};transform:rotate({giro}deg)">{bots}'
            f'<div class="pant">{dentro}<i class="reflejo"></i></div><i class="isla"></i></div>')


def recorte(n, caja, nombre, tapar=(), escala=1):
    os.makedirs(TMP, exist_ok=True)
    im = Image.open(os.path.join(CRUDO, n)).convert("RGB")
    dr = ImageDraw.Draw(im)
    for c in tapar:
        # color de fondo: el más repetido en una franja justo debajo de la zona tapada
        franja = im.crop((c[0], c[3] + 1, c[2], c[3] + 8)).getcolors(4096) or [(1, im.getpixel((c[0] - 3, c[3] + 3)))]
        dr.rectangle(c, fill=max(franja)[1])
    d = os.path.join(TMP, nombre)
    im = im.crop(caja)
    if escala > 1:   # capturas de 800 px en pantallas grandes: Lanczos + enfoque suave
        from PIL import ImageFilter
        im = im.resize((im.width * escala, im.height * escala), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=1.6, percent=110, threshold=2))
    im.save(d, quality=95)
    return "file://" + d


def hoja_ficha(n, cajas, nombre):
    """La ficha del panel de Maps, hecha con uno o varios recortes apilados (así se quitan las partes que solo ve
    el dueño: «Gestionar tu Perfil», visualizaciones, «Empezar a anunciar»)."""
    from PIL import ImageFilter
    im = Image.open(os.path.join(CRUDO, n)).convert("RGB")
    trozos = [im.crop(c) for c in cajas]
    w = max(t.width for t in trozos)
    out = Image.new("RGB", (w, sum(t.height for t in trozos)), "white")
    y = 0
    for t in trozos:
        out.paste(t, (0, y)); y += t.height
    out = out.resize((out.width * 2, out.height * 2), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=1.4, percent=90, threshold=2))
    os.makedirs(TMP, exist_ok=True)
    d = os.path.join(TMP, nombre); out.save(d, quality=95)
    return "file://" + d


def movil_mapa(n, pin, hojas, slug):
    """Google Maps en el móvil (capturas de Maps de Álvaro, 1.920 × 919): arriba el mapa real alrededor del pin
    del negocio, con su nombre; abajo, la ficha abierta como hoja deslizable."""
    px, py = pin
    mapa = recorte(n, (px - 165, py - 250, px + 235, py + 170), f"{slug}-mapa.jpg", escala=2)
    hoja = hoja_ficha(n, hojas, f"{slug}-hoja.jpg")
    return (barra_estado("transparent", "#111")
            + f'<div class="mapa"><img src="{mapa}" style="left:0;top:0;width:100%;height:auto"></div>'
            + f'<div class="hoja"><img src="{hoja}" style="padding-top:12px"></div>')


# Ficha de cada caso en Maps: (captura, pin del negocio, recortes del panel de arriba abajo)
MAPAS = {
    "marcos": ("maps-marcos-cerrajeros.png", (1414, 442), [(72, 252, 474, 700)]),
    "dotti": ("maps-dotti.png", (1200, 442), [(72, 252, 474, 690)]),
    "balgas": ("maps-balgas.png", (1200, 442), [(72, 255, 474, 372), (72, 466, 474, 514), (72, 656, 474, 900)]),
}


def mm(slug):
    n, pin, hojas = MAPAS[slug]
    return movil_mapa(n, pin, hojas, slug)


def hd(n, caja):
    """Captura HD recortada (la columna de la web, sin fondo lateral ni aviso de cookies)."""
    os.makedirs(TMP, exist_ok=True)
    d = os.path.join(TMP, n + "-recorte.png")
    Image.open(os.path.join(CRUDO + "-hd", n + ".png")).convert("RGB").crop(caja).save(d)
    return "file://" + d


def obj(n, x, y, w, rot=0, z=4):
    return f'<img class="obj" src="{objeto(n)}" style="left:{x}px;top:{y}px;width:{w}px;z-index:{z};transform:rotate({rot}deg)">'


def suelo(x, y, w, h=34, op=1):
    return f'<i class="suelo" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;opacity:{op}"></i>'


def composiciones():
    C = {}
    C["escaparate-balgas"] = (F_CREMA,
        resplandor(600, 640, 420, "#E6D9CB", .9) + suelo(150, 610, 880, 30, .55)
        + portatil(130, 86, 820, ruta("balgas-escritorio.jpg"), "reparacioncalderasbalgas.es")
        + movil(872, 196, 212, dentro=mm("balgas"))
        + obj("cursor", 1010, 34, 150, -10, 1))
    C["escaparate-marcos-cerrajeros"] = (F_BERENJENA,
        resplandor(820, 300, 330, "#E0067A", .5) + suelo(150, 610, 880, 30, .7)
        + portatil(110, 86, 820, ruta("marcos-cerrajeros-escritorio.jpg"), "marcoscerrajeros.es")
        + movil(856, 196, 212, dentro=mm("marcos"))
        + obj("estrella-cromo", 40, 470, 170, -10, 4))
    C["escaparate-aquita"] = (F_ROSA,
        resplandor(560, 300, 360, "#FFFFFF", .55) + suelo(320, 640, 520, 22, .5)
        + sobremesa(170, 18, 760, ruta("aquita-escritorio.jpg"), "aquita.es")
        + movil(860, 214, 190, ruta("aquita-movil.jpg"))
        + obj("chincheta", 26, 300, 190, -6, 4))
    C["escaparate-las-tejas"] = (F_BERENJENA,
        resplandor(420, 260, 360, "#FF7AB8", .28) + suelo(380, 640, 520, 22, .7)
        + sobremesa(260, 18, 760, ruta("las-tejas-escritorio.jpg"), "restaurantelastejas.es")
        + movil(120, 210, 190, ruta("las-tejas-movil.jpg"))
        + obj("estrella", 1040, 470, 140, 10, 4))
    C["escaparate-solvento"] = (F_MALVA,
        simbolo_marca(-40, 60, 600, "#FFFFFF", .45) + resplandor(700, 260, 300, "#FFFFFF", .5) + suelo(380, 640, 520, 22, .45)
        + sobremesa(270, 18, 760, hd("solvento-v2-escritorio", (0, 0, 1904, 919)), "solvento.es")   # web v2 (03/10)
        + movil(130, 210, 190, "file://" + os.path.join(CRUDO, "solvento-v2-movil.jpg"))
        + obj("abanico", 1030, 40, 140, 8, 4))
    C["escaparate-rfg-andrade"] = (F_FUCSIA,
        simbolo_marca(640, -80, 760, "#FF5AAB", .32) + suelo(150, 610, 880, 30, .6)
        + portatil(120, 86, 820, ruta("rfg-andrade-escritorio.jpg"), "rfgandrade.es")
        + movil(872, 226, 196, ruta("rfg-andrade-movil.jpg"))
        + obj("bocadillo", 1010, 40, 140, 6, 1))
    busq = recorte("dotti-busqueda-google.jpg", (0, 0, 800, 505), "dotti-busqueda.jpg", tapar=[(752, 0, 800, 34)], escala=2)
    C["escaparate-dotti-peluqueria"] = (F_BERENJENA,
        resplandor(760, 300, 330, "#E0067A", .5) + suelo(90, 560, 700, 26, .6)
        + portatil(70, 92, 680, busq, "google.com")
        + movil(760, 70, 262, dentro=mm("dotti"), z=3)
        + obj("chincheta", 1040, 330, 150, 10, 4))
    # --- v5.7 · Los trabajos que estaban solo en la galería de la portada (GALERIA_EXTRA) ---
    C["escaparate-jif-2026"] = (F_BERENJENA,
        resplandor(500, 260, 360, "#E0067A", .35) + suelo(380, 640, 520, 22, .7)
        + sobremesa(250, 18, 760, ruta("jif-2026-escritorio.jpg"), "jif26.es")
        + movil(110, 210, 190, ruta("jif-2026-movil.jpg"))
        + obj("estrella-cromo", 1030, 460, 150, 10, 4))
    C["escaparate-vinos-pousada"] = (F_CREMA,
        resplandor(600, 640, 420, "#E6D9CB", .9) + suelo(170, 600, 860, 30, .55)
        + portatil(160, 70, 880, hd("vinos-pousada-escritorio", (0, 0, 1904, 919)), "vinospousada.es")
        + obj("abanico", 1040, 400, 140, 8, 4))
    C["escaparate-psicorazon"] = (F_ROSA,
        resplandor(600, 300, 380, "#FFFFFF", .55) + suelo(170, 600, 860, 30, .5)
        + portatil(160, 70, 880, ruta("psicorazon-escritorio.jpg"), "psicorazon.com")
        + obj("bocadillo", 40, 420, 150, -8, 4))
    C["escaparate-expertise"] = (F_FUCSIA,
        simbolo_marca(700, -60, 760, "#FF5AAB", .32) + suelo(330, 640, 540, 22, .6)
        + sobremesa(250, 22, 700, hd("expertise-escritorio", (225, 0, 1695, 880)), "expertise.es")
        + obj("cursor", 1010, 60, 140, -10, 4))
    C["escaparate-delfinia"] = (F_MALVA,
        resplandor(600, 280, 360, "#FFFFFF", .5) + suelo(350, 640, 500, 22, .45)
        + sobremesa(290, 18, 620, hd("delfinia-escritorio", (298, 0, 1608, 840)), "delfiniapiscinas.com")
        + obj("estrella", 1000, 440, 150, 10, 4))
    return C


def main(nombres):
    from playwright.sync_api import sync_playwright
    os.makedirs(SALIDA, exist_ok=True); os.makedirs(TMP, exist_ok=True)
    C = composiciones()
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=2)
        for n in (nombres or list(C)):
            fondo, piezas = C[n]
            html = (f"<!doctype html><html><head><meta charset=utf-8><style>{CSS}</style></head><body>"
                    f'<div class="lienzo"><div class="fondo" style="background:{fondo}"></div>{piezas}</div></body></html>')
            f = os.path.join(TMP, n + ".html"); open(f, "w", encoding="utf-8").write(html)
            pg.goto("file://" + f); pg.wait_for_load_state("networkidle"); pg.wait_for_timeout(150)
            tmp = os.path.join(TMP, n + ".png"); pg.screenshot(path=tmp)
            im = Image.open(tmp).convert("RGB")
            im.save(os.path.join(SALIDA, n + ".jpg"), quality=92)
            print(n, im.size)
        b.close()


if __name__ == "__main__":
    main(sys.argv[1:])
