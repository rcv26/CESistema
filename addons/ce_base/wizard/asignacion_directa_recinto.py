from odoo import api,fields,models,_
from datetime import date, datetime, timedelta
from odoo.exceptions import ValidationError

class AsignacionDirectaRecintoWizard(models.TransientModel):
    _name = 'ce_base.asignacion_directa_recinto.wizard'
    _description = "Wizard para asignar recinto al coordinador "

    delegado_id = fields.Many2one('ce_base.delegado', string = 'Delegado', required=True)
    tipo_delegado = fields.Selection([
        ('djrv', 'DELEGADO JUNTA RECEPTORA DEL VOTO'),
        ('dcdr', 'DELEGADO COORDINADOR DE RECINTO'),
        ('dcda', 'DELEGADO A CDA'),
        ('djp', 'DELEGADO A JUNTA PROVINCIAL')], string='Tipo de Delegado', related = 'delegado_id.tipo_delegado')
    celular =  fields.Char(string='Celular', related = 'delegado_id.celular')
    cedula = fields.Char(string='Cedula', related = 'delegado_id.cedula')
    nombres= fields.Char(string='Nombres', related = 'delegado_id.nombres')
    operadora = fields.Selection([
        ('claro', 'Claro'),
        ('movistar', 'Movistar'),
        ('cnt', 'CNT'),
        ('tuenti', 'Tuenti')], string='Operadora Celular', related = 'delegado_id.operadora')
    email = fields.Char(string='e-mail' ,related = 'delegado_id.email')
    cod_recinto = fields.Many2one('ce_base.recinto', string = "Recinto", related = 'delegado_id.cod_recinto')
    cod_provincia = fields.Many2one('ce_base.provincia', string = "Provincia" , related = 'delegado_id.cod_provincia')
    cod_canton = fields.Many2one('ce_base.canton', string = "Canton", related = 'delegado_id.cod_canton')
    cod_parroquia = fields.Many2one('ce_base.parroquia', string = "Parroquia", related = 'delegado_id.cod_parroquia')
    cod_zona = fields.Many2one('ce_base.zona', string = "Zona", related = 'delegado_id.cod_zona')
    genero = fields.Selection([
        ('M', 'Masculino'),
        ('F', 'Femenino')], string='Genero', related = 'delegado_id.genero')
    numero_junta = fields.Integer(string='Junta',  related = 'delegado_id.numero_junta')
    coor_recinto_id = fields.Many2one('ce_base.recinto',string='Recitos que coordino', related = 'delegado_id.coor_recinto_id')
    nuevo_coor_recinto_id = fields.Many2one('ce_base.recinto',string='Recitos que coordino')

    @api.model
    def default_get(self, default_fields):
        result = super(AsignacionDirectaRecintoWizard, self).default_get(default_fields)
        if self._context.get('default_delegado_id') is not None:
            result['delegado_id'] = self._context.get('default_delegado_id')
        return result

    def asignar(self):
        if self.nuevo_coor_recinto_id :
            delegado = self.env['ce_base.delegado'].sudo().search([('id', '=', self.delegado_id.id)])
            delegado.tipo_ingreso = 's'
            # delegado.estado = 'i'
            delegado.coor_recinto_id = self.nuevo_coor_recinto_id
        else:
            raise ValidationError('Debe de seleccionar una junta')
