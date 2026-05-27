from odoo import api, fields, models, _
from odoo.exceptions import MissingError


class Junta(models.Model):
    _name = 'ce_base.junta'
    _description = "Juntas Receptoras del voto"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'combination'

    cod_provincia = fields.Many2one('ce_base.provincia', string="Provincia",required=True)
    cod_canton = fields.Many2one('ce_base.canton', string="Canton", required=True)
    cod_parroquia = fields.Many2one('ce_base.parroquia', string="Parroquia", required=True)
    cod_zona = fields.Many2one('ce_base.zona', string="Zona", required=True)
    cod_recinto = fields.Many2one('ce_base.recinto', string="Recinto", required=True)
    genero = fields.Selection([
        ('M', 'Masculino'),
        ('F', 'Femenino')], string='Genero', readonly=True)
    numero_junta = fields.Integer(string='Junta', required=True, readonly=True, group_operator='count')
    # pregunta a paul
    # reclutado = fields.Boolean(string='Reclutado', required=True, readonly=True)
    estado_junta = fields.Selection([
        ('a', 'Activa'),
        ('r', 'Reclutado'),
        ('c', 'Confirmado'),
        ('i', 'Inactiva')], string='Estado Junta', required=True)
    delegado_id = fields.Many2one('ce_base.delegado')
    tiene_delegado = fields.Boolean(string='Tiene Delegado', compute='_compute_tiene_delegado',store=True)
    cedula = fields.Char(string='Cedula', related='delegado_id.cedula')
    tipo_ingreso_delegado = fields.Selection([
        ('a', 'Automatico'),
        ('c', 'Contingencia'),
        ('s', 'Ingresado por Supervisor')],string='Tipo de Estado', related='delegado_id.tipo_ingreso')
    estado_delegado = fields.Selection([
        ('i', 'Ingresado'),
        ('r', 'Revisado'),
        ('c', 'Cancelado')],string='Estado Delegado', store=True, related='delegado_id.estado')
    tipo_delegado = fields.Selection([
        ('djrv', 'DELEGADO JUNTA RECEPTORA DEL VOTO'),
        ('dcdr', 'DELEGADO COORDINADOR DE RECINTO'),
        ('dcda', 'DELEGADO A CDA'),
        ('djp', 'DELEGADO A JUNTA PROVINCIAL')], string='Tipo de Delegado', related='delegado_id.tipo_delegado')
    distrito = fields.Char(string='Distrito')

    combination = fields.Char(string='Combination', compute='_compute_fields_combination')

    @api.depends('cod_recinto', 'genero','numero_junta')
    def _compute_fields_combination(self):
        for test in self:
            test.combination = str(test.cod_recinto.nom_recinto) + ' - ' + str(test.genero) + ' - ' + str(test.numero_junta)

    @api.depends('delegado_id')
    def _compute_tiene_delegado(self):
        for test in self:
            test.tiene_delegado = True if len(test.delegado_id) else False