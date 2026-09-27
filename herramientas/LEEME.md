# Herramientas

Las que se montaron en la primera web GYF-Orisa y ahorran horas en cada web. Se copian al repositorio del cliente
(carpeta `herramientas/`) o se usan desde aquí.

| Herramienta | Paso del protocolo | Qué hace |
|---|---|---|
| `servir.sh` | 28-30 | Genera la web y la sirve en local (`http://localhost:8765`) para las capturas y Lighthouse |
| `capturas.js` | 29 | Primera pantalla del móvil y del ordenador, página entera, desborde horizontal, errores de consola y si en la primera pantalla del móvil se ven la foto, la nota y el botón de llamar |
| `lighthouse.sh` | 30 | Lighthouse móvil tres veces por página y la mediana (la nota varía entre pasadas) |
| `entrega.py` | 27 | Prepara `08-WEB`: la copia completa con `sitio/` en tandas de 95, `vN-CAMBIOS` con solo lo que cambia (partido en tandas si pasa de 95) y el `LEEME.txt` con el orden de arrastre |

**Orden de una vuelta de trabajo:** `bash servir.sh` → `node capturas.js …` → `bash lighthouse.sh …`
→ commit → `python3 entrega.py …` → la carpeta `08-WEB` se copia a la del cliente.

Todas se lanzan desde la raíz del repositorio del cliente. `capturas.js` lee la clave de cookies de
`generador/config.py`, así que no hay que tocar nada.
