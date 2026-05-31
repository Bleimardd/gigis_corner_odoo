# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)


class GigisController(http.Controller):

    def _get_gigis_company(self):
        """Devuelve siempre la empresa Gigi's Corner."""
        return request.env['res.company'].sudo().search(
            [('name', 'ilike', "Gigi's Corner")], limit=1
        )

    # ── HOME ──────────────────────────────────────────────────
    @http.route('/', type='http', auth='public', website=True)
    def home(self, **kwargs):
        return request.render('gigis_corner.view_home_page', {})

    # ── HISTORIAS — lista ─────────────────────────────────────
    @http.route('/historias', type='http', auth='public', website=True)
    def historias_lista(self, **kwargs):
        company = self._get_gigis_company()
        domain = [('website_published', '=', True)]
        if company:
            domain.append(('company_id', '=', company.id))
        historias = request.env['gigis.historia'].sudo().search(
            domain, order='sequence, id'
        )
        return request.render('gigis_corner.view_historias_page', {
            'historias': historias,
        })

    # ── HISTORIAS — detalle ───────────────────────────────────
    @http.route('/historias/<string:slug>', type='http', auth='public', website=True)
    def historia_detalle(self, slug, **kwargs):
        company = self._get_gigis_company()
        domain = [('slug', '=', slug), ('website_published', '=', True)]
        if company:
            domain.append(('company_id', '=', company.id))
        historia = request.env['gigis.historia'].sudo().search(domain, limit=1)
        if not historia:
            return request.not_found()
        return request.render('gigis_corner.view_historia_detalle', {
            'historia': historia,
        })

    # ── NOSOTROS ──────────────────────────────────────────────
    @http.route('/nosotros', type='http', auth='public', website=True)
    def nosotros(self, **kwargs):
        return request.render('gigis_corner.view_nosotros_page', {})

    # ── PERSONALIZADOS — formulario ───────────────────────────
    @http.route('/personalizados', type='http', auth='public', website=True)
    def personalizados(self, **kwargs):
        return request.render('gigis_corner.view_personalizado_page', {})

    # ── PERSONALIZADOS — recibir POST ─────────────────────────
    @http.route('/personalizados/enviar', type='http', auth='public',
                website=True, methods=['POST'], csrf=True)
    def personalizado_submit(self, **post):
        try:
            # Buscar empresa Gigi's Corner
            company = self._get_gigis_company()

            vals = {
                'nombre_nino':     post.get('nombre_nino', '').strip(),
                'edad':            post.get('edad', '').strip(),
                'tema_favorito':   post.get('tema_favorito', '').strip(),
                'colores':         post.get('colores', '').strip(),
                'historia':        post.get('historia', '').strip(),
                'nombre_contacto': post.get('nombre_contacto', '').strip(),
                'telefono':        post.get('telefono', '').strip(),
                'email':           post.get('email', '').strip(),
                'como_conocio':    post.get('como_conocio') or False,
                'presupuesto':     post.get('presupuesto') or False,
            }

            # Asignar siempre a Gigi's Corner
            if company:
                vals['company_id'] = company.id

            if not vals['nombre_nino'] or not vals['nombre_contacto']:
                return request.render('gigis_corner.view_personalizado_page', {
                    'error': 'Por favor completa el nombre del niño y tu nombre.',
                    'valores': post,
                })

            fecha_str = post.get('fecha_requerida', '').strip()
            if fecha_str:
                vals['fecha_requerida'] = fecha_str

            request.env['gigis.personalizacion'].sudo().create(vals)

        except Exception as e:
            _logger.error("Error solicitud Gigi's Corner: %s", e)
            return request.render('gigis_corner.view_personalizado_page', {
                'error': 'Hubo un error. Por favor escríbenos por WhatsApp.',
                'valores': post,
            })

        return request.redirect('/gracias')

    # ── GRACIAS ───────────────────────────────────────────────
    @http.route('/gracias', type='http', auth='public', website=True)
    def gracias(self, **kwargs):
        return request.render('gigis_corner.view_gracias_page', {})
