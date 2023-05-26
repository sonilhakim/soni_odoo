from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.safe_eval import safe_eval

from odoo.addons import decimal_precision as dp

class HrContributionRegisterRef(models.Model):
    _name = 'hr.contribution.register'
    _inherit = 'hr.contribution.register'

    pendapat_id = fields.Many2one( "vit.pendapat","Pendapat",  help="")