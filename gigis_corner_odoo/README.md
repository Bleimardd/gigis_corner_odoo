# 🕯️ Gigi's Corner — Módulo Odoo 17
## Portal Web Completo — Guía de Instalación y Uso

---

## 📦 INSTALACIÓN (5 pasos)

### Paso 1 — Copiar el módulo
Copia la carpeta `gigis_corner` completa a:
```
/tu-servidor/addons/gigis_corner
```

### Paso 2 — Activar modo desarrollador
En Odoo: **Configuración → Activar modo desarrollador**

### Paso 3 — Actualizar lista de módulos
**Configuración → Técnico → Actualizar lista de módulos**

### Paso 4 — Instalar el módulo
**Aplicaciones → buscar "Gigi's Corner" → Instalar**

### Paso 5 — Listo ✅
El sitio web aparece con todas las páginas y estilos cargados.

---

## 📸 AGREGAR FOTOS Y VIDEOS (es todo lo que necesitas hacer)

El módulo viene con **placeholders** en todas las posiciones donde van fotos/videos.
Para reemplazarlos, usa el **editor visual de Odoo** (el lápiz azul en la barra superior).

### Fotos a reemplazar:

| Sección | Descripción | Dónde está |
|---------|-------------|------------|
| Hero principal | Lámpara encendida con nombre | Página de inicio, parte derecha |
| Amira y el Mar | Foto/video de la lámpara | Home → Historias, y página /historias/amira-y-el-mar |
| Pepe la Tortuga | Foto/video | Home → Historias |
| Valentina Astronauta | Foto/video | Home → Historias |
| Proceso artesanal (×6) | Fotos de cada paso | Sección "Así nace una lámpara" |
| Ana con Helana | Foto familiar | Sección "Historia de Ana" |
| Equipo (×4) | Fotos de Ana, Marlene, Leidy, Bryan | Sección "El equipo" |
| Galería familias (×12) | Fotos de habitaciones con lámparas | Sección "Galería de Familias" |
| Testimonios (×3) | Fotos opcionales de clientes | Sección "Testimonios" |
| Personalizados galería (×8) | Mejores trabajos realizados | Página /personalizados |
| Nosotros capítulos | Fotos de la historia de Ana | Página /nosotros |

### Cómo reemplazar una foto:
1. Ve a la página en cuestión
2. Clic en el **lápiz azul** (editar)
3. Haz clic sobre el placeholder
4. Clic en **"Reemplazar imagen"**
5. Sube tu foto
6. Clic en **Guardar**

### Cómo agregar un video:
1. Edita la página
2. Clic sobre el placeholder del video
3. En el atributo `data-video`, pega la URL del video
4. Para videos de Instagram/TikTok, usa el enlace directo al archivo .mp4
5. Guarda

---

## 📝 EDITAR TEXTOS

Todos los textos están marcados con comentarios `<!-- ▼▼▼ EDITA ESTE TEXTO ▼▼▼ -->`.

### Desde el editor visual:
1. Clic en **Editar**
2. Clic sobre el texto que quieres cambiar
3. Escribe el nuevo texto
4. **Guardar**

### Textos principales a personalizar:
- **Historia de Amira** en `/historias/amira-y-el-mar` → sección de capítulos
- **Historia de Pepe** → agregar página similar duplicando la de Amira
- **Historia de Ana** en `/nosotros` → capítulos 1, 2, 3, 4
- **Testimonios** → citar textualmente lo que digan las familias reales

---

## 💬 FORMULARIO DE PERSONALIZACIÓN

Las solicitudes llegan automáticamente a:
- **Odoo CRM** → Pipeline → "Solicitud Personalización"
- **Modelo propio** → Formularios recibidos

Para ver las solicitudes: **CRM → Pipeline** o **Sitio Web → Formularios**

---

## 📱 WHATSAPP

El número configurado es: **+52 55 2945 1680**

Para cambiarlo, busca en los archivos XML:
```
https://wa.me/525529451680
```
Y reemplaza con tu número en formato internacional sin espacios.

---

## 🎨 PERSONALIZAR COLORES

Los colores están definidos en:
`static/src/css/gigis_main.css` → sección `:root { --gc-coral: ... }`

Puedes cambiarlos sin tocar el HTML. Los cambios aplican a todo el sitio.

---

## 📄 PÁGINAS INCLUIDAS

| URL | Descripción |
|-----|-------------|
| `/` | Home completo con 9 secciones |
| `/historias` | Galería de todas las historias |
| `/historias/amira-y-el-mar` | Página detalle de Amira |
| `/nosotros` | Historia de Ana en capítulos |
| `/personalizados` | Formulario completo de diseño |
| `/gracias` | Página de confirmación post-formulario |
| `/shop` | Tienda eCommerce de Odoo (nativa) |

---

## 🆘 SOPORTE

¿Tienes dudas técnicas sobre la instalación?
Escribe a: info@gigiscorner.com.mx
