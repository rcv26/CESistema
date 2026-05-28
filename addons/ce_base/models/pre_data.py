from odoo import fields, models, api

class Pre_data(models.Model):
    _name = 'ce_base.pre_data'
    _description = 'Datos externos'
    cod_provincia = fields.Integer(string='')
    nom_provincia = fields.Char(string='')
    cod_canton = fields.Integer(string='')
    nom_canton = fields.Char(string='')
    cod_parroquia = fields.Integer(string='')
    nom_parroquia = fields.Char(string='')
    cod_zona = fields.Integer(string='')
    nom_zona = fields.Char(string='')
    cod_recinto = fields.Integer(string='')
    nom_recinto = fields.Char(string='')
    sex_padron = fields.Char(string='') 
    junta = fields.Integer(string='') 
    ced_padron = fields.Char(string='')
    dig_padron = fields.Char(string='')
    cedula = fields.Char(string='')
    nom_padron = fields.Char(string='')
    sec_padron = fields.Integer(string='') 
    status = fields.Integer(string='') 
    num_cert_vot = fields.Char(string='')