from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AccountPaymentNote(models.Model):
    _name = 'account.payment'
    _inherit = 'account.payment'

    note = fields.Text(string='Keterangan',)