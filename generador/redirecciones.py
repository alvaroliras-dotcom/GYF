# -*- coding: utf-8 -*-
"""Redirecciones de la web vieja (WordPress) a la nueva · caso E: todo es nuevo.
Fuente: nuria2/arquitectura.md, sección c.1 (76 filas: 65 × 301, 3 × 302, 2 × 410, 6 que siguen con 200) y c.2;
adjuntos de la mediateca desde bruno/media.json. Rutas SIN barra inicial ni final (la regla casa con y sin barra).
Destinos relativos a la raíz: rematar.py los escribe ABSOLUTOS (https, sin www) y ANTES de las reglas de host,
así cualquier variante (http, www, sin barra) llega en UN solo salto."""

# 301 · URL vieja → URL nueva (fila de arquitectura.md)
REDIRECCIONES = [
    ("servicios", "/"),                                                      # 2
    ("mapa-de-servicios", "/"),                                              # 3
    ("servicios/seo-local", "/seo-local/"),                                  # 4
    ("servicios/seo-local/optimizacion-ficha-gbp-02", "/seo-local/"),        # 5
    ("servicios/seo-local/optimizacion-ficha-gbp", "/seo-local/"),           # 6
    ("servicios/seo-local/estrategia-resenas-reputacion", "/seo-local/"),    # 7
    ("servicios/seo-local/auditoria-seo-local", "/auditoria-seo-local/"),    # 8
    ("servicios/seo-local/redaccion-seo-local", "/redaccion-seo-copywriting/"), # 9
    ("auditoria-gratis", "/auditoria-seo-local/"),                           # 10
    ("servicios/diseno-web", "/diseno-web/"),                                # 11
    ("servicios/diseno-web/webs-para-conversion", "/diseno-web/"),           # 12
    ("servicios/diseno-web/responsive-velocidad", "/diseno-web/"),           # 13
    ("servicios/diseno-web/integraciones-analitica-ficha-google", "/diseno-web/"), # 14
    ("servicios/diseno-web/arquitectura-web-seo", "/diseno-web/"),           # 15
    ("servicios/desarrollo-paginas-web", "/diseno-web/"),                    # 16
    ("servicios/mantenimiento", "/diseno-web/"),                             # 17
    ("servicios/google-ads", "/google-ads/"),                                # 18
    ("servicios/google-ads/google-ads-local", "/google-ads/"),               # 19
    ("servicios/google-ads/paginas-aterrizaje-conversion", "/google-ads/"),  # 20
    ("servicios/google-ads/display-geolocalizado", "/google-ads/"),          # 21
    ("servicios/google-ads/anuncios-en-maps-youtube", "/google-ads/"),       # 22
    ("servicios/diseno-grafico", "/diseno-grafico/"),                        # 23
    ("servicios/diseno-grafico/imagen-marca-branding", "/diseno-grafico/"),  # 24
    ("servicios/diseno-grafico/diseno-grafico-para-web-y-redes-sociales", "/diseno-grafico/"), # 25
    ("servicios/diseno-grafico/packaging-etiquetado-producto", "/diseno-grafico/"), # 26
    ("servicios/diseno-grafico/diseno-editorial-y-publicitario", "/diseno-grafico/"), # 27
    ("servicios/diseno", "/diseno-grafico/"),                                # 28
    ("servicios/marketing-contenidos", "/redaccion-seo-copywriting/"),       # 29
    ("servicios/marketing-contenidos/redaccion-seo-web", "/redaccion-seo-copywriting/"), # 30
    ("servicios/marketing-contenidos/copywriting-emocional", "/redaccion-seo-copywriting/"), # 31
    ("servicios/marketing-contenidos/entradas-blog-local", "/redaccion-seo-copywriting/"), # 32
    ("servicios/marketing-contenidos/publicaciones-para-gbp", "/seo-local/"), # 33
    ("servicios/estrategia-contenido", "/redaccion-seo-copywriting/"),       # 34
    ("servicios/analitica-web", "/analitica-web/"),                          # 35
    ("servicios/analitica-web/implementacion-ga4-search-console", "/analitica-web/"), # 36
    ("servicios/analitica-web/informes-mensuales-personalizados", "/analitica-web/"), # 37
    ("servicios/analitica-web/cuadro-de-mando-local", "/analitica-web/"),    # 38
    ("servicios/analitica-web/auditorias-de-rendimiento-local", "/analitica-web/"), # 39
    ("informes-mensuales-personalizados", "/analitica-web/"),                # 40
    ("servicios/estrategia", "/"),                                           # 41
    ("servicios/posicionamiento-buscadores", "/"),                           # 42
    ("sobre-gyf", "/quienes-somos/"),                                        # 43
    ("empresa", "/quienes-somos/"),                                          # 45
    ("formulario-ampliado-de-contaco", "/contacto/"),                        # 47
    ("arrancamos", "/"),                                                     # 48
    ("en-construccion", "/"),                                                # 49
    ("politica-de-cookies-ue", "/politica-de-cookies/"),                     # 53
    ("mas-informacion-sobre-las-cookies", "/politica-de-cookies/"),          # 54
    ("trabajos/curso-de-google-analytics", "/analitica-web/"),               # 60
    ("trabajos/luxurycomm", "/"),                                            # 61
    ("trabajos/el-atelier-de-fabula", "/"),                                  # 62
    ("trabajos/ines-ingenieros-consultores", "/"),                           # 63
    ("trabajos/psicorazon", "/"),                                            # 64
    ("trabajos/maribel-yebenes", "/"),                                       # 65
    ("trabajos/vinos-pousada", "/"),                                         # 66
    ("trabajos/expertise", "/"),                                             # 67
    ("trabajos/apunto-let", "/"),                                            # 68
    ("trabajos/zinzin-madrid", "/"),                                         # 69
    ("trabajos/momentos-madrid", "/"),                                       # 70
    ("trabajos/maria-lisboa-villa", "/"),                                    # 71
    ("trabajos/mundo-calor", "/"),                                           # 72
    ("trabajos/aurea", "/"),                                                 # 73
    ("trabajos/red-yellow-red", "/"),                                        # 74
    ("trabajos/delfinia-piscinas", "/"),                                     # 75
    ("trabajos/sure-limpieza-sostenible", "/"),                              # 76
]

# 302 temporales: /trabajos/ y los dos casos que volverán a servir 200 cuando exista el portfolio
REDIRECCIONES_302 = [
    ("trabajos", "/"),  # 57
    ("trabajos/solvento", "/"),  # 58
    ("trabajos/la-casita-de-los-animales", "/"),  # 59
]

# 410 · ya no existen y no vuelven: filas 410 de la tabla, categorías de la plantilla de WordPress (c.2)
# y páginas de adjunto de la mediateca (bruno/media.json)
GONE_410 = [
    "error-404",  # 55
    "cookies",  # 56
    "lifestyle",  # categoría (c.2)
    "mobile",  # categoría (c.2)
    "motion",  # categoría (c.2)
    "news",  # categoría (c.2)
    "photography",  # categoría (c.2)
    "priest",  # categoría (c.2)
    "sport",  # categoría (c.2)
    "subjects",  # categoría (c.2)
    "technology",  # categoría (c.2)
    "uncategorized",  # categoría (c.2)
    "00-slider-sobre-gyf",
    "000-equipo-gyf",
    "001-alvaro-liras-grande-jpg",
    "001-alvaro-liras-grande",
    "001-alvaro-liras",
    "002-jean-pierre",
    "003-merche",
    "004-jean-paul",
    "005-inaki",
    "006-marta",
    "007-gonzalo",
    "008-matias",
    "009-dani",
    "010-vanesa",
    "011-lorena",
    "146-diseno-piezas",
    "147-coherencia-entre-piezas",
    "148-gerarquia-claridad",
    "149-adaptacion-soporte",
    "154-sobre-gyf-01",
    "155-sobre-gyf-02",
    "156-sobre-gyf-03",
    "chatgpt-image-5-ene-2026-05_48_12-p-m",
    "diseno-editorial-01",
    "diseno-editorial-02",
    "diseno-editorial-03",
    "diseno-editorial-04",
    "diseno-marca",
    "legit-2-png",
    "materiales-impresos-no-funcionan",
    "reunion-trabajo-barman",
    "servicios/seo-local/01-slider-servicios-seo-local-00",
    "tarjeta-logo-gyf",
]

# Patrones 410 (expresión regular sobre la ruta sin barra inicial): adjuntos colgados de páginas viejas
GONE_410_PATRONES = [
    r"^servicios/[^/]+/[^/]+/[^/]+/?$",                       # /servicios/<servicio>/<subservicio>/<adjunto>/
    r"^(auditoria-gratis|contacto|home-gyf|icono-gyf)/[^/]+/?$",   # /contacto/157-hablemos-contacto/ y similares
    r"^index\.php$",
]
