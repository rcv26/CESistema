from odoo import api, fields, models, _
from odoo.exceptions import MissingError, ValidationError


class JuntaDignidad(models.Model):
    _name = 'ce_result.junta_dignidad'
    _description = "Dignidades de cada junta"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order_by =  ['cod_provincia','cod_canton','cod_parroquia','cod_zona','genero','numero_junta']
    _rec_name = 'combination'

    junta_id = fields.Many2one("ce_base.junta")
    cod_provincia = fields.Many2one('ce_base.provincia', string="Provincia", required=True, readonly = True)
    cod_canton = fields.Many2one('ce_base.canton', string="Canton", required=True, readonly = True)
    cod_parroquia = fields.Many2one('ce_base.parroquia', string="Parroquia", required=True, readonly = True)
    cod_zona = fields.Many2one('ce_base.zona', string="Zona", required=True, readonly = True)
    cod_recinto = fields.Many2one('ce_base.recinto', string="Recinto", required=True, readonly = True)
    genero = fields.Selection([
         ('M', 'Masculino'),
         ('F', 'Femenino')], string='Genero', readonly=True)
    numero_junta = fields.Integer(string='Junta', required=True, readonly=True, group_operator='count')
    dignidad_id = fields.Many2one("ce_base.dignidad", readonly = True)
    total_sufragantes = fields.Integer(string="Total de sufragantes", default = 0)
    votos_blancos= fields.Integer(string="Blancos", default = 0)
    votos_nulos= fields.Integer(string="Nulos", default = 0)
    codigo_cne = fields.Integer(string="CNE", default = 0)
    state = fields.Selection([
        ('a', 'Activo'),
        ('r', 'Registrada'),
        ('d', 'Digitada'),
        ('c', 'Control Calidad'),
        ('i', 'Inconsistencia'),
        ('t', 'Terminada')], string="Estado",tracking=True)

    candidato_ids = fields.One2many('ce_result.junta_dignidad_candidato','junta_dignidad_id',string = 'Votos de Candidatos',tracking=True)
    file = fields.Binary(string="PDF",tracking=True) 
    file_name = fields.Char("File Name")
    tiene_foto = fields.Boolean(string="Tiene Foto", default = False) 
    tarea = fields.Char(string="Tarea", default = '1')
    combination = fields.Char(string='Combination', compute='_compute_fields_combination')
    tiene_inconsistencia = fields.Boolean(string="Acta con Novedad", default = False,tracking=True) 
    observacion = fields.Text(string="Observacion",tracking=True)



    @api.depends('dignidad_id','cod_provincia','cod_canton','cod_parroquia','cod_zona', 'genero','numero_junta')
    def _compute_fields_combination(self):
        for test in self:
            test.combination = str(test.cod_provincia.nom_prov) + ' - ' +  str(test.cod_canton.nom_canton) + ' - ' +  str(test.cod_parroquia.nom_parroquia) + ' - ' + str(test.cod_zona.nom_zona) + ' - ' + str(test.genero) + ' - ' + str(test.numero_junta)
    
    
    
    
    # inconsistencia = fields.Boolean()
    # foto = fields.Binary() 
    # attachment_ids =  fields.Many2many('ir.attachment', 'class_ir_attachments_rel', 'class_id', 'attachment_id', 'Attachments')



    # @api.model
    # def default_get(self, default_fields):
    #     result = super(JuntaDignidad, self).default_get(default_fields)
    #     if self._context.get('default_tarea') is not None:
    #         result['tarea'] = self._context.get('default_tarea')
    #     return result

    @api.constrains('file')
    def _check_file(self):
        if str(self.file_name.split(".")[1]) != 'pdf' :
            raise ValidationError("Cannot upload file different from .pdf file")

    def write(self, vals):
        if self.env.context.get('tarea') == 'd':
            vals['state'] = 'd'
        elif self.env.context.get('tarea') == 'c':
            
            total = int(self.total_sufragantes)
            blancos = int(self.votos_blancos)
            nulos = int(self.votos_nulos)
            votos = 0
            map_candidatos  = self.mapped('candidato_ids')
            for rec in map_candidatos:
                votos += int(rec['voto'])
            uno_porciento = total * 0.01
            votos = votos + blancos + nulos
            result = total - votos
            if abs(result) > uno_porciento:
                vals['state'] = 'i'
            else:
                vals['state'] = 'c'
        elif self.env.context.get('tarea') == 'f':
            if vals['file'] != None:
                vals['tiene_foto'] = True
        return super().write(vals)


    def action_registrar(self):
        for rec in self:
            rec.state = 'r'



    def action_sin_novedad(self):
        for rec in self:
            rec.state = 'c'
            rec.tiene_inconsistencia = False
            rec.observacion = ''



    def action_validar(self):
        total = int(self.total_sufragantes)
        blancos = int(self.votos_blancos)
        nulos = int(self.votos_nulos)
        votos = 0
        map_candidatos  = self.mapped('candidato_ids')
        for rec in map_candidatos:
            votos += rec.get['votos']
        uno_porciento = total * 0.01
        votos = votos + blancos + nulos
        result = total - votos
        if abs(result) > uno_porciento:
            self.state = 'i'


