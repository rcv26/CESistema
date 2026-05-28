
from odoo import api,fields,models,_
from odoo.exceptions import MissingError
import re
from odoo.exceptions import ValidationError, UserError

class Delegado(models.Model):
    _name = 'ce_base.delegado'
    _description = "Delegados ingresados al sistema"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'nombres'

    ASIGNACION_AUTOMATICA = False

    def _rec_count(self):
        # Junta = self.env['ce_base.Junta']
        for rec in self:
            rec.juntas_count = len(rec.juntas_ids)


    
    cedula = fields.Char(string='Cedula', required=True)
    nombres= fields.Char(string='Nombres', required=True)
    cod_provincia = fields.Many2one('ce_base.provincia', required=True, string = "Provincia")
    cod_canton = fields.Many2one('ce_base.canton', required=True , string = "Canton")
    cod_parroquia = fields.Many2one('ce_base.parroquia', required=True , string = "Parroquia")
    cod_zona = fields.Many2one('ce_base.zona', required=True , string = "Zona")
    cod_recinto = fields.Many2one('ce_base.recinto', required=True, string = "Recinto", tracking=True)
    genero = fields.Selection([
        ('M', 'Masculino'),
        ('F', 'Femenino')], string='Genero')
    numero_junta = fields.Integer(string='Junta', required = True, tracking=True) 
    celular =  fields.Char(string='Celular', required = True, tracking=True)
    operadora = fields.Selection([
        ('claro', 'Claro'),
        ('movistar', 'Movistar'),
        ('cnt', 'CNT'),
        ('tuenti', 'Tuenti')], string='Operadora Celular', default = 'claro')
    email = fields.Char(string='e-mail', required = True, tracking=True)
    tipo_delegado= fields.Selection([
        ('djrv', 'DELEGADO JUNTA RECEPTORA DEL VOTO'),
        ('dcdr', 'DELEGADO COORDINADOR DE RECINTO'),
        ('dcda', 'DELEGADO A CDA'),
        ('djp', 'DELEGADO A JUNTA PROVINCIAL')], string='Tipo de Delegado')
    referencia1 =fields.Many2one(comodel_name='ce_base.referencia', string='Referencia 1', domain=[('nivel','in',('1','2','3','4'))],required=True, tracking=True)
    referencia2 =fields.Many2one(comodel_name='ce_base.referencia', string='Referencia 2')
    referencia3 =fields.Many2one(comodel_name='ce_base.referencia', string='Referencia 3')
    referencia4 =fields.Many2one(comodel_name='ce_base.referencia', string='Referencia 4')

    tipo_ingreso = fields.Selection([
        ('a', 'Automatico'),
        ('c', 'Contingencia'),
        ('s', 'Ingresado por Supervisor')],string='Tipo de Ingreso')
    estado = fields.Selection([
        ('i', 'Ingresado'),
        ('r', 'Revisado'),
        ('c', 'Cancelado'),
        ('n', 'Numero Incorrecto')],string='Estado', tracking=True)
    juntas_ids = fields.One2many('ce_base.junta','delegado_id',string='Juntas')
    juntas_count = fields.Integer(compute='_rec_count', string='# Juntas')

    coor_recinto_id = fields.Many2one('ce_base.recinto',string='Recitos que coordino', tracking=True)

    def action_juntas(self):
        action = self.env["ir.actions.actions"]._for_xml_id("ce_base.action_junta")
        action['domain'] = [('delegado_id','=',self.id)]
        # action['context'] = {'default_patient_id': self.id, 'default_physician_id': self.primary_doctor.id}
        return action

    @api.onchange('cedula')
    def onchange_cedula(self):
        if self.cedula:
            datos = self.env['ce_base.pre_data'].sudo().search([('cedula', '=', self.cedula)])
            if datos:
                self.nombres = datos.nom_padron
                self.cod_provincia = datos.cod_provincia
                self.cod_canton = datos.cod_canton
                self.cod_parroquia = datos.cod_parroquia
                self.cod_zona = datos.cod_zona
                # self.cod_recinto = None if self.tipo_delegado == 'dcdr' else datos.cod_recinto
                self.cod_recinto = datos.cod_recinto
                self.genero = datos.sex_padron
                self.numero_junta = datos.junta
            #:
            # evaluar si son mayores de 18 osea los que no estan en el padron por que recien cumplieron

    @api.onchange('cod_recinto')
    def onchange_cod_recinto(self):
        if self.cod_recinto:
            recinto = self.env['ce_base.recinto'].sudo().search([('cod_recinto', '=', self.cod_recinto.id)])
            if recinto:
                self.cod_provincia = recinto.cod_provincia
                self.cod_canton = recinto.cod_canton
                self.cod_parroquia = recinto.cod_parroquia
                self.cod_zona = recinto.cod_zona
                self.cod_recinto = recinto.cod_recinto

            #:
            # evaluar si son mayores de 18 osea los que no estan en el padron por que recien cumplieron

    @api.constrains('email')
    @api.onchange('email')
    def validate_mail(self):
        if self.email:
            match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.email)
            if match == None:
                raise ValidationError('E-mail invalido')


    @api.constrains('celular')
    @api.onchange('celular')
    def validate_celular(self):
        if self.celular:
            match = re.match('^\d{10}$', self.celular)
            if match == None:
                raise ValidationError('Celular invalido')


    @api.onchange('referencia1')
    def onchange_referencia1(self):
        if self.referencia1:
            self.referencia2 = None
            self.referencia3 = None
            self.referencia4 = None
            if self.referencia1.referido_id:
                self.referencia2 = self.referencia1.referido_id
                if self.referencia2.referido_id:
                    self.referencia3 = self.referencia2.referido_id
                    if self.referencia3.referido_id:
                        self.referencia4 = self.referencia3.referido_id
                        # evaluar si son mayores de 18 osea los que no estan en el padron por que recien cumplieron
    @api.model
    def create(self, values):
        if values.get('tipo_delegado') == 'djrv':
            # deseas asignacion automatica
            if self.ASIGNACION_AUTOMATICA == False:
                # contingencia
                values['tipo_ingreso']='c'
                values['estado']='i'
                res = super(Delegado, self).create(values)
            else:
                datos = self.env['ce_base.junta'].sudo().search([   ('cod_provincia', '=', values.get('cod_provincia')),
                                                                        ('cod_canton', '=', values.get('cod_canton')),
                                                                        ('cod_parroquia', '=', values.get('cod_parroquia')),
                                                                        ('cod_zona', '=', values.get('cod_zona')),
                                                                        ('cod_recinto', '=', values.get('cod_recinto')),
                                                                        ('genero', '=', values.get('genero')),
                                                                        ('numero_junta', '=', values.get('numero_junta'))])
                # La junta tiene delegado
                if datos.delegado_id:
                    print('Tomada')
                    anterior = self.env['ce_base.junta'].sudo().search([   ('cod_provincia', '=', values.get('cod_provincia')),
                                                                        ('cod_canton', '=', values.get('cod_canton')),
                                                                        ('cod_parroquia', '=', values.get('cod_parroquia')),
                                                                        ('cod_zona', '=', values.get('cod_zona')),
                                                                        ('cod_recinto', '=', values.get('cod_recinto')),
                                                                        ('genero', '=', values.get('genero')),
                                                                        ('numero_junta', '=', int(values.get('numero_junta'))-1)])
                    # si la junta anterior tiene delegado
                    if anterior.delegado_id or not anterior.id:
                        siguiente = self.env['ce_base.junta'].sudo().search([   ('cod_provincia', '=', values.get('cod_provincia')),
                                                                        ('cod_canton', '=', values.get('cod_canton')),
                                                                        ('cod_parroquia', '=', values.get('cod_parroquia')),
                                                                        ('cod_zona', '=', values.get('cod_zona')),
                                                                        ('cod_recinto', '=', values.get('cod_recinto')),
                                                                        ('genero', '=', values.get('genero')),
                                                                        ('numero_junta', '=', int(values.get('numero_junta'))+1)])
                        # si la junta siguiente tiene delegado
                        if siguiente.delegado_id or not siguiente.id:
                            # contingencia
                            values['tipo_ingreso']='c'
                            values['estado']='i'
                            res = super(Delegado, self).create(values)

                        else:
                            values['tipo_ingreso']='a'
                            values['estado']='i'
                            res = super(Delegado, self).create(values)
                            junta_ids = self.env['ce_base.junta'].search([('id', '=', siguiente.id)])
                            for record in junta_ids:
                                record.write({
                                    'delegado_id': res.id,
                                    'estado_junta': 'a'
                                })
                    else:
                        # grabo con la junat anterior
                        values['tipo_ingreso']='a'
                        values['estado']='i'
                        res = super(Delegado, self).create(values)
                        junta_ids = self.env['ce_base.junta'].search([('id', '=', anterior.id)])
                        for record in junta_ids:
                            record.write({
                                'delegado_id': res.id,
                                'estado_junta': 'a'
                            })
                else:
                    values['tipo_ingreso']='a'
                    values['estado']='i'
                    res = super(Delegado, self).create(values)
                    junta_ids = self.env['ce_base.junta'].search([('id', '=', datos.id)])
                    for record in junta_ids:
                        record.write({
                            'delegado_id': res.id,
                            'estado_junta': 'a'
                        })  
        elif values.get('tipo_delegado') == 'dcdr':
            recinto = self.env['ce_base.recinto'].sudo().search([('cod_recinto', '=', values.get('cod_recinto'))])

            if len(recinto.dcdr_ids) == 0:
                values['tipo_ingreso']='a'
                values['estado']='i'
                values['coor_recinto_id'] = values.get('cod_recinto')
                res = super(Delegado, self).create(values)
            else:
                    values['tipo_ingreso']='c'
                    values['estado']='i'
                    res = super(Delegado, self).create(values)
        else:
            values['tipo_ingreso']='a'
            values['estado']='i'
            res = super(Delegado, self).create(values)

        return res

    def write(self, vals):
        # if self.estado == 'r':
        #     raise ValidationError("No se puede modificar delegado ya revisado")
        # else:
        return super().write(vals)


    def asignacion_directa(self):
            # if self.estado in ('i','c','n'): 
            # delegado = self.env['ce_base.delegado'].search([('id', '=', self.id)])
            # for rec in delegado.llamada_ids:
            #     if rec.pregunta1 == 'no' and rec.pregunta2 == 'no' :
            #         raise ValidationError('El delegado contesto NO en las preguntas de validacion - Consultar con al Administrador')
            view = self.env.ref('ce_base.view_asignacion_directa_wizard_form')
            return {'name': 'Asignacion Directa de Junta ',
                'view_type': 'form',
                'view_mode': 'form',
                'target': 'new',
                'res_model': 'ce_base.asignacion_directa.wizard',
                'view_id': view.id,
                'views': [(view.id, 'form')],
                'type': 'ir.actions.act_window',
                'context': {'default_delegado_id': self.id}
                    }
            # else:
            #     raise ValidationError('El delegado ya fue Revisado')

    def asignacion_directa_coordinador(self):
        # if self.estado in ('i','c','n'):
        # delegado = self.env['ce_base.delegado'].search([('id', '=', self.id)])
        # for rec in delegado.llamada_ids:
        #     if rec.pregunta1 == 'no' and rec.pregunta2 == 'no' :
        #         raise ValidationError('El Coordinador contesto NO en las preguntas de validacion - Consultar con al Administrador')
        view = self.env.ref('ce_base.view_asignacion_directa_recinto_wizard_form')
        return {'name': 'Asignacion Directa de Recinto para coordinar ',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'res_model': 'ce_base.asignacion_directa_recinto.wizard',
            'view_id': view.id,
            'views': [(view.id, 'form')],
            'type': 'ir.actions.act_window',
            'context': {'default_delegado_id': self.id}
                }
        # else:
        #     raise ValidationError('El coordinador ya fue Revisado')


    _sql_constraints = [ ('cedula','UNIQUE (cedula)','Persona ya ingresada como delegada'), ]