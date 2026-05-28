from odoo import api,fields,models,_

class Candidato(models.Model):
    _name = 'ce_base.candidato'
    _description = "Candidatos"
    _rec_name = 'nombres'

    nombres = fields.Char(string='Nombre', required=True)
    partido = fields.Char(string='Partido Politico', required=True)
    orden =  fields.Integer(string='Orden', required=True)
    dignidad_id = fields.Many2one('ce_base.dignidad')
