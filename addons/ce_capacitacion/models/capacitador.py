from odoo import api,fields,models,_
from odoo.exceptions import MissingError
import re
from odoo.exceptions import ValidationError

class Capacitador(models.Model):
    _name = 'ce_capacitacion.capacitador'
    _description = "Capacitador para el sistema de control electoral"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'nombres'

    def _rec_count(self):
        # Junta = self.env['ce_base.Junta']
        for rec in self:
            rec.capacitacion_count = len(rec.capacitacion_ids)

    cedula = fields.Char(string='Cedula', required=True, tracking=True)
    nombres= fields.Char(string='Nombres', required=True, tracking=True)
    genero = fields.Selection([
        ('M', 'Masculino'),
        ('F', 'Femenino')], string='Genero', tracking=True)
    celular =  fields.Char(string='Celular', required = True, tracking=True)
    operadora = fields.Selection([
        ('claro', 'Claro'),
        ('movistar', 'Movistar'),
        ('cnt', 'CNT'),
        ('tuenti', 'Tuenti')], string='Operadora Celular', default = 'claro')
    email = fields.Char(string='e-mail', required = True, tracking=True)

    capacitacion_ids = fields.One2many('ce_capacitacion.capacitacion','capacitador_id',string='Capacitaciones', tracking=True)
    capacitacion_count = fields.Integer(compute='_rec_count', string='# Capacitaciones')

    def action_capacitacion(self):
        action = self.env["ir.actions.actions"]._for_xml_id("ce_capacitacion.action_capacitacion")
        action['domain'] = [('capacitador_id','=',self.id)]
        action['context'] = {'create':False,'edit':False}
        # action['context'] = {'default_patient_id': self.id, 'default_physician_id': self.primary_doctor.id}
        return action

    @api.onchange('cedula')
    def onchange_cedula(self):
        if self.cedula:
            datos = self.env['ce_base.pre_data'].sudo().search([('cedula', '=', self.cedula)])
            if datos:
                self.nombres = datos.nom_padron
                self.genero = datos.sex_padron

            #:
            # evaluar si son mayores de 18 osea los que no estan en el padron por que recien cumplieron


    @api.constrains('email')
    @api.onchange('email')
    def validate_mail(self):
        if self.email:
            match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.email)
            if match == None:
                raise ValidationError('E-mail invalido cargame las puertas')


    @api.constrains('celular')
    @api.onchange('celular')
    def validate_celular(self):
        if self.celular:
            match = re.match('^\d{10}$', self.celular)
            if match == None:
                raise ValidationError('Celular invalido')

    _sql_constraints = [ ('cedula','UNIQUE (cedula)','Capacitador ya existe'), ]