/* GYF · Escultor (v2): la familia de objetos 3D de la marca, renderizada en Chromium sin cabeza.
   Formas de campo de distancia (SDF) poligonizadas con marching cubes (tablas de three) + piezas primitivas.
   Se compila con esbuild a escultor.bundle.js (IIFE, window.Escultor) y lo usa generar.py. */
import { WebGLRenderer, Scene, PerspectiveCamera, Group, Mesh, BufferGeometry, BufferAttribute, Box3, Vector3, Sphere,
  ACESFilmicToneMapping, SRGBColorSpace, ExtrudeGeometry, TorusGeometry, CapsuleGeometry, SphereGeometry, Color } from "three";
import { edgeTable, triTable } from "three/examples/jsm/objects/MarchingCubes.js";
import { SVGLoader } from "three/examples/jsm/loaders/SVGLoader.js";
import { prepararEntorno, lucesApoyo, material, piezaPrimitiva, simboloMalla } from "./estudio.js";

/* ================= SDF (fórmulas de Íñigo Quílez) ================= */
const len2 = (x, y) => Math.hypot(x, y), len3 = (x, y, z) => Math.hypot(x, y, z);
const clamp = (x, a, b) => Math.max(a, Math.min(b, x));
function sdRoundBox(x, y, z, bx, by, bz, r) {
  const qx = Math.abs(x) - bx + r, qy = Math.abs(y) - by + r, qz = Math.abs(z) - bz + r;
  return len3(Math.max(qx, 0), Math.max(qy, 0), Math.max(qz, 0)) + Math.min(Math.max(qx, Math.max(qy, qz)), 0) - r;
}
function smin(a, b, k) { const h = clamp(.5 + .5 * (b - a) / k, 0, 1); return b + (a - b) * h - k * h * (1 - h); }
function smax(a, b, k) { return -smin(-a, -b, k); }
function sdStar5(px, py, r, rf) {   // estrella de 5 puntas 2D
  const k1x = 0.809016994375, k1y = -0.587785252292, k2x = -k1x, k2y = k1y;
  px = Math.abs(px);
  let d = k1x * px + k1y * py; px -= 2 * Math.max(d, 0) * k1x; py -= 2 * Math.max(d, 0) * k1y;
  d = k2x * px + k2y * py; px -= 2 * Math.max(d, 0) * k2x; py -= 2 * Math.max(d, 0) * k2y;
  px = Math.abs(px); py -= r;
  const bax = rf * -k1y, bay = rf * k1x - 1;   // ba = rf*(-k1.y,k1.x) - (0,1)
  const h = clamp((px * bax + py * bay) / (bax * bax + bay * bay), 0, r);
  return len2(px - bax * h, py - bay * h) * Math.sign(py * bax - px * bay);
}
function sdPoly(px, py, v) {        // polígono 2D (lista [x,y])
  let d = (px - v[0][0]) ** 2 + (py - v[0][1]) ** 2, s = 1;
  for (let i = 0, j = v.length - 1; i < v.length; j = i, i++) {
    const ex = v[j][0] - v[i][0], ey = v[j][1] - v[i][1], wx = px - v[i][0], wy = py - v[i][1];
    const h = clamp((wx * ex + wy * ey) / (ex * ex + ey * ey), 0, 1);
    d = Math.min(d, (wx - ex * h) ** 2 + (wy - ey * h) ** 2);
    const c1 = py >= v[i][1], c2 = py < v[j][1], c3 = ex * wy > ey * wx;
    if ((c1 && c2 && c3) || (!c1 && !c2 && !c3)) s = -s;
  }
  return s * Math.sqrt(d);
}
function sdRoundRect2(px, py, bx, by, r) {
  const qx = Math.abs(px) - bx + r, qy = Math.abs(py) - by + r;
  return len2(Math.max(qx, 0), Math.max(qy, 0)) + Math.min(Math.max(qx, qy), 0) - r;
}
// Extrusión «hinchada»: una forma 2D con grosor h y los cantos redondeados de radio r
function extruir(d2, z, h, r) { const wx = d2 + r, wy = Math.abs(z) - h + r; return Math.min(Math.max(wx, wy), 0) + len2(Math.max(wx, 0), Math.max(wy, 0)) - r; }

/* ================= Marching cubes con vértices compartidos y normales del gradiente ================= */
function poligonizar(sdf, B, n) {
  const N1 = n + 1, st = 2 * B / n;
  const val = new Float32Array(N1 * N1 * N1);
  for (let k = 0; k < N1; k++) for (let j = 0; j < N1; j++) for (let i = 0; i < N1; i++)
    val[(k * N1 + j) * N1 + i] = sdf(-B + i * st, -B + j * st, -B + k * st);
  const idx = (i, j, k) => (k * N1 + j) * N1 + i;
  const mapa = new Map(), P = [], I = [];
  const OFF = [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0], [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]];
  const EDGE = [[0, 1], [1, 2], [2, 3], [3, 0], [4, 5], [5, 6], [6, 7], [7, 4], [0, 4], [1, 5], [2, 6], [3, 7]];
  const cv = new Float32Array(8), ev = new Int32Array(12);
  for (let k = 0; k < n; k++) for (let j = 0; j < n; j++) for (let i = 0; i < n; i++) {
    let ci = 0;
    for (let c = 0; c < 8; c++) { cv[c] = val[idx(i + OFF[c][0], j + OFF[c][1], k + OFF[c][2])]; if (cv[c] < 0) ci |= 1 << c; }
    const e = edgeTable[ci]; if (!e) continue;
    for (let q = 0; q < 12; q++) {
      if (!(e & (1 << q))) continue;
      const [a, b] = EDGE[q];
      const ia = idx(i + OFF[a][0], j + OFF[a][1], k + OFF[a][2]), ib = idx(i + OFF[b][0], j + OFF[b][1], k + OFF[b][2]);
      const key = ia < ib ? ia * 4194304 + ib : ib * 4194304 + ia;
      let v = mapa.get(key);
      if (v === undefined) {
        const t = cv[a] / (cv[a] - cv[b]);
        const x = -B + (i + OFF[a][0] + (OFF[b][0] - OFF[a][0]) * t) * st;
        const y = -B + (j + OFF[a][1] + (OFF[b][1] - OFF[a][1]) * t) * st;
        const z = -B + (k + OFF[a][2] + (OFF[b][2] - OFF[a][2]) * t) * st;
        v = P.length / 3; P.push(x, y, z); mapa.set(key, v);
      }
      ev[q] = v;
    }
    for (let t = 0; triTable[ci * 16 + t] !== -1; t += 3)
      I.push(ev[triTable[ci * 16 + t]], ev[triTable[ci * 16 + t + 1]], ev[triTable[ci * 16 + t + 2]]);
  }
  // Normales desde el gradiente del campo (superficie lisa sin facetas)
  const Nn = new Float32Array(P.length), h = st * .5;
  for (let v = 0; v < P.length; v += 3) {
    const x = P[v], y = P[v + 1], z = P[v + 2];
    let nx = sdf(x + h, y, z) - sdf(x - h, y, z), ny = sdf(x, y + h, z) - sdf(x, y - h, z), nz = sdf(x, y, z + h) - sdf(x, y, z - h);
    const l = Math.hypot(nx, ny, nz) || 1; Nn[v] = nx / l; Nn[v + 1] = ny / l; Nn[v + 2] = nz / l;
  }
  // Orientación de los triángulos coherente con la normal
  for (let t = 0; t < I.length; t += 3) {
    const a = I[t] * 3, b = I[t + 1] * 3, c = I[t + 2] * 3;
    const ux = P[b] - P[a], uy = P[b + 1] - P[a + 1], uz = P[b + 2] - P[a + 2];
    const wx = P[c] - P[a], wy = P[c + 1] - P[a + 1], wz = P[c + 2] - P[a + 2];
    const fx = uy * wz - uz * wy, fy = uz * wx - ux * wz, fz = ux * wy - uy * wx;
    if (fx * Nn[a] + fy * Nn[a + 1] + fz * Nn[a + 2] < 0) { const s = I[t + 1]; I[t + 1] = I[t + 2]; I[t + 2] = s; }
  }
  const geo = new BufferGeometry();
  geo.setAttribute("position", new BufferAttribute(new Float32Array(P), 3));
  geo.setAttribute("normal", new BufferAttribute(Nn, 3));
  geo.setIndex(P.length / 3 > 65535 ? new BufferAttribute(new Uint32Array(I), 1) : new BufferAttribute(new Uint16Array(I), 1));
  return geo;
}

/* ================= Las formas ================= */
const FORMAS = {
  // Jaula: cubo redondeado hueco con un agujero redondo en cada cara (el objeto de Rayo, a la GYF)
  jaula: { B: 1.25, sdf(x, y, z) {
    const caja = sdRoundBox(x, y, z, 1, 1, 1, .42);
    const hueca = Math.abs(caja + .17) - .17;
    const r = .66;
    const cx = len2(y, z) - r, cy = len2(x, z) - r, cz = len2(x, y) - r;
    return smax(hueca, -Math.min(cx, Math.min(cy, cz)), .12);
  } },
  // Cinta retorcida: banda de Möbius gruesa (tres medias vueltas)
  cinta: { B: 1.6, sdf(x, y, z) {
    const R = 1.05, th = Math.atan2(z, x), q = len2(x, z) - R;
    const a = th * 1.5, c = Math.cos(a), s = Math.sin(a);
    const u = c * q - s * y, v = s * q + c * y;
    return sdRoundRect2(u, v, .44, .09, .085) * .8;
  } },
  // Chincheta de Google Maps hinchada, con su agujero
  chincheta: { B: 1.55, sdf(x, y, z) {
    const cabeza = len2(x, y - .35) - .92;
    const punta = sdPoly(x, y, [[-.78, .0], [.78, .0], [0, -1.42]]);
    let d2 = smin(cabeza, punta, .28);
    d2 = smax(d2, -(len2(x, y - .38) - .36), .06);
    return extruir(d2, z, .34, .3);
  } },
  // Estrella de reseña, hinchada
  estrella: { B: 1.35, sdf(x, y, z) { return extruir(sdStar5(x, y + .06, 1.12, .52) - .06, z, .3, .28); } },
  // Flecha de cursor (anuncios)
  cursor: { B: 1.45, sdf(x, y, z) {
    const v = [[-.72, 1.18], [-.72, -.72], [-.27, -.3], [.06, -1.12], [.42, -.96], [.1, -.16], [.72, -.14]];
    return extruir(sdPoly(x, y, v) - .08, z, .26, .22);
  } },
  // Bocadillo (redacción) con tres puntos
  bocadillo: { B: 1.45, sdf(x, y, z) {
    const caja = sdRoundRect2(x, y - .12, 1.12, .76, .5);
    const cola = sdPoly(x, y, [[-.6, -.35], [.02, -.35], [-.66, -1.02]]) - .06;
    return extruir(smin(caja, cola, .12), z, .3, .27);
  } },
  // Esfera de celosía giroide (abstracta, como la del vídeo de Rayo)
  giroide: { B: 1.2, sdf(x, y, z) {
    const f = 3.6;
    const g = (Math.sin(x * f) * Math.cos(y * f) + Math.sin(y * f) * Math.cos(z * f) + Math.sin(z * f) * Math.cos(x * f)) / f;
    const concha = Math.abs(g) - .07;
    return smax(concha, len3(x, y, z) - 1.08, .05);
  } },
};

/* ================= Escenas ================= */
let R = null;
function renderer(tam) {
  if (!R) {
    R = new WebGLRenderer({ antialias: true, alpha: true, preserveDrawingBuffer: true });
    R.setPixelRatio(1); R.setClearColor(0x000000, 0);
    R.toneMapping = ACESFilmicToneMapping; R.toneMappingExposure = 1.0; R.outputColorSpace = SRGBColorSpace;
    document.body.appendChild(R.domElement);
  }
  R.setSize(tam, tam);
  return R;
}

function malla(nombre, mat, res) { const F = FORMAS[nombre]; return new Mesh(poligonizar(F.sdf, F.B, res), material(mat)); }

let SVG_TXT = null;
function simbolo(mat) {
  const datos = new SVGLoader().parse(SVG_TXT);
  const g = new Group(); const cj = new Box3();
  const shapes = []; datos.paths.forEach(p => SVGLoader.createShapes(p).forEach(s => shapes.push(s)));
  shapes.forEach(sh => { const t = new ExtrudeGeometry(sh, { depth: 1, bevelEnabled: false }); t.computeBoundingBox(); cj.union(t.boundingBox); t.dispose(); });
  const tm = new Vector3(); cj.getSize(tm); const m = Math.max(tm.x, tm.y);
  const mt = material(mat);
  shapes.forEach(sh => g.add(new Mesh(new ExtrudeGeometry(sh, { depth: m * .12, bevelEnabled: true, bevelThickness: m * .035, bevelSize: m * .022, bevelSegments: 14, curveSegments: 64 }), mt)));
  const b = new Box3().setFromObject(g), c = b.getCenter(new Vector3());
  g.children.forEach(x => x.geometry.translate(-c.x, -c.y, -c.z));
  g.scale.set(2 / m, -2 / m, 2 / m);
  return g;
}

function construir(p, res) {
  const g = new Group(), mats = p.mats || [];
  const M = (i, def) => mats[i] || def;
  switch (p.forma) {
    case "jaula": case "cinta": case "chincheta": case "estrella": case "cursor": case "giroide":
      g.add(malla(p.forma, M(0, "cromo"), res)); break;
    case "bocadillo": {
      g.add(malla("bocadillo", M(0, "crema"), res));
      [-.5, 0, .5].forEach(x => { const s = new Mesh(new SphereGeometry(.15, 48, 32), material(M(1, "fucsia"))); s.position.set(x, .12, .34); g.add(s); });
      break;
    }
    case "lupa": {
      const aro = new Mesh(new TorusGeometry(.72, .17, 64, 160), material(M(0, "cromo")));
      aro.position.set(-.25, .3, 0);
      const cristal = new Mesh(new SphereGeometry(.72, 64, 32), material("cristal")); cristal.scale.set(1, 1, .12); cristal.position.copy(aro.position);
      const mango = new Mesh(new CapsuleGeometry(.2, .95, 24, 48), material(M(1, "fucsia")));
      mango.position.set(.62, -.62, 0); mango.rotation.z = Math.PI / 4;
      g.add(aro, cristal, mango); break;
    }
    case "barras": {
      const alt = [.9, 1.5, 1.15, 2.1], col = ["crema", "rosa", "berenjena", "fucsia"];
      alt.forEach((h, i) => {
        const F = (x, y, z) => sdRoundBox(x, y, z, .3, h / 2, .3, .16);
        const me = new Mesh(poligonizar(F, Math.max(1.1, h / 2 + .1), Math.round(res * .6)), material(M(i, col[i])));
        me.position.set(-1.05 + i * .7, h / 2 - 1.05, (i % 2) * .08); g.add(me);
      });
      break;
    }
    case "abanico": {
      const col = ["crema", "rosa", "fucsia", "berenjena", "cromo"];
      col.forEach((c, i) => {
        const F = (x, y, z) => sdRoundBox(x, y, z, .28, 1.05, .045, .04);
        const me = new Mesh(poligonizar(F, 1.12, Math.round(res * .7)), material(M(i, c)));
        const gg = new Group(); me.position.y = .85; gg.add(me);
        gg.rotation.z = (i - 2) * -.32; gg.position.z = i * .1; g.add(gg);
      });
      const eje = new Mesh(new SphereGeometry(.13, 48, 32), material("cromo")); eje.position.set(0, 0, .6); eje.scale.z = .5; g.add(eje);
      break;
    }
    case "simbolo": g.add(simboloMalla(SVG_TXT, [M(0, "fucsia"), M(1, M(0, "fucsia"))], { despiece: p.despiece })); break;
    case "grupo": {   // varios símbolos pequeños en composición: [x, y, z, escala, rx, ry, rz, matG, matF]
      (p.grupo || []).forEach(q => {
        const s = simboloMalla(SVG_TXT, [q[7], q[8] || q[7]]);
        s.position.set(q[0], q[1], q[2]); s.scale.setScalar(q[3]); s.rotation.set(q[4], q[5], q[6]); g.add(s);
      });
      break;
    }
    case "nudo": case "anillos": case "pildoras": case "esferas": {
      const ms = {}; if (mats.length) ["fucsia", "crema", "berenjena", "rosa", "cromo"].forEach((n, i) => { if (mats[i]) ms[n] = material(mats[i]); });
      g.add(piezaPrimitiva(p.forma, ms)); break;
    }
  }
  return g;
}

/* p: { forma, mats[], giro:[x,y,z], tam, res, margen, svg } → devuelve un PNG (dataURL) con alfa */
export async function render(p) {
  if (p.svg) SVG_TXT = p.svg;
  const tam = p.tam || 2400;
  const r = renderer(tam);
  const sc = new Scene(); prepararEntorno(r, sc); lucesApoyo(sc);
  const obj = construir(p, p.res || 170);
  const piv = new Group(); piv.add(obj);
  const gi = p.giro || [0, 0, 0]; piv.rotation.set(gi[0], gi[1], gi[2] || 0);
  sc.add(piv);
  // Encuadre: la esfera que envuelve al objeto ocupa el cuadro menos el margen
  piv.updateMatrixWorld(true);
  const bb = new Box3().setFromObject(piv), esf = bb.getBoundingSphere(new Sphere());
  const cam = new PerspectiveCamera(26, 1, .1, 200);
  const fov = 26 * Math.PI / 180, margen = p.margen == null ? .07 : p.margen;
  const dist = esf.radius / Math.sin(fov / 2) * (1 + margen * 2) * (p.zoom || 1);
  cam.position.set(esf.center.x, esf.center.y, esf.center.z + dist); cam.lookAt(esf.center);
  r.render(sc, cam);
  return r.domElement.toDataURL("image/png");
}
