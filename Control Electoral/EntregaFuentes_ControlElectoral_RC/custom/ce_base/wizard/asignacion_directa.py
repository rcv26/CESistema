from odoo import api,fields,models,_
from datetime import date, datetime, timedelta
from odoo.exceptions import ValidationError

class AsignacionDirectaWizard(models.TransientModel):
    _name = 'ce_base.asignacion_directa.wizard'
    _description = "Wizard para asignar junta "

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
    nueva_junta = fields.Many2one('ce_base.junta', string = "Junta")

    @api.onchange('genero')
    def _get_juntas(self):
        for rec in self:
            # pedido por paul salazar el dia 1 de febrero del 2023 y aun no ha probado nada .!!! cargamelaspuerta!!!!!
            # return {'domain':{'nueva_junta':[('delegado_id', '=', False), ('genero','=',rec.genero)]}}
            return {'domain':{'nueva_junta':[('delegado_id', '=', False)]}}




    @api.model
    def default_get(self, default_fields):
        result = super(AsignacionDirectaWizard, self).default_get(default_fields)
        if self._context.get('default_delegado_id') is not None:
            result['delegado_id'] = self._context.get('default_delegado_id')
        return result

    def asignar(self):
        if self.nueva_junta :
            delegado = self.env['ce_base.delegado'].sudo().search([('id', '=', self.delegado_id.id)])
            delegado.cod_provincia = self.nueva_junta.cod_provincia
            delegado.cod_canton = self.nueva_junta.cod_canton
            delegado.cod_parroquia = self.nueva_junta.cod_parroquia
            delegado.cod_zona = self.nueva_junta.cod_zona
            delegado.cod_recinto = self.nueva_junta.cod_recinto
            delegado.numero_junta = self.nueva_junta.numero_junta
            delegado.tipo_ingreso = 's'
            # delegado.estado = 'i'
            delegado.juntas_ids = None
            junta_ids = self.env['ce_base.junta'].search([('id', '=', self.nueva_junta.id)])
            for record in junta_ids:
                record.write({
                                'delegado_id': delegado.id,
                                'estado_junta': 'a'
                            })
        else:
            raise ValidationError('Debe de seleccionar una junta')




    # def contesto(self):
    #     if self.pregunta1 and self.pregunta2 and self.whatsapp:
    #         delegado = self.env['ce_base.delegado'].sudo().search([('id', '=', self.delegado_id.id)])
    #         delegado.operadora = self.operadora
    #         delegado.email = self.email
    #         delegado.whatsapp = self.whatsapp
    #         if self.pregunta2 == 'no':
    #             delegado.estado = 'c'
    #         else:
    #             delegado.estado = 'r'
    #         llamada_data = {
    #             'delegado_id': self.delegado_id.id,
    #             'fecha_ini': self.date_start,
    #             'fecha_fin': self.date_start,
    #             'intento': int(delegado.call_count) + 1,
    #             'estado' : True,
    #             'pregunta1' : self.pregunta1,
    #             'pregunta2' : self.pregunta2,
    #         }
    #         llamada = self.env['ce_callcenter.llamada'].create(llamada_data)
    #     else:
    #         raise ValidationError('Verifique que esten llenos todos los campos de seleccion Pregunta 1,2 y WhatsApp')


    # def no_contesto(self):
    #     delegado = self.env['ce_base.delegado'].sudo().search([('id', '=', self.delegado_id.id)])
         
    #     if int(delegado.call_count) + 1 >= 5:
    #         delegado.estado = 'c'
                    
    #     llamada_data = {
    #         'delegado_id': self.delegado_id.id,
    #         'fecha_ini': self.date_start,
    #         'fecha_fin': datetime.now(),
    #         'intento': int(delegado.call_count) + 1,
    #         'estado': False,
    #     }
    #     llamada = self.env['ce_callcenter.llamada'].create(llamada_data)
    #     return {'type':'ir.actions.act_window_close'}

    # def num_incorrecto(self):
        # delegado = self.env['ce_base.delegado'].sudo().search([('id', '=', self.delegado_id.id)])

        # if int(delegado.call_count) + 1 >= 5:
        #     delegado.estado = 'c'
        # else:
        #     delegado.estado = 'n'

        # llamada_data = {
        #     'delegado_id': self.delegado_id.id,
        #     'fecha_ini': self.date_start,
        #     'fecha_fin': datetime.now(),
        #     'intento': int(delegado.call_count) + 1,
        #     'estado': False,
        # }
        # llamada = self.env['ce_callcenter.llamada'].create(llamada_data)
        # return {'type': 'ir.actions.act_window_close'}
