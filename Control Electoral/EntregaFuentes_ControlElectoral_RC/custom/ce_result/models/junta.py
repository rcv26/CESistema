from odoo import api, fields, models, _
from odoo.exceptions import MissingError


class Junta(models.Model):
    _inherit = 'ce_base.junta'

class Recinto(models.Model):
    _inherit = 'ce_base.recinto'