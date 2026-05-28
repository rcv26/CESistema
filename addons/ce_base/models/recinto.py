from odoo import api,fields,models,_


class Recinto(models.Model):
    _name = 'ce_base.recinto'
    _description = "Recintos Electorales"
    _rec_name= 'nom_recinto'


    def _rec_count(self):
        Juntas = self.env['ce_base.junta']
        for rec in self:
            rec.coordinador_count = len(rec.dcdr_ids)
            rec.juntas_count = len(rec.juntas_ids)
            rec.juntas_masculino_count = Juntas.search_count([('cod_recinto','=',rec.id),('genero','=','M'),('delegado_id','!=',False)])
            rec.juntas_femenino_count = Juntas.search_count([('cod_recinto','=',rec.id),('genero','=','F'),('delegado_id','!=',False)])
            rec.juntas_porc_asignacion = ((int(rec.juntas_masculino_count) + int(rec.juntas_femenino_count))/ int(rec.juntas_count))*100

    cod_provincia = fields.Integer(string='')
    nom_provincia = fields.Char(string='Provincia')
    cod_canton = fields.Integer(string='')
    nom_canton = fields.Char(string='Canton')
    cod_parroquia = fields.Integer(string='')
    nom_parroquia = fields.Char(string='Parroquia')
    cod_zona = fields.Integer(string='')
    nom_zona = fields.Char(string='Zona')
    cod_recinto = fields.Integer(string='')
    nom_recinto = fields.Char(string='Recinto')
    dir_recinto = fields.Char(string='')
    telefono = fields.Char(string='')
    zona_utm = fields.Char(string='')
    coord_x = fields.Char(string='')
    coord_y = fields.Char(string='')
    long = fields.Char(string='')
    lat = fields.Char(string='')
    u_r = fields.Char(string='')
    jun_fem = fields.Integer(string='J-Fem')
    jun_mas = fields.Integer(string='J-Masc')
    num_junr = fields.Integer(string='Juntas')
    jun_inif = fields.Integer(string='')
    jun_finf = fields.Integer(string='')
    jun_inim = fields.Integer(string='')
    jun_finm = fields.Integer(string='')
    num_electores = fields.Integer(string='')


    # campos computados o mas
    # coordinador_ids = fields.One2many('ce_base.delegado','cod_recinto',string='Coordinadores', domain=[('tipo_delegado','=','dcdr'),('tipo_ingreso','!=','c')])
    dcdr_ids =  fields.One2many('ce_base.delegado','coor_recinto_id',string='Delegado Cordinador Recinto')
    coordinador_count = fields.Integer(compute='_rec_count', string='# Coordinador')
    juntas_ids = fields.One2many('ce_base.junta','cod_recinto',string='Juntas')
    juntas_count = fields.Integer(compute='_rec_count', string='Juntas', store = True)
    juntas_masculino_count = fields.Integer(compute='_rec_count', string='J-Masc Asig')
    juntas_femenino_count = fields.Integer(compute='_rec_count', string='J-Fem Asig')
    juntas_porc_asignacion = fields.Integer(compute='_rec_count', string='% Asig')
    cedula = fields.Char(string='Cedula', related='dcdr_ids.cedula')
    tipo_ingreso_coordinador = fields.Selection([
        ('a', 'Automatico'),
        ('c', 'Contingencia'),
        ('s', 'Ingresado por Supervisor')], string='Tipo de Estado', related='dcdr_ids.tipo_ingreso')
    estado_coordinador = fields.Selection([
        ('i', 'Ingresado'),
        ('r', 'Revisado'),
        ('c', 'Cancelado')], string='Estado Coordinador', store = True, related='dcdr_ids.estado')
    distrito = fields.Char(string='Distrito')


    def action_coordinador(self):
        action = self.env["ir.actions.actions"]._for_xml_id("ce_base.action_coordinadorreciento")
        action['domain'] = [('id','in',self.dcdr_ids.ids)]
        action['context'] = {'create':False,'edit':False}
        return action

    def action_calculo_masculino(self):
        pass

    def action_calculo_femenino(self):
        pass

    def action_mostrar_juntas(self):
        action = self.env["ir.actions.actions"]._for_xml_id("ce_base.action_junta")
        action['domain'] = [('cod_recinto','=',self.id)]
        action['context'] = {'create':False,'edit':False}
        return action