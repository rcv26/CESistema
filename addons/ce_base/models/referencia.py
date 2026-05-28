from odoo import api,fields,models,_
from odoo.exceptions import MissingError
import re
from odoo.exceptions import ValidationError


class Referencia(models.Model):
    _name = 'ce_base.referencia'
    _description = "Referencias o Referidos por"
    _rec_name = 'nombres'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    cedula = fields.Char(string='Cedula', required = True)
    nombres= fields.Char(string='Nombres', required = True)
    genero = fields.Selection([
        ('M', 'Masculino'),
        ('F', 'Femenino')], string='Genero', required = True)
    celular =  fields.Char(string='Celular', required = True)
    operadora = fields.Selection([
        ('claro', 'Claro'),
        ('movistar', 'Movistar'),
        ('cnt', 'CNT'),
        ('tuenti', 'Tuenti')], string='Operadora Celular', default = 'claro', required = True)
    email = fields.Char(string='e-mail', required = True)
    nivel = fields.Selection([
        ('1', 'Dirigente Provincial'),
        ('2', 'Dirigente Cantonal'),
        ('3', 'Dirigente Parroquial'),
        ('4', 'Dirigente')], string='Nivel', required = True)
    referido_id = fields.Many2one('ce_base.referencia')
    total_coordinadores = fields.Integer(string='Total Cordinadores de recinto')
    total_delegados = fields.Integer(string='Total Delegados JRV')
    distrito = fields.Selection([
        ('DISTRITO 1', 'DISTRITO 1'),
        ('DISTRITO 2', 'DISTRITO 2'),
        ('DISTRITO 3', 'DISTRITO 3'),
        ('DISTRITO RURAL', 'DISTRITO RURAL')], string='Distrito')
    estado = fields.Boolean(string='Estado', default=True)



    @api.onchange('cedula')
    def onchange_cedula(self):
        if self.cedula:
            datos = self.env['ce_base.pre_data'].sudo().search([('cedula', '=', self.cedula)])
            if datos:
                self.nombres = datos.nom_padron
                self.genero = datos.sex_padron

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


    _sql_constraints = [ ('cedula','UNIQUE (cedula)','Referido ya existe'), ]