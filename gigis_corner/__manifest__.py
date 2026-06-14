# -*- coding: utf-8 -*-
{
    'name': "Gigi's Corner – Portal Web",
    'summary': "Sitio web completo. 100% Odoo 17 Community.",
    'author': "Gigi's Corner",
    'website': "https://gigiscorner.com.mx",
    'category': 'Website',
    'version': '17.0.2.0.0',
    'depends': ['website', 'mail', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'data/gigis_data.xml',
        'views/gigis_templates.xml',
        'views/gigis_home.xml',
        'views/gigis_historias.xml',
        'views/gigis_categoria.xml',
        'views/gigis_nosotros.xml',
        'views/gigis_personalizado.xml',
        'views/gigis_menus.xml',
    ],
    # ── Assets: sintaxis nativa Odoo 17 ──────────────────────
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
