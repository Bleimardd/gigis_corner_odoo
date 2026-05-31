# -*- coding: utf-8 -*-
{
    'name': "Gigi's Corner – Portal Web",
    'summary': "Sitio web completo para Gigi's Corner. 100% compatible con Odoo 17 Community.",
    'description': """
        Portal web completo para Gigi's Corner – Lámparas infantiles personalizadas.

        COMPATIBLE CON ODOO 17 COMMUNITY ✅
        No requiere módulos Enterprise.

        Incluye:
        - Home con 9 secciones
        - Página Historias (manejada por controlador propio)
        - Página Nosotros
        - Formulario de Personalización (guarda en BD + notificación por email)
        - Página de Gracias
        - Navbar y Footer personalizados
        - Diseño responsive con colores de marca
        - Animaciones CSS
        - Botón WhatsApp flotante
    """,
    'author': "Gigi's Corner",
    'website': "https://gigiscorner.com.mx",
    'category': 'Website',
    'version': '17.0.1.0.0',

    # ─────────────────────────────────────────────────────────
    # SOLO módulos disponibles en Odoo 17 COMMUNITY
    # ─────────────────────────────────────────────────────────
    'depends': [
        'website',        # ✅ Community — sitio web base
        'mail',           # ✅ Community — email y notificaciones
        'web',            # ✅ Community — framework base
    ],

    'data': [
        'security/ir.model.access.csv',
        'data/gigis_data.xml',
        'views/gigis_templates.xml',
        'views/gigis_home.xml',
        'views/gigis_historias.xml',
        'views/gigis_nosotros.xml',
        'views/gigis_personalizado.xml',
        'views/gigis_menus.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'gigis_corner/static/src/css/gigis_main.css',
            'gigis_corner/static/src/css/gigis_animations.css',
            'gigis_corner/static/src/js/gigis_main.js',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
