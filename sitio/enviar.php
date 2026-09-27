<?php
/* El Gordo y el Flaco · formularios de la web: «Que me llaman» (tarjeta de la portada) y contacto.
   Antispam: trampa + tiempo en la página + sin enlaces en el mensaje. Sin captcha. El mensaje es opcional.
   «t» lo rellena main.js al enviar: milisegundos que lleva la página abierta (performance.now()),
   así no depende del reloj del servidor ni del del móvil. Válido entre 3 s y 24 h. */
header('X-Robots-Tag: noindex');
if ($_SERVER['REQUEST_METHOD'] !== 'POST') { header('Location: /contacto/'); exit; }
$c = function ($k, $max) { return trim(mb_substr(strip_tags($_POST[$k] ?? ''), 0, $max)); };
$tipo = ($_POST['tipo'] ?? '') === 'llamada' ? 'llamada' : 'contacto';
$pagina = $c('pagina', 120);
if (!preg_match('#^/[a-z0-9\-/]*$#', $pagina) || strpos($pagina, '//') !== false) { $pagina = '/'; }
$nombre = $c('nombre', 80); $telefono = $c('telefono', 20); $municipio = $c('municipio', 60); $mensaje = $c('mensaje', 2000);
$trampa = $_POST['web'] ?? ''; $t = (int)($_POST['t'] ?? 0);
$motivo = '';
if ($trampa !== '') { $motivo = 'trampa'; }
elseif ($t < 3000 || $t > 86400000) { $motivo = 'tiempo'; }
elseif ($nombre === '' || !preg_match('/^[0-9 +()\-]{9,20}$/', $telefono)) { $motivo = 'datos'; }
elseif (preg_match_all('#https?://#i', $mensaje) > 0) { $motivo = 'enlaces'; }
$ok = $motivo === '';
if ($tipo === 'llamada') { $vuelta = $pagina; $clave = 'llamada'; $ancla = '#te-llamamos'; $ancla_ko = '#te-llamamos'; }
else { $vuelta = '/contacto/'; $clave = 'enviado'; $ancla = '#form-ok'; $ancla_ko = '#form-error'; }
if (!$ok) { header('Location: ' . $vuelta . '?' . $clave . '=0&motivo=' . $motivo . $ancla_ko); exit; }
$para = 'info@elgordoyelflaco.es';
if ($tipo === 'llamada') {
  $asunto = '=?UTF-8?B?' . base64_encode('QUE ME LLAMEN · ' . $nombre . ' · ' . $telefono) . '?=';
  $cuerpo = "Petición de llamada desde la web.\n\nNombre: $nombre\nTeléfono: $telefono\nPágina: https://elgordoyelflaco.es$pagina\n";
} else {
  $asunto = '=?UTF-8?B?' . base64_encode('Web El Gordo y el Flaco: ' . $nombre . ($municipio ? ' (' . $municipio . ')' : '')) . '?=';
  $cuerpo = "Nombre: $nombre\nTeléfono: $telefono\nMunicipio: $municipio\n\n$mensaje\n\n-- Enviado desde elgordoyelflaco.es/contacto/";
}
$cab = "From: Web El Gordo y el Flaco <web@elgordoyelflaco.es>\r\nContent-Type: text/plain; charset=UTF-8\r\n";
$enviado = @mail($para, $asunto, $cuerpo, $cab);
header('Location: ' . $vuelta . '?' . $clave . '=' . ($enviado ? '1' . $ancla : '0&motivo=envio' . $ancla_ko));
