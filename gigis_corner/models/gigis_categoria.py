# -*- coding: utf-8 -*-
from odoo import models, fields


class GigisCategoria(models.Model):
    _name = 'gigis.categoria'
    _description = "Gigi's Corner — Categoría"
    _order = 'sequence, id'
    _rec_name = 'titulo'

    titulo = fields.Char(string='Título', required=True)
    slug = fields.Char(string='URL amigable', required=True,
                       help='Ej: aventuras-mar → /categoria/aventuras-mar')
    emoji = fields.Char(string='Emoji', default='🌟')
    color = fields.Char(string='Color de fondo (hex)', default='#D6EDFB')
    descripcion = fields.Text(string='Descripción')

    # ── Encabezado (HERO) — editable con foto o video ──────────
    imagen_hero = fields.Binary(string='Imagen del encabezado', attachment=True)
    video_url = fields.Char(string='URL del video del encabezado',
                            help='YouTube, Vimeo o .mp4. Si lo defines aparece el botón ▶ sobre la imagen.')

    # ── Sección de ejemplos ────────────────────────────────────
    seccion_etiqueta = fields.Char(string='Etiqueta de la sección',
                                   default='Ejemplos de esta categoría')
    seccion_titulo = fields.Char(string='Título de la sección',
                                 default='Lámparas que inspiran')
    ejemplo_ids = fields.One2many('gigis.categoria.ejemplo', 'categoria_id',
                                  string='Ejemplos')

    # ── Publicación / tienda ───────────────────────────────────
    sequence = fields.Integer(string='Orden', default=10)
    active = fields.Boolean(string='Activa', default=True)
    website_published = fields.Boolean(string='Publicada en web', default=True)
    public_category_id = fields.Many2one(
        'product.public.category',
        string='Categoría de tienda (eCommerce)',
        help='Liga esta categoría con una categoría de la tienda para mostrar el botón "Ver en la tienda".',
    )

    # ── Multi-empresa ──────────────────────────────────────────
    company_id = fields.Many2one(
        'res.company',
        string='Empresa',
        default=lambda self: self.env.company,
    )

    _sql_constraints = [
        ('slug_unique', 'unique(slug)', 'El URL de la categoría debe ser único.'),
    ]


class GigisCategoriaEjemplo(models.Model):
    _name = 'gigis.categoria.ejemplo'
    _description = "Gigi's Corner — Ejemplo de categoría"
    _order = 'sequence, id'
    _rec_name = 'titulo'

    categoria_id = fields.Many2one('gigis.categoria', string='Categoría',
                                   required=True, ondelete='cascade')
    titulo = fields.Char(string='Título', required=True, default='Diseño')
    descripcion = fields.Text(string='Descripción')
    imagen = fields.Binary(string='Imagen', attachment=True)
    video_url = fields.Char(string='URL del video',
                            help='YouTube, Vimeo o .mp4 (opcional).')
    sequence = fields.Integer(string='Orden', default=10)
