from odoo import api, fields, models, _
import time
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

class AccountInvoiceKB(models.Model):
    _name = "account.invoice"
    _inherit = "account.invoice"

    btb_number = fields.Char('BTB')

    @api.model
    def create(self, vals):
        res = super(AccountInvoiceKB, self).create(vals)
        # import pdb;pdb.set_trace()
        bill = self.env['account.invoice'].search([('id','=',res.id)])
        if res.type == 'in_invoice':
            if res.origin:
                origin = [x.strip() for x in res.origin.split(',')]
                btbs = self.env['stock.picking'].search([('bill_number', '=', False), ('origin', 'in', origin), ('state','=','done')])
                if btbs:                    
                    res.btb_number = ', '.join(btbs.mapped('name'))
                    for btb in btbs:
                        btb.bill_number = bill
        return res
