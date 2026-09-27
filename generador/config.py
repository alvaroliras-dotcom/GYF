# -*- coding: utf-8 -*-
"""GYF-Rayo · CONFIGURACIÓN · WEB DE EL GORDO Y EL FLACO (elgordoyelflaco.es) · v1 (pasos 23-24, protocolo v8).
Datos de la ficha de Google (mandan sobre cualquier otro). Textos: textos-v2 (Merche). Reseñas reales en
contenido/resenas.json. Arquitectura y 301: nuria2/arquitectura.md (sección c). Caso E: todo es nuevo.
Lo que falta confirmar está marcado [PENDIENTE] y sale como aviso en controles.py.
"""

VERSION = "1"

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

# Casos: capturas reales en maqueta de dispositivo (DIRECCION §3.6), aún sin hacer → marcadores
CASOS = [  # muestra local de este año (Álvaro 26/09); capturas reales en recursos/casos/
    ("Balgas", "Web, ficha y Google Ads", "diseno-web-alcorcon-caso-balgas.webp", None, "g"),
    ("Marcos Cerrajeros", "Ficha y web nueva", "diseno-web-alcorcon-caso-marcos-cerrajeros.webp", "https://www.marcoscerrajeros.es/", "v"),
    ("Aquita", "Ficha y web desde cero", "diseno-web-arroyomolinos-caso-aquita.webp", "https://aquita.es/", "h"),
    ("Las Tejas", "Web del restaurante", "diseno-web-alcorcon-caso-las-tejas.webp", "https://www.restaurantelastejas.es/", "v"),
    ("La Boutique", "Web", "diseno-web-caso-la-boutique.webp", None, "g"),
    ("RFG Andrade", "Web", "diseno-web-caso-rfg-andrade.webp", "https://www.rfgandrade.es/", "h"),
    ("Dotti Peluquería", "Ficha de Google", "seo-local-caso-dotti-peluqueria.webp", None, "v"),
]
CASOS_VER = "Ver la web"

CINTA_PORTADA = ["Alcorcón", "SEO local", "Google Maps", "Webs que llaman"]
CINTA_SECUNDARIA = None

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
                   "- Un solo interlocutor por proyecto, profesionales de confianza cuando hacen falta y un equipo de agentes de IA con nombre propio, presentados como tales.",
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
                 "expertise": "Expertise"}

# Imagen para redes (Open Graph) por página, 1200 × 630: la genera rematar.py con PIL (fondo crema, H1 en Outfit,
# símbolo fucsia). Fuentes TTF y símbolo en recursos/og/.
OG = {"fondo": "#F5F1EC", "texto": "#1C1219", "acento": "#E0067A", "gris": "#6B5F66"}
