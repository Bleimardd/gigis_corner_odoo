# -*- coding: utf-8 -*-
{
    'name': "Gigi's Corner – Portal Web",
    'summary': "Sitio web completo para Gigi's Corner – Lámparas infantiles personalizadas",
    'description': """
        Portal web completo para Gigi's Corner.
        Incluye: Home, Historias, Nosotros, Personalizados y páginas de producto.
        Solo requiere agregar fotos y videos para estar 100% listo.
    """,
    'author': "Gigi's Corner",
    'website': "https://gigiscorner.com.mx",
    'category': 'Website',
    'version': '17.0.1.0.0',
    'depends': [
        'website',
        'website_sale',
        'website_blog',
        'website_form',
        'mail',
        'crm',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/gigis_data.xml',
        'views/gigis_templates.xml',
        'views/gigis_home.xml',
        'views/gigis_historias.xml',
        'views/gigis_nosotros.xml',
        'views/gigis_personalizado.xml',
        'views/gigis_snippets.xml',
        'views/gigis_menus.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'gigis_corner/static/src/css/gigis_main.css',
            'gigis_corner/static/src/css/gigis_animations.css',
            'gigis_corner/static/src/js/gigis_main.js',
        ],
    },
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
