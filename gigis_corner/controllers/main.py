# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)


class GigisController(http.Controller):

    # ─────────────────────────────────────────────────────────
    # HISTORIAS — lista
    # ─────────────────────────────────────────────────────────
    @http.route('/historias', type='http', auth='public', website=True)
    def historias_lista(self, **kwargs):
        historias = request.env['gigis.historia'].sudo().search(
            [('website_published', '=', True)],
            order='sequence, id',
        )
        return request.render('gigis_corner.view_historias_page', {
            'historias': historias,
        })

    # ─────────────────────────────────────────────────────────
    # HISTORIAS — detalle por slug
    # ─────────────────────────────────────────────────────────
    @http.route('/historias/<string:slug>', type='http', auth='public', website=True)
    def historia_detalle(self, slug, **kwargs):
        historia = request.env['gigis.historia'].sudo().search(
            [('slug', '=', slug), ('website_published', '=', True)],
            limit=1,
        )
        if not historia:
            return request.not_found()
        return request.render('gigis_corner.view_historia_detalle', {
            'historia': historia,
        })

    # ─────────────────────────────────────────────────────────
    # NOSOTROS
    # ─────────────────────────────────────────────────────────
    @http.route('/nosotros', type='http', auth='public', website=True)
    def nosotros(self, **kwargs):
        return request.render('gigis_corner.view_nosotros_page', {})

    # ─────────────────────────────────────────────────────────
    # PERSONALIZADOS — formulario
    # ─────────────────────────────────────────────────────────
    @http.route('/personalizados', type='http', auth='public', website=True)
    def personalizados(self, **kwargs):
        return request.render('gigis_corner.view_personalizado_page', {})

    # ─────────────────────────────────────────────────────────
    # PERSONALIZADOS — recibir el formulario (POST)
    # ─────────────────────────────────────────────────────────
    @http.route('/personalizados/enviar', type='http', auth='public',
                website=True, methods=['POST'], csrf=True)
    def personalizado_submit(self, **post):
        try:
            vals = {
                'nombre_nino':      post.get('nombre_nino', '').strip(),
                'edad':             post.get('edad', '').strip(),
                'tema_favorito':    post.get('tema_favorito', '').strip(),
                'colores':          post.get('colores', '').strip(),
                'historia':         post.get('historia', '').strip(),
                'nombre_contacto':  post.get('nombre_contacto', '').strip(),
                'telefono':         post.get('telefono', '').strip(),
                'email':            post.get('email', '').strip(),
                'como_conocio':     post.get('como_conocio', False) or False,
                'presupuesto':      post.get('presupuesto', False) or False,
            }

            # Validar campos requeridos
            if not vals['nombre_nino'] or not vals['nombre_contacto']:
                return request.render('gigis_corner.view_personalizado_page', {
                    'error': 'Por favor completa el nombre del niño y tu nombre.',
                    'valores': post,
                })

            # Fecha requerida (puede venir vacía)
            fecha_str = post.get('fecha_requerida', '').strip()
            if fecha_str:
                vals['fecha_requerida'] = fecha_str

            # Crear el registro
            request.env['gigis.personalizacion'].sudo().create(vals)

        except Exception as e:
            _logger.error("Error guardando solicitud Gigi's Corner: %s", e)
            return request.render('gigis_corner.view_personalizado_page', {
                'error': 'Hubo un error. Por favor escríbenos por WhatsApp.',
                'valores': post,
            })

        return request.redirect('/gracias')

    # ─────────────────────────────────────────────────────────
    # GRACIAS
    # ─────────────────────────────────────────────────────────
    @http.route('/gracias', type='http', auth='public', website=True)
    def gracias(self, **kwargs):
        return request.render('gigis_corner.view_gracias_page', {})
