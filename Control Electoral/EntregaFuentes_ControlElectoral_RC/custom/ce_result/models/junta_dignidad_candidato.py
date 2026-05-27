from odoo import api, fields, models, _
from odoo.exceptions import MissingError


class JuntaDignidadCandidato(models.Model):
    _name = 'ce_result.junta_dignidad_candidato' 
    _description = "Candidatos de cada junta"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    junta_dignidad_id = fields.Many2one("ce_result.junta_dignidad")
    dignidad_id = fields.Many2one("ce_base.dignidad", string="Dignidad")
    cod_provincia = fields.Many2one('ce_base.provincia', string="Provincia")
    cod_canton = fields.Many2one('ce_base.canton', string="Canton")
    cod_parroquia = fields.Many2one('ce_base.parroquia', string="Parroquia")
    cod_zona = fields.Many2one('ce_base.zona', string="Zona")
    cod_recinto = fields.Many2one('ce_base.recinto', string="Recinto")
    candidato_id = fields.Many2one("ce_base.candidato")
    voto = fields.Integer(string="Votos", default = 0, tracking = True, group_operator='sum')


