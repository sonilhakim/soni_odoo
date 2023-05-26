from odoo import api, fields, models, _
import time
from odoo.exceptions import UserError, Warning
import logging
from dateutil import relativedelta
_logger = logging.getLogger(__name__)

class asset(models.Model):
    _name = 'account.asset.asset'
    _inherit = 'account.asset.asset'

    value = fields.Float(string='Nilai Kotor', required=True, readonly=True, digits=0, states={'draft': [('readonly', False)]}, oldname='purchase_value', track_visibility='onchange')
    