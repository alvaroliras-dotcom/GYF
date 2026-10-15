# -*- coding: utf-8 -*-
"""GYF · v5.11 · Portfolio: /trabajos/ (rejilla desfasada o lista, con filtros por servicio) y /trabajos/<slug>/
(ficha por bloques: portada tipográfica, ficha + entradilla, maqueta a sangre, cómo estaba, qué hicimos, la web en un
navegador, el móvil, la ficha en Maps, resultado, llamada y siguiente trabajo). Estructura de ajaestudio.com
(004-AJA, §10), piel de GYF. Los datos, en trabajos.py."""
import html, re
import plantilla as T
import config as C
from datos import esc
from trabajos import TRABAJOS, FILTROS

A = lambda x: html.escape(str(x), quote=True)
D = C.DOMINIO
ETQ = dict(FILTROS)
URL_HUB = "/trabajos/"


def url_de(t):
    return f"{URL_HUB}{t['slug']}/"


def migas(cad):
    li = [f'<li><a href="{u}">{esc(n)}</a></li>' if i < len(cad) - 1 else f'<li aria-current="page">{esc(n)}</li>' for i, (u, n) in enumerate(cad)]
    return f'<nav class="migas" aria-label="Migas de pan"><ol>{"".join(li)}</ol></nav>'


def breadcrumb_schema(cad):
    return {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": D + u}
                                                           for i, (u, n) in enumerate(cad)]}


def areas(t):
    return " · ".join(ETQ[s] for s in t["servicios"] if s in ETQ)


def og(cab, imagen):
    """La imagen para redes de estas páginas es su maqueta (rematar.py no genera /og/ para ellas)."""
    base = imagen.rsplit(".", 1)[0]
    return re.sub(r'(<meta (?:property="og:image"|name="twitter:image") content=")[^"]+(")', rf'\g<1>{D}/img/{base}-1200.jpg\g<2>', cab)


def cabeza(url, titulo, meta, schema, imagen):
    p = {"url": url, "title": titulo, "meta": meta, "h1": titulo}
    return og(T.cabeza(p, schema, "index, follow"), imagen)


def navegador(img, dominio, alt, enlace=None, pie=None, clase=""):
    w, h = T.medida(img)
    foto = T.foto(img, alt, "(max-width: 900px) 94vw, 1200px", clase="pf-nav__foto")
    cap = ""
    if pie or enlace:
        ir = f'<a class="pf-nav__ir" href="{A(enlace)}" rel="noopener" target="_blank">{esc(dominio)} {T.ico("flecha-diagonal")}</a>' if enlace else ""
        cap = f'<figcaption class="pf-nav__pie"><span>{esc(pie or "")}</span>{ir}</figcaption>'
    return (f'<figure class="pf-nav {clase}"><div class="pf-nav__marco"><div class="pf-nav__barra" aria-hidden="true"><i></i><i></i><i></i>'
            f'<span>{esc(dominio)}</span></div><div class="pf-nav__ventana" style="aspect-ratio:{w}/{h}">{foto}</div></div>{cap}</figure>')


def movil(img, alt):
    return (f'<div class="pf-movil"><div class="pf-movil__marco"><i class="pf-movil__isla" aria-hidden="true"></i>'
            f'<div class="pf-movil__pant">{T.foto(img, alt, "340px", clase="pf-movil__foto")}</div></div></div>')


# ---------- /trabajos/ ----------
def pagina_hub():
    url = URL_HUB
    n = len(TRABAJOS)
    cuenta = {k: sum(1 for t in TRABAJOS if k in t["servicios"]) for k, _ in FILTROS}
    filtros = (f'<button class="pf-filtro is-on" type="button" data-pf-filtro="todos" aria-pressed="true">Todos<sup>{n}</sup></button>'
               + "".join(f'<button class="pf-filtro" type="button" data-pf-filtro="{k}" aria-pressed="false">{esc(e)}<sup>{cuenta[k]}</sup></button>'
                         for k, e in FILTROS if cuenta[k]))
    items = []
    for i, t in enumerate(TRABAJOS):
        lugar = t.get("municipio") or t.get("relacion") or ""
        frase = f'<p class="pf-item__frase">{esc(t["frase"])}</p>' if t.get("frase") else ""
        cl = (" par" if i % 2 else "") + (" cuadrada" if i % 3 == 1 else "")
        items.append(f"""<li class="pf-item{cl}" data-pf-item data-servicios="{' '.join(t['servicios'])}">
   <a class="pf-item__enlace" href="{url_de(t)}">
    <div class="pf-item__media">{T.foto(t['imagenes']['tarjeta'], f"{t['nombre']}: {areas(t)}", "(max-width: 700px) 92vw, 45vw", clase="pf-item__foto")}</div>
    <div class="pf-item__meta"><span class="pf-item__num">{i + 1:02d}</span><h2 class="pf-item__nombre">{esc(t['nombre'])}</h2><span class="pf-item__lugar">{esc(lugar)}</span>{frase}<p class="pf-item__areas">{esc(areas(t))}</p></div>
   </a>
  </li>""")
    cad = [("/", "Inicio"), (url, "Trabajos")]
    schema = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "url": D + url, "name": "Trabajos de El Gordo y el Flaco",
         "hasPart": [{"@type": "CreativeWork", "name": t["nombre"], "url": D + url_de(t)} for t in TRABAJOS]},
        breadcrumb_schema(cad)]}
    cab = cabeza(url, "Trabajos: webs, fichas de Google y marcas | GYF",
                 "Una muestra de nuestros trabajos para negocios de Alcorcón y alrededores: webs, fichas de Google, Google Ads e imagen de marca.",
                 schema, TRABAJOS[0]["imagenes"]["maqueta"])
    cuerpo = f"""<main id="contenido" class="pf">
<section class="pf-hub-cab"><div class="contenedor">
 {migas(cad)}
 <p class="etiqueta">{T.simbolo("etiqueta__sim")}Trabajos</p>
 <h1 class="pf-hub-cab__tit">Trabajos<sup class="pf-hub-cab__n">({n})</sup> <span class="gris">con nombre y apellidos.</span></h1>
 <p class="pf-hub-cab__txt">Una muestra de lo que hacemos: webs, fichas de Google, anuncios e imagen de marca para negocios de Alcorcón y alrededores.</p>
</div></section>
<section class="pf-hub" data-pf><div class="contenedor">
 <div class="pf-barra"><div class="pf-filtros" role="group" aria-label="Filtrar por servicio">{filtros}</div>
  <div class="pf-vistas" role="group" aria-label="Vista"><button class="pf-vista is-on" type="button" data-pf-vista="rejilla" aria-pressed="true">Rejilla</button><button class="pf-vista" type="button" data-pf-vista="lista" aria-pressed="false">Lista</button></div></div>
 <p class="sr" aria-live="polite" data-pf-estado></p>
 <ol class="pf-lista is-rejilla" data-pf-lista>
  {"".join(items)}
 </ol>
</div></section>
{llamada()}
</main>"""
    return cab + T.cabecera(url) + cuerpo + T.pie()


# ---------- /trabajos/<slug>/ ----------
def llamada():
    return f"""<section class="pf-cta"><div class="contenedor pf-cta__in">
 <h2 class="pf-cta__tit">¿Quiere lo mismo <span class="gris">para su negocio?</span></h2>
 <p class="pf-cta__txt">La primera reunión es en su negocio y sin coste. Quien le coge el teléfono es quien lleva su proyecto.</p>
 <div class="acciones">{T.btn_llamar(extra=' data-zona="portfolio"')}{T.btn_whatsapp("btn--linea")}</div>
</div></section>"""


def bloque_texto(etq, tit, txt):
    p = f'<p class="pf-texto__p">{esc(txt)}</p>' if txt else ""
    return f'<section class="pf-b pf-texto"><div class="contenedor pf-rej"><p class="pf-etq">{esc(etq)}</p><div class="pf-texto__cuerpo"><h2 class="pf-texto__tit">{esc(tit)}</h2>{p}</div></div></section>'


def filas(n, maximo):
    """Reparte n piezas en filas equilibradas de como mucho `maximo`, sin ninguna fila huérfana (7 → 4+3, 5 → 3+2)."""
    k = -(-n // maximo)
    base, extra = divmod(n, k)
    return [base + (1 if i < extra else 0) for i in range(k)]


def galeria(items):
    anchas = [x for x in items if x[3] == "ancha"]
    chicas = [x for x in items if x[3] != "ancha"]

    def fig(f, alt, pie, forma, sz):
        return (f'<figure class="pf-gal__it pf-gal__it--{forma}">{T.foto(f, alt, sz, clase="pf-gal__foto")}'
                f'<figcaption>{esc(pie)}</figcaption></figure>')
    out = []
    for lista, maximo, tipo, sz in ((anchas, 3, "ancha", "(max-width: 700px) 92vw, 420px"), (chicas, 4, "chica", "(max-width: 700px) 46vw, 320px")):
        i = 0
        for n in filas(len(lista), maximo) if lista else []:
            fs = "".join(fig(*x, sz) for x in lista[i:i + n]); i += n
            out.append(f'<div class="pf-gal__fila pf-gal__fila--{tipo}" style="--n:{n}">{fs}</div>')
    return (f'<section class="pf-b pf-gal"><div class="contenedor"><div class="pf-rej pf-piezas__cab"><p class="pf-etq">Las piezas</p>'
            f'<h2 class="pf-piezas__tit">Lo que se ve en la calle.</h2></div><div class="pf-gal__rej">{"".join(out)}</div></div></section>')


# ---------- v5.20 · ficha a medida: secciones con fondo propio, en los colores de la marca del cliente ----------
def _fig(f, alt, pie=None, clase="", sizes="(max-width: 800px) 100vw, 50vw", pos=None):
    cap = f"<figcaption>{esc(pie)}</figcaption>" if pie else ""
    estilo = f' style="--pos:{pos}"' if pos else ""
    return f'<figure class="pv-fig {clase}"{estilo}>{T.foto(f, alt, sizes)}{cap}</figure>'


def _cab_pv(etq, tit):
    return f'<div class="pf-rej pv__cab"><p class="pf-etq">{esc(etq)}</p><h2 class="pv__tit">{esc(tit)}</h2></div>'


def b_marca(b, t):
    return (f'<section class="pv pv--fondo"><div class="contenedor">{_cab_pv(b["etq"], b["tit"])}'
            f'<div class="pv-marca">{_fig(*b["positivo"], clase="pv-fig--blanco")}{_fig(*b["negativo"])}</div></div></section>')


def b_par(b, t):
    figs = "".join(_fig(f, alt, pie, "pv-fig--43") for f, alt, pie in b["fotos"])
    return (f'<section class="pv pv--sin-pad-inf"><div class="contenedor">{_cab_pv(b["etq"], b["tit"])}</div>'
            f'<div class="pv-par">{figs}</div></section>')


def b_split(b, t):
    figs = "".join(_fig(f, alt, None, "", "(max-width: 900px) 50vw, 30vw", pos=pos) for f, alt, pos in b["fotos"])
    return (f'<section class="pv-split"><div class="pv-split__txt"><p class="pv-split__etq">{esc(b["etq"])}</p>'
            f'<h2 class="pv-split__tit">{esc(b["tit"])}</h2><p class="pv-split__pie">{esc(b["pie"])}</p></div>'
            f'<div class="pv-split__fotos">{figs}</div></section>')


def b_papeleria(b, t):
    f, alt, pie = b["bodegon"]
    ha, hb = b["hojas"]
    hoja = lambda h, k: f'<figure class="pv-hoja pv-hoja--{k}">{T.foto(h[0], h[1], "(max-width: 900px) 40vw, 240px")}</figure>'
    lista = "".join(f"<li>{esc(x)}</li>" for x in b["lista"])
    return (f'<section class="pv pv--crema"><div class="contenedor">{_cab_pv(b["etq"], b["tit"])}'
            f'<div class="pv-pap"><div>{_fig(f, alt, None, "pv-pap__bodegon", "(max-width: 900px) 100vw, 58vw")}<p class="pv-pap__pie">{esc(pie)}</p></div>'
            f'<div class="pv-pap__hojas">{hoja(ha, "a")}{hoja(hb, "b")}</div></div>'
            f'<ul class="pv-pap__lista">{lista}</ul></div></section>')


def b_sangre(b, t):
    f, alt, pie = b["foto"]
    return (f'<section class="pv-sangre">{T.foto(f, alt, "100vw")}<span class="pv-sangre__velo" aria-hidden="true"></span>'
            f'<div class="contenedor pv-sangre__txt"><p class="pv-sangre__etq">{esc(b["etq"])}</p><p class="pv-sangre__pie">{esc(pie)}</p></div></section>')


def b_web(b, t):
    im, nom = t["imagenes"], t["nombre"]
    mov = f'<div class="pv-web__movil">{movil(im["movil"], "Web de " + nom + " en el móvil")}</div>' if im.get("movil") else ""
    nav = navegador(im["web"], t["dominio"], "Web de " + nom + " en el ordenador", t["url"], "La web, en el ordenador.")
    return (f'<section class="pv pv--claro"><div class="contenedor">{_cab_pv(b["etq"], b["tit"])}<div class="pv-web">{nav}{mov}</div>'
            f'<p class="pv-web__pie">{esc(b["pie"])}</p></div></section>')


BLOQUES = {"marca": b_marca, "par": b_par, "split": b_split, "papeleria": b_papeleria, "sangre": b_sangre, "web": b_web}


def bloques_a_medida(t):
    return [BLOQUES[b["tipo"]](b, t) for b in t["bloques"]]


def pagina_caso(i, t):
    url = url_de(t)
    a_medida = bool(t.get("bloques"))
    im = t["imagenes"]
    sig = TRABAJOS[(i + 1) % len(TRABAJOS)]
    cad = [("/", "Inicio"), (URL_HUB, "Trabajos"), (url, t["nombre"])]
    lugar = t.get("municipio")
    frase = f'<p class="pf-caso-cab__frase">{esc(t["frase"])}</p>' if t.get("frase") else ""
    ficha = [("Cliente", esc(t["nombre"]))]
    if lugar:
        ficha.append(("Dónde", esc(lugar)))
    if t.get("relacion"):
        ficha.append(("Cuándo", esc(t["relacion"])))
    ficha.append(("Qué hicimos", "<br>".join(esc(ETQ[s]) for s in t["servicios"] if s in ETQ)))
    dl = "".join(f"<div><dt>{a}</dt><dd>{b}</dd></div>" for a, b in ficha)
    entrada = f'<p class="pf-intro__lead">{esc(t["entrada"])}</p>' if t.get("entrada") else ""
    nom = t["nombre"]
    alt_maq = f"{nom}: maqueta de su trabajo"
    bloques = [f'<section class="pf-b pf-media{" pf-media--foto" if t.get("galeria") else ""}"><div class="pf-media__marco">{T.foto(im["maqueta"], alt_maq, "100vw", prioridad=True, clase="pf-media__foto")}</div></section>']
    if t.get("dato"):
        num, txt = t["dato"]
        bloques.append(f'<section class="pf-b pf-dato"><div class="contenedor pf-rej"><p class="pf-etq">El resultado</p><div class="pf-dato__cuerpo"><p class="pf-dato__num">{esc(num)}</p><p class="pf-dato__txt">{esc(txt)}</p></div></div></section>')
    if t.get("partida"):
        bloques.append(bloque_texto("Cómo estaba", *t["partida"]))
    piezas = "".join(f'<li class="pf-pieza"><span class="pf-pieza__n">{k + 1:02d}</span><h3 class="pf-pieza__nombre">{esc(n)}</h3>'
                     f'{("<p class=pf-pieza__txt>" + esc(l) + "</p>") if l else ""}</li>' for k, (n, l) in enumerate(t["piezas"]))
    if len(t["piezas"]) > 1 or t.get("galeria"):
      bloques.append(f'<section class="pf-b pf-piezas"><div class="contenedor"><div class="pf-rej pf-piezas__cab"><p class="pf-etq">Qué hicimos</p>'
                   f'<h2 class="pf-piezas__tit">{"Todo, con un solo interlocutor." if len(t["piezas"]) > 1 else "Una sola pieza, bien hecha."}</h2></div>'
                   f'<ol class="pf-piezas__lista">{piezas}</ol></div></section>')
    if a_medida:
        bloques.extend(bloques_a_medida(t))
    elif t.get("galeria"):
        bloques.append(galeria(t["galeria"]))
    if t.get("frase_suelta"):
        bloques.append(f'<section class="pf-b pf-suelta"><div class="contenedor"><p class="pf-suelta__txt">{esc(t["frase_suelta"])}</p></div></section>')
    if im.get("web") and not a_medida:
        bloques.append(f'<section class="pf-b"><div class="contenedor">{navegador(im["web"], t["dominio"], "Web de " + nom + " en el ordenador", t["url"], "La web, en el ordenador.")}</div></section>')
    if im.get("movil") and not a_medida:
        bloques.append(f'<section class="pf-b pf-movil-b"><div class="contenedor pf-rej"><p class="pf-etq">En el móvil</p><div class="pf-movil-b__fila">{movil(im["movil"], "Web de " + nom + " en el móvil")}'
                       f'<p class="pf-movil-b__txt">Pensada primero para el móvil, que es desde donde le buscan y le llaman.</p></div></div></section>')
    if im.get("mapa"):
        bloques.append(f'<section class="pf-b"><div class="contenedor pf-rej pf-mapa-cab"><p class="pf-etq">Google Maps</p><h2 class="pf-texto__tit">Su ficha de Google.</h2></div>'
                       f'<div class="contenedor">{navegador(im["mapa"], "google.com/maps", "Ficha de Google de " + nom + " en Google Maps", None, "Captura de Google Maps.")}</div></section>')
    if t.get("resultado"):
        lis = "".join(f"<li>{esc(r)}</li>" for r in t["resultado"])
        fuente = f'<p class="pf-res__fuente">{esc(t["fuente_resultado"])}</p>' if t.get("fuente_resultado") else ""
        bloques.append(f'<section class="pf-b pf-res"><div class="contenedor pf-rej"><p class="pf-etq">Resultado</p><div class="pf-res__cuerpo"><ul class="pf-res__lista">{lis}</ul>{fuente}</div></div></section>')
    siguiente = f"""<section class="pf-sig"><a class="pf-sig__enlace" href="{url_de(sig)}">
 <div class="pf-sig__media">{T.foto(sig['imagenes']['maqueta'], f"{sig['nombre']}: maqueta de su trabajo", "100vw", clase="pf-sig__foto")}</div><span class="pf-sig__velo" aria-hidden="true"></span>
 <div class="contenedor pf-sig__txt"><p class="etiqueta">Siguiente trabajo</p><p class="pf-sig__nombre">{esc(sig['nombre'])}</p>{T.ico("flecha-diagonal", "pf-sig__ico")}</div>
</a></section>"""
    schema = {"@context": "https://schema.org", "@graph": [
        {"@type": "CreativeWork", "@id": D + url + "#trabajo", "name": f"{t['nombre']}: {areas(t)}", "url": D + url,
         "creator": {"@id": D + "/#negocio"}, "about": {"@type": "Organization", "name": t["nombre"], **({"url": t["url"]} if "google.com" not in t["url"] else {})},
         **({"locationCreated": {"@type": "Place", "name": lugar}} if lugar else {}),
         "image": f"{D}/img/{im['maqueta'].rsplit('.', 1)[0]}-1600.jpg"},
        breadcrumb_schema(cad)]}
    titulo = f"{t['nombre']}: {areas(t).lower().replace(' · ', ', ')}" + (f" en {lugar}" if lugar else "") + " | GYF"
    base = t.get("entrada") or f"{t['nombre']}: {areas(t).lower().replace(' · ', ', ')}" + (f" en {lugar}." if lugar else ".")
    meta = base if len(base) >= 120 else base + " Un trabajo de El Gordo y el Flaco, agencia SEO y de marketing en Alcorcón."
    if len(meta) > 158:
        meta = meta[:155].rsplit(" ", 1)[0] + "…"
    if len(titulo) < 35:
        titulo = titulo.replace(" | GYF", " | El Gordo y el Flaco")
    tm = t.get("tema") or {}
    vestido = (f' data-vestido style="--cl-fondo:{tm.get("fondo", "#1C1219")};--cl-tono:{tm.get("tono", "#E0067A")};--cl-claro:{tm.get("claro", "#F5F1EC")}"'
               if a_medida else "")
    cuerpo = f"""<main id="contenido" class="pf pf-caso"{vestido}>
<section class="pf-caso-cab"><div class="contenedor">
 {migas(cad)}
 <p class="etiqueta">{T.simbolo("etiqueta__sim")}Trabajo {i + 1:02d}{f" · {esc(lugar)}" if lugar else ""}</p>
 <h1 class="pf-caso-cab__nombre">{esc(t['nombre'])}</h1>
 {frase}
</div></section>
<section class="pf-intro"><div class="contenedor pf-rej"><dl class="pf-intro__ficha">{dl}</dl>{entrada}</div></section>
{"".join(bloques)}
{llamada()}
{siguiente}
</main>"""
    return cabeza(url, titulo, meta, schema, im["maqueta"]) + T.cabecera(url) + cuerpo + T.pie()


def paginas():
    """[(url, html)] del portfolio."""
    out = [(URL_HUB, pagina_hub())]
    out += [(url_de(t), pagina_caso(i, t)) for i, t in enumerate(TRABAJOS)]
    return out
