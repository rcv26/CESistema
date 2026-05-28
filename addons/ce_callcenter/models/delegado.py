
from datetime import date, datetime, timedelta
from odoo import api,fields,models,_
from odoo.exceptions import MissingError
import re
from odoo.exceptions import ValidationError

class Delegado(models.Model):
    _inherit = 'ce_base.delegado'

    def _rec_count(self):
        rec = super(Delegado, self)._rec_count()
        for rec in self:
            rec.call_count = len(rec.llamada_ids)

    whatsapp = fields.Selection([
        ('si', 'SI'),
        ('no', 'NO')], string="Usa Whatsapp?",required = True, tracking=True)
    call_count = fields.Integer(compute='_rec_count', string='# LLamadas')

    llamada_ids = fields.One2many('ce_callcenter.llamada', 'delegado_id', string='Llamadas', tracking=True)

    
    def action_llamadas(self):
        action = self.env["ir.actions.actions"]._for_xml_id("ce_callcenter.action_llamada")
        action['domain'] = [('id','in',self.llamada_ids.ids)]
        action['context'] = {'default_delegado_id': self.id}
        return action
        
    
    
    def call_delegado(self):
        if self.call_count >= 5:
            raise ValidationError('Al delegado se lo llamo 5 veces sin tener exito')
        else:
            if self.estado =='i': 
                view = self.env.ref('ce_callcenter.view_call_center_wizard_form')
                return {'name': 'Realizar Llamada',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'target': 'new',
                    'res_model': 'ce_callcenter.call_delegado.wizard',
                    'view_id': view.id,
                    'views': [(view.id, 'form')],
                    'type': 'ir.actions.act_window',
                    'context': {'default_delegado_id': self.id,
                                'default_operadora': self.operadora,
                                'default_email': self.email,
                                'default_date_start' : datetime.now(),
                                }
                        }
            else:
                raise ValidationError('El delegado ya fue Revisado o Cancelado')


        # action = self.env["ir.actions.act_window"]._for_xml_id("ce_callcenter.action_call_center_wizard")
        # action['context'] = {
        #                     'delegado_id': [self.id],
        #                     'date_start' : 'datetime.now()',
        #                     }
        # return action