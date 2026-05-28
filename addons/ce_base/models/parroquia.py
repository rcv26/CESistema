from odoo import api,fields,models,_


class Parroquia(models.Model):
    _name = 'ce_base.parroquia'
    _description = "Parroquia de los cantones del Ecuador para el sistema de control electoral"
    _rec_name = 'nom_parroquia'

    cod_parroquia = fields.Integer(string='Codigo de Parroquia', required=True)
    nom_parroquia = fields.Char(string='Nombre de Parroquia', required=True)
    cod_canton = fields.Many2one('ce_base.canton', required=True)

