/* GYF · Piezas que giran en vivo (v2). Tres primitivas de three (nudo, anillos, píldoras) con la misma luz y
   los mismos materiales que sus imágenes fijas (estudio.js). Solo ordenador, sin movimiento reducido y con WebGL:
   la imagen fija de debajo es el respaldo y el lienzo se funde encima cuando ha pintado su primer fotograma.
   Cada pieza pinta solo mientras se ve (IntersectionObserver) y se para con la pestaña oculta. */
import { WebGLRenderer, Scene, PerspectiveCamera, Group, Box3, Sphere, ACESFilmicToneMapping, SRGBColorSpace } from "three";
import { prepararEntorno, lucesApoyo, piezaPrimitiva, simboloMalla } from "./estudio.js";

/* v3: la pieza es el símbolo G+F (data-pieza="simbolo", data-mats="fucsia" o "berenjena,fucsia"), extruido desde el
   SVG real (/marca/simbolo-3d.svg, se descarga una vez para las tres). Las primitivas siguen disponibles. */
let svgProm = null;
const svg = () => svgProm || (svgProm = fetch("/marca/simbolo-3d.svg").then(r => r.text()));

let mx = 0, my = 0;
addEventListener("pointermove", e => { mx = e.clientX / innerWidth - .5; my = e.clientY / innerHeight - .5; }, { passive: true });

export async function montarPieza(caja, opts) {
  opts = opts || {};
  const tipo = caja.getAttribute("data-pieza");
  const txt = tipo === "simbolo" ? await svg() : null;
  const lienzo = caja.querySelector("[data-lienzo]") || caja;
  const W = () => lienzo.clientWidth || 300, H = () => lienzo.clientHeight || 300;
  const r = new WebGLRenderer({ antialias: true, alpha: true, powerPreference: "low-power" });
  r.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.75));
  r.setSize(W(), H());
  r.setClearColor(0x000000, 0);
  r.toneMapping = ACESFilmicToneMapping; r.outputColorSpace = SRGBColorSpace;
  r.domElement.setAttribute("aria-hidden", "true");
  lienzo.appendChild(r.domElement);
  const sc = new Scene(); prepararEntorno(r, sc); lucesApoyo(sc);
  const p = tipo === "simbolo" ? simboloMalla(txt, (caja.getAttribute("data-mats") || "fucsia").split(","), { calidad: .6 }) : piezaPrimitiva(tipo);
  const piv = new Group(); piv.add(p); sc.add(piv);
  const giro = (caja.getAttribute("data-giro") || "0.3,0.3").split(",").map(Number);
  piv.rotation.set(giro[0], giro[1], 0);
  piv.updateMatrixWorld(true);
  const esf = new Box3().setFromObject(piv).getBoundingSphere(new Sphere());
  p.position.sub(esf.center.clone().applyMatrix4(piv.matrixWorld.clone().invert()));
  const cam = new PerspectiveCamera(26, 1, .1, 100);
  const encuadra = () => { cam.aspect = W() / H(); cam.position.set(0, 0, esf.radius / Math.sin(13 * Math.PI / 180) * .8 * Math.max(1, 1 / cam.aspect)); cam.updateProjectionMatrix(); };
  encuadra();
  const vel = .32 + Math.random() * .12, fase = Math.random() * 6;
  let raf = 0, vivo = true, visible = false;
  const t0 = performance.now();
  function pinta() {
    const t = (performance.now() - t0) / 1000;
    piv.rotation.y = giro[1] + Math.sin(t * vel * 1.6 + fase) * .7 + mx * .5;   // vaivén: el símbolo nunca queda de canto
    piv.rotation.x = giro[0] + Math.sin(t * .7 + fase) * .16 + my * .3;
    piv.position.y = Math.sin(t * 1.1 + fase) * .06;
    r.render(sc, cam);
  }
  function bucle() {
    cancelAnimationFrame(raf);
    if (!vivo || !visible || document.hidden) return;
    raf = requestAnimationFrame(() => { pinta(); bucle(); });
  }
  const io = new IntersectionObserver(e => { visible = e[e.length - 1].isIntersecting; bucle(); }, { rootMargin: "60px" });
  io.observe(caja);
  document.addEventListener("visibilitychange", bucle);
  addEventListener("resize", () => { r.setSize(W(), H()); encuadra(); pinta(); });
  pinta();
  if (opts.listo) requestAnimationFrame(() => opts.listo(r.domElement));
  return { parar() { vivo = false; cancelAnimationFrame(raf); io.disconnect(); r.dispose(); } };
}
