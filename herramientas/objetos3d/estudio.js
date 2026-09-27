/* GYF · Estudio 3D común (v2).
   La luz de estudio y los materiales de la marca, compartidos por:
   - escultor.js  → genera las imágenes fijas de la familia de objetos (herramientas/objetos3d/generar.py)
   - piezas.js    → las tres piezas que giran en vivo en la web (cliente/js/vendor/piezas3d.min.js)
   Así la pieza en vivo y su imagen fija de respaldo salen con la misma luz y el mismo material. */
import { SVGLoader } from "three/examples/jsm/loaders/SVGLoader.js";
import { ExtrudeGeometry, Box3, Vector3 } from "three";
import { Scene, Mesh, BoxGeometry, SphereGeometry, PlaneGeometry, MeshBasicMaterial, BackSide, Color,
  MeshPhysicalMaterial, BufferAttribute, PMREMGenerator, Group, TorusKnotGeometry, TorusGeometry,
  CapsuleGeometry, DirectionalLight } from "three";

/* ---------- Entorno: estudio oscuro con cajas de luz (reflejos limpios en el cromo y en la laca) ---------- */
export function entornoEstudio() {
  const s = new Scene();
  // Fondo: esfera con degradado (arriba casi negro, horizonte gris cálido, suelo medio)
  const g = new SphereGeometry(60, 64, 32);
  const pos = g.attributes.position, col = [];
  for (let i = 0; i < pos.count; i++) {
    const y = pos.getY(i) / 60;
    let c;
    if (y > 0) c = 0.025 + Math.pow(1 - y, 3) * 0.3;  // cielo: casi negro arriba → 0,22 en el horizonte
    else c = 0.22 - Math.min(1, -y * 3) * 0.17;     // suelo: 0,22 → 0,05
    col.push(c * 1.02, c * 0.96, c * 0.97);          // un punto cálido
  }
  g.setAttribute("color", new BufferAttribute(new Float32Array(col), 3));
  s.add(new Mesh(g, new MeshBasicMaterial({ vertexColors: true, side: BackSide })));
  const panel = (w, h, x, y, z, int, color = 0xffffff) => {
    const m = new MeshBasicMaterial({ color: new Color(color).multiplyScalar(int), side: 2 });
    const p = new Mesh(new PlaneGeometry(w, h), m);
    p.position.set(x, y, z); p.lookAt(0, 0, 0); s.add(p); return p;
  };
  panel(30, 16, -18, 26, 22, 8);          // caja principal: arriba a la izquierda, delante
  panel(5, 34, 30, 6, -14, 10);            // tira de contraluz a la derecha, detrás
  panel(22, 8, -30, -4, 4, 2.4);
  panel(60, 1.6, 0, 16, 34, 9);              // línea de luz horizontal delante (el filo blanco del cromo)           // relleno bajo a la izquierda
  panel(16, 22, -8, 6, -34, 2.6, 0xE0067A); // panel fucsia detrás: tiñe los reflejos del cromo
  panel(14, 8, 24, 20, 26, 3.2);            // pequeño acento arriba a la derecha
  panel(50, 50, 0, -30, 0, 1.3, 0xF5EDE6); // suelo claro (el cromo refleja algo por abajo)
  return s;
}

export function prepararEntorno(renderer, scene) {
  const pm = new PMREMGenerator(renderer);
  const env = pm.fromScene(entornoEstudio(), 0.02).texture;
  scene.environment = env;
  pm.dispose();
  return env;
}

export function lucesApoyo(scene) {
  const k = new DirectionalLight(0xffffff, 1.1); k.position.set(-3, 5, 4); scene.add(k);
  const r = new DirectionalLight(0xffd9ec, 0.6); r.position.set(4, 1, -3); scene.add(r);
}

/* ---------- Materiales de la marca ---------- */
export const COLORES = { fucsia: "#E0067A", rosa: "#FF7AB8", berenjena: "#2B1726", crema: "#F3ECE3" };
export function material(nombre) {
  switch (nombre) {
    case "fucsia": return new MeshPhysicalMaterial({ color: COLORES.fucsia, roughness: .26, metalness: 0, clearcoat: 1, clearcoatRoughness: .05 });
    case "rosa": return new MeshPhysicalMaterial({ color: COLORES.rosa, roughness: .3, metalness: 0, clearcoat: 1, clearcoatRoughness: .06 });
    case "berenjena": return new MeshPhysicalMaterial({ color: COLORES.berenjena, roughness: .22, metalness: 0, clearcoat: 1, clearcoatRoughness: .04 });
    case "crema": return new MeshPhysicalMaterial({ color: COLORES.crema, roughness: .55, metalness: 0, clearcoat: .25, clearcoatRoughness: .4, sheen: .4, sheenColor: new Color("#ffffff") });
    case "cromo": return new MeshPhysicalMaterial({ color: "#F2F2F4", roughness: .05, metalness: 1 });
    case "cromo-fucsia": return new MeshPhysicalMaterial({ color: "#F07AB4", roughness: .12, metalness: 1 });
    case "cristal-fucsia": return new MeshPhysicalMaterial({ color: "#FFC2DF", roughness: .3, metalness: 0, transmission: 1, thickness: .6, ior: 1.35,
      attenuationColor: new Color("#FF4FA3"), attenuationDistance: 2.2, clearcoat: 1, clearcoatRoughness: .12, specularIntensity: 1, envMapIntensity: 1.6 });
    case "crema-mate": return new MeshPhysicalMaterial({ color: COLORES.crema, roughness: .78, metalness: 0, sheen: .6, sheenRoughness: .8, sheenColor: new Color("#ffffff") });
    case "cristal": return new MeshPhysicalMaterial({ color: "#fff4fa", roughness: 0, metalness: 0, clearcoat: 1, transparent: true, opacity: .28 });
    default: return new MeshPhysicalMaterial({ color: "#888" });
  }
}

/* ---------- Piezas primitivas (sirven en vivo: sin datos que descargar) ---------- */
export function piezaPrimitiva(tipo, mats) {
  const m = n => (mats && mats[n]) || material(n);
  const g = new Group();
  if (tipo === "nudo") {
    g.add(new Mesh(new TorusKnotGeometry(1, .36, 360, 64, 2, 3), m("fucsia")));
  } else if (tipo === "anillos") {
    const a = new Mesh(new TorusGeometry(1, .26, 64, 160), m("cromo"));
    const b = new Mesh(new TorusGeometry(1, .26, 64, 160), m("fucsia"));
    const c = new Mesh(new TorusGeometry(1, .26, 64, 160), m("berenjena"));
    a.position.x = -1.05; b.rotation.y = Math.PI / 2; c.position.x = 1.05;
    g.add(a, b, c);
  } else if (tipo === "pildoras") {
    const cols = ["fucsia", "crema", "berenjena", "rosa"];
    cols.forEach((n, i) => {
      const p = new Mesh(new CapsuleGeometry(.42, 1.55, 24, 64), m(n));
      p.rotation.z = Math.PI / 2 + [.12, -.16, .2, -.1][i];
      p.rotation.y = [.25, -.3, .15, -.35][i];
      p.position.set([-.1, .22, -.18, .15][i], 1.2 - i * .8, [0, .1, 0, .12][i]);
      g.add(p);
    });
  } else if (tipo === "esferas") {
    [[0, 0, 0, 1, "fucsia"], [1.25, .7, -.3, .55, "cromo"], [-1.05, -.75, .4, .5, "berenjena"], [.62, -1.02, .7, .34, "crema"], [-.72, 1.0, .5, .3, "rosa"]]
      .forEach(([x, y, z, r, n]) => { const s = new Mesh(new SphereGeometry(r, 96, 64), m(n)); s.position.set(x, y, z); g.add(s); });
  }
  return g;
}

/* ---------- El símbolo G+F extruido desde el SVG real (la G y la F son los dos trazados del SVG) ----------
   mats: [material de la G, material de la F] (nombres o materiales) · despiece: [[x,y,z,rx,ry,rz] G, [..] F]
   Devuelve un grupo centrado de unas 2 unidades de alto. */
const _geo = new Map();
export function simboloMalla(svgTxt, mats, opts) {
  opts = opts || {};
  const mt = n => (typeof n === "string" ? material(n) : n);
  const clave = svgTxt.length + "|" + (opts.calidad || 1);
  let piezas = _geo.get(clave);
  if (!piezas) {
    const datos = new SVGLoader().parse(svgTxt);
    const cj = new Box3();
    const porTrazado = datos.paths.map(p => SVGLoader.createShapes(p));
    porTrazado.flat().forEach(sh => { const t = new ExtrudeGeometry(sh, { depth: 1, bevelEnabled: false }); t.computeBoundingBox(); cj.union(t.boundingBox); t.dispose(); });
    const tm = new Vector3(); cj.getSize(tm); const m = Math.max(tm.x, tm.y), c = cj.getCenter(new Vector3());
    const q = opts.calidad || 1;
    piezas = porTrazado.map(shs => shs.map(sh => {
      const gg = new ExtrudeGeometry(sh, { depth: m * .12, bevelEnabled: true, bevelThickness: m * .035, bevelSize: m * .022,
        bevelSegments: Math.round(14 * q), curveSegments: Math.round(64 * q) });
      gg.translate(-c.x, -c.y, -m * .06); gg.scale(2 / m, -2 / m, 2 / m); gg.computeVertexNormals();
      return gg;
    }));
    _geo.set(clave, piezas);
  }
  const g = new Group();
  piezas.forEach((geos, i) => {
    const sub = new Group();
    const mat = mt((mats && (mats[i] || mats[0])) || "fucsia");
    geos.forEach(gg => sub.add(new Mesh(gg, mat)));
    const d = opts.despiece && opts.despiece[i];
    if (d) { sub.position.set(d[0], d[1], d[2]); sub.rotation.set(d[3] || 0, d[4] || 0, d[5] || 0); }
    g.add(sub);
  });
  return g;
}
