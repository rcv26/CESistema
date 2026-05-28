
from odoo import api,fields,models,_


class Provincia(models.Model):
    _name = 'ce_base.provincia'
    _description = "Provincias del Ecuador para el sistema de control electoral"
    _rec_name = 'nom_prov'

    cod_provincia = fields.Integer(string='Codigo', required=True)
    nom_prov = fields.Char(string='Nombre', required=True)

