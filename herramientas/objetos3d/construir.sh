#!/usr/bin/env bash
# Compila el módulo 3D de la web (objeto de portada + piezas en vivo) con una sola copia de three.
#   bash herramientas/objetos3d/construir.sh   (desde la raíz del repositorio)
# three@0.160 llega por el enlace node_modules → /home/claude/gyf/simbolo3d/node_modules (o npm i three@0.160.0 aquí).
set -e
cd "$(dirname "$0")"
[ -d node_modules/three ] || npm i --no-save three@0.160.0 >/dev/null
[ -e ../objeto3d/node_modules ] || ln -s "$(pwd)/node_modules" ../objeto3d/node_modules
npx --yes esbuild web3d.js --bundle --minify --format=iife --global-name=Web3D --target=es2019 \
  --legal-comments=none --outfile=../../cliente/js/vendor/web3d.min.js
ls -l ../../cliente/js/vendor/web3d.min.js
gzip -c ../../cliente/js/vendor/web3d.min.js | wc -c | awk '{printf "comprimido (gzip): %.0f KB\n", $1/1024}'
