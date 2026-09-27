# Fotos a generar · elgordoyelflaco.es (v3)

Quince fotografías «de lo que se está hablando, pero más artísticas». El diseño ya tiene los huecos hechos, con
su encuadre, su tratamiento y un marcador de la marca mientras no llegan. No hace falta tocar código.

## Cómo se ponen

1. Genera la foto con el prompt de su ficha, al tamaño indicado o mayor, en JPG.
2. Guárdala en `recursos/fotos/` con **el nombre exacto** de la ficha. También valen `.png` y `.webp` con el mismo nombre.
3. Regenera la web: `python3 generador/build.py && python3 generador/rematar.py && python3 generador/controles.py`.
   `rematar.py` saca las versiones de 800 y 1.600 px en JPG y WebP. El marcador desaparece solo y `controles.py`
   deja de avisar de esa foto.
4. Súbela a GitHub como siempre: `recursos/fotos/<archivo>` y los `sitio/img/<archivo>-800|1600.jpg|webp` nuevos.

## Tratamientos (los pone la web, no el generador)

- **Duotono:** la web pasa la foto a grises y la tiñe, con sombras en berenjena y luces en fucsia. Pide fotos
  **con mucho contraste de luz y formas claras**; el color original da igual.
- **Viñeta:** la foto va en su color, con los bordes oscurecidos a berenjena y un velo fucsia suave. Aquí sí
  importa el color: tonos cálidos y neutros, y un acento fucsia en la escena.

## Reglas para todas

Estilo editorial y artístico (revista de diseño, no banco de imágenes). Luz natural lateral, profundidad de campo
corta y encuadres cuidados con aire. **Sin caras identificables:** manos, espaldas o siluetas fuera de foco, y nunca
Álvaro. **Sin texto legible, sin logotipos ni marcas ajenas, sin pantallas con interfaces reales reconocibles.**
El fucsia de la marca (#E0067A) va como acento: un objeto, una luz o un reflejo, nunca como filtro general.

Añade siempre al final del prompt: *«fotografía editorial, 35 mm, grano fino, sin texto, sin logotipos, sin caras reconocibles»*.

---

## Prioridad 1: las que más se ven

### 1 · Portada, foto a sangre tras el manifiesto
- **Archivo:** `foto-portada-mesa-de-trabajo.jpg` · **Formato:** 21:9 · **Tamaño:** 2.520 × 1.080 · **Tratamiento:** viñeta
- **Dónde:** home, a todo el ancho del contenedor, justo después de «Quiénes somos» (se mueve dentro del marco con el scroll).
- **Prompt:** Bodegón editorial cenital y ligeramente inclinado de una mesa de trabajo de madera clara junto a una ventana con luz de tarde. Hay un móvil boca arriba cuya pantalla muestra un mapa desenfocado con una chincheta fucsia, un cuaderno abierto con bocetos a lápiz, una taza de café, unas pruebas de color impresas y un pequeño objeto fucsia lacado. Sombras largas y suaves de la ventana cruzan la mesa. Paleta crema y madera con un único acento fucsia intenso. Composición panorámica con mucho aire a la derecha.

### 2 · Banda final («Hablemos en su negocio, sin coste»)
- **Archivo:** `foto-banda-mostrador.jpg` · **Formato:** 16:9 · **Tamaño:** 2.400 × 1.350 · **Tratamiento:** viñeta (va al fondo del panel berenjena, bajo el texto blanco)
- **Prompt:** Mostrador de madera de un pequeño comercio de barrio al final de la tarde, visto de lado y a la altura del mostrador. Encima, dos tazas de café, un cuaderno abierto y un bolígrafo; al fondo, muy desenfocadas, las estanterías del negocio y la luz cálida del escaparate. Dos manos (sin caras) conversan sobre el cuaderno. Mucha zona oscura en la mitad izquierda para el texto y una luz fucsia tenue que entra desde un letrero fuera de campo.

### 3 · «¿Quién hay detrás de El Gordo y el Flaco?»
- **Archivo:** `foto-quien-atico.jpg` · **Formato:** 4:5 · **Tamaño:** 1.600 × 2.000 · **Tratamiento:** viñeta
- **Prompt:** Interior de un ático de trabajo bajo cubierta inclinada con viga de madera y una ventana abuhardillada por la que entra una luz lateral dorada. Una mesa grande con un portátil cerrado, papeles, pruebas de imprenta colgadas con pinzas en un cordel y una lámpara de brazo. Una silla vacía girada hacia la ventana. Ambiente de estudio creativo y ordenado, cálido, con un cojín o una carpeta fucsia como único acento. Sin personas.

### 4 · «¿Cómo trabajamos con negocios de Alcorcón?» (franja berenjena)
- **Archivo:** `foto-como-trabajamos-reunion.jpg` · **Formato:** 16:7 · **Tamaño:** 2.400 × 1.050 · **Tratamiento:** duotono
- **Prompt:** Reunión en el mostrador de un negocio de barrio: primer plano de las manos de dos personas, una señalando un cuaderno con un esquema dibujado a mano y la otra sujetando un móvil. Luz lateral dura que marca bien las manos y el papel, fondo del local oscuro. Encuadre muy horizontal con las manos en el tercio central y aire a ambos lados. Mucho contraste de luces y sombras.

## Prioridad 2: un servicio, una foto (tarjetas apiladas de la home y cabecera de cada servicio)

Todas en **4:5 · 1.600 × 2.000 · duotono**. La foto va a la izquierda del caso real en la tarjeta apilada y, en la
página del servicio, de fondo de la tarjeta de la cabecera, con el objeto 3D delante: deja **aire arriba a la derecha**.

### 5 · SEO local: `foto-servicio-seo-local.jpg`
- **Prompt:** Persiana a medio subir de un comercio de barrio al atardecer, vista desde la acera en diagonal, con la luz rasante del sol recortando las lamas metálicas. En el suelo, la sombra alargada de un poste. Al fondo, la calle desenfocada con otros comercios. Contraste fuerte, geometría de líneas, sensación de «abrimos».

### 6 · Auditoría SEO local: `foto-servicio-auditoria.jpg`
- **Prompt:** Primer plano de un informe impreso sobre una mesa, con anotaciones y subrayados a mano ilegibles y un rotulador fucsia destapado encima. Al lado, unas gafas de pasta. Luz de ventana lateral que proyecta sombras de las gafas sobre el papel. Profundidad de campo muy corta: solo la punta del rotulador y una línea subrayada en foco.

### 7 · Diseño web: `foto-servicio-diseno-web.jpg`
- **Prompt:** Una mano sostiene un móvil en vertical en la calle, con la pantalla iluminada mostrando una web abstracta y desenfocada (bloques de color, sin texto legible). Detrás, luces de escaparates desenfocadas en bokeh. Encuadre vertical, el móvil en el tercio inferior izquierdo, mucho fondo arriba.

### 8 · Google Ads: `foto-servicio-google-ads.jpg`
- **Prompt:** Macro de un pulgar a punto de tocar un botón circular verde de llamada en la pantalla de un móvil apoyado sobre una mesa de cafetería. Pantalla sin textos legibles. Reflejo de una luz fucsia en el cristal del móvil. Fondo oscuro con bokeh cálido.

### 9 · Diseño gráfico: `foto-servicio-diseno-grafico.jpg`
- **Prompt:** Bodegón de estudio de diseño: pruebas de imprenta sin textos legibles, un abanico de muestras de color abierto con tonos fucsia, rosa, berenjena y crema, tarjetas de visita en blanco apiladas y un cúter. Vista cenital inclinada, luz lateral suave y sombras marcadas. Composición diagonal.

### 10 · Redacción publicitaria: `foto-servicio-redaccion.jpg`
- **Prompt:** Cuaderno abierto con líneas escritas a mano, tachadas y reescritas (sin texto legible), junto al borde de un teclado y una pluma estilográfica. Luz de ventana muy lateral que resalta la textura del papel. Profundidad de campo corta, el foco en el trazo de tinta.

### 11 · Analítica: `foto-servicio-analitica.jpg`
- **Prompt:** Pantalla de portátil muy desenfocada con formas de gráficas de barras y líneas (sin números ni textos legibles), y en primer plano, en foco, una taza de café con el vapor a contraluz. Ambiente de primera hora de la mañana, luz fría de ventana y un reflejo fucsia de la pantalla en la taza.

## Prioridad 3: zonas, municipios, quiénes somos y contacto

### 12 · «Dónde trabajamos» (franja fucsia de la home)
- **Archivo:** `foto-zonas-calle.jpg` · **Formato:** 3:2 · **Tamaño:** 1.800 × 1.200 · **Tratamiento:** duotono
- **Prompt:** Calle comercial de un municipio del sur de Madrid a media tarde: aceras anchas, árboles, fachadas de ladrillo de los años setenta y escaparates con toldos, vista en perspectiva hacia el fondo. Viandantes muy lejanos y desenfocados, sin caras. Sin rótulos legibles. Luz rasante que dibuja las sombras de los árboles en la acera.

### 13 · Cabecera de las 10 páginas de municipio (tarjeta con el nombre del pueblo)
- **Archivo:** `foto-municipio-escaparates.jpg` · **Formato:** 4:5 · **Tamaño:** 1.600 × 2.000 · **Tratamiento:** duotono (oscurecido, con la chincheta 3D delante)
- **Prompt:** Fila de escaparates y puertas de pequeños comercios de barrio vistos en diagonal desde la acera, con toldos y persianas, en vertical. Sin rótulos legibles. Luz de atardecer que cae en diagonal. Deja la mitad superior más limpia (cielo o fachada) para el objeto 3D y el nombre del municipio abajo a la izquierda.

### 14 · Cabecera de «Quiénes somos»
- **Archivo:** `foto-quienes-somos-oficio.jpg` · **Formato:** 4:5 · **Tamaño:** 1.600 × 2.000 · **Tratamiento:** viñeta (va sobre la tarjeta fucsia con el símbolo de cromo delante)
- **Prompt:** Herramientas del oficio de una agencia de publicidad colocadas con orden sobre una superficie crema: lápices, una regla metálica, pruebas de color, un cuentahílos de imprenta, un móvil boca abajo y una libreta con tapa fucsia. Vista cenital, sombras suaves, mucho aire en la mitad superior.

### 15 · Cabecera de «Contacto»
- **Archivo:** `foto-contacto-telefono.jpg` · **Formato:** 4:5 · **Tamaño:** 1.600 × 2.000 · **Tratamiento:** duotono
- **Prompt:** Móvil apoyado sobre una mesa de madera con la pantalla encendida mostrando una llamada entrante abstracta (círculo verde, sin nombre ni número legibles). Luz de tarde por la izquierda, sombra larga del móvil, y al fondo, desenfocada, una taza y una planta. Encuadre vertical con el móvil en el tercio inferior.

---

Lista completa (la misma que en `generador/config.py`, `FOTOS`):

| # | Archivo | Formato | Tamaño | Tratamiento | Sección |
|---|---|---|---|---|---|
| 1 | foto-portada-mesa-de-trabajo.jpg | 21:9 | 2.520 × 1.080 | viñeta | Home, tras el manifiesto |
| 2 | foto-banda-mostrador.jpg | 16:9 | 2.400 × 1.350 | viñeta | Banda final de todas las páginas |
| 3 | foto-quien-atico.jpg | 4:5 | 1.600 × 2.000 | viñeta | Home, «¿Quién hay detrás?» |
| 4 | foto-como-trabajamos-reunion.jpg | 16:7 | 2.400 × 1.050 | duotono | Home, «Cómo trabajamos» |
| 5 | foto-servicio-seo-local.jpg | 4:5 | 1.600 × 2.000 | duotono | Tarjeta y cabecera de SEO local |
| 6 | foto-servicio-auditoria.jpg | 4:5 | 1.600 × 2.000 | duotono | Auditoría SEO local |
| 7 | foto-servicio-diseno-web.jpg | 4:5 | 1.600 × 2.000 | duotono | Diseño web |
| 8 | foto-servicio-google-ads.jpg | 4:5 | 1.600 × 2.000 | duotono | Google Ads |
| 9 | foto-servicio-diseno-grafico.jpg | 4:5 | 1.600 × 2.000 | duotono | Diseño gráfico |
| 10 | foto-servicio-redaccion.jpg | 4:5 | 1.600 × 2.000 | duotono | Redacción publicitaria |
| 11 | foto-servicio-analitica.jpg | 4:5 | 1.600 × 2.000 | duotono | Analítica |
| 12 | foto-zonas-calle.jpg | 3:2 | 1.800 × 1.200 | duotono | Home, «Dónde trabajamos» |
| 13 | foto-municipio-escaparates.jpg | 4:5 | 1.600 × 2.000 | duotono | Cabecera de los 10 municipios |
| 14 | foto-quienes-somos-oficio.jpg | 4:5 | 1.600 × 2.000 | viñeta | Cabecera de Quiénes somos |
| 15 | foto-contacto-telefono.jpg | 4:5 | 1.600 × 2.000 | duotono | Cabecera de Contacto |
