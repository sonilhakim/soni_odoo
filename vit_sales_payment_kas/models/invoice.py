from odoo import models, fields, api, _
from odoo.exceptions import UserError
import time
from datetime import datetime
import sys
import math
from odoo.tools import float_utils, float_compare
from odoo.addons import decimal_precision as dp
import logging
_logger = logging.getLogger(__name__)

class AcountInvoiceKas(models.Model):
    _inherit = "account.invoice"

    change = fields.Float('Kembalian', digits=dp.get_precision('Account'), help="")
    total_item = fields.Integer('Total Item')
    total_qty = fields.Float('Total Qty')
    tunai = fields.Boolean('Tunai')
    discount_global_amount = fields.Float(string='Discount Global', digits=dp.get_precision('Discount'), default=0.0)
    # cara_bayar  = fields.Selection([('cash', 'Cash'), ('debit', 'Debit Card'), ('credit', 'Credit Card')], string='Cara Pembayaran')

    @api.onchange('discount_global_persen','discount_global_val')
    def onchange_global_discount(self):
        for order in self:
            if order.discount_global_persen:
                order.discount_global_amount = order.amount_untaxed * (order.discount_global_persen/100)
            elif order.discount_global_val:
                order.discount_global_amount = order.discount_global_val

    @api.multi
    def print_struk(self):

        return self.env.ref('vit_sales_payment_kas.action_report_struk').report_action(self)