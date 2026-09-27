# -*- coding: utf-8 -*-
"""GYF-Rayo · CONFIGURACIÓN · WEB DE EL GORDO Y EL FLACO (elgordoyelflaco.es) · v2 (color, cajas, objetos 3D y movimiento de Rayo).
Datos de la ficha de Google (mandan sobre cualquier otro). Textos: textos-v2 (Merche). Reseñas reales en
contenido/resenas.json. Arquitectura y 301: nuria2/arquitectura.md (sección c). Caso E: todo es nuevo.
Lo que falta confirmar está marcado [PENDIENTE] y sale como aviso en controles.py.
"""

VERSION = "4"

# ---------- Sitio ----------
DOMINIO = "https://elgordoyelflaco.es"
HOST_PRODUCCION = ("elgordoyelflaco.es", "www.elgordoyelflaco.es")
GTM_ID = "GTM-PM84H37"
COOKIES_CLAVE = "gyf-cookies"
COLOR_TEMA = "#FAF7F6"
from redirecciones import REDIRECCIONES, REDIRECCIONES_302, GONE_410, GONE_410_PATRONES   # nuria2/arquitectura.md §c
GA4_ID = "G-LG8DGCHZMK"      # va DENTRO del GTM heredado; la web no carga gtag por su cuenta
CONTACTO_INDEXABLE = True

FUENTES_PRECARGA = ["outfit-600.woff2", "outfit-400.woff2"]

# ---------- Negocio (ficha de Google) ----------
NEGOCIO = {
    "nombre": "El Gordo y el Flaco",
    "nombre_largo": "El Gordo y el Flaco MKonline",
    "razon_social": "El Gordo y el Flaco MKonline",       # nombre comercial (pie). El titular y el NIF, SOLO en los legales
    "telefono": "670 78 19 40",
    "telefono_e164": "+34670781940",
    "whatsapp": "34670781940",
    "email": "info@elgordoyelflaco.es",
    "calle": "Av. del Alcalde José Aranda, 51",
    "cp": "28924",
    "localidad": "Alcorcón",
    "provincia": "Madrid",
    "region": "Madrid",
    "horario_texto": "De lunes a viernes, de 9:00 a 19:00",
    "horario_corto": "L-V · 9:00-19:00",
    "dias_texto": "Lunes a viernes",
    "abre": "09:00", "cierra": "19:00",
    "dias_schema": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
    "zona_horaria": "Europe/Madrid",
    # Festivos: «d/m» se repite cada año; «d/m/aaaa» solo ese año (traslados). Pascua: Jueves y Viernes Santo.
    # 2026: nacionales + Comunidad de Madrid (2/5, Jueves Santo, 2/11 y 7/12 por caer 1/11 y 6/12 en domingo).
    # [PENDIENTE] Los dos locales de Alcorcón: las fuentes no coinciden (8/9 en todas; el otro, 6/4 o 9/9).
    # Confirmar en el BOCM y añadirlos aquí; hasta entonces no se marcan (aviso en controles.py).
    "festivos": ["1/1", "6/1", "1/5", "2/5", "15/8", "12/10", "1/11", "6/12", "8/12", "25/12", "2/11/2026", "7/12/2026", "8/9", "6/4/2026"],  # locales de Alcorcón: 8/9 Virgen de los Remedios y 6/4/2026 (calendarios.ideal.es)
    "festivos_pascua": [-3, -2],
    "festivos_locales_pendientes": False,
    "valoracion": "5,0",
    "resenas": "11",
    "anios": "20",                      # años de oficio de la casa en publicidad
    "anios_marca": "15",                # Álvaro, paso 22: 15 años de agencia
    "garantia": "",
    "fundacion": None,
    "devuelve_llamada": None,
    "cambia_equipos": None,
    "cid": "10293855805443705389",
    "lat": 40.34983, "lng": -3.81639,   # ficha de Google (Matías, paso 5)
    "schema_tipo": "ProfessionalService",
    "servicio_tipo": "Agencia SEO y de marketing online",
    "precio": None,
    "pago": "Bizum, transferencia, tarjeta o efectivo",
    "knows_about": ["SEO local", "Google Business Profile", "Diseño web", "Google Ads", "Diseño gráfico", "Redacción publicitaria", "Analítica web"],
    "persona": None,  # Álvaro 26/09: la web es de la marca, sin persona en el schema
}

MARCA = {
    "simbolo": "simbolo-color.svg",
    "logo": "logo-horizontal-color.svg",
    "logo_ancho": 726, "logo_alto": 118,
    "logo_blanco": "logo-horizontal-blanco.svg",
    "og": "og-image-1200x630.jpg",
}

OBJETO_PORTADA = {
    "tipo": "3d",
    "imagen": "objeto-portada.png",
    "ancho": 840, "alto": 840,
    "alt": "",
    "video_webm": None, "video_mov": None,
    "svg_3d": "simbolo-3d.svg",
    "color_3d": "#E0067A",
    "color_unico": True,
    "en_banda": True,
}

URLS = {
    "hub": None,
    "municipio": "/agencia-seo-",
    "marca": None,
    "empresa": "/quienes-somos/",
    "contacto": "/contacto/",
}
MUNICIPIOS = [("/agencia-seo-getafe/", "Getafe"), ("/agencia-seo-mostoles/", "Móstoles"), ("/agencia-seo-leganes/", "Leganés"),
              ("/agencia-seo-fuenlabrada/", "Fuenlabrada"), ("/agencia-seo-majadahonda/", "Majadahonda"),
              ("/agencia-seo-boadilla-del-monte/", "Boadilla del Monte"), ("/agencia-seo-arroyomolinos/", "Arroyomolinos"),
              ("/agencia-seo-villaviciosa-de-odon/", "Villaviciosa de Odón"), ("/agencia-seo-pozuelo-de-alarcon/", "Pozuelo de Alarcón"),
              ("/agencia-seo-brunete/", "Brunete")]
PREFIJOS_MUNICIPIO = ["Agencia SEO en"]
MUNICIPIO_ANCLA = "Agencia SEO en {pueblo}"

SERVICIOS_HOME = [
    ("SEO local", "Ficha de Google, reseñas y publicaciones al día.", "/seo-local/", "seo-local", ["Ficha de Google", "Reseñas", "Publicaciones"], None),
    ("Auditoría SEO local", "Gratuita y por escrito: qué le frena, lo más grave primero.", "/auditoria-seo-local/", "auditoria", ["Ficha", "Web", "Informe escrito"], None),
    ("Diseño web", "Webs rápidas en el móvil, hechas para que le llamen.", "/diseno-web/", "diseno-web", ["Web estática", "Móvil", "Conversión"], None),
    ("Google Ads", "Anuncios en Google y en Maps para su zona.", "/google-ads/", "google-ads", ["Búsqueda", "Google Maps", "Cuenta a su nombre"], None),
    ("Diseño gráfico", "Logotipo, imagen de marca e imprenta.", "/diseno-grafico/", "diseno-grafico", ["Logotipo", "Marca", "Imprenta"], None),
    ("Redacción publicitaria", "Textos de web, ficha y anuncios.", "/redaccion-seo-copywriting/", "redaccion", ["Web", "Ficha", "Anuncios"], None),
    ("Analítica", "GA4, Search Console e informe mensual.", "/analitica-web/", "analitica", ["GA4", "Search Console", "Informe"], None),
]
SERVICIOS_SECCION = True
SERVICIOS_TITULO = "Lo que hacemos por su negocio"
SERVICIOS_TEXTO = "Ficha de Google, web y anuncios para negocios de Alcorcón y alrededores."
PASOS_ICONOS = ["paso-llamada", "paso-visita", "paso-auditoria", "paso-presupuesto", "paso-trabajo", "paso-mantenimiento"]
ICONO_URL = {u: ic for _, _, u, ic, _, _ in SERVICIOS_HOME}
ICONO_URL["/contacto/"] = "contacto"

MENU = [
    ("Inicio", "/"),
    ("Servicios", [(t, u) for t, _, u, _, _, _ in SERVICIOS_HOME]),
    ("Zonas", [(n, u) for u, n in MUNICIPIOS]),
    ("Quiénes somos", "/quienes-somos/"),
    ("Contacto", "/contacto/"),
]
NOMBRE_CORTO = {"/": "Inicio", "/quienes-somos/": "Quiénes somos", "/contacto/": "Contacto",
                **{u: t for t, _, u, _, _, _ in SERVICIOS_HOME}}

# Casos (v2): composiciones de estudio con las capturas reales (herramientas/maquetas/maquetas.py → recursos/casos/).
# (título, qué se hizo, imagen de la galería de la portada, enlace, formato de la galería v/h/g, imagen grande 16:10)
CASOS = [  # muestra local de este año (Álvaro 26/09)
    ("Balgas", "Web, ficha y Google Ads", "diseno-web-alcorcon-caso-balgas-vertical.jpg", None, "g", "diseno-web-alcorcon-caso-balgas.jpg"),
    ("Marcos Cerrajeros", "Ficha y web nueva", "diseno-web-alcorcon-caso-marcos-cerrajeros-movil.jpg", "https://www.marcoscerrajeros.es/", "v", "diseno-web-alcorcon-caso-marcos-cerrajeros.jpg"),
    ("Aquita", "Ficha y web desde cero", "diseno-web-arroyomolinos-caso-aquita-portatil.jpg", "https://aquita.es/", "h", "diseno-web-arroyomolinos-caso-aquita.jpg"),
    ("Las Tejas", "Web del restaurante", "diseno-web-alcorcon-caso-las-tejas-movil.jpg", "https://www.restaurantelastejas.es/", "v", "diseno-web-alcorcon-caso-las-tejas.jpg"),
    ("Solvento", "Imagen de marca y web", "diseno-web-caso-solvento-vertical.jpg", "https://solvento.es/", "g", "diseno-web-caso-solvento.jpg"),
    ("RFG Andrade", "Web", "diseno-web-caso-rfg-andrade-portatil.jpg", "https://www.rfgandrade.es/", "h", "diseno-web-caso-rfg-andrade.jpg"),
    ("Dotti Peluquería", "Ficha de Google", "seo-local-caso-dotti-peluqueria-movil.jpg", None, "v", "seo-local-caso-dotti-peluqueria.jpg"),
]
# Etiquetas de cada caso en la lista grande de «Lo más reciente» (lo que se hizo, en píldoras)
CASOS_ETQ = {"Balgas": ["Web", "Ficha de Google", "Google Ads"], "Marcos Cerrajeros": ["Ficha de Google", "Web"],
             "Aquita": ["Ficha de Google", "Web"], "Las Tejas": ["Web"], "Solvento": ["Imagen de marca", "Rotulación", "Web"], "RFG Andrade": ["Web"],
             "Dotti Peluquería": ["Ficha de Google"]}
CASOS_VER = "Ver la web"
# v4 · Cada trabajo puede estar en varias categorías (Álvaro 27/09: «algunos entran en varias»). Las categorías son las
# URLs de los servicios. Sirve para elegir el caso de cada página cuando no lo fija CASO_URL y será la base del filtro
# del portfolio. Delfinia y Pousada entrarán en la galería cuando tengan capturas.
CASOS_CATEGORIAS = {
    "Balgas": ["/diseno-web/", "/seo-local/", "/google-ads/", "/analitica-web/"],
    "Marcos Cerrajeros": ["/seo-local/", "/diseno-web/", "/auditoria-seo-local/", "/analitica-web/"],
    "Aquita": ["/seo-local/", "/diseno-web/", "/auditoria-seo-local/"],
    "Las Tejas": ["/diseno-web/", "/redaccion-seo-copywriting/"],
    "Solvento": ["/diseno-grafico/", "/diseno-web/"],
    "RFG Andrade": ["/diseno-web/", "/redaccion-seo-copywriting/"],
    "Dotti Peluquería": ["/seo-local/"],
    "Delfinia Piscinas": ["/diseno-grafico/"],
    "Vinos Gallegos Pousada": ["/diseno-grafico/", "/diseno-web/"],
}

CINTA_PORTADA = ["Alcorcón", "SEO local", "Google Maps", "Webs que llaman"]
CINTA_SECUNDARIA = None

# ---------- v2 · Objetos 3D de la marca (herramientas/objetos3d/master → sitio/img/obj/) ----------
# Objeto de cada servicio (tarjetas apiladas de la home, cabecera de su página y tarjetas de «Otros servicios»)
OBJETO_URL = {"/seo-local/": "chincheta", "/auditoria-seo-local/": "lupa", "/diseno-web/": "simbolo-despiece",
              "/google-ads/": "cursor", "/diseno-grafico/": "abanico", "/redaccion-seo-copywriting/": "bocadillo",
              "/analitica-web/": "barras", "/quienes-somos/": "simbolo-cromo", "/contacto/": "bocadillo"}
# v3 · objetos «casi todo fucsia»: van sobre berenjena o crema, nunca sobre fucsia
OBJETOS_FUCSIA = {"chincheta", "cursor", "barras", "estrella", "simbolo-fucsia", "simbolo-fucsia-perfil", "simbolo-despiece", "simbolo-cerca"}
OBJETO_MUNICIPIO = "chincheta"
# Caso que acompaña a cada página interior (foto dentro de la columna de lectura, tras el segundo bloque)
CASO_URL = {"/seo-local/": "Dotti Peluquería", "/auditoria-seo-local/": "Marcos Cerrajeros", "/diseno-web/": "Balgas",
            "/google-ads/": "Balgas", "/diseno-grafico/": "Solvento", "/redaccion-seo-copywriting/": "RFG Andrade",
            "/analitica-web/": "Aquita", "/quienes-somos/": "Las Tejas", "/agencia-seo-arroyomolinos/": "Aquita", "/agencia-seo-pozuelo-de-alarcon/": "Dotti Peluquería"}
# Imagen de cada tarjeta apilada de servicio: composición propia con un caso real (herramientas/maquetas)
# (archivo, texto alternativo)
IMG_SERVICIO = {"/seo-local/": ("servicio-seo-local-ficha-dotti.jpg", "Ficha de Google de Dotti Peluquería en el móvil y su búsqueda en Google"),
                "/auditoria-seo-local/": ("servicio-auditoria-aquita.jpg", "Web de Aquita en un portátil"),
                "/diseno-web/": ("servicio-diseno-web-las-tejas.jpg", "Web del Restaurante Las Tejas en el portátil y en el móvil"),
                "/google-ads/": ("servicio-google-ads-balgas.jpg", "Web de Balgas en el móvil y en el portátil"),
                "/diseno-grafico/": ("servicio-diseno-grafico-solvento.jpg", "Web de Solvento en el móvil y en el portátil"),
                "/redaccion-seo-copywriting/": ("servicio-redaccion-rfg-andrade.jpg", "Web de RFG Andrade en un portátil"),
                "/analitica-web/": ("servicio-analitica-marcos.jpg", "Web de Marcos Cerrajeros en el portátil y en el móvil")}
# Cifras: el objeto que se sale de cada tarjeta
OBJETOS_CIFRAS = ["estrella-cromo", "simbolo-fucsia-perfil", "simbolo-despiece-crema", "simbolos-grupo"]
# «¿Quién hay detrás…?»: los párrafos 2, 3 y 4 van en tres tarjetas oscuras con una pieza que gira en vivo
QUIEN_H2 = "¿Quién hay detrás"
# v3: el símbolo G+F en tres materiales (pieza, imagen fija de respaldo, giro inicial, materiales G,F)
PIEZAS_VIVAS = [("simbolo", "simbolo-fucsia", "-0.16,-0.5", "fucsia"), ("simbolo", "simbolo-cromo", "-0.18,0.5", "cromo"),
                ("simbolo", "simbolo-berenjena", "0.12,-0.55", "berenjena")]
# Etiqueta corta de cada una de esas tres tarjetas (microtexto de interfaz)
PIEZAS_ETQ = ["Un solo interlocutor", "Especialistas de verdad", "Agentes de IA"]
CASOS_H2 = "Lo más reciente"

CIFRAS = [
    ("{valoracion}", "", "de valoración media en Google", ("Leer las opiniones", "#opiniones"), "check"),
    ("{anios}", "+", "años de oficio en publicidad, diseño y SEO", ("Quiénes somos", "/quienes-somos/"), "redaccion"),
    ("15", "", "años con la agencia abierta en Alcorcón", None, "contacto"),
    ("100", "+", "clientes en quince años de agencia", ("Lo más reciente", "#casos"), "seo-local"),
]
CIFRAS_EN = {"home": 2, "empresa": 1, "servicio": 0, "municipio": 0}

CTA_H2 = r"^(Pida |Llámenos|Hablemos|Veamos|Cuéntenos)"
CTA_ULTIMO = True
ZONA_H2 = "Dónde trabajamos"
HORARIO_H2 = "Horario"
CTA_EXTRA = ("Pida su auditoría gratuita", "/auditoria-seo-local/")

CREDITO = None   # es la web de la propia agencia: sin «Diseño y SEO: …» en el pie
LEGALES = [
    ("Aviso legal", "/aviso-legal/"),
    ("Política de privacidad", "/politica-de-privacidad/"),
    ("Política de cookies", "/politica-de-cookies/"),
]
CONTACTO_YA = set()   # «¿Cuándo puedo llamar?» se publica: trae la mención a Álvaro (paso 25)
BANDA_TIT = {}

TEXTOS = {
    "lgfoto_pie": "El Gordo y el Flaco · Agencia SEO y de marketing online en Alcorcón",
    "oficio": "marketing online",
    "logo_alt": "{nombre} · Agencia SEO y de marketing online en {localidad}",
    "whatsapp_saludo": "Hola, le escribo desde la web de {nombre}",
    "whatsapp_pueblo": " (mi negocio está en {pueblo})",
    "etiqueta_portada": "Agencia SEO · {pueblo}",
    "corta_municipio": "Ficha de Google, web y anuncios para negocios de {pueblo}, desde nuestra oficina de Alcorcón.",
    "corta": "Ficha de Google, web y anuncios para negocios de {localidad} y alrededores.",
    "tarjeta_titulo": "¿Le llamamos nosotros?",
    "tarjeta_ir": "Déjenos su teléfono",
    "llamada_titulo": "Le llamamos nosotros",
    "llamada_promesa": "Déjenos su nombre y su teléfono y le llamamos.",
    "llamada_ok": "Recibido. {horario}, le llamamos {devuelve}.",
    "llamada_boton": "Que me llamen",
    "promesa_abierto": "Le llamamos hoy, en cuanto colguemos.",
    "promesa_antes": "Le llamamos hoy a partir de las {abre}.",
    "promesa_siguiente": "Le llamamos {dia} a partir de las {abre}.",
    "declara_etiqueta": "Quiénes somos",
    "indice_titulo": "En esta página",
    "indice_llamar": "¿Lo hablamos en su negocio?",
    "opiniones_etiqueta": "Opiniones en Google",
    "opiniones_titular": "Lo que dicen de {nombre}",
    "opiniones_sello": "{valoracion} EN GOOGLE · OPINIONES REALES · ",
    "resenas_ficha": "Valoración media en la ficha de {nombre}",
    "faq_etiqueta": "Dudas habituales",
    "faq_titulo": "Preguntas frecuentes",
    "faq_cta": "¿No está su pregunta? Llámenos",
    "cifras_etiqueta": "{nombre} en cifras",
    "cifras_titulo": "Lo que se puede contar",
    "cifras_fecha": "Nota y reseñas de la ficha de Google, actualizadas en {fecha}.",
    "zona_titulo": "Agencia SEO en los municipios de alrededor",
    "mapa_titular": "La oficina, en {localidad}",
    "mapa_texto": "Recibimos con cita. Casi siempre somos nosotros los que vamos a su negocio.",
    "privacidad_llamada": "Usamos sus datos solo para llamarle.",
    "privacidad_form": "Usamos sus datos solo para contestarle.",
    "form_ok": "Mensaje enviado. Le llamamos {horario_min}.",
    "form_confianza": "Primera reunión en su negocio, sin coste. Le llamamos {horario_min}.",
    "form_municipio_ph": "Alcorcón, Móstoles, Getafe…",
    "form_mensaje_label": "¿Qué necesita su negocio?",
    "form_mensaje_ph": "Su negocio, su web o su ficha, y qué le gustaría conseguir",
    "form_boton": "Enviar",
    "contacto_horario_extra": "Fuera de horario, déjenos su teléfono y le llamamos al día siguiente.",
    "banda_etiqueta": "Primera reunión sin coste",
    "banda_titulo": "Hablemos en su negocio, sin coste",
    "banda_texto": "Vamos a verle, vemos cómo le encuentran hoy sus clientes y le pasamos un presupuesto a medida.",
    "estado_abierto": "Abierto ahora · hasta las {cierra}",
    "estado_fuera": "Ahora cerrado · déjenos su teléfono",
    "pie_titular": "¿Hablamos de<br>su negocio?",
    "error_texto": "Puede que el enlace esté mal o que la página haya cambiado de sitio. Llámenos y lo vemos.",
    "llms_titulo": "# {nombre} · Agencia SEO y de marketing online en {localidad}",
    "llms_resumen": "Agencia SEO y de marketing online de {localidad} para negocios locales: ficha de Google, web, Google Ads, diseño gráfico, redacción y analítica.",
    "llms_horario_extra": "Reuniones en el negocio del cliente; la oficina recibe con cita.",
    "llms_datos": ["- 15 años de agencia en Alcorcón y más de 20 años de oficio en publicidad.",
                   "- Un solo interlocutor por proyecto, un equipo de especialistas (personas) en diseño gráfico, diseño web, analítica web y Google Ads, y un equipo propio de agentes de IA con nombre propio, presentados como tales.",
                   "- Primera reunión en el negocio del cliente, sin coste; presupuesto a medida por escrito.",
                   "- Mantenimiento mensual sin permanencia."],
    "llms_no_hace": ["- No da precios cerrados por la web: el presupuesto llega tras la reunión."],
    "llms_no_instala": "",
}
LLMS_PRINCIPALES = ["/", "/seo-local/", "/auditoria-seo-local/", "/diseno-web/", "/google-ads/", "/diseno-grafico/",
                    "/redaccion-seo-copywriting/", "/analitica-web/", "/quienes-somos/", "/contacto/"]
LLMS_MARCAS = []


def texto(clave, **extra):
    """Devuelve TEXTOS[clave] con los marcadores rellenos."""
    N = NEGOCIO
    pe = N.get("persona") or {}
    cred = (pe.get("credenciales") or [("", "")])[0][1] or f"{N['anios']} años en el oficio"
    v = dict(nombre=N["nombre"], localidad=N["localidad"], telefono=N["telefono"], horario=N["horario_texto"],
             horario_min=N["horario_texto"][0].lower() + N["horario_texto"][1:], anios=N["anios"],
             anios_marca=N["anios_marca"], abre=N["abre"].lstrip("0"), cierra=N["cierra"].lstrip("0"),
             garantia=N["garantia"], valoracion=N["valoracion"], resenas=N["resenas"], credencial=cred,
             pueblo=N["localidad"], devuelve=N.get("devuelve_llamada") or "en cuanto podamos")
    v.update(extra)
    v["PUEBLO"] = v["pueblo"].upper()
    return TEXTOS[clave].format(**v)


# Nota y número de reseñas: viven en contenido/resenas.json (en la web, /resenas.json).
import json as _json, os as _os
_R = _json.load(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "contenido", "resenas.json"), encoding="utf-8"))
NEGOCIO["valoracion"] = _R["valoracion"]
NEGOCIO["resenas"] = str(_R["resenas"])
OPINIONES = _R.get("opiniones", [])
FICHA = f"https://maps.google.com/?cid={NEGOCIO['cid']}"
NOTA_CON_NUMERO = False  # Álvaro 26/09: no se enseña el número de reseñas
# aggregateRating en el schema: NO (decisión paso 26, ver LEEME). Google no da estrellas a un negocio por sus
# propias reseñas y el número no está a la vista en la página: marcar lo que no se ve es contrario a sus directrices.
SCHEMA_VALORACION = False
SAME_AS = [FICHA]   # [PENDIENTE] LinkedIn de empresa, cuando esté corregido (planos-ia 2.4)

# Tira de logotipos de clientes (en gris, pasan a color al pasar el ratón). Fuente: recursos/clientes/.
# Si está vacía y existe LOGOS_ORIGEN, build.py copia de ahí (svg/png/webp; logos.json opcional con
# [{"archivo": "...", "nombre": "..."}] para el orden y el nombre). Sin logos: sale el marcador.
LOGOS_ORIGEN = "/home/claude/gyf/logos-clientes"
LOGOS_TITULO = "Negocios que confían en nosotros"
LOGOS_NOMBRES = {"asesoria-mayo": "Asesoría Mayo", "jif-2026": "JIF 2026", "ele-room": "Ele Room", "las-tejas": "Restaurante Las Tejas",
                 "marcos-cerrajeros": "Marcos Cerrajeros", "ines-ingenieros": "Inés Ingenieros", "psicorazon": "Psicorazon",
                 "vinos-gallegos-pousada": "Vinos Gallegos Pousada", "aquita": "Aquita", "balgas": "Balgas", "solvento": "Solvento",
                 "expertise": "Expertise",
                 "ayuntamiento-madrid": "Ayuntamiento de Madrid", "dotti-peluqueria": "Dotti Peluquería", "imdea": "IMDEA Materiales",
                 "diversey": "Diversey", "solenis": "Solenis", "taski": "TASKI", "jardines-con-estilo": "Jardines con Estilo",
                 "delfinia-piscinas": "Delfinia Piscinas", "lisboa-dental": "Lisboa Dental", "hotel-las-truchas": "Hotel Las Truchas"}

# Imagen para redes (Open Graph) por página, 1200 × 630: la genera rematar.py con PIL (fondo crema, H1 en Outfit,
# símbolo fucsia). Fuentes TTF y símbolo en recursos/og/.
OG = {"fondo": "#F5F1EC", "texto": "#1C1219", "acento": "#E0067A", "gris": "#6B5F66"}


# ---------- v3 · Fotografías artísticas del tema (huecos ya integrados en el diseño) ----------
# Para sustituir un marcador por la foto: soltar el archivo en recursos/fotos/ con ESTE nombre (vale .jpg, .png o .webp)
# y regenerar (build.py + rematar.py). Encargo y prompts: 08-WEB/v3-CAMBIOS/FOTOS-A-GENERAR.md
# formato = proporción del hueco (CSS aspect-ratio) · trat = tratamiento: «duotono» (sombras berenjena, luces fucsia)
# o «vineta» (color natural con viñeta berenjena y un velo fucsia suave)
FOTOS = {
    "portada":        dict(archivo="foto-portada-mesa-de-trabajo.jpg", formato="21/9", trat="vineta",
                           alt="Mesa de madera al atardecer: las sombras de lápices y reglas dibujan un plano de calles con una chincheta fucsia"),
    "/seo-local/":    dict(archivo="foto-servicio-seo-local.jpg", formato="4/5", trat="vineta",
                           alt="Calle de persianas bajadas al anochecer con un solo comercio encendido"),
    "/auditoria-seo-local/": dict(archivo="foto-servicio-auditoria.jpg", formato="4/5", trat="vineta",
                           alt="Cuentahílos sobre un plano de calles con un cruce marcado en fucsia"),
    "/diseno-web/":   dict(archivo="foto-servicio-diseno-web.jpg", formato="4/5", trat="vineta",
                           alt="Mano que sostiene un móvil con una web abierta en una calle empedrada, con una tienda iluminada al fondo"),
    "/google-ads/":   dict(archivo="foto-servicio-google-ads.jpg", formato="4/5", trat="vineta",
                           alt="Móvil con la pantalla encendida junto a un vaso de agua con ondas, sobre una barra oscura"),
    "/diseno-grafico/": dict(archivo="foto-servicio-diseno-grafico.jpg", formato="4/5", trat="vineta",
                           alt="Abanico de muestras de color con una ficha fucsia y su sombra en la pared"),
    "/redaccion-seo-copywriting/": dict(archivo="foto-servicio-redaccion.jpg", formato="4/5", trat="vineta",
                           alt="Folio con una firma en tinta fucsia y una pluma, rodeado de bolas de papel arrugado"),
    "/analitica-web/": dict(archivo="foto-servicio-analitica.jpg", formato="4/5", trat="vineta",
                           alt="Estelas de luz de los coches en una avenida de noche"),
    "pasos":          dict(archivo="foto-como-trabajamos-reunion.jpg", formato="16/7", trat="vineta",
                           alt="Un rayo de luz sobre el mostrador de un negocio: manos, un folio, un móvil y un rotulador fucsia"),
    "quien":          dict(archivo="foto-quien-atico.jpg", formato="4/5", trat="vineta",
                           alt="Estudio en un ático con claraboya, pruebas de color colgadas y una mesa de trabajo"),
    "zonas":          dict(archivo="foto-zonas-calle.jpg", formato="3/2", trat="vineta",
                           alt="Vista aérea de un barrio residencial del sur de Madrid con rutas marcadas en fucsia"),
    "municipio":      dict(archivo="foto-municipio-escaparates.jpg", formato="4/5", trat="vineta",
                           alt="Hilera de comercios con un toldo fucsia a la luz del atardecer"),
    "banda":          dict(archivo="foto-banda-mostrador.jpg", formato="16/9", trat="vineta",
                           alt="Mostrador de una tienda al cerrar, con la persiana a medias y un neón fucsia"),
    "/quienes-somos/": dict(archivo="foto-quienes-somos-oficio.jpg", formato="4/5", trat="vineta",
                           alt="Cuaderno fucsia, muestras de color, cuentahílos y pluma sobre una mesa con luz de persiana"),
    "/contacto/":     dict(archivo="foto-contacto-telefono.jpg", formato="4/5", trat="vineta",
                           alt="Móvil sobre una mesa de madera con un cable en espiral fucsia"),
}

# v4 · Foto que se ve dentro de las letras del logotipo (sección de la home tras la cinta de tarjetas)
LOGOTIPO_FOTO = "/quienes-somos/"
