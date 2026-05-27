from odoo import api,fields,models,_


class Capacitacion(models.Model):
    _name = 'ce_capacitacion.capacitacion'
    _description = "Capacitaciones para el sistema de control electoral"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'nombre'

    def _rec_count(self):
        for rec in self:
            rec.cantidad = len(rec.delegados_ids)

    nombre = fields.Char(string='Nombre de la Capacitacion', required=True, tracking=True)
    fecha = fields.Date(string='Fecha', required=True, tracking=True)
    lugar = fields.Char(string='Lugar de la Capacitacion', required=True, tracking=True)
    capacitador_id = fields.Many2one('ce_capacitacion.capacitador', string="Capacitador",required=True, tracking=True)
    estado = fields.Boolean(string='Estado', default=True, tracking=True)
    delegados_ids = fields.Many2many('ce_base.delegado',string='Delegados', tracking=True)
    cantidad = fields.Integer(string='Cantidad de Capacitados', compute='_rec_count')