# -*- coding: utf-8 -*-
"""GYF-Rayo · CONFIGURACIÓN · WEB DE EL GORDO Y EL FLACO (elgordoyelflaco.es) · v2 (color, cajas, objetos 3D y movimiento de Rayo).
Datos de la ficha de Google (mandan sobre cualquier otro). Textos: textos-v2 (Merche). Reseñas reales en
contenido/resenas.json. Arquitectura y 301: nuria2/arquitectura.md (sección c). Caso E: todo es nuevo.
Lo que falta confirmar está marcado [PENDIENTE] y sale como aviso en controles.py.
"""

VERSION = "5"

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
    "anios_marca": "13",                # Álvaro, 27/09: abierta desde 2013 (corrige los 15)
    "garantia": "",
    "fundacion": 2013,                 # Álvaro, 27/09
    "devuelve_llamada": "enseguida",   # Álvaro, 27/09: coge la llamada en el momento
    "cambia_equipos": None,
    "cid": "10293855805443705389",
    "lat": 40.34983, "lng": -3.81639,   # ficha de Google (Matías, paso 5)
    "schema_tipo": "ProfessionalService",
    "servicio_tipo": "Agencia SEO y de marketing online",
    "precio": None,
    "pago": "Bizum, transferencia, tarjeta o efectivo",
    "knows_about": ["SEO local", "Google Business Profile", "Diseño web", "Google Ads", "Diseño gráfico", "Redacción SEO", "Redacción publicitaria", "Analítica web"],
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
    ("Redacción SEO", "Textos de web, ficha y anuncios.", "/redaccion-seo-copywriting/", "redaccion", ["Web", "Ficha", "Anuncios"], None),
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
    ("Balgas", "Web, ficha y Google Ads", "diseno-web-alcorcon-caso-balgas-vertical.jpg", "https://reparacioncalderasbalgas.es/", "g", "diseno-web-alcorcon-caso-balgas.jpg"),
    ("Marcos Cerrajeros", "Ficha y web nueva", "diseno-web-alcorcon-caso-marcos-cerrajeros-movil.jpg", "https://www.marcoscerrajeros.es/", "v", "diseno-web-alcorcon-caso-marcos-cerrajeros.jpg"),
    ("Aquita", "Ficha y web desde cero", "diseno-web-arroyomolinos-caso-aquita-portatil.jpg", "https://aquita.es/", "h", "diseno-web-arroyomolinos-caso-aquita.jpg"),
    ("Las Tejas", "Web del restaurante", "diseno-web-alcorcon-caso-las-tejas-movil.jpg", "https://www.restaurantelastejas.es/", "v", "diseno-web-alcorcon-caso-las-tejas.jpg"),
    ("Solvento", "Imagen de marca y web", "diseno-web-caso-solvento-vertical.jpg", "https://solvento.es/", "g", "diseno-web-caso-solvento.jpg"),
    ("RFG Andrade", "Web", "diseno-web-caso-rfg-andrade-portatil.jpg", "https://www.rfgandrade.es/", "h", "diseno-web-caso-rfg-andrade.jpg"),
    ("Dotti Peluquería", "Ficha de Google", "seo-local-caso-dotti-peluqueria-movil.jpg", "https://www.google.com/maps/search/?api=1&query=Sal%C3%B3n+de+Belleza+Dotti+Peluquer%C3%ADa+Aravaca", "v", "seo-local-caso-dotti-peluqueria.jpg"),
]
# Etiquetas de cada caso en la lista grande de «Lo más reciente» (lo que se hizo, en píldoras)
CASOS_ETQ = {"Balgas": ["Web", "Ficha de Google", "Google Ads"], "Marcos Cerrajeros": ["Ficha de Google", "Web"],
             "Aquita": ["Ficha de Google", "Web"], "Las Tejas": ["Web"], "Solvento": ["Imagen de marca", "Rotulación", "Web"], "RFG Andrade": ["Web"],
             "Dotti Peluquería": ["Ficha de Google"]}
CASOS_VER = "Ver la web"
CASOS_VER_CASO = {"Dotti Peluquería": "Ver la ficha"}   # v5.7 · Dotti no tiene web: se enlaza su ficha de Google
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

CINTA_PORTADA = ["Alcorcón", "SEO local", "Google Maps", "Más llamadas"]
CINTA_SECUNDARIA = None

# ---------- v2 · Objetos 3D de la marca (herramientas/objetos3d/master → sitio/img/obj/) ----------
# Objeto de cada servicio (tarjetas apiladas de la home, cabecera de su página y tarjetas de «Otros servicios»)
OBJETO_URL = {"/seo-local/": "chincheta", "/auditoria-seo-local/": "lupa", "/diseno-web/": "estrella",
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
OBJETOS_CIFRAS = ["estrella-cromo", "lupa", "barras", "chincheta"]   # v5: monograma 3D solo en portada, «Quién hay detrás» y cierre
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
    ("2013", "", "el año en que abrimos la agencia en Alcorcón", None, "contacto"),
    ("100", "+", "clientes desde que abrimos", ("Lo más reciente", "#casos"), "seo-local"),
]
CIFRAS_EN = {"home": 2, "empresa": 1, "servicio": 0, "municipio": 0}

CTA_H2 = r"^(Pida |Llámenos|Hablemos|Veamos|Cuéntenos)"
CTA_ULTIMO = True
ZONA_H2 = "Dónde trabajamos"
HORARIO_H2 = "Horario"
CTA_EXTRA = ("Pida su auditoría gratuita", "/auditoria-seo-local/#pedir-auditoria")

CREDITO = None   # es la web de la propia agencia: sin «Diseño y SEO: …» en el pie
LEGALES = [
    ("Aviso legal", "/aviso-legal/"),
    ("Política de privacidad", "/politica-de-privacidad/"),
    ("Política de cookies", "/politica-de-cookies/"),
]
CONTACTO_YA = set()   # «¿Cuándo puedo llamar?» se publica: trae la mención a Álvaro (paso 25)
BANDA_TIT = {}

TEXTOS = {
    "aud_titular": "Pida su auditoría gratuita",
    "aud_texto": "Revisamos su ficha de Google, su web o las dos, y le entregamos un informe en PDF, fácil de leer, con lo que más le frena primero.",
    "aud_puntos": "Informe en PDF, fácil de leer|Sin compromiso y sin letra pequeña|En horario, el informe le llega en unos 30 minutos|Si no vemos oportunidad de mejora, se lo decimos",
    "aud_ok": "Recibido. En horario, le enviamos el informe en unos 30 minutos; fuera de horario, a primera hora del siguiente día laborable.",
    "aud_negocio_ph": "Por ejemplo: mipeluqueria.es o Peluquería Ana, Móstoles",
    "aud_boton": "Pedir mi auditoría",
    "lgfoto_pie": "El Gordo y el Flaco · Agencia SEO y de marketing online en Alcorcón",
    "oficio": "marketing online",
    "logo_alt": "{nombre} · Agencia SEO y de marketing online en {localidad}",
    "whatsapp_saludo": "Hola, le escribo desde la web de {nombre}",
    "whatsapp_pueblo": " (mi negocio está en {pueblo})",
    "whatsapp_auditoria": "Hola, quiero la auditoría gratuita de mi negocio. Se llama: ",
    "portada_gratis": "Primera reunión en su negocio, sin coste",
    "etiqueta_portada": "Agencia SEO · {pueblo}",
    "corta_municipio": "Ficha de Google, web y anuncios para negocios de {pueblo}, desde nuestra oficina de Alcorcón.",
    "corta": "Ficha de Google, web y anuncios para negocios de {localidad} y alrededores.",
    "tarjeta_titulo": "¿Le llamamos nosotros?",
    "tarjeta_ir": "Déjenos su teléfono",
    "llamada_titulo": "Le llamamos nosotros",
    "llamada_promesa": "Déjenos su nombre y su teléfono y le llamamos.",
    "llamada_ok": "Recibido. Le llamamos {devuelve}.",
    "llamada_boton": "Que me llamen",
    "promesa_abierto": "Le llamamos enseguida.",
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
    "cifras_titulo": "En cifras",
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
    "contacto_horario_extra": "En horario, le atendemos en el momento. Fuera de horario, déjenos su teléfono y le llamamos a primera hora del siguiente día laborable.",
    "banda_etiqueta": "Primera reunión sin coste",
    "banda_titulo": "Hablemos en su negocio",
    "banda_texto": "Vamos a verle, vemos cómo le encuentran hoy sus clientes y le pasamos un presupuesto según lo que necesite.",
    "estado_abierto": "Abierto ahora · hasta las {cierra}",
    "estado_fuera": "Ahora cerrado · déjenos su teléfono",
    "pie_titular": "¿Hablamos de<br>su negocio?",
    "error_texto": "Puede que el enlace esté mal o que la página haya cambiado de sitio. Llámenos y lo vemos.",
    "llms_titulo": "# {nombre} · Agencia SEO y de marketing online en {localidad}",
    "llms_resumen": "Agencia SEO y de marketing online de {localidad} para negocios locales: ficha de Google, web, Google Ads, diseño gráfico, redacción y analítica.",
    "llms_horario_extra": "Reuniones en el negocio del cliente; la oficina recibe con cita.",
    "llms_datos": ["- Agencia abierta en Alcorcón desde 2013 y más de 20 años de oficio en publicidad. La sociedad de 2016 que aparece en registros mercantiles es la misma agencia; hoy trabaja sin forma de sociedad.",
                   "- Un solo interlocutor por proyecto, un equipo de especialistas (personas) en diseño gráfico, diseño web, analítica web y Google Ads, y un equipo propio de agentes de IA con nombre propio, presentados como tales.",
                   "- Primera reunión en el negocio del cliente, sin coste; presupuesto por escrito, según lo que necesite el negocio.",
                   "- Mantenimiento mensual opcional, con un mínimo de seis meses; después, mes a mes.",
                   "- Auditoría SEO local gratuita: en horario, el informe llega en unos 30 minutos; fuera de horario, a primera hora del siguiente día laborable."],
    "llms_no_hace": ["- No publica precios: el presupuesto llega tras la reunión.",
                     "- No promete posiciones concretas en Google.",
                     "- No mantiene alojamientos: el dominio y el alojamiento se contratan a nombre del cliente.",
                     "- No trabaja en Madrid capital ni en el norte de la Comunidad: su zona es Alcorcón y diez municipios de alrededor.",
                     "- No hace gestión de redes sociales como servicio principal."],
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
SAME_AS = [FICHA]   # v5.7 (Álvaro 27/09): sin redes sociales. La marca no tiene Facebook ni X y los perfiles personales no se enlazan.

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
                           alt="Vista aérea de un barrio residencial con rutas marcadas en fucsia"),
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

# v5 · Un Service propio por página (Bruno y Turing): nombre descriptivo y tipo de servicio real
SERVICIO_SCHEMA = {
    "/seo-local/": ("SEO local y optimización de la ficha de Google Business Profile", "SEO local"),
    "/auditoria-seo-local/": ("Auditoría SEO local gratuita de ficha de Google y web", "Auditoría SEO local"),
    "/diseno-web/": ("Diseño de webs para negocios locales", "Diseño web"),
    "/google-ads/": ("Campañas de Google Ads y anuncios en Google Maps", "Publicidad en Google Ads"),
    "/diseno-grafico/": ("Diseño gráfico, logotipo e imagen de marca", "Diseño gráfico"),
    "/redaccion-seo-copywriting/": ("Redacción SEO y redacción publicitaria", "Redacción SEO"),
    "/analitica-web/": ("Analítica web con Google Analytics 4 y Search Console", "Analítica web"),
}
ALTERNATE_NAME = ["El Gordo y el Flaco", "GYF"]

# v5 · Reseñas por página (auditoría N1). Cada página enseña primero las que hablan de su servicio o su zona.
# Las etiquetas salen de lo que dice cada reseña en Google (o de lo que contó Álvaro del cliente), no se inventan.
OPINION_ETIQUETA = {
    "Pablo": "SEO local y fichas de Google",
    "Sergio": "Web, SEO local y Google Ads · Calderas Balgas",
    "Eva Ma Arguijo Fonseca": "Ficha de Google · peluquería",
    "Alberto Martín": "Imagen de marca y web · Delfinia Piscinas",
    "Victor Javier Cubero Segura": "Web · Mundo Calor",
    "David Diaz Gonzalez": "Web · distribuidora de vinos",
    "Raúl De León": "Herramientas web · multinacional química",
    "J G": "Web de maquinaria de limpieza industrial",
    "Raúl Pérez": "Web de un congreso científico",
}
_OP_HOME = ["Pablo", "Sergio", "Eva Ma Arguijo Fonseca", "Alberto Martín", "Victor Javier Cubero Segura", "David Diaz Gonzalez",
            "Raúl De León", "J G", "Raúl Pérez", "Ruben Agudo", "Alicia Muro"]
OPINION_ORDEN = {  # URL → nombres por orden. Las interiores enseñan 3 y mandan a Google para el resto.
    # Pablo nombra Alcorcón, Móstoles, Getafe y Leganés en su reseña: primero en esos municipios
    "/agencia-seo-getafe/": ["Pablo", "Sergio", "Eva Ma Arguijo Fonseca"],
    "/agencia-seo-mostoles/": ["Pablo", "Sergio", "Alberto Martín"],
    "/agencia-seo-leganes/": ["Pablo", "Eva Ma Arguijo Fonseca", "Sergio"],
    "/agencia-seo-pozuelo-de-alarcon/": ["Eva Ma Arguijo Fonseca", "Pablo", "Sergio"],
    "/": _OP_HOME,
    "/seo-local/": ["Pablo", "Sergio", "Eva Ma Arguijo Fonseca"],
    "/auditoria-seo-local/": ["Sergio", "Pablo", "Eva Ma Arguijo Fonseca"],
    "/google-ads/": ["Sergio", "Pablo", "Eva Ma Arguijo Fonseca"],
    "/diseno-web/": ["Victor Javier Cubero Segura", "Sergio", "J G"],
    "/diseno-grafico/": ["Alberto Martín", "David Diaz Gonzalez", "Victor Javier Cubero Segura"],
    "/redaccion-seo-copywriting/": ["David Diaz Gonzalez", "Alberto Martín", "Raúl De León"],
    "/analitica-web/": ["Pablo", "Sergio", "Victor Javier Cubero Segura"],
    "/quienes-somos/": ["Alberto Martín", "Raúl De León", "Sergio"],
    "/contacto/": ["Sergio", "Pablo", "Eva Ma Arguijo Fonseca"],
}
OPINION_MUNICIPIO = [  # rota para que ninguna zona repita las tres mismas en el mismo orden
    ["Pablo", "Sergio", "Eva Ma Arguijo Fonseca"], ["Sergio", "Pablo", "Alberto Martín"], ["Eva Ma Arguijo Fonseca", "Sergio", "Victor Javier Cubero Segura"],
    ["Alberto Martín", "Pablo", "Sergio"], ["Sergio", "Eva Ma Arguijo Fonseca", "Alberto Martín"], ["Victor Javier Cubero Segura", "Pablo", "Eva Ma Arguijo Fonseca"],
    ["Eva Ma Arguijo Fonseca", "Alberto Martín", "Sergio"], ["Alberto Martín", "Sergio", "Pablo"], ["Pablo", "Victor Javier Cubero Segura", "Sergio"],
    ["Sergio", "Alberto Martín", "Eva Ma Arguijo Fonseca"],
]

# v5 · Casos con municipio y punto de partida (auditoría N2). Sin cifras: son trabajos recientes sin histórico
# (Álvaro, tanda 8). Datos de las tandas 5, 7 y 8 y de la reseña de Sergio (Balgas). None = no se sabe.
CASO_DETALLE = {  # v5.1: «Hoy», confirmado por Álvaro (27/09) o citado de la reseña del cliente
    "Balgas": ("Alcorcón", "Partía de una web de otra agencia que en tres años no había posicionado. Resultado, en palabras de su dueño: «en unos 3 meses nuestra empresa \"calderas Balgas\" posicionaba en los 10 primeros resultados de Google en las zonas solicitadas»."),
    "Marcos Cerrajeros": ("Alcorcón", "Partía de una web antigua y una ficha sin trabajar. Hoy: sale en Google Maps cuando se busca cerrajero en Alcorcón."),
    "Aquita": ("Arroyomolinos", "Partía sin web y con la ficha sin trabajar. Hoy: sale en Google Maps cuando se busca control de plagas en Arroyomolinos."),
    "Las Tejas": ("Alcorcón", None),
    "Solvento": (None, "Partía de cero: marca, rotulación, papelería y web."),
    "RFG Andrade": ("Madrid", "Web de presentación de una consulta privada."),
    "Dotti Peluquería": ("Aravaca, junto a Pozuelo", "Sin web: todo el trabajo, en la ficha de Google, para salir en Aravaca y en Pozuelo."),
}
# Caso más cercano para cada municipio (Alcorcón linda con Getafe, Móstoles, Leganés, Fuenlabrada y Villaviciosa)
CASO_URL.update({
    "/agencia-seo-getafe/": "Balgas", "/agencia-seo-mostoles/": "Aquita", "/agencia-seo-leganes/": "Marcos Cerrajeros",
    "/agencia-seo-fuenlabrada/": "Balgas", "/agencia-seo-villaviciosa-de-odon/": "Marcos Cerrajeros",
    "/agencia-seo-brunete/": "Aquita", "/agencia-seo-boadilla-del-monte/": "Dotti Peluquería", "/agencia-seo-majadahonda/": "Dotti Peluquería",
})
CASOS_RECIENTES = ["Balgas", "Marcos Cerrajeros", "Aquita"]   # v5 · «Lo más reciente» de la home (los de SEO local)

# v5 · «Quiénes somos»: cada agente de IA con el objeto 3D de su oficio (sin caras: decisión de Álvaro)
AGENTES_OBJETO = {"Jean Pierre": "simbolo-cromo", "Jean Paul": "abanico", "Merche": "bocadillo", "Matías": "chincheta",
                  "Nuria": "lupa", "Bruno": "simbolo-despiece", "Turing": "estrella", "Dani": "cursor",
                  "Iñaki": "barras", "Kubrick": "estrella-cromo"}
MUESTRA_CASO = {}   # nombre en la lista → nombre en CASOS, si no coinciden
# v5 · Municipios vecinos de cada página de municipio (banda «La zona»)
VECINOS = {"getafe": ["leganes", "fuenlabrada"], "mostoles": ["fuenlabrada", "arroyomolinos"], "leganes": ["getafe", "fuenlabrada"],
           "fuenlabrada": ["mostoles", "leganes"], "majadahonda": ["pozuelo-de-alarcon", "boadilla-del-monte"],
           "boadilla-del-monte": ["majadahonda", "villaviciosa-de-odon"], "arroyomolinos": ["mostoles", "fuenlabrada"],
           "villaviciosa-de-odon": ["boadilla-del-monte", "brunete"], "pozuelo-de-alarcon": ["majadahonda", "boadilla-del-monte"],
           "brunete": ["villaviciosa-de-odon", "boadilla-del-monte"]}

# v5.2 · Frase de cada reseña que se cita junto a los formularios (literal: el generador comprueba que está en el texto)
OPINION_CITA = {
    "Pablo": "Nos ayudaron a mejorar tanto la web como las fichas de Google Business Profile para reforzar nuestra visibilidad en zonas como Alcorcón, Móstoles, Getafe y Leganés.",
    "Sergio": "Teníamos nuestra página web creada por otra empresa del sector desde hacía más de 3 años y no funcionaba, no conseguía posicionar y los resultados no llegaban nunca, aún pagando un mantenimiento mensual por ella.",
    "Raúl De León": "Desde hace años colaboramos con el gordo y el flaco y cuando nuestra compañía multinacional no nos da soluciones, con El gordo y el flaco hemos encontrado la manera de ir al grano, coger atajos y solucionar de manera agil, rapida, personalizada y eficaz problemas concretos con soluciones concretas.",
    "Eva Ma Arguijo Fonseca": "Se nota cuando alguien controla bien este tema y sabe cómo hacer que el negocio tenga mejor presencia online.",
    "Alberto Martín": "Supieron entender muy bien lo que queríamos transmitir y darle una imagen profesional y coherente a Delfinia Piscinas.",
    "Victor Javier Cubero Segura": "Supieron ordenar muy bien toda la información y darle un enfoque claro, serio y pensado para que el cliente encuentre rápido lo que necesita.",
    "David Diaz Gonzalez": "Supieron captar exactamente lo que necesitaba y lo plasmaron de forma moderna, funcional y visualmente atractiva.",
    "J G": "Está todo claro, bien organizado y pensado para que el cliente entienda rápido qué ofrecemos.",
    "Raúl Pérez": "Gran profesional y muy atento a todos los detalles.",
}
MUESTRA_OBJETO = {"JIF 2026": "bocadillo", "Delfinia Piscinas": "abanico", "Vinos Gallegos Pousada": "estrella-cromo"}
_SERGIO_RES = "…en unos 3 meses nuestra empresa \"calderas Balgas\" posicionaba en los 10 primeros resultados de Google en las zonas solicitadas…"
OPINION_CITA_PAGINA = {u: {"Sergio": _SERGIO_RES} for u in ("/google-ads/", "/seo-local/", "/diseno-web/", "/contacto/")}

# v5.7 · Maqueta propia de las muestras de «Quiénes somos» que no están en la galería (captura HD de Álvaro).
# (archivo en recursos/casos, qué se hizo). Solo se usa si el archivo existe.
MUESTRA_FOTO = {"JIF 2026": ("diseno-web-caso-jif-2026-muestra.jpg", "Web del congreso"),
                "Delfinia Piscinas": ("diseno-grafico-caso-delfinia-muestra.jpg", "Imagen de marca"),
                "Vinos Gallegos Pousada": ("diseno-web-caso-vinos-pousada-muestra.jpg", "Imagen de marca y web")}
