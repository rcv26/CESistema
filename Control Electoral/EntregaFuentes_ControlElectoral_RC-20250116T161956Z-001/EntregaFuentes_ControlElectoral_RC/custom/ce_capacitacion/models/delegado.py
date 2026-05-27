from odoo import api, fields, models, _


class Delegado(models.Model):
    _inherit = 'ce_base.delegado'
    capacitacion_ids = fields.Many2many('ce_capacitacion.capacitacion',string='Capacitaciones')

