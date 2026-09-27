/* GYF · Módulo 3D de la web (v2): una sola copia de three para el objeto de portada (símbolo extruido)
   y las tres piezas que giran en vivo. Compilar:  bash herramientas/objetos3d/construir.sh
   → cliente/js/vendor/web3d.min.js (IIFE, window.Web3D). Lo carga main.js en diferido, solo en ordenador. */
export { montar, soporta } from "../objeto3d/objeto3d.js";
export { montarPieza } from "./piezas.js";
