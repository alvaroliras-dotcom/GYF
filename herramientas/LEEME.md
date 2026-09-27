# Herramientas

Las que se montaron en la primera web GYF-Orisa y ahorran horas en cada web. Se copian al repositorio del cliente
(carpeta `herramientas/`) o se usan desde aquí.

| Herramienta | Paso del protocolo | Qué hace |
|---|---|---|
| `servir.sh` | 28-30 | Genera la web y la sirve en local (`http://localhost:8765`) para las capturas y Lighthouse |
| `capturas.js` | 29 | Primera pantalla del móvil y del ordenador, página entera, desborde horizontal, errores de consola y si en la primera pantalla del móvil se ven la foto, la nota y el botón de llamar |
| `lighthouse.sh` | 30 | Lighthouse móvil tres veces por página y la mediana (la nota varía entre pasadas) |
| `entrega.py` | 27 | Prepara `08-WEB`: la copia completa con `sitio/` en tandas de 95, `vN-CAMBIOS` con solo lo que cambia (partido en tandas si pasa de 95) y el `LEEME.txt` con el orden de arrastre |

### Nuevas en la v2 (web de GYF)

| Herramienta | Qué hace |
|---|---|
| `objetos3d/generar.py` | La familia de 20 objetos 3D de la marca (cromo, fucsia lacado, berenjena, crema) pintada con three.js en Chromium sin cabeza (SwiftShader). Deja los máster PNG 1.600 con alfa en `objetos3d/master/`; `rematar.py` saca los WebP 400/800/1.200. `hoja.py` hace la hoja de revisión |
| `objetos3d/construir.sh` | Compila `cliente/js/vendor/web3d.min.js`: el símbolo 3D de la portada y las tres piezas que giran en vivo (`piezas.js`), con una sola copia de three y la misma luz de estudio (`estudio.js`) que las imágenes fijas |
| `maquetas/maquetas.py` | Las composiciones de los casos: capturas reales (`/home/claude/gyf/casos/crudo/`) en portátil y móvil dibujados en CSS, con perspectiva, sombra, fondo de la marca y un objeto 3D. Salen en `recursos/casos/` |
| `logos_color.py` | La versión en su color original de cada logotipo de cliente (`recursos/clientes-color/`), para el paso de gris a color |
| `capturas_v2.py` | Página entera a 1.440 y 390 (con movimiento reducido: la página sale quieta y completa); avisa de errores de JS y desborde |
| `tira_v2.py` | Tira de fotogramas (y vídeo con `--video`) del desplazamiento de la home CON movimiento |
| `lighthouse_v2.py` | Lighthouse móvil con el servidor en un hilo (mediana de N pasadas) |

`python3 generador/rematar.py rapido` rehace solo CSS, JS y archivos del servidor (las imágenes se conservan entre builds y
solo se regeneran si su original cambia). Para la entrega, siempre el `rematar.py` completo.

**Orden de una vuelta de trabajo:** `bash servir.sh` → `node capturas.js …` → `bash lighthouse.sh …`
→ commit → `python3 entrega.py …` → la carpeta `08-WEB` se copia a la del cliente.

Todas se lanzan desde la raíz del repositorio del cliente. `capturas.js` lee la clave de cookies de
`generador/config.py`, así que no hay que tocar nada.
