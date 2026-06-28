# -*- coding: utf-8 -*-
from odoo import models, fields, api


class GigisConfig(models.Model):
    _name = 'gigis.config'
    _description = "Gigi's Corner — Configuración"

    name = fields.Char(string='Nombre', default="Configuración")

    # ── Aviso por correo de las Solicitudes ────────────────────
    notif_activo = fields.Boolean(
        string='Enviar aviso por correo',
        default=True,
        help='Si está activo, cada solicitud del formulario "Personalizados" se envía por correo.',
    )
    notif_email = fields.Char(
        string='Correo para recibir solicitudes',
        help='A este correo llegará una copia de cada solicitud del formulario de Personalizados. '
             'Puedes poner varios separados por coma.',
    )

    @api.model
    def get_config(self):
        """Devuelve (creando si no existe) el registro único de configuración."""
        cfg = self.sudo().search([], limit=1)
        if not cfg:
            cfg = self.sudo().create({'name': "Configuración"})
        return cfg
