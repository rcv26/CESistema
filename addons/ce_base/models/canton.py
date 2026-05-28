from odoo import api,fields,models,_


class Canton(models.Model):
    _name = 'ce_base.canton'
    _description = "Cantones del Ecuador para el sistema de control electoral"
    _rec_name = 'nom_canton'

    cod_canton = fields.Integer(string='Codigo del Canton', required=True)
    nom_canton = fields.Char(string='Nombre del Canton', required=True)
    cod_provincia = fields.Many2one('ce_base.provincia', required=True)