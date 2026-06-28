# -*- coding: utf-8 -*-
import base64
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

    def _es_sitio_gigis(self):
        """True si el sitio web actual es el de Gigi's Corner.
        Solo restringe cuando existe más de un sitio web; si Gigi's
        es el único sitio, nunca bloquea."""
        website = getattr(request, 'website', False)
        if not website:
            return True
        total_sitios = request.env['website'].sudo().search_count([])
        if total_sitios <= 1:
            return True
        nombre = (website.name or '').lower()
        return 'gigi' in nombre

    # ── HOME ──────────────────────────────────────────────────
    @http.route('/', type='http', auth='public', website=True)
    def home(self, **kwargs):
        if not self._es_sitio_gigis():
            return request.not_found()
        return request.render('gigis_corner.view_home_page', {})

    # ── HISTORIAS — lista ─────────────────────────────────────
    @http.route('/historias', type='http', auth='public', website=True)
    def historias_lista(self, **kwargs):
        if not self._es_sitio_gigis():
            return request.not_found()
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
        if not self._es_sitio_gigis():
            return request.not_found()
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
        if not self._es_sitio_gigis():
            return request.not_found()
        return request.render('gigis_corner.view_nosotros_page', {})

    # ── CATEGORÍAS ────────────────────────────────────────────
    # El contenido (título, descripción, imagen, video y ejemplos) se
    # administra desde el backend: Gigi's Corner → Categorías
    # (modelo gigis.categoria). Ya no se define en Python.
    @http.route('/categoria/<string:slug>', type='http', auth='public', website=True)
    def categoria(self, slug, **kwargs):
        if not self._es_sitio_gigis():
            return request.not_found()
        company = self._get_gigis_company()
        domain = [('slug', '=', slug), ('website_published', '=', True)]
        if company:
            domain.append(('company_id', '=', company.id))
        cat = request.env['gigis.categoria'].sudo().search(domain, limit=1)
        if not cat:
            return request.not_found()
        return request.render('gigis_corner.view_categoria_page', {
            'cat': cat,
            'slug': slug,
        })

    # ── PERSONALIZADOS — formulario ───────────────────────────
    @http.route('/personalizados', type='http', auth='public', website=True)
    def personalizados(self, **kwargs):
        if not self._es_sitio_gigis():
            return request.not_found()
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

            rec = request.env['gigis.personalizacion'].sudo().create(vals)
            self._guardar_imagenes_ref(rec)

        except Exception as e:
            _logger.error("Error solicitud Gigi's Corner: %s", e)
            return request.render('gigis_corner.view_personalizado_page', {
                'error': 'Hubo un error. Por favor escríbenos por WhatsApp.',
                'valores': post,
            })

        return request.redirect('/gracias')

    def _guardar_imagenes_ref(self, rec):
        """Guarda las imágenes de referencia que sube el cliente como
        adjuntos de la solicitud y las publica en el chatter."""
        try:
            files = request.httprequest.files.getlist('imagenes_ref')
        except Exception:
            files = []
        attachment_ids = []
        for f in files[:8]:  # máximo 8 imágenes
            if not f or not f.filename:
                continue
            if not (f.content_type or '').startswith('image/'):
                continue
            data = f.read()
            if not data or len(data) > 10 * 1024 * 1024:  # máx 10 MB c/u
                continue
            att = request.env['ir.attachment'].sudo().create({
                'name': f.filename,
                'datas': base64.b64encode(data),
                'res_model': 'gigis.personalizacion',
                'res_id': rec.id,
                'mimetype': f.content_type,
            })
            attachment_ids.append(att.id)
        if attachment_ids:
            rec.sudo().message_post(
                body="📎 Imágenes de referencia enviadas por el cliente.",
                attachment_ids=attachment_ids,
            )

    # ── GRACIAS ───────────────────────────────────────────────
    @http.route('/gracias', type='http', auth='public', website=True)
    def gracias(self, **kwargs):
        return request.render('gigis_corner.view_gracias_page', {})
