/* GYF-Rayo · main.js
   Los marcadores con doble guion bajo (Europe/Madrid, ["1/1", "6/1", "1/5", "2/5", "15/8", "12/10", "1/11", "6/12", "8/12", "25/12", "2/11/2026", "7/12/2026", "8/9", "6/4/2026"]…) los rellena generador/rematar.py con config.py.
   BASE GYF (igual que en 002): estado abierto/cerrado, reseñas desde /resenas.json, formularios (antispam de
   tiempo, recuperar lo escrito, avisos de vuelta), cookies con modo de consentimiento, GTM solo en producción,
   eventos de medición, barra fija del móvil, FAQ con una abierta.
   CAPA DE RAYO (003): cabecera que se esconde y vuelve (R4-B), menú a pantalla completa (R34), apariciones (R18/R20),
   contadores (R32), carrusel de opiniones (R33), foto que sigue al cursor (R23), índice activo, subir (R10) y,
   con GSAP + ScrollTrigger + Lenis (solo ordenador) cargados al terminar la página: cintas que aceleran con el
   scroll (R14), portada fija con salida (R5), palabras que se encienden (R11), banda que se abre (R21),
   paralaje dentro del marco (R22), sello que gira con el scroll (R25) y el objeto 3D diferido.
   Sin JS o con movimiento reducido, todo se ve quieto y completo. */
(function () {
  "use strict";
  var d = document, w = window, html = d.documentElement;
  html.classList.add("js");
  var reducido = w.matchMedia && w.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var raton = w.matchMedia && w.matchMedia("(hover: hover) and (pointer: fine)").matches;
  var ancho = function () { return w.innerWidth; };

  /* ---------- v5 · Botones: el HTML lleva el texto una sola vez (lo que lee Google); aquí se parte en letras
     para la animación, con el texto para lectores de pantalla aparte. ---------- */
  (function () {
    var e1 = function (c) { return c === " " ? "&nbsp;" : ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c] || c); };
    var letras = function (t) { var o = ""; for (var i = 0; i < t.length; i++) o += '<span style="--i:' + i + '">' + e1(t.charAt(i)) + "</span>"; return o; };
    if (!raton) return;   /* sin ratón no hay hover: el texto se queda tal cual */
    var parte = function () { d.querySelectorAll(".btn__txt").forEach(function (e) {
      if (e.firstElementChild) return;
      var t = e.textContent, sr = d.createElement("span");
      sr.className = "sr"; sr.textContent = t; e.parentNode.insertBefore(sr, e);
      e.setAttribute("aria-hidden", "true");
      e.innerHTML = '<span class="btn__a">' + letras(t) + '</span><span class="btn__b">' + letras(t) + "</span>";
    }); };
    if ("requestIdleCallback" in w) w.requestIdleCallback(parte, { timeout: 1500 }); else setTimeout(parte, 300);
  })();

  /* ---------- v2 · Cortinilla fucsia entre páginas: al pulsar un enlace interno sube desde abajo y, al
     cubrir la pantalla, se navega; en la página nueva sale hacia arriba (CSS). Sin JS o con movimiento
     reducido, no existe. Vuelta atrás desde la caché: se quita. ---------- */
  var cortina = d.querySelector("[data-cortina]");
  if (cortina && !reducido) {
    d.addEventListener("click", function (e) {
      var a = e.target.closest && e.target.closest("a[href]");
      if (!a || e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
      if (a.target === "_blank" || a.hasAttribute("download")) return;
      var url;
      try { url = new URL(a.href, w.location.href); } catch (x) { return; }
      if (url.origin !== w.location.origin || !/^https?:$/.test(url.protocol)) return;
      if (url.pathname === w.location.pathname && url.hash) return;          /* ancla en la misma página */
      if (/\.(php|xml|txt|json|pdf|jpg|png|webp)$/i.test(url.pathname)) return;
      e.preventDefault();
      try { sessionStorage.setItem("gyf-cortina", "1"); } catch (x) {}   /* v5.1: la página siguiente sale con cortinilla; desde Google, no */
      cortina.classList.remove("entra"); void cortina.offsetWidth; cortina.classList.add("entra");
      setTimeout(function () { w.location.href = url.href; }, 280);   /* v5: 280 ms (antes 520) */
    });
    w.addEventListener("pageshow", function (e) { if (e.persisted) { cortina.classList.remove("entra"); cortina.style.animation = "none"; cortina.style.transform = "translateY(-101%)"; } });
  }

  /* ---------- v2 · Logotipos: en pantallas sin ratón pasan a color solos, uno detrás de otro, al verse ---------- */
  var logos = d.querySelector("[data-logos]");
  if (logos && !raton && "IntersectionObserver" in w) {
    var ioL = new IntersectionObserver(function (ents) {
      if (!ents[0].isIntersecting) return;
      [].forEach.call(logos.querySelectorAll(".logo"), function (l, i) { setTimeout(function () { l.classList.add("en-color"); }, reducido ? 0 : 150 + i * 110); });
      ioL.disconnect();
    }, { threshold: .35 });
    ioL.observe(logos);
  }

  /* ---------- Cabecera: siempre a la vista (Álvaro, 27/09: el menú no puede desaparecer); al bajar, compacta y con fondo ---------- */
  var cab = d.querySelector("[data-cab]"), menu = d.querySelector("[data-menu]"), yAnt = 0;
  function alScroll() {
    var y = w.scrollY;
    if (cab && !(menu && menu.classList.contains("abierta"))) {
      cab.classList.toggle("con-fondo", y >= 10);
    }
    yAnt = y;
    if (subir) subir.classList.toggle("visible", y > (d.documentElement.scrollHeight - w.innerHeight) * .2 && y > 600);
  }
  var subir = d.querySelector("[data-subir]");
  w.addEventListener("scroll", alScroll, { passive: true }); alScroll();

  /* ---------- Menú a pantalla completa (R34) ---------- */
  var burger = d.querySelector(".cab__burger");
  function toggle(ab) {
    if (!menu) return;
    menu.classList.toggle("abierta", ab);
    menu.setAttribute("aria-hidden", ab ? "false" : "true");
    if (burger) burger.setAttribute("aria-expanded", ab ? "true" : "false");
    d.body.style.overflow = ab ? "hidden" : "";
    if (w.__lenis) { if (ab) w.__lenis.stop(); else w.__lenis.start(); }
    if (ab) { var c = menu.querySelector(".menu__cerrar"); if (c) setTimeout(function () { c.focus(); }, 50); } else if (burger) burger.focus();
  }
  if (burger) burger.addEventListener("click", function () { toggle(true); });
  if (menu) {
    menu.addEventListener("click", function (e) { if (e.target.closest(".menu__cerrar") || e.target.closest("a")) toggle(false); });
    d.addEventListener("keydown", function (e) {
      if (!menu.classList.contains("abierta")) return;
      if (e.key === "Escape") toggle(false);
      if (e.key === "Tab") { /* el foco no sale del menú */
        var f = menu.querySelectorAll("a[href], button"), a = f[0], z = f[f.length - 1];
        if (e.shiftKey && d.activeElement === a) { e.preventDefault(); z.focus(); }
        else if (!e.shiftKey && d.activeElement === z) { e.preventDefault(); a.focus(); }
      }
    });
  }

  /* ---------- Estado en vivo: horario de la ficha (config.py: abre, cierra, dias_schema, zona_horaria) ---------- */
  var FEST = ["1/1", "6/1", "1/5", "2/5", "15/8", "12/10", "1/11", "6/12", "8/12", "25/12", "2/11/2026", "7/12/2026", "8/9", "6/4/2026"], PASCUA = [-3, -2], LABORABLES = [1, 2, 3, 4, 5];
  var DIAS = ["domingo", "lunes", "martes", "miércoles", "jueves", "viernes", "sábado"];
  function pascua(y) {
    var a = y % 19, b = Math.floor(y / 100), c = y % 100, dd = Math.floor(b / 4), e = b % 4, f = Math.floor((b + 8) / 25),
      g = Math.floor((b - f + 1) / 3), h = (19 * a + b - dd - g + 15) % 30, i = Math.floor(c / 4), k = c % 4,
      l = (32 + 2 * e + 2 * i - h - k) % 7, m = Math.floor((a + 11 * h + 22 * l) / 451), mes = Math.floor((h + l - 7 * m + 114) / 31);
    return Date.UTC(y, mes - 1, ((h + l - 7 * m + 114) % 31) + 1);
  }
  function esLaborable(dt) {
    var dias = Math.round((dt.getTime() - pascua(dt.getUTCFullYear())) / 864e5);
    return LABORABLES.indexOf(dt.getUTCDay()) > -1 && PASCUA.indexOf(dias) < 0 && FEST.indexOf(dt.getUTCDate() + "/" + (dt.getUTCMonth() + 1)) < 0 &&
      FEST.indexOf(dt.getUTCDate() + "/" + (dt.getUTCMonth() + 1) + "/" + dt.getUTCFullYear()) < 0;   /* «d/m» cada año; «d/m/aaaa» solo ese año */
  }
  var ABIERTO = null;
  function estado() {
    var p = {};
    try {
      new Intl.DateTimeFormat("en-GB", { timeZone: "Europe/Madrid", year: "numeric", day: "numeric", month: "numeric", hour: "numeric", minute: "numeric", hour12: false })
        .formatToParts(new Date()).forEach(function (x) { p[x.type] = x.value; });
    } catch (e) { return; }
    var h = parseInt(p.hour, 10) % 24;
    var hoy = new Date(Date.UTC(parseInt(p.year, 10), parseInt(p.month, 10) - 1, parseInt(p.day, 10)));
    var laborable = esLaborable(hoy);
    var abierto = ABIERTO = laborable && h >= 9 && h < 19;
    d.querySelectorAll("[data-estado]").forEach(function (el) {
      el.classList.add(abierto ? "abierto" : "fuera");
      var s = el.querySelector("span");
      if (s) s.textContent = abierto ? "Abierto ahora · hasta las 19:00" : "Ahora cerrado · déjenos su teléfono";
    });
    var txt;
    if (abierto) txt = "Le llamamos enseguida.";
    else if (laborable && h < 9) txt = "Le llamamos hoy a partir de las 9:00.";
    else {
      var sig = new Date(hoy.getTime()), n = 0;
      do { sig.setUTCDate(sig.getUTCDate() + 1); n++; } while (!esLaborable(sig) && n < 15);
      txt = "Le llamamos {dia} a partir de las 9:00.".replace("{dia}", n === 1 ? "mañana" : "el " + DIAS[sig.getUTCDay()]);
    }
    d.querySelectorAll("[data-promesa]").forEach(function (el) { el.textContent = txt; });
  }
  estado();
  d.querySelectorAll("[data-anio]").forEach(function (e) { e.textContent = new Date().getFullYear(); });

  /* ---------- Reseñas: nota, número y opiniones desde /resenas.json ---------- */
  function esc(x) { return String(x || "").replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function ponResenas(r) {
    /* v5.1: /resenas.json solo lleva la nota; las reseñas ya van ordenadas por página en el HTML */
    if (!r || !r.valoracion) return;
    var nota = String(r.valoracion);
    d.querySelectorAll("[data-nota], [data-fuente='valoracion']").forEach(function (e) { e.textContent = nota; });
  }
  w.__resenas = ("fetch" in w) ? fetch("/resenas.json", { cache: "no-cache" }).then(function (x) { return x.ok ? x.json() : null; }).then(ponResenas).catch(function () {}) : null;

  /* ---------- Formularios: sello de tiempo, recuperar lo escrito y avisos de vuelta ---------- */
  var q = w.location.search;
  function claveForm(f) { var t = f.querySelector('input[name="tipo"]'); return "gyf-form-" + (t ? t.value : (f.classList.contains("llamada__form") ? "llamada" : "contacto")); }
  function camposForm(f) { return [].filter.call(f.querySelectorAll("input[name], textarea[name]"), function (i) { return i.type !== "hidden" && i.type !== "checkbox" && i.name !== "web"; }); }
  d.addEventListener("submit", function (e) {
    var f = e.target, t = f.querySelector && f.querySelector('input[name="t"]');
    if (t) t.value = Math.round(w.performance && performance.now ? performance.now() : 0);
    if (!f.querySelectorAll) return;
    var datos = {}; camposForm(f).forEach(function (i) { datos[i.name] = i.value; });
    try { sessionStorage.setItem(claveForm(f), JSON.stringify(datos)); } catch (x) {}
  }, true);
  var errForm = /[?&](llamada|enviado|auditoria)=0/.test(q), okForm = /[?&](llamada|enviado|auditoria)=1/.test(q);
  if (errForm || okForm) d.querySelectorAll("form").forEach(function (f) {
    var k = claveForm(f);
    try {
      if (okForm) { sessionStorage.removeItem(k); return; }
      var datos = JSON.parse(sessionStorage.getItem(k) || "null"); if (!datos) return;
      camposForm(f).forEach(function (i) { if (datos[i.name] && !i.value) i.value = datos[i.name]; });
    } catch (x) {}
  });
  var ok = d.getElementById("form-ok"), ko = d.getElementById("form-error");
  if (ok && /enviado=1/.test(q)) {
    ok.hidden = false;
    d.querySelectorAll(".formulario").forEach(function (f) {
      if (f.contains(ok)) { [].forEach.call(f.children, function (ch) { if (ch !== ok) ch.hidden = true; }); f.classList.add("formulario--hecho"); }
      else f.hidden = true;
    });
  }
  if (ko && /enviado=0/.test(q)) ko.hidden = false;
  var lok = d.querySelector("[data-llamada-ok]"), lko = d.querySelector("[data-llamada-error]");
  if (lok && /llamada=1/.test(q)) {
    lok.hidden = false;
    var tj = lok.closest(".llamada") || d;
    tj.querySelectorAll(".llamada__form, .llamada__tit, [data-promesa]").forEach(function (x) { x.hidden = true; });
  }
  if (lko && /llamada=0/.test(q)) lko.hidden = false;
  /* v5 · Vuelta del formulario de la auditoría gratis */
  var aok = d.getElementById("aud-ok"), ako = d.getElementById("aud-error");
  if (aok && /auditoria=1/.test(q)) {
    aok.hidden = false;
    var af = aok.closest("form"); if (af) { [].forEach.call(af.children, function (ch) { if (ch !== aok) ch.hidden = true; }); af.classList.add("formulario--hecho"); }
  }
  if (ako && /auditoria=0/.test(q)) ako.hidden = false;
  /* v5.2 · De qué página venía quien pide la auditoría o escribe (la última interna antes de esta) */
  try {
    var prev = sessionStorage.getItem("gyf-pag-actual");
    if (prev && prev !== w.location.pathname) sessionStorage.setItem("gyf-pag-previa", prev);
    sessionStorage.setItem("gyf-pag-actual", w.location.pathname);
    var pv = sessionStorage.getItem("gyf-pag-previa");
    if (pv) d.querySelectorAll("[data-origen]").forEach(function (i) { i.value = pv; });
  } catch (x) {}
  /* v5.2 · El «Recibido» de la llamada dice cuándo llamamos, según el horario */
  if (lok && /llamada=1/.test(q) && typeof ABIERTO !== "undefined" && ABIERTO === false) lok.textContent = "Recibido. Le llamamos a primera hora del siguiente día laborable.";
  /* v5 · El aviso de error dice qué ha fallado (motivo que devuelve enviar.php) */
  var mot = /[?&]motivo=([a-z_\-]+)/i.exec(q), TEL = "670 78 19 40";
  var textoMotivo = { datos: "Revise el nombre y el teléfono: el teléfono necesita al menos 9 cifras. Si lo prefiere, llámenos al " + TEL + ".",
    tiempo: "No se ha podido enviar. Vuelva a intentarlo en unos segundos o llámenos al " + TEL + ".",
    enlaces: "El mensaje no puede llevar enlaces a otras webs. Quítelos y vuelva a enviarlo, o llámenos al " + TEL + "." };
  if (mot && textoMotivo[mot[1]]) [ko, lko, ako].forEach(function (x) { if (x && !x.hidden) x.textContent = textoMotivo[mot[1]]; });
  var avisoVuelta = (ok && !ok.hidden && ok) || (ko && !ko.hidden && ko) || (lok && !lok.hidden && lok) || (lko && !lko.hidden && lko) || (aok && !aok.hidden && aok) || (ako && !ako.hidden && ako);
  if (avisoVuelta) {
    for (var pr = avisoVuelta; pr; pr = pr.parentElement) if (pr.classList && pr.classList.contains("rv")) pr.classList.add("dentro");
    if (w.requestAnimationFrame) requestAnimationFrame(function () { try { avisoVuelta.scrollIntoView({ block: "center" }); } catch (x) {} });
  }

  /* ---------- Cookies + GTM (solo en el dominio de producción) ---------- */
  var PROD = new RegExp("^(elgordoyelflaco\\.es|www\\.elgordoyelflaco\\.es)$").test(w.location.hostname);
  var GTM = html.getAttribute("data-gtm");
  w.dataLayer = w.dataLayer || [];
  function gtag() { w.dataLayer.push(arguments); }
  var CLAVE = "gyf-cookies";
  function leer() { try { return localStorage.getItem(CLAVE); } catch (e) { return null; } }
  function guardar(v) { try { localStorage.setItem(CLAVE, v); } catch (e) {} }
  var eleccion = leer();
  gtag("consent", "default", { ad_storage: "denied", ad_user_data: "denied", ad_personalization: "denied", analytics_storage: "denied", wait_for_update: 500 });
  if (eleccion === "si") aceptar(true);
  function aceptar(silencioso) {
    gtag("consent", "update", { ad_storage: "granted", ad_user_data: "granted", ad_personalization: "granted", analytics_storage: "granted" });
    if (!silencioso) guardar("si");
  }
  if (/llamada=1/.test(q)) w.dataLayer.push({ event: "solicitud_llamada", pagina: w.location.pathname });
  if (/enviado=1/.test(q)) w.dataLayer.push({ event: "formulario_enviado", pagina: w.location.pathname });
  if (/auditoria=1/.test(q)) w.dataLayer.push({ event: "solicitud_auditoria", pagina: w.location.pathname });
  if (/(llamada|enviado|auditoria)=/.test(q) && w.history && history.replaceState) {
    try { history.replaceState(null, "", w.location.pathname + w.location.hash); } catch (e) {}
  }
  /* Medición: Llamar y WhatsApp (con la zona y si estamos en horario), reseñas de Google, «Déjenos su teléfono» y el CTA extra */
  var PAG = w.location.pathname;
  function ubicacion(a) {
    var zona = a.closest("[data-zona], .lectura__lado, .audform, .cab, .menu, .portada-a, .cab-int, .tarjeta, .llamada, .banda, .horario, .faq, .mapa, .lectura, .pie, .barra-movil, section");
    var LIMPIO = { cab: "cabecera", menu: "menu", "portada-a": "portada", "cab-int": "portada_interior", tarjeta: "tarjeta_portada",
      llamada: "le_llamamos", banda: "banda_final", horario: "horario", faq: "preguntas", mapa: "mapa", lectura: "texto", pie: "pie",
      "barra-movil": "barra_movil", seccion: "seccion", franja: "seccion", lectura__lado: "indice", audform: "auditoria" };
    if (!zona) return "otra";
    var cl = zona.className.split(" ")[0];
    return zona.getAttribute("data-zona") || LIMPIO[cl] || "seccion";
  }
  d.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest("a[href]");
    if (!a) return;
    var href = a.getAttribute("href");
    if (/^tel:/.test(href) || /wa\.me\//.test(href)) {
      w.dataLayer.push({ event: /^tel:/.test(href) ? "click_llamar" : "click_whatsapp", ubicacion: ubicacion(a), pagina: PAG, abierto: ABIERTO === true });
    } else if (/^mailto:/.test(href)) {
      w.dataLayer.push({ event: "click_email", ubicacion: ubicacion(a), pagina: PAG });
    } else if (/maps\.google\.com\/\?cid/.test(href)) {
      w.dataLayer.push({ event: "click_resenas_google", ubicacion: ubicacion(a), pagina: PAG });
    } else if (a.classList.contains("tarjeta__ir")) {
      w.dataLayer.push({ event: "click_te_llamamos", pagina: PAG });
    } else if (a.matches(".tarjeta__extra, .banda__extra, .mini__extra")) {
      w.dataLayer.push({ event: "click_cta_extra", ubicacion: ubicacion(a), destino: href, pagina: PAG });
    }
  }, true);
  function tipoForm(f) { var t = f.querySelector('input[name="tipo"]'); return t ? t.value : (f.classList.contains("llamada__form") ? "llamada" : "contacto"); }
  d.addEventListener("focusin", function (e) {
    var f = e.target.form; if (!f || f._inicio || !/^(INPUT|TEXTAREA|SELECT)$/.test(e.target.tagName) || e.target.type === "hidden") return;
    f._inicio = true;
    w.dataLayer.push({ event: "form_inicio", formulario: tipoForm(f), campo: e.target.name || "", pagina: PAG });
  });
  d.addEventListener("invalid", function (e) {
    var f = e.target.form; if (!f) return;
    var ahora = Date.now(); if (f._err && ahora - f._err < 800) return;
    f._err = ahora;
    w.dataLayer.push({ event: "form_error", formulario: tipoForm(f), campo: e.target.name || "", motivo: "validacion", pagina: PAG });
  }, true);
  var mq = /[?&](llamada|enviado|auditoria)=0/.exec(q);
  if (mq) {
    var mm = /[?&]motivo=([a-z_\-]+)/i.exec(q);
    w.dataLayer.push({ event: "form_error", formulario: mq[1] === "enviado" ? "contacto" : mq[1], motivo: mm ? mm[1] : "servidor", pagina: PAG });
  }
  if (PROD && GTM) {
    w.dataLayer.push({ "gtm.start": Date.now(), event: "gtm.js" });
    var s = d.createElement("script"); s.async = true; s.src = "https://www.googletagmanager.com/gtm.js?id=" + GTM;
    d.head.appendChild(s);
  }
  var aviso = d.getElementById("cookies");
  if (aviso && !eleccion) aviso.classList.add("visible");
  d.addEventListener("click", function (e) {
    var b = e.target.closest("[data-cookies]");
    if (!b) return;
    if (b.getAttribute("data-cookies") === "si") aceptar(false); else guardar("no");
    if (aviso) aviso.classList.remove("visible");
  });
  d.querySelectorAll("[data-cookies-config]").forEach(function (a) {
    a.addEventListener("click", function (e) { e.preventDefault(); if (aviso) aviso.classList.add("visible"); });
  });

  /* ---------- Barra fija del móvil: fuera mientras se ven los botones de la cabecera de la página ---------- */
  var barra = d.querySelector(".barra-movil"), accPortada = d.querySelector(".portada-a__top .acciones, .cab-int .acciones");
  if (barra && accPortada && "IntersectionObserver" in w) {
    new IntersectionObserver(function (ents) {
      barra.classList.toggle("barra-movil--fuera", ents[ents.length - 1].isIntersecting);
    }, { rootMargin: "0px 0px -88px 0px" }).observe(accPortada);
  }

  /* ---------- FAQ: una abierta a la vez (respaldo de <details name>) ---------- */
  d.querySelectorAll(".faq__lista").forEach(function (l) {
    l.addEventListener("toggle", function (e) {
      if (!e.target.open) return;
      l.querySelectorAll("details[open]").forEach(function (x) { if (x !== e.target) x.open = false; });
    }, true);
  });

  /* ---------- Índice de las interiores: plegado en móvil y enlace activo al leer ---------- */
  var indice = d.querySelector("[data-indice]");
  if (indice) {
    if (ancho() < 1200) indice.open = false;
    var enl = [].slice.call(indice.querySelectorAll("a[href^='#']"));
    if ("IntersectionObserver" in w) {
      var ioI = new IntersectionObserver(function (ents) {
        ents.forEach(function (en) {
          if (!en.isIntersecting) return;
          enl.forEach(function (a) { a.classList.toggle("activo", a.getAttribute("href") === "#" + en.target.id); });
        });
      }, { rootMargin: "-30% 0px -60% 0px" });
      enl.forEach(function (a) { var t = d.getElementById(a.getAttribute("href").slice(1)); if (t) ioI.observe(t); });
    }
  }

  /* ---------- v4.1 · Opiniones: tarjetas iguales (4:5); la reseña larga se corta con «Leer más» y se lee entera en una
     tarjeta grande encima (dialog nativo: Esc, X o clic fuera). Sin JS no se corta nada. El texto completo sigue en la página. ---------- */
  var opDlg = null;
  function dialogoOp() {
    if (opDlg) return opDlg;
    opDlg = d.createElement("dialog"); opDlg.className = "op-dialogo"; opDlg.setAttribute("aria-label", "Reseña completa");
    opDlg.innerHTML = '<button type="button" class="op-dialogo__x" aria-label="Cerrar">×</button><div class="op-dialogo__in"></div>';
    d.body.appendChild(opDlg);
    opDlg.querySelector(".op-dialogo__x").addEventListener("click", function () { opDlg.close(); });
    opDlg.addEventListener("click", function (e) { if (e.target === opDlg) opDlg.close(); });
    return opDlg;
  }
  function recortaOp() {
    var ul = d.querySelector("[data-opiniones]"); if (!ul) return;
    ul.classList.add("op-recorta");
    ul.querySelectorAll(".op").forEach(function (li) {
      var c = li.querySelector(".op__cuerpo"), b = li.querySelector("[data-op-mas]"); if (!c || !b) return;
      var larga = c.scrollHeight > c.clientHeight + 2;
      li.classList.toggle("op--larga", larga); b.hidden = !larga;
    });
  }
  d.addEventListener("click", function (e) {
    var b = e.target.closest && e.target.closest("[data-op-mas]"); if (!b) return;
    var li = b.closest(".op"), dl = dialogoOp(), cl = li.cloneNode(true);
    cl.classList.remove("op--larga"); var mb = cl.querySelector("[data-op-mas]"); if (mb) mb.remove();
    var inn = dl.querySelector(".op-dialogo__in"); inn.innerHTML = ""; inn.appendChild(cl);
    if (dl.showModal) dl.showModal(); else dl.setAttribute("open", "");
  });
  recortaOp();
  w.addEventListener("resize", function () { w.requestAnimationFrame(recortaOp); }, { passive: true });
  if (d.fonts && d.fonts.ready) d.fonts.ready.then(recortaOp);

  /* ---------- Opiniones: flechas y contador «1 / N» (R33, sin automático) ---------- */
  var opl = d.querySelector("[data-opiniones]"), opc = d.querySelector("[data-op-cuenta]");
  function cuentaOp() {
    if (!opl || !opc) return;
    var li = opl.querySelector(".op"); if (!li) return;
    var n = opl.querySelectorAll(".op").length, i = Math.round(opl.scrollLeft / (li.offsetWidth + 24));
    opc.textContent = Math.min(n, i + 1) + " / " + n;
    /* El carril toma el alto de la reseña que se ve: una reseña larga no deja a las cortas con un hueco en blanco */
    if (opl.classList.contains("op-recorta")) { opl.style.height = ""; return; }
    var act = opl.querySelectorAll(".op")[Math.min(n - 1, i)];
    if (act) opl.style.height = (act.offsetHeight + 6) + "px";
  }
  w.addEventListener("resize", function () { w.requestAnimationFrame(cuentaOp); }, { passive: true });
  w.addEventListener("load", cuentaOp);
  cuentaOp();
  if (opl) opl.addEventListener("scroll", function () { w.requestAnimationFrame(cuentaOp); }, { passive: true });
  d.querySelectorAll("[data-op]").forEach(function (b) {
    b.addEventListener("click", function () {
      var li = opl && opl.querySelector(".op");
      if (li) opl.scrollBy({ left: parseInt(b.getAttribute("data-op"), 10) * (li.offsetWidth + 24), behavior: reducido ? "auto" : "smooth" });
    });
  });

  /* ---------- R23 · La foto sigue al cursor en las filas de servicios (solo ordenador) ---------- */
  var cf = d.querySelector("[data-cursor-foto]");
  if (cf && raton && !reducido && ancho() >= 1000) {
    var actual = null;
    d.querySelectorAll("[data-sigue] .fila.con-foto").forEach(function (li) {
      li.addEventListener("mouseenter", function () {
        var pic = li.querySelector(".fila__foto picture");
        if (pic && actual !== li) { cf.innerHTML = ""; cf.appendChild(pic.cloneNode(true)); actual = li; }
        cf.classList.add("visible");
      });
      li.addEventListener("mouseleave", function () { cf.classList.remove("visible"); });
      li.addEventListener("mousemove", function (e) {
        cf.style.setProperty("--x", (e.clientX - 140) + "px");
        cf.style.setProperty("--y", (e.clientY - 272) + "px");
      });
    });
  }

  /* ---------- R32 · Contadores: cuentan al entrar (sin odómetro); respetan la coma decimal ---------- */
  function cuenta(el) {
    var v = el.getAttribute("data-cuenta") || "", n = parseFloat(v.replace(",", ".")), dec = (v.split(/[.,]/)[1] || "").length;
    if (isNaN(n) || reducido) return;
    var t0 = null, dur = 1400;
    function paso(t) {
      if (!t0) t0 = t;
      var k = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - k, 3);
      el.textContent = (n * e).toFixed(dec).replace(".", ",");
      if (k < 1) requestAnimationFrame(paso); else el.textContent = v;
    }
    requestAnimationFrame(paso);
  }

  /* ---------- R18 / R20 · Apariciones: una sola vez; las que entran juntas, escalonadas ---------- */
  var rv = d.querySelectorAll(".rv");
  if (reducido || !("IntersectionObserver" in w)) {
    rv.forEach(function (el) { el.classList.add("dentro"); });
  } else {
    var io = new IntersectionObserver(function (ents) {
      var k = 0;
      ents.forEach(function (en) {
        if (!en.isIntersecting) return;
        en.target.style.setProperty("--d", (k++ * .08) + "s");
        en.target.classList.add("dentro"); io.unobserve(en.target);
      });
    }, { rootMargin: "0px 0px -8% 0px" });
    rv.forEach(function (el) { io.observe(el); });
    var ioC = new IntersectionObserver(function (ents) {
      ents.forEach(function (en) { if (en.isIntersecting) { cuenta(en.target); ioC.unobserve(en.target); } });
    }, { threshold: .6 });
    var arrancaCuentas = function () { d.querySelectorAll("[data-cuenta]").forEach(function (el) { ioC.observe(el); }); };
    if (w.__resenas) w.__resenas.then(arrancaCuentas, arrancaCuentas); else arrancaCuentas();
  }

  /* =================== Carga diferida: GSAP (capa de Rayo) y el objeto 3D ===================
     Se cargan cuando la página ya ha terminado de cargar, para no quitarle ancho de banda a la portada. */
  function carga(lista, fin) {
    if (!lista.length) return fin();
    var sc = d.createElement("script"); sc.src = lista[0]; sc.async = false;
    sc.onload = function () { carga(lista.slice(1), fin); }; sc.onerror = function () { carga(lista.slice(1), fin); };
    d.body.appendChild(sc);
  }
  function arranca() {
    if (!reducido && !d.querySelector(".legal")) carga(["/js/vendor/gsap.min.js", "/js/vendor/ScrollTrigger.min.js", "/js/vendor/lenis.min.js"], capa);
    objeto3d();
  }
  if (d.readyState === "complete") arranca(); else w.addEventListener("load", arranca);

  /* Objeto 3D y piezas en vivo (v2: un solo módulo, /js/vendor/web3d.min.js, con una copia de three): solo
     ordenador, sin movimiento reducido y con WebGL. Las imágenes fijas de debajo son el LCP y el respaldo; cada
     lienzo se funde encima cuando ya ha pintado. Las piezas se montan al acercarse a su sección. */
  var web3d = null;
  function conWeb3D(fn) {
    if (w.Web3D) return fn(w.Web3D);
    if (web3d) return web3d.push(fn);
    web3d = [fn];
    carga(["/js/vendor/web3d.min.js"], function () { var l = web3d; web3d = null; if (w.Web3D) l.forEach(function (f) { f(w.Web3D); }); });
  }
  function hayWebGL() { try { var cv = d.createElement("canvas"); return !!(cv.getContext("webgl2") || cv.getContext("webgl")); } catch (e) { return false; } }
  function objeto3d() {
    if (reducido || !raton || ancho() < 900 || !hayWebGL()) return;
    var el = d.querySelector("[data-objeto3d]");
    var ya = function () {
      if (el) conWeb3D(function (M) {
        M.montar(el.querySelector(".objeto__lienzo"), {
          svg: el.getAttribute("data-objeto3d"), color: el.getAttribute("data-color") || null,
          listo: function () { requestAnimationFrame(function () { el.classList.add("con-3d"); }); }
        }).catch(function () {});
      });
    };
    /* v5.4: el módulo 3D (530 KB) espera al primer gesto (ratón, rueda o tecla) o a 4 s: no compite con la carga */
    var hecho = false, una = function () { if (hecho) return; hecho = true; ["pointermove", "wheel", "keydown", "touchstart"].forEach(function (ev) { w.removeEventListener(ev, una); }); ya(); };
    ["pointermove", "wheel", "keydown", "touchstart"].forEach(function (ev) { w.addEventListener(ev, una, { passive: true, once: true }); });
    setTimeout(una, 4000);
    var piezas = d.querySelector("[data-piezas]");
    if (piezas && "IntersectionObserver" in w) {
      var ioP = new IntersectionObserver(function (ents) {
        if (!ents[0].isIntersecting) return;
        ioP.disconnect();
        conWeb3D(function (M) {
          [].forEach.call(piezas.querySelectorAll("[data-pieza]"), function (c) {
            try {
              var r = M.montarPieza(c, { listo: function () { c.classList.add("con-3d"); } });
              if (r && r.catch) r.catch(function () {});
            } catch (e) {}
          });
        });
      }, { rootMargin: "600px 0px" });
      ioP.observe(piezas);
    }
  }

  /* Divide en palabras los nodos de texto de un elemento (conserva enlaces y negritas) */
  function palabras(el) {
    var out = [];
    (function rec(n) {
      [].slice.call(n.childNodes).forEach(function (c) {
        if (c.nodeType === 3) {
          var f = d.createDocumentFragment();
          c.textContent.split(/(\s+)/).forEach(function (t) {
            if (!t) return;
            if (/^\s+$/.test(t)) { f.appendChild(d.createTextNode(t)); return; }
            var s = d.createElement("span"); s.className = "pal"; s.textContent = t; f.appendChild(s); out.push(s);
          });
          c.parentNode.replaceChild(f, c);
        } else if (c.nodeType === 1) rec(c);
      });
    })(el);
    return out;
  }

  function capa() {
    var G = w.gsap, ST = w.ScrollTrigger;
    if (!G || !ST) return;
    G.registerPlugin(ST);

    /* R3 · Scroll suave solo en ordenador. En táctil, el nativo. */
    if (raton && w.Lenis && ancho() > 1080) {
      var lenis = w.__lenis = new w.Lenis({ lerp: .1 });
      lenis.on("scroll", ST.update);
      G.ticker.add(function (t) { lenis.raf(t * 1000); });
      G.ticker.lagSmoothing(0);
      d.querySelectorAll('a[href^="#"]').forEach(function (a) {
        a.addEventListener("click", function (e) {
          var id = a.getAttribute("href"); if (id.length < 2) return;
          var t = d.querySelector(id); if (!t) return;
          e.preventDefault(); lenis.scrollTo(t, { offset: -100, duration: 1 });
        });
      });
    }

    /* R14 · Cintas: avanzan solas (30 s por grupo) y se aceleran con la velocidad del scroll (×1 a ×6) */
    d.querySelectorAll("[data-cinta]").forEach(function (p) {
      var dir = parseFloat(p.getAttribute("data-cinta")) || -1;
      var tw = dir < 0 ? G.to(p, { xPercent: -50, duration: 30, ease: "none", repeat: -1 })
                       : G.fromTo(p, { xPercent: -50 }, { xPercent: 0, duration: 30, ease: "none", repeat: -1 });
      var vuelta;
      ST.create({
        trigger: p.parentNode, start: "top bottom", end: "bottom top",
        onToggle: function (s) { tw.paused(!s.isActive); },
        onUpdate: function (s) {
          var v = Math.min(6, Math.max(1, Math.abs(s.getVelocity()) / 200));
          G.to(tw, { timeScale: v, duration: .2, overwrite: true });
          if (vuelta) vuelta.kill();
          vuelta = G.to(tw, { timeScale: 1, duration: 1.5, delay: .25 });
        }
      });
    });

    /* R5 · Portada fija: la galería sube por encima; la frase, los servicios y la tarjeta salen hacia arriba
       estirándose y, al final, toda la capa se funde. Solo con la portada fija (ordenador con altura suficiente). */
    var hero = d.querySelector(".hero--galeria"), gal = hero && hero.querySelector("[data-galeria]");
    if (gal && w.matchMedia("(min-width: 900px) and (min-height: 800px)").matches) {
      G.to(hero.querySelectorAll("[data-sale]"), { y: -80, scaleY: 1.3, opacity: 0, transformOrigin: "50% 0%", ease: "sine.in",
        scrollTrigger: { trigger: gal, start: "top 92%", end: "top 38%", scrub: true } });
      G.to(hero.querySelector(".portada-a__centro"), { opacity: 0, ease: "none",
        scrollTrigger: { trigger: gal, start: "bottom 150%", end: "bottom 100%", scrub: true } });
    }
    /* R22 · Paralaje de las fotos dentro de su marco (×1,2) */
    d.querySelectorAll(".caso__foto img").forEach(function (im) {
      G.fromTo(im, { yPercent: -5 }, { yPercent: 5, ease: "none", scrollTrigger: { trigger: im.closest(".caso"), start: "top bottom", end: "bottom top", scrub: true } });
    });

    /* v2 · Titulares que se revelan: cada palabra de los H2 sube desde su máscara al entrar (0,9 s, power4.out,
       60 ms entre palabras). R11 · La segunda mitad gris se enciende palabra a palabra con el scroll. */
    function envuelve(el) {
      var out = [];
      (function rec(n, gris) {
        [].slice.call(n.childNodes).forEach(function (c) {
          if (c.nodeType === 3) {
            var f = d.createDocumentFragment();
            c.textContent.split(/(\s+)/).forEach(function (t) {
              if (!t) return;
              if (/^\s+$/.test(t)) { f.appendChild(d.createTextNode(t)); return; }
              var m = d.createElement("span"); m.className = "rev-l";
              var s2 = d.createElement("span"); s2.textContent = t; if (gris) s2.className = "pal";
              m.appendChild(s2); f.appendChild(m); out.push(s2);
            });
            c.parentNode.replaceChild(f, c);
          } else if (c.nodeType === 1) rec(c, gris || c.classList.contains("gris"));
        });
      })(el, false);
      return out;
    }
    d.querySelectorAll("main .h2, .banda__tit, .pie__titular").forEach(function (h) {
      var pals = envuelve(h);
      if (!pals.length) return;
      G.set(pals, { yPercent: 110 });
      ST.create({ trigger: h, start: "top 88%", once: true, onEnter: function () {
        G.to(pals, { yPercent: 0, duration: .9, ease: "power4.out", stagger: .06 });
      } });
    });
    d.querySelectorAll(".enciende").forEach(function (el) {
      var esH2 = el.classList.contains("h2");
      var pals = esH2 ? [].slice.call(el.querySelectorAll(".gris .pal")) : palabras(el);
      if (!pals.length) return;
      if (raton) {
        G.fromTo(pals, { opacity: .2 }, { opacity: 1, stagger: .1, ease: "none",
          scrollTrigger: { trigger: el, start: "top 85%", end: esH2 ? "top 40%" : "bottom 55%", scrub: true } });
      } else {
        G.fromTo(pals, { opacity: .2 }, { opacity: 1, stagger: .05, duration: .5, ease: "power1.out", scrollTrigger: { trigger: el, start: "top 80%" } });
      }
    });

    /* v2 · R7 · Tarjetas apiladas: se pegan arriba (sticky, CSS) y la de debajo encoge y se oscurece un poco
       cuando la siguiente sube a taparla. */
    var apil = ancho() >= 900 ? [].slice.call(d.querySelectorAll("[data-apil]")) : [];   /* v5.1: en el móvil van en carrusel */
    apil.forEach(function (li, i) {
      var sig = apil[i + 1]; if (!sig) return;
      G.to(li.querySelector(".apil__in"), { scale: .93, ease: "none",
        scrollTrigger: { trigger: sig, start: "top bottom", end: "top " + (24 + (i + 1) * 12) + "px", scrub: true } });
    });
    d.querySelectorAll(".apil__obj").forEach(function (o) {
      G.fromTo(o, { y: 40, rotation: -6 }, { y: -40, rotation: 6, ease: "none", scrollTrigger: { trigger: o.closest(".apil"), start: "top bottom", end: "bottom top", scrub: true } });
    });

    /* R5 · Galería de la portada: cada caso sube a su velocidad (data-vel) por encima de la portada fija */
    if (w.matchMedia("(min-width: 900px)").matches) {
      d.querySelectorAll(".galeria .caso[data-vel]").forEach(function (c) {
        var v = parseFloat(c.getAttribute("data-vel")) || 1;
        G.fromTo(c, { y: (v - 1) * 260 }, { y: (1 - v) * 260, ease: "none", scrollTrigger: { trigger: c, start: "top bottom", end: "bottom top", scrub: true } });
      });
    }
    /* v3 · R22 · La foto a sangre del manifiesto y las fotos de las franjas se mueven dentro de su marco */
    d.querySelectorAll(".foto-sangre .fotohueco__img img, .franja__foto .fotohueco__img img").forEach(function (im) {
      G.fromTo(im, { yPercent: -6 }, { yPercent: 6, ease: "none", scrollTrigger: { trigger: im.closest(".fotohueco"), start: "top bottom", end: "bottom top", scrub: true } });
    });
    /* R22 · Los casos grandes se mueven dentro de su marco */
    d.querySelectorAll(".proy__foto img").forEach(function (im) {
      G.fromTo(im, { yPercent: -5 }, { yPercent: 5, ease: "none", scrollTrigger: { trigger: im.closest(".proy"), start: "top bottom", end: "bottom top", scrub: true } });
    });
    /* R19 · Los objetos de las cifras entran de lado y con escala; los de las franjas, con paralaje */
    d.querySelectorAll(".cifra__obj").forEach(function (o, i) {
      G.from(o, { x: i % 2 ? -70 : 70, y: 50, scale: 1.2, opacity: 0, duration: 1.1, ease: "power3.out", scrollTrigger: { trigger: o.parentNode, start: "top 80%", once: true } });
    });
    d.querySelectorAll(".franja__obj, .horario__obj, .banda__objeto, .opiniones__obj, .contacto__obj, .cab-int__obj").forEach(function (o) {
      G.fromTo(o, { y: 50 }, { y: -50, ease: "none", scrollTrigger: { trigger: o.parentNode, start: "top bottom", end: "bottom top", scrub: true } });
    });
    /* R17 · El nombre gigante del pie baja desde arriba con el scroll */
    /* v4 · GORDO entra por la izquierda, FLACO por la derecha y el monograma G+F cae girando hasta su sitio */
    var pl = d.querySelector("[data-pie-nombre] .lg");
    if (pl) {
      var stp = { trigger: pl, start: "top 100%", end: "top 45%", scrub: true };
      G.fromTo(pl.querySelector(".lg__gordo"), { xPercent: -45, opacity: .2 }, { xPercent: 0, opacity: 1, ease: "none", scrollTrigger: stp });
      G.fromTo(pl.querySelector(".lg__flaco"), { xPercent: 45, opacity: .2 }, { xPercent: 0, opacity: 1, ease: "none", scrollTrigger: stp });
      G.fromTo(pl.querySelector(".lg__simbolo"), { yPercent: -120, rotation: -200, scale: 1.6 }, { yPercent: 0, rotation: 0, scale: 1, ease: "none", scrollTrigger: stp });
    }
    /* v4 · La foto se mueve dentro de las letras del logotipo; el trazo se dibuja y el monograma gira */
    d.querySelectorAll("[data-lgfoto]").forEach(function (c) {
      var im = c.querySelector(".lgfoto__mascara img");
      if (im) G.fromTo(im, { yPercent: -18 }, { yPercent: 18, ease: "none", scrollTrigger: { trigger: c, start: "top bottom", end: "bottom top", scrub: true } });
      var a = c.querySelector(".lgfoto__trazo .lg__simbolo");
      if (a) G.fromTo(a, { rotation: -90, scale: .6 }, { rotation: 0, scale: 1, ease: "none", scrollTrigger: { trigger: c, start: "top 90%", end: "top 35%", scrub: true } });
      G.from(c.querySelectorAll(".lgfoto__trazo .lg__gordo, .lgfoto__trazo .lg__flaco"), { opacity: 0, duration: 1.2, stagger: .15, ease: "power2.out", scrollTrigger: { trigger: c, start: "top 80%", once: true } });
    });
    /* v4 · El logotipo en trazo de las franjas oscuras se desliza en horizontal */
    d.querySelectorAll("[data-marca-agua]").forEach(function (m) {
      G.fromTo(m, { xPercent: 6 }, { xPercent: -14, ease: "none", scrollTrigger: { trigger: m.parentNode, start: "top bottom", end: "bottom top", scrub: true } });
    });

    /* R21 · La banda final se abre: el fondo pasa de scaleX 1,14 y radio 200 a su sitio (el texto no se deforma) */
    d.querySelectorAll("[data-abre] .banda__fondo").forEach(function (f) {
      var r = getComputedStyle(f).borderTopLeftRadius;
      G.fromTo(f, { scaleX: 1.14, borderRadius: 200 }, { scaleX: 1, borderRadius: r, ease: "power4.inOut",
        scrollTrigger: { trigger: f.parentNode, start: "top 82%", end: "top 14%", scrub: true } });
    });

    /* R25 · El sello de Google gira con el scroll */
    d.querySelectorAll("[data-gira]").forEach(function (s) {
      G.to(s, { rotation: 300, transformOrigin: "50% 50%", ease: "none", scrollTrigger: { trigger: s, start: "top bottom", end: "bottom top", scrub: true } });
    });

    ST.refresh();
  }
})();
