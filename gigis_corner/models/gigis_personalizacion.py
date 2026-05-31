# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class GigisPersonalizacion(models.Model):
    _name = 'gigis.personalizacion'
    _description = "Gigi's Corner — Solicitud de Personalización"
    _order = 'create_date desc'
    _rec_name = 'nombre_nino'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    nombre_nino     = fields.Char(string='Nombre del niño/a', required=True, tracking=True)
    edad            = fields.Char(string='Edad')
    tema_favorito   = fields.Char(string='Tema favorito')
    colores         = fields.Char(string='Colores preferidos')
    historia        = fields.Text(string='Historia detrás del diseño')
    nombre_contacto = fields.Char(string='Nombre del papá/mamá', required=True)
    telefono        = fields.Char(string='WhatsApp / Teléfono')
    email           = fields.Char(string='Correo electrónico')
    fecha_requerida = fields.Date(string='Fecha requerida')

    presupuesto = fields.Selection([
        ('500-800',   '$500 – $800 MXN'),
        ('800-1200',  '$800 – $1,200 MXN'),
        ('1200-2000', '$1,200 – $2,000 MXN'),
        ('2000+',     '$2,000+ MXN'),
        ('consulta',  'Quiero asesoría'),
    ], string='Presupuesto')

    como_conocio = fields.Selection([
        ('instagram',     'Instagram'),
        ('facebook',      'Facebook'),
        ('tiktok',        'TikTok'),
        ('recomendacion', 'Recomendación'),
        ('google',        'Google'),
        ('whatsapp',      'WhatsApp'),
        ('otro',          'Otro'),
    ], string='¿Cómo nos conoció?')

    state = fields.Selection([
        ('nuevo',         '🆕 Nuevo'),
        ('contactado',    '📱 Contactado'),
        ('en_diseno',     '🎨 En diseño'),
        ('en_produccion', '🔨 En producción'),
        ('enviado',       '📦 Enviado'),
        ('entregado',     '✅ Entregado'),
    ], string='Estado', default='nuevo', tracking=True)

    notas_internas = fields.Text(string='Notas internas')

    # ── Multi-empresa: fija a Gigi's Corner ───────────────────
    company_id = fields.Many2one(
        'res.company',
        string='Empresa',
        default=lambda self: self._get_gigis_company(),
        required=True,
    )

    def _get_gigis_company(self):
        """Siempre asigna las solicitudes a la empresa Gigi's Corner."""
        gigis = self.env['res.company'].sudo().search(
            [('name', 'ilike', "Gigi's Corner")], limit=1
        )
        return gigis or self.env.company

    # ── Acciones de estado ────────────────────────────────────
    def action_contactado(self):    self.state = 'contactado'
    def action_en_diseno(self):     self.state = 'en_diseno'
    def action_en_produccion(self): self.state = 'en_produccion'
    def action_enviado(self):       self.state = 'enviado'
    def action_entregado(self):     self.state = 'entregado'

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for rec in records:
            rec._enviar_notificacion_interna()
        return records

    def _enviar_notificacion_interna(self):
        try:
            subject = f"✨ Nueva solicitud — Lámpara para {self.nombre_nino}"
            body = f"""
<div style="font-family:Arial,sans-serif;max-width:600px;">
  <div style="background:#FF5C64;padding:20px;border-radius:12px 12px 0 0;text-align:center;">
    <h2 style="color:white;margin:0;">💡 Nueva Solicitud de Lámpara</h2>
  </div>
  <div style="background:#FFF8EE;padding:24px;border-radius:0 0 12px 12px;border:1px solid #F5E6D0;">
    <h3 style="color:#1E3A5F;">👶 Datos del niño/a</h3>
    <table style="width:100%;border-collapse:collapse;">
      <tr><td style="padding:6px 0;color:#666;width:40%"><strong>Nombre:</strong></td>
          <td><strong>{self.nombre_nino}</strong></td></tr>
      <tr><td style="padding:6px 0;color:#666"><strong>Edad:</strong></td>
          <td>{self.edad or '—'}</td></tr>
      <tr><td style="padding:6px 0;color:#666"><strong>Tema favorito:</strong></td>
          <td>{self.tema_favorito or '—'}</td></tr>
      <tr><td style="padding:6px 0;color:#666"><strong>Colores:</strong></td>
          <td>{self.colores or '—'}</td></tr>
      <tr><td style="padding:6px 0;color:#666"><strong>Presupuesto:</strong></td>
          <td>{dict(self._fields['presupuesto'].selection).get(self.presupuesto, '—')}</td></tr>
    </table>
    <h3 style="color:#FF5C64;margin-top:20px;">💌 Historia</h3>
    <div style="background:white;padding:16px;border-radius:8px;border-left:4px solid #FF5C64;line-height:1.6;">
      {self.historia or 'Sin historia proporcionada'}
    </div>
    <h3 style="color:#1E3A5F;margin-top:20px;">📱 Contacto</h3>
    <table style="width:100%;border-collapse:collapse;">
      <tr><td style="padding:6px 0;color:#666;width:40%"><strong>Nombre:</strong></td>
          <td>{self.nombre_contacto}</td></tr>
      <tr><td style="padding:6px 0;color:#666"><strong>WhatsApp:</strong></td>
          <td><a href="https://wa.me/{(self.telefono or '').replace(' ','').replace('+','')}"
                 style="color:#25D366;font-weight:bold;">{self.telefono or '—'}</a></td></tr>
      <tr><td style="padding:6px 0;color:#666"><strong>Email:</strong></td>
          <td>{self.email or '—'}</td></tr>
    </table>
  </div>
</div>"""
            self.message_post(
                subject=subject, body=body,
                message_type='email',
                subtype_xmlid='mail.mt_comment',
            )
        except Exception as e:
            _logger.warning("Notificación Gigi's Corner: %s", e)
