from odoo import api,fields,models,_
from datetime import date, datetime, timedelta
from odoo.exceptions import ValidationError

class CallDelegadoWizard(models.TransientModel):
    _name = 'ce_callcenter.call_delegado.wizard'
    _description = "Call Delegado Wizard"

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
        ('tuenti', 'Tuenti')], string='Operadora Celular')
    email = fields.Char(string='e-mail')
    cod_recinto = fields.Many2one('ce_base.recinto', string = "Recinto", related = 'delegado_id.cod_recinto')
    cod_provincia = fields.Many2one('ce_base.provincia', string = "Provincia" , related = 'delegado_id.cod_provincia')
    cod_canton = fields.Many2one('ce_base.canton', string = "Canton", related = 'delegado_id.cod_canton')
    cod_parroquia = fields.Many2one('ce_base.parroquia', string = "Parroquia", related = 'delegado_id.cod_parroquia')
    cod_zona = fields.Many2one('ce_base.zona', string = "Zona", related = 'delegado_id.cod_zona')
    call_count = fields.Integer(string="# Intento", related = 'delegado_id.call_count')
    genero = fields.Selection([
        ('M', 'Masculino'),
        ('F', 'Femenino')], string='Genero', related = 'delegado_id.genero')
    numero_junta = fields.Integer(string='Junta',  related = 'delegado_id.numero_junta')
    whatsapp = fields.Selection([
        ('si', 'SI'),
        ('no', 'NO')], string="Usa Whatsapp?")
    date_start = fields.Datetime(string='Inicio')
    date_end = fields.Datetime(string='Fin')
    call_duration = fields.Float('Consultation Time', readonly=True, copy=False)
    call_duration_timer = fields.Float('Consultation Timer', readonly=True, default="0.1", copy=False)

    pregunta1 = fields.Selection([
        ('si', 'SI'),
        ('no', 'NO'),
        ('no tengo idea', 'No tengo idea')],string='Usted tiene conocimiento que es delegado?')
    pregunta2 = fields.Selection([
        ('si', 'SI'),
        ('no', 'NO')],string='Usted esta de acuerdo?')


    @api.model
    def default_get(self, default_fields):
        result = super(CallDelegadoWizard, self).default_get(default_fields)
        if self._context.get('default_delegado_id') is not None:
            result['delegado_id'] = self._context.get('default_delegado_id')
        if self._context.get('default_operadora') is not None:
            result['operadora'] = self._context.get('default_operadora')
        if self._context.get('default_email') is not None:
            result['email'] = self._context.get('default_email')
        if self._context.get('default_date_start') is not None:
            result['date_start'] = self._context.get('default_date_start')
        return result

    def contesto(self):
        if self.pregunta1 and self.pregunta2 and self.whatsapp:
            delegado = self.env['ce_base.delegado'].sudo().search([('id', '=', self.delegado_id.id)])
            delegado.operadora = self.operadora
            delegado.email = self.email
            delegado.whatsapp = self.whatsapp
            if self.pregunta2 == 'no':
                delegado.estado = 'c'
            else:
                delegado.estado = 'r'
            llamada_data = {
                'delegado_id': self.delegado_id.id,
                'fecha_ini': self.date_start,
                'fecha_fin': self.date_start,
                'intento': int(delegado.call_count) + 1,
                'estado' : True,
                'pregunta1' : self.pregunta1,
                'pregunta2' : self.pregunta2,
            }
            llamada = self.env['ce_callcenter.llamada'].create(llamada_data)
        else:
            raise ValidationError('Verifique que esten llenos todos los campos de seleccion Pregunta 1,2 y WhatsApp')


    def no_contesto(self):
        delegado = self.env['ce_base.delegado'].sudo().search([('id', '=', self.delegado_id.id)])
        
        if int(delegado.call_count) + 1 >= 5:
            delegado.estado = 'c'
            junta_ids = self.env['ce_base.junta'].search([('id', '=', delegado.juntas_ids.id)])
            for record in junta_ids:
                record.write({
                    'delegado_id': None,
                    'estado_junta': 'i'
                })
        llamada_data = {
            'delegado_id': self.delegado_id.id,
            'fecha_ini': self.date_start,
            'fecha_fin': datetime.now(),
            'intento': int(delegado.call_count) + 1,
            'estado': False,
        }
        llamada = self.env['ce_callcenter.llamada'].create(llamada_data)
        return {'type':'ir.actions.act_window_close'}

    def num_incorrecto(self):
        delegado = self.env['ce_base.delegado'].sudo().search([('id', '=', self.delegado_id.id)])

        if int(delegado.call_count) + 1 >= 5:
            delegado.estado = 'c'
            junta_ids = self.env['ce_base.junta'].search([('id', '=', delegado.juntas_ids.id)])
            for record in junta_ids:
                record.write({
                    'delegado_id': None,
                    'estado_junta': 'i'
                })
        else:
            delegado.estado = 'n'
            junta_ids = self.env['ce_base.junta'].search([('id', '=', delegado.juntas_ids.id)])
            for record in junta_ids:
                record.write({
                    'delegado_id': None,
                    'estado_junta': 'i'
                })

        llamada_data = {
            'delegado_id': self.delegado_id.id,
            'fecha_ini': self.date_start,
            'fecha_fin': datetime.now(),
            'intento': int(delegado.call_count) + 1,
            'estado': False,
        }
        llamada = self.env['ce_callcenter.llamada'].create(llamada_data)
        return {'type': 'ir.actions.act_window_close'}
