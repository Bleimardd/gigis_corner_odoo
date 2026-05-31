# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class GigisPersonalizacion(models.Model):
    """
    Solicitudes de lámparas personalizadas desde el formulario web.
    100% Community — sin dependencia de crm ni enterprise.
    """
    _name = 'gigis.personalizacion'
    _description = "Gigi's Corner — Solicitud de Personalización"
    _order = 'create_date desc'
    _rec_name = 'nombre_nino'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # ── DATOS DEL NIÑO ──────────────────────────────────
    nombre_nino = fields.Char(
        string='Nombre del niño/a',
        required=True,
        tracking=True,
    )
    edad = fields.Char(string='Edad')
    tema_favorito = fields.Char(string='Tema favorito')
    colores = fields.Char(string='Colores preferidos')
    historia = fields.Text(
        string='Historia detrás del diseño',
        help='El campo más importante: la historia personal del niño.',
    )

    # ── DATOS DE CONTACTO ───────────────────────────────
    nombre_contacto = fields.Char(string='Nombre del papá/mamá', required=True)
    telefono = fields.Char(string='WhatsApp / Teléfono')
    email = fields.Char(string='Correo electrónico')

    # ── DETALLES DEL PEDIDO ─────────────────────────────
    fecha_requerida = fields.Date(string='Fecha requerida')
    presupuesto = fields.Selection([
        ('500-800',   '$500 – $800 MXN'),
        ('800-1200',  '$800 – $1,200 MXN'),
        ('1200-2000', '$1,200 – $2,000 MXN'),
        ('2000+',     '$2,000+ MXN'),
        ('consulta',  'Quiero asesoría'),
    ], string='Presupuesto')

    como_conocio = fields.Selection([
        ('instagram',      'Instagram'),
        ('facebook',       'Facebook'),
        ('tiktok',         'TikTok'),
        ('recomendacion',  'Recomendación'),
        ('google',         'Google'),
        ('whatsapp',       'WhatsApp'),
        ('otro',           'Otro'),
    ], string='¿Cómo nos conoció?')

    # ── ESTADO DEL PEDIDO ───────────────────────────────
    state = fields.Selection([
        ('nuevo',        '🆕 Nuevo'),
        ('contactado',   '📱 Contactado'),
        ('en_diseno',    '🎨 En diseño'),
        ('en_produccion','🔨 En producción'),
        ('enviado',      '📦 Enviado'),
        ('entregado',    '✅ Entregado'),
    ], string='Estado', default='nuevo', tracking=True)

    notas_internas = fields.Text(string='Notas internas del equipo')

    # ── ACCIONES ────────────────────────────────────────
    def action_contactado(self):
        self.state = 'contactado'

    def action_en_diseno(self):
        self.state = 'en_diseno'

    def action_en_produccion(self):
        self.state = 'en_produccion'

    def action_enviado(self):
        self.state = 'enviado'

    def action_entregado(self):
        self.state = 'entregado'

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for rec in records:
            rec._enviar_notificacion_interna()
        return records

    def _enviar_notificacion_interna(self):
        """Notifica al equipo por email cuando llega una nueva solicitud."""
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
          <td style="color:#333"><strong>{self.nombre_nino}</strong></td></tr>
      <tr><td style="padding:6px 0;color:#666"><strong>Edad:</strong></td>
          <td style="color:#333">{self.edad or '—'}</td></tr>
      <tr><td style="padding:6px 0;color:#666"><strong>Tema favorito:</strong></td>
          <td style="color:#333">{self.tema_favorito or '—'}</td></tr>
      <tr><td style="padding:6px 0;color:#666"><strong>Colores:</strong></td>
          <td style="color:#333">{self.colores or '—'}</td></tr>
      <tr><td style="padding:6px 0;color:#666"><strong>Fecha requerida:</strong></td>
          <td style="color:#333">{self.fecha_requerida or 'Flexible'}</td></tr>
      <tr><td style="padding:6px 0;color:#666"><strong>Presupuesto:</strong></td>
          <td style="color:#333">{dict(self._fields['presupuesto'].selection).get(self.presupuesto, '—')}</td></tr>
    </table>

    <h3 style="color:#FF5C64;margin-top:20px;">💌 Historia</h3>
    <div style="background:white;padding:16px;border-radius:8px;border-left:4px solid #FF5C64;
                color:#333;line-height:1.6;">
      {self.historia or 'Sin historia proporcionada'}
    </div>

    <h3 style="color:#1E3A5F;margin-top:20px;">📱 Contacto</h3>
    <table style="width:100%;border-collapse:collapse;">
      <tr><td style="padding:6px 0;color:#666;width:40%"><strong>Nombre:</strong></td>
          <td style="color:#333">{self.nombre_contacto}</td></tr>
      <tr><td style="padding:6px 0;color:#666"><strong>WhatsApp:</strong></td>
          <td><a href="https://wa.me/{(self.telefono or '').replace(' ','').replace('+','')}"
                 style="color:#25D366;font-weight:bold;">{self.telefono or '—'}</a></td></tr>
      <tr><td style="padding:6px 0;color:#666"><strong>Email:</strong></td>
          <td><a href="mailto:{self.email or ''}" style="color:#5DA7E8;">{self.email or '—'}</a></td></tr>
      <tr><td style="padding:6px 0;color:#666"><strong>Nos conoció por:</strong></td>
          <td style="color:#333">{dict(self._fields['como_conocio'].selection).get(self.como_conocio, '—')}</td></tr>
    </table>

    <div style="margin-top:24px;text-align:center;">
      <a href="/odoo/gigis-personalizaciones"
         style="background:#FF5C64;color:white;padding:12px 28px;
                border-radius:50px;text-decoration:none;font-weight:bold;">
        Ver en Odoo →
      </a>
    </div>
  </div>
</div>
            """
            # Notificar a los seguidores del registro
            self.message_post(
                subject=subject,
                body=body,
                message_type='email',
                subtype_xmlid='mail.mt_comment',
            )
        except Exception as e:
            _logger.warning("No se pudo enviar notificación Gigi's Corner: %s", e)
