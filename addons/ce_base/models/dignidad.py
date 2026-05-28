from odoo import api,fields,models,_

class Dignidad(models.Model):
    _name = 'ce_base.dignidad'
    _description = "Dignidad"
    _rec_name = 'nombre'

    nombre = fields.Char(string='Nombre de la Digniodad', required=True)
    nivel = fields.Selection([
        ('provincia', 'Provincia'),
        ('canton', 'Canton')], string='Nivel')
    cod_provincia = fields.Many2one('ce_base.provincia', string="Provincia")
    cod_canton = fields.Many2one('ce_base.canton', string="Canton",)
    estado = fields.Boolean(string='estado', default=True, required=True)
