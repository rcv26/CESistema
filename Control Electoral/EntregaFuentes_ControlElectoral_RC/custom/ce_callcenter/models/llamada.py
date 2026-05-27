from datetime import date, datetime, timedelta
from odoo import api,fields,models,_
from odoo.exceptions import MissingError
import re
from odoo.exceptions import ValidationError

class Llamada(models.Model):
    _name = 'ce_callcenter.llamada'
    _description = "LLamadas al delegado"
    _order_by =  "intento"

    delegado_id = fields.Many2one('ce_base.delegado', string = 'Delegado', required=True)

    fecha_ini = fields.Datetime(string="Inicio de llamada", tracking=True) 
    fecha_fin = fields.Datetime(string="Fin de llamada", tracking=True)
    intento = fields.Integer(string="Intento", tracking=True, group_operator='count')
    estado = fields.Boolean(string="Estado", default=False) 

    pregunta1 = fields.Selection([
        ('si', 'SI'),
        ('no', 'NO'),
        ('no tengo idea', 'No tengo idea')],string='Usted tiene conocimiento que es delegado?', tracking=True)
    pregunta2 = fields.Selection([
        ('si', 'SI'),
        ('no', 'NO')],string='Usted esta de acuerdo?', tracking=True)


