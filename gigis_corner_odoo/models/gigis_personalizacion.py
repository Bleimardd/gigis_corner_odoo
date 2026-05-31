# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.http import request


class GigisPersonalizacion(models.Model):
    """
    Modelo para capturar las solicitudes de lámparas personalizadas
    desde el formulario web de Gigi's Corner.
    Cada registro llega al CRM automáticamente.
    """
    _name = 'gigis.personalizacion'
    _description = "Gigi's Corner - Solicitud de Personalización"
    _order = 'create_date desc'
    _rec_name = 'nombre_nino'

    # ── DATOS DEL NIÑO ──
    nombre_nino = fields.Char(
        string='Nombre del niño/a',
        required=True,
    )
    edad = fields.Char(
        string='Edad',
    )
    tema_favorito = fields.Char(
        string='Tema favorito',
    )
    colores = fields.Char(
        string='Colores preferidos',
    )
    historia = fields.Text(
        string='Historia detrás del diseño',
        help='El campo más importante: la historia personal del niño.',
    )

    # ── DATOS DE CONTACTO ──
    nombre_contacto = fields.Char(
        string='Nombre del papá/mamá',
        required=True,
    )
    telefono = fields.Char(
        string='WhatsApp / Teléfono',
    )
    email = fields.Char(
        string='Correo electrónico',
    )

    # ── DETALLES DEL PEDIDO ──
    fecha_requerida = fields.Date(
        string='Fecha requerida',
    )
    presupuesto = fields.Selection(
        selection=[
            ('500-800', '$500 – $800 MXN'),
            ('800-1200', '$800 – $1,200 MXN'),
            ('1200-2000', '$1,200 – $2,000 MXN'),
            ('2000+', '$2,000+ MXN'),
            ('consulta', 'Quiero asesoría'),
        ],
        string='Presupuesto',
    )
    como_conocio = fields.Selection(
        selection=[
            ('instagram', 'Instagram'),
            ('facebook', 'Facebook'),
            ('tiktok', 'TikTok'),
            ('recomendacion', 'Recomendación'),
            ('google', 'Google'),
            ('whatsapp', 'WhatsApp'),
            ('otro', 'Otro'),
        ],
        string='¿Cómo nos conoció?',
    )

    # ── ESTADO ──
    state = fields.Selection(
        selection=[
            ('nuevo', '🆕 Nuevo'),
            ('contactado', '📱 Contactado'),
            ('en_diseno', '🎨 En diseño'),
            ('en_produccion', '🔨 En producción'),
            ('enviado', '📦 Enviado'),
            ('entregado', '✅ Entregado'),
        ],
        string='Estado',
        default='nuevo',
    )
    crm_lead_id = fields.Many2one(
        'crm.lead',
        string='Oportunidad CRM',
        readonly=True,
    )
    notas_internas = fields.Text(
        string='Notas internas del equipo',
    )

    @api.model_create_multi
    def create(self, vals_list):
        """Al crear una solicitud, crea automáticamente un lead en CRM."""
        records = super().create(vals_list)
        for rec in records:
            rec._crear_crm_lead()
        return records

    def _crear_crm_lead(self):
        """Crea un lead en CRM con la información de la solicitud."""
        if not self.env['ir.model'].search([('model', '=', 'crm.lead')]):
            return

        description = f"""
🌟 NUEVA SOLICITUD DE LÁMPARA PERSONALIZADA

👶 Niño/a: {self.nombre_nino or 'No especificado'}
🎂 Edad: {self.edad or 'No especificada'}
🎨 Tema favorito: {self.tema_favorito or 'No especificado'}
🎨 Colores: {self.colores or 'No especificados'}
📅 Fecha requerida: {self.fecha_requerida or 'Flexible'}
💰 Presupuesto: {dict(self._fields['presupuesto'].selection).get(self.presupuesto, 'No especificado')}

💌 HISTORIA:
{self.historia or 'Sin historia especificada'}

📱 CONTACTO:
{self.nombre_contacto}
Tel: {self.telefono or 'No proporcionado'}
Email: {self.email or 'No proporcionado'}

📣 Nos conoció por: {dict(self._fields['como_conocio'].selection).get(self.como_conocio, 'No especificado')}
        """

        lead_vals = {
            'name': f"💡 Lámpara para {self.nombre_nino} – {self.nombre_contacto}",
            'contact_name': self.nombre_contacto,
            'phone': self.telefono,
            'email_from': self.email,
            'description': description,
            'tag_ids': [],
        }

        # Buscar etapa de personalización
        stage = self.env['crm.stage'].search(
            [('name', 'ilike', 'Personalización')], limit=1
        )
        if stage:
            lead_vals['stage_id'] = stage.id

        lead = self.env['crm.lead'].create(lead_vals)
        self.crm_lead_id = lead.id

        # Enviar notificación interna
        self.message_post(
            body=f"✅ Lead creado en CRM: <a href='/web#id={lead.id}&model=crm.lead'>Ver oportunidad</a>",
            message_type='comment',
            subtype_xmlid='mail.mt_note',
        )
