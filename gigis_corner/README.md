# 💡 Gigi's Corner — Módulo Odoo 17 Community
## ✅ 100% Compatible con Odoo 17 Community Edition

---

## ¿Por qué es Community compatible?

| Función | Versión anterior (Enterprise) | Esta versión (Community) |
|---------|-------------------------------|--------------------------|
| Historias | `website_blog` ❌ Enterprise | Modelo propio `gigis.historia` ✅ |
| Formulario | `website_form` ❌ Enterprise | Controlador HTTP propio ✅ |
| Pipeline clientes | `crm` ❌ Enterprise | Notificación por email + modelo propio ✅ |
| Tienda | `website_sale` ❌ Enterprise | No incluida (agregar manualmente) ✅ |
| Sitio web | `website` ✅ Community | `website` ✅ Community |

**Dependencias usadas:** `website`, `mail`, `web` — todas disponibles en Community.

---

## 📦 INSTALACIÓN

### Paso 1 — Copiar el módulo
```bash
cp -r gigis_corner /ruta/a/tu/odoo/addons/
```

### Paso 2 — Reiniciar Odoo
```bash
sudo systemctl restart odoo
# o
./odoo-bin -c odoo.conf -u gigis_corner
```

### Paso 3 — Activar modo desarrollador
**Configuración → Activar modo desarrollador** (agregar `?debug=1` a la URL)

### Paso 4 — Instalar
**Aplicaciones → Actualizar lista → buscar "Gigi's Corner" → Instalar**

---

## 📸 AGREGAR FOTOS Y VIDEOS

### Opción A — Desde el editor visual (recomendada)
1. Abre la página en el navegador
2. Clic en **Editar** (lápiz azul en la barra superior)
3. Clic sobre el placeholder de la foto
4. Clic en **Reemplazar imagen** → sube tu foto
5. **Guardar**

### Opción B — Desde el backend de Odoo
Para las historias con fotos del proceso:

1. Ve a **Odoo (backend) → Gigi's Corner → Historias**
2. Abre la historia que quieres editar
3. Sube la **Imagen principal** y las **Fotos del proceso**
4. Pega la **URL del video** si tienes uno
5. Guarda

---

## ✍️ EDITAR TEXTOS DE LAS HISTORIAS

Desde el backend: **Gigi's Corner → Historias → [selecciona una historia]**

Campos editables:
- **Título** y **subtítulo**
- **Extracto** (texto que aparece en la tarjeta)
- **La historia** (capítulo 1)
- **El proceso** (capítulo 2)
- **El resultado** (capítulo 3)

---

## ➕ AGREGAR NUEVAS HISTORIAS

1. **Gigi's Corner → Historias → Nuevo**
2. Llena los campos:
   - **Título**: `Luna y las Estrellas`
   - **URL amigable (slug)**: `luna-y-las-estrellas` ← sin espacios, con guiones
   - **Emoji**: 🌙
   - **Extracto**: texto corto para la tarjeta
   - **Capítulos**: historia, proceso, resultado
3. Sube la foto principal
4. Marca **Publicada en web** ✅
5. Guarda → aparece en `/historias` automáticamente

---

## 📋 VER SOLICITUDES DEL FORMULARIO

Las solicitudes del formulario de personalización llegan a:

**Odoo Backend → Gigi's Corner → Solicitudes de Personalización**

Desde ahí puedes cambiar el estado del pedido:
- 🆕 Nuevo → 📱 Contactado → 🎨 En diseño → 🔨 En producción → 📦 Enviado → ✅ Entregado

---

## 📧 CONFIGURAR NOTIFICACIONES POR EMAIL

Para recibir un email cuando llegue una nueva solicitud:

1. **Odoo → Gigi's Corner → Solicitudes**
2. Abre cualquier solicitud
3. Clic en **Seguir** (el ícono de ojo/campana)
4. Desde ese momento recibirás emails de nuevas solicitudes

O configura un usuario como seguidor permanente desde el código:
```python
# En gigis_personalizacion.py, método _enviar_notificacion_interna()
# Agrega el email del equipo como seguidor
```

---

## 🌐 PÁGINAS INCLUIDAS

| URL | Descripción |
|-----|-------------|
| `/` | Home (9 secciones completas) |
| `/historias` | Lista de todas las historias |
| `/historias/amira-y-el-mar` | Historia de Amira |
| `/historias/pepe-la-tortuga` | Historia de Pepe |
| `/historias/valentina-astronauta` | Historia de Valentina |
| `/historias/mateo-constructor` | Historia de Mateo |
| `/historias/<slug>` | Cualquier historia nueva que agregues |
| `/nosotros` | Historia de Ana y el equipo |
| `/personalizados` | Formulario de diseño personalizado |
| `/gracias` | Confirmación tras el formulario |

---

## 🎨 CAMBIAR COLORES DE MARCA

Edita el archivo:
```
static/src/css/gigis_main.css
```

Sección `:root { }` al inicio del archivo:
```css
--gc-coral:     #FF5C64;   /* color principal botones */
--gc-blue:      #5DA7E8;   /* azul secundario */
--gc-turquoise: #34C9B8;   /* turquesa */
--gc-yellow:    #F5C640;   /* amarillo/estrellas */
--gc-cream:     #F7F3EB;   /* fondo general */
```

---

## 📱 CAMBIAR NÚMERO DE WHATSAPP

Busca en todos los archivos:
```
525529451680
```
Y reemplaza con tu número en formato: `52` + código de área + número (sin espacios ni +).

Ejemplo para +52 55 1234 5678 → `5255123456780`

---

## 🆘 PROBLEMAS FRECUENTES

**El módulo no aparece en la lista de aplicaciones:**
→ Ve a Configuración → Actualizar lista de módulos

**Error al instalar — modelo no encontrado:**
→ Asegúrate de que la carpeta se llame exactamente `gigis_corner`

**Las páginas de historias dan 404:**
→ Verifica que el campo "slug" no tenga espacios ni caracteres especiales

**El formulario no envía:**
→ Verifica que Odoo esté en modo producción o que el CSRF esté habilitado
