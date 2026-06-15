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
