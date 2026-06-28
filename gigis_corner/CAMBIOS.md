# Gigi's Corner — Cambios v17.0.2.0.0

## Qué se corrigió
1. **Imágenes editables (lápiz de Odoo):** todos los bloques que antes eran emojis/placeholder
   ahora son <img> reales con imágenes de muestra de Unsplash. Edítalas con el editor
   de Odoo (doble clic sobre la imagen → seleccionar/subir).
   - Hero principal
   - Las 6 categorías
   - Historias que iluminan (3 tarjetas del home)
   - Fotos del proceso (6)
   - Bloque "Una mamá construyendo sueños" (la foto de Ana, que antes salía en blanco)
   - Equipo (4 fotos)
   - **Familias que iluminan: ahora son 6 bloques con imagen + título + historia editables**
   - Página Nosotros: hero, 4 capítulos y 4 fotos de equipo
   - Galería de Personalizados

2. **Bloque en blanco:** la foto de Ana usaba aspect-ratio sin altura y colapsaba.
   Ahora tiene height:420px fijo + imagen real.

3. **Video:** el botón ▶ tenía data-video vacío y no abría nada. Ahora solo aparece si
   defines la URL del video (variable video_amira / video_pepe / video_valentina en el
   home, o el campo video_url de cada Historia en la base de datos).

4. **Categorías:** antes iban a /shop (inexistente). Ahora cada una abre su propia página
   /categoria/<slug> con imagen grande arriba + 3 bloques de ejemplos editables.
   Páginas: dulces-suenos, suena-grande, exploradores, amigos-especiales, aventuras-mar.

5. **Iniciar sesión:** agregado en el navbar (arriba a la derecha). Orden: primero
   "Diseñar mi lámpara" (coral), luego "Iniciar sesión" (borde azul). Si el usuario ya
   inició sesión, muestra "Mi cuenta" (/my).

6. **Visibilidad solo en Gigi's Corner:** las páginas se bloquean en otros sitios web
   cuando existe más de un sitio. Si Gigi's es el único sitio, no bloquea nada.

## Cómo cambiar las imágenes de muestra por las tuyas
Entra al editor del sitio (botón "Editar" de Odoo), haz doble clic sobre cualquier
imagen y sube la tuya. Todas las imágenes de muestra son de Unsplash (libres).

## Cómo activar un video en el home
En views/gigis_home.xml busca `video_amira` (o pepe / valentina) y pon la URL del MP4
entre las comillas de t-value.

## v17.0.3.0.0 — Bloques vacíos resueltos
**Causa raíz:** las imágenes de muestra venían de Unsplash (URL externa). Unsplash
bloquea la carga directa (hotlink) desde otros dominios, así que esas imágenes salían
como BLOQUES VACÍOS en la web.

**Solución:** todas las imágenes de muestra ahora están INCRUSTADAS dentro del módulo
(carpeta static/src/img/samples/). Cargan siempre, sin depender de internet.
Son placeholders con los colores de la marca y un texto que dice qué va en cada bloque.

**Cómo reemplazarlas por tus fotos reales:** entra al editor del sitio (botón Editar de
Odoo), doble clic sobre cualquier imagen de muestra y sube la tuya. Cada imagen indica
en su texto qué contenido le corresponde (ej. "Foto de Ana y Helana").

- Logo: incrustado (navbar crema + footer transparente).
- 43 imágenes de muestra locales: hero, 6 categorías, 3 historias, 6 proceso, Ana,
  4 equipo, 6 familias, hero+capítulos de Nosotros, hero+galería de Personalizados,
  hero+ejemplos de las páginas de categoría.

## v17.0.4.0.0 — Imágenes ocultas / bloques vacíos al cargar
**Problema:** al subir tus fotos reales, los bloques se veían vacíos hasta que
hacías clic en ellos.

**Causa:** la animación "fade-up" ponía los bloques en opacity:0 y solo los
revelaba al detectar scroll con JavaScript. En el editor de Odoo (o si el JS no
disparaba el observer) el bloque se quedaba invisible. Al hacer clic, el navegador
forzaba un repaint y aparecía.

**Solución:**
1. Ahora el contenido es VISIBLE por defecto. La animación solo se activa si el JS
   confirma que puede animar (clase .gc-animate en <html>).
2. Failsafe: a los 2.5s se revela cualquier bloque que siguiera oculto.
3. En el editor de Odoo (.editor_enable/.o_editable) todo se fuerza visible.
4. Blindaje de imágenes: clases .gc-img-box / .gc-img-cover garantizan que la
   imagen llene su contenedor y sea visible aunque Odoo le cambie los estilos al
   reemplazarla.

IMPORTANTE tras instalar: actualiza el módulo y haz Ctrl+F5 (o ventana incógnito)
para limpiar el CSS/JS viejo cacheado.

## v17.0.5.0.0 — TODAS las imágenes ahora son editables
**Problema:** las imágenes generadas con bucles (t-foreach / t-att-src) NO se podían
editar desde el editor web de Odoo (aparecían "bloqueadas").

**Solución:** se reescribieron como etiquetas <img src> FIJAS individuales. Ahora el
editor de Odoo permite hacer doble clic en cualquiera y reemplazarla.

Imágenes editables por página (55 en total):
- INICIO: hero, 6 categorías, 3 historias, 6 fotos de proceso, foto de Ana,
  4 del equipo, 6 de familias.
- NOSOTROS: hero, 3 capítulos, 4 del equipo.
- PERSONALIZADOS: hero + 7 de la galería de trabajos.
- CATEGORÍA: hero (uno por categoría) + 3 ejemplos.
- HISTORIAS: se editan desde el panel Odoo → Gigi's Corner → Historias
  (imagen principal, video y 4 fotos de proceso por cada historia).
- Logos (navbar y footer): incrustados en el módulo.

CÓMO EDITAR UNA IMAGEN:
1. Entra a la página y pulsa el botón "Editar" (arriba a la derecha en Odoo).
2. Haz doble clic sobre la imagen que quieras cambiar.
3. Sube tu foto o elige una. Pulsa "Guardar".
   (NO uses el panel "Bloques" de la derecha; ese es para arrastrar bloques nuevos.)

## v17.0.6.0.0 — CAUSA REAL de las imágenes bloqueadas: faltaba oe_structure
**El verdadero problema:** Odoo NO permite editar el contenido de una página
(imágenes, textos) a menos que esté dentro de un contenedor con la clase
"oe_structure". El módulo tenía <div id="wrap"> SIN esa clase, por eso TODO
salía bloqueado en el editor.

**Solución (confirmada en docs oficiales de Odoo 17):**
Se cambió <div id="wrap"> por <div id="wrap" class="oe_structure"> en todas las
páginas (inicio, historias, nosotros, personalizados, categoría).
Ahora el editor web de Odoo permite cambiar imágenes y textos.

CÓMO EDITAR AHORA:
1. Abre la página y pulsa "Editar" (arriba a la derecha).
2. Haz clic / doble clic en cualquier imagen → botón "Reemplazar" / "Replace".
3. Sube tu foto. Guarda.
También puedes editar cualquier texto haciendo clic sobre él.

NOTA: como ahora la página es totalmente editable, evita arrastrar o borrar
secciones completas sin querer. Para cambiar una imagen, solo haz clic en ella
(no la arrastres).

IMPORTANTE tras instalar:
- Actualiza el módulo con -u o desde Apps.
- Si ya habías editado la página antes desde el front-end, Odoo pudo marcar la
  vista como "no actualizable". Si no ves los cambios: Ajustes → Técnico →
  Vistas → busca "Gigi's Corner - Home" → si está, bórrala y actualiza el módulo,
  o desmarca "No actualizable".
- Ctrl+F5 para limpiar caché.

## v17.0.7.0.0 — Panel para administrar Historias (y Solicitudes)
**Problema:** la sección "Historias que iluminan" mostraba siempre el placeholder
"Foto/Video de Amira · Imagen de muestra" y no se podía cambiar. Las imágenes de las
historias vienen de la BASE DE DATOS (modelo gigis.historia), NO del editor web. Pero
el módulo NO tenía menú ni formulario para administrarlas, así que era imposible subir
esas fotos por ningún lado.

**Solución:** se creó un menú nuevo en Odoo llamado "Gigi's Corner" con:
- HISTORIAS: crear/editar cada historia y subir su imagen principal, video y hasta 4
  fotos de proceso. En cuanto subes la foto, el placeholder "A" desaparece solo.
- SOLICITUDES: ver los pedidos que llegan del formulario "Personalizados".

CÓMO SUBIR LAS FOTOS DE LAS HISTORIAS:
1. En Odoo, abre el menú "Gigi's Corner" (barra superior) → "Historias".
2. Verás Amira, Pepe, Valentina y Mateo (ya vienen de ejemplo). Abre una.
3. Sube la "Imagen principal", pega el link del video (opcional) y las fotos de proceso.
4. Guarda. La web se actualiza sola.
Para una historia nueva: botón "Nuevo", llena título, slug (url), etiqueta, los 3
capítulos y la imagen. Marca "Publicada en web".

IMPORTANTE: este cambio agrega vistas nuevas, así que hay que ACTUALIZAR el módulo
(-u gigis_corner) para que aparezca el menú.

## v17.0.8.0.0 — Videos unificados en TODO el sitio
**Problema:** había DOS sistemas de video distintos y solo uno servía.
- Inicio: video por texto editable (gc-video-url) — funcionaba.
- Listado y Detalle de historias: video por `data-video` desde la BD, pero el
  reproductor viejo solo aceptaba archivos .mp4 directos (no YouTube ni Vimeo) y el
  botón ▶ no estaba conectado al reproductor corregido.

**Solución (static/src/js/gigis_main.js):**
- Un solo reproductor para todo el sitio. Soporta YouTube, Vimeo y .mp4.
- El botón ▶ (.gc-play-btn) ahora lee el video de DOS fuentes automáticamente:
  1) atributo data-video  → historias guardadas en la base de datos (listado/detalle)
  2) texto .gc-video-url  → tarjetas editables del inicio
- Si no hay URL válida, el botón ▶ no se muestra (en el inicio el texto de la URL
  solo es visible cuando estás EDITANDO con el lápiz).

DÓNDE PONER CADA VIDEO:
- Inicio (3 tarjetas): editor web (lápiz) → clic en el texto "Pega aquí la URL del
  video" de cada tarjeta y pega el link. Guarda.
- Páginas de detalle e historias /historias: menú "Gigi's Corner" → Historias →
  abre la historia → campo "URL del video". Guarda.

RECORDATORIO CRÍTICO: hay que ACTUALIZAR el módulo (-u gigis_corner) para que el
servidor tome este código. Si el sitio sigue mostrando "Imagen de muestra · reemplázala
con el lápiz de Odoo", es que la BASE DE DATOS tiene una versión vieja guardada:
Ajustes → Técnico → Vistas → busca "Gigi's Corner" → borra las vistas duplicadas/editadas
y vuelve a actualizar el módulo (o desinstala e instala de nuevo).

## v17.0.9.0.0 — Categorías editables desde el backend + Carrito de compra (eCommerce)

### 1) Encabezados de categoría DESBLOQUEADOS (causa raíz resuelta)
**Problema:** en /categoria/<slug> (ej. /categoria/aventuras-mar) NO se podía editar el
encabezado (título, descripción, emoji ni la imagen). La razón real: ese contenido venía
de un diccionario en Python (controllers/main.py) y se pintaba con t-esc / t-if, y Odoo
NUNCA deja editar contenido dinámico (t-esc, t-if, t-foreach) desde el editor web.

**Solución:** se creó el modelo `gigis.categoria` (igual que las Historias). Ahora cada
categoría es un registro de base de datos con: título, slug, emoji, color, descripción,
imagen del encabezado, URL de video y una lista de "ejemplos" (cada uno con su imagen,
video, título y texto).

CÓMO EDITAR LAS CATEGORÍAS AHORA:
1. En Odoo, menú superior "Gigi's Corner" → "Categorías".
2. Abre una (Dulces Sueños, Sueña en Grande, Exploradores, Amigos Especiales,
   Aventuras al Mar). Vienen precargadas.
3. Cambia el título/descripción, sube la "Imagen del encabezado", pega una "URL de video"
   (YouTube/Vimeo/.mp4) y, en la pestaña "Ejemplos", agrega tarjetas con foto/video/texto.
4. Guarda → la página /categoria/<slug> se actualiza sola.
Mientras no subas tu imagen, se muestra la imagen de muestra de cada categoría.

### 2) CARRITO DE COMPRA real (eCommerce de Odoo Community)
**Qué se agregó:** el módulo ahora depende de `website_sale` (eCommerce, gratis en
Community) y `sale_management`. Esto habilita la tienda completa:
- Página /shop con productos, carrito (/shop/cart), checkout y pago en línea.
- Ícono de carrito con contador en el navbar + enlace "Tienda" (navbar y footer).
- 5 categorías de tienda (product.public.category) y 5 productos de EJEMPLO (lámparas)
  para que /shop no salga vacío. Edítalos o bórralos en Comercio electrónico → Productos.
- Cada categoría del sitio se liga a su categoría de tienda; la página /categoria/<slug>
  muestra el botón "Ver lámparas en la tienda".

IMPORTANTE tras instalar:
- Actualiza el módulo (-u gigis_corner). Al instalar website_sale se activan también las
  apps de Ventas/Facturación/Pagos (es lo que necesita un carrito real).
- Para cobrar en línea hay que configurar un proveedor de pago en
  Comercio electrónico → Configuración → Proveedores de pago.
- Sube las fotos y precios reales de tus productos en Comercio electrónico → Productos.

### 3) Etapas (pipeline) en las Solicitudes
**Qué se agregó:** las solicitudes del formulario ahora tienen un flujo de etapas visual.
- Barra de etapas (statusbar) arriba del formulario, clic para avanzar.
- Vista Kanban (tablero) agrupada por etapa: arrastra cada solicitud entre columnas.
- Etapas: 🆕 Nuevo → 📱 Contactado → 🎨 En proceso → 📦 Enviado → ✅ Atendido.
NOTA: si una solicitud vieja tenía "En diseño/En producción/Entregado", esos nombres se
unificaron; solo arrástrala a la columna correcta.

### 4) Correcciones de contenido
- Sección "Así nace una lámpara": se quitó el paso 5 "Personalizamos el nombre" (era lo
  mismo que el paso 1) y se aclaró el paso 1 (se diseña la figura de la lámpara con el
  nombre). Quedaron 5 pasos y se quitó la foto "Nombre" del proceso.
- Equipo (inicio y Nosotros): Marlene y Bryan diseñan cada lámpara (Marlene además
  desarrolla el software); Leidy se encarga del corte de cada pieza.

## v17.0.10.0.0 — Menú Configuración + correo de aviso de Solicitudes

**Qué se agregó:** un menú nuevo **Gigi's Corner → Configuración** con el modelo
`gigis.config` (registro único). Ahí defines:
- **Enviar aviso por correo** (sí/no).
- **Correo para recibir solicitudes** (uno o varios separados por coma).

Ahora, cada vez que alguien envía el formulario de «Personalizados», además de guardarse
en *Solicitudes* y dejar la nota interna, se manda una **copia por correo** a la dirección
configurada (vía mail.mail). Antes no llegaba a nadie.

CÓMO CONFIGURARLO:
1. Menú **Gigi's Corner → Configuración**.
2. Activa «Enviar aviso por correo» y escribe el/los correo(s).
3. Guarda.
REQUISITO: tener un **servidor de correo saliente** configurado en Odoo
(Ajustes → Técnico → Servidores de correo saliente).

## v17.0.11.0.0 — El cliente puede subir imágenes de referencia

**Qué se agregó:** en el formulario de «Personalizados» hay un campo nuevo
**"Imágenes de referencia (opcional)"** donde el cliente puede subir hasta 8
fotos o dibujos que lo inspiren.

- El formulario ahora usa `enctype="multipart/form-data"` (necesario para archivos).
- El controlador valida (solo imágenes, máx. 10 MB c/u, máx. 8) y guarda cada
  archivo como adjunto (ir.attachment) ligado a la solicitud, y lo publica en
  el chatter de la solicitud.
- Se agregó el **chatter** al formulario de Solicitudes en el backend, así que
  las imágenes de referencia (y las notificaciones) se ven al abrir la solicitud.

DÓNDE VERLAS: Gigi's Corner → Solicitudes → abre la solicitud → en el chatter
(lado derecho) aparecen las imágenes que subió el cliente.

## v17.0.12.0.0 — Encabezado de categoría editable con el lápiz (inline)

**Qué cambió:** en /categoria/<slug>, el **título, la descripción y el emoji**
del encabezado ahora son `t-field`, así que se pueden **editar directo en la
página con el lápiz** del editor web. Como cada URL carga su propio registro
(gigis.categoria), cada edición se guarda en ESA categoría, sin chocar entre las
5 páginas.

- Texto del encabezado (título/descripción/emoji) → **lápiz** (en la página) o
  también desde Gigi's Corner → Categorías.
- Imagen de fondo del encabezado → sigue desde **Gigi's Corner → Categorías**
  (la imagen queda protegida del editor para no romper las 5 páginas; abrir el
  lápiz no la altera).
