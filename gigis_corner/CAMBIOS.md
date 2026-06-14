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
