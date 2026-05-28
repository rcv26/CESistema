from odoo import api,fields,models,_


class Zona(models.Model):
    _name = 'ce_base.zona'
    _description = "Zonas del Ecuador para el sistema de control electoral"
    _rec_name = 'nom_zona'

    cod_zona = fields.Integer(string='Codigo de la zona', required=True)
    nom_zona = fields.Char(string='Nombre de la zona', required=True)
    cod_parroquia = fields.Many2one('ce_base.parroquia', required=True)
    cod_zona_cne = fields.Integer(string='Codigo de la zona del cne')


