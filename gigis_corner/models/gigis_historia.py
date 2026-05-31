# -*- coding: utf-8 -*-
from odoo import models, fields, api


class GigisHistoria(models.Model):
    """
    Modelo propio para las historias de los niños.
    Reemplaza website_blog (Enterprise) con un sistema propio Community.
    """
    _name = 'gigis.historia'
    _description = "Gigi's Corner — Historia de un niño"
    _order = 'sequence, id'
    _rec_name = 'titulo'

    titulo = fields.Char(string='Título', required=True)
    slug = fields.Char(
        string='URL amigable',
        required=True,
        help='Ej: amira-y-el-mar  →  /historias/amira-y-el-mar',
    )
    nombre_nino = fields.Char(string='Nombre del niño/a')
    subtitulo = fields.Char(string='Subtítulo corto')
    extracto = fields.Text(string='Extracto (tarjeta)')
    emoji = fields.Char(string='Emoji representativo', default='🌟')
    color_fondo = fields.Char(
        string='Color de fondo (CSS)',
        default='var(--gc-light-blue)',
        help='Ej: var(--gc-mint) o #D6EDFB',
    )
    etiqueta = fields.Char(string='Etiqueta', help='Ej: 🌊 Mar')

    # ── CAPÍTULOS DE LA HISTORIA ──
    capitulo_historia = fields.Text(string='La historia')
    capitulo_proceso = fields.Text(string='El proceso')
    capitulo_resultado = fields.Text(string='El resultado ❤️')

    # ── MEDIA ──
    imagen_principal = fields.Binary(string='Imagen/foto principal', attachment=True)
    imagen_filename = fields.Char(string='Nombre archivo imagen')
    video_url = fields.Char(
        string='URL del video',
        help='URL directa al archivo .mp4 o enlace embed',
    )
    # Fotos del proceso (hasta 6)
    foto_proceso_1 = fields.Binary(string='Foto proceso 1', attachment=True)
    foto_proceso_2 = fields.Binary(string='Foto proceso 2', attachment=True)
    foto_proceso_3 = fields.Binary(string='Foto proceso 3', attachment=True)
    foto_proceso_4 = fields.Binary(string='Foto proceso 4', attachment=True)

    sequence = fields.Integer(string='Orden', default=10)
    active = fields.Boolean(string='Activa', default=True)
    website_published = fields.Boolean(string='Publicada en web', default=True)

    _sql_constraints = [
        ('slug_unique', 'unique(slug)', 'El URL de la historia debe ser único.'),
    ]
