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

class SaleOrderInvKas(models.Model):
    _inherit = "sale.order"

    cara_bayar  = fields.Selection([('cash', 'Cash'), ('debit', 'Debit Card'), ('credit', 'Credit Card')], string='Cara Bayar')
    # change = fields.Float('Kembalian', digits=dp.get_precision('Account'), help="")
    # total_item = fields.Integer('Total Item')
    # total_qty = fields.Float('Total Qty')
    discount_global_amount = fields.Float(string='Discount Global', digits=dp.get_precision('Discount'), default=0.0)

    # @api.onchange('order_line')
    # def total_onchanges(self):
    #     if self.order_line:
    #         self.total_item = len(self.order_line)

    #     for line in self.order_line:
    #         if line.product_uom_qty:
    #             self.total_qty = sum(l.product_uom_qty for l in self.order_line)

    @api.onchange('discount_global_persen','discount_global_val')
    def onchange_global_discount(self):
        for order in self:
            if order.discount_global_persen:
                order.discount_global_amount = order.amount_untaxed * (order.discount_global_persen/100)
            elif order.discount_global_val:
                order.discount_global_amount = order.discount_global_val

    # @api.multi
    # def action_invoice_create(self, grouped=False, final=False):
    #     res = super(SaleOrderInvKas, self).action_invoice_create()
    #     invoice = self.env['account.invoice'].browse(res)
    #     invoice.cara_bayar = self.cara_bayar

    #     if self.cara_bayar == 'cash':
    #         if self.discount_global_amount:
    #             invoice.discount_global_amount = self.discount_global_amount
    #         invoice.action_invoice_open()
    #         payment_id = self.env['account.payment']
    #         journal = self.env['account.journal'].search([('type','=','cash')], limit=1)
    #         payment_methods = journal.inbound_payment_method_ids
    #         payment_methods_list = payment_methods.ids

    #         payment_methode = self.env['account.payment.method'].search([('payment_type','=','inbound'),('id', 'in', payment_methods_list)])

    #         if invoice.state == 'open':
    #             # import pdb;pdb.set_trace()
    #             data = {
    #                     'journal_id': journal.id,
    #                     'payment_method_id': payment_methode.id,
    #                     'payment_date': datetime.now(),
    #                     'communication': invoice.number,
    #                     'invoice_ids': [(6, 0, invoice.ids)],
    #                     'payment_type': 'inbound',
    #                     'amount': abs(invoice.amount_total),
    #                     'currency_id': invoice.currency_id.id,
    #                     'partner_id': invoice.partner_id.id,
    #                     'partner_type': 'customer',
    #                     'multi': False,
    #                     'payment_difference_handling': 'reconcile',
    #                     }
    #             payment = payment_id.create(data)
    #             payment.post()

    #     return res


    # @api.multi
    # def print_struk(self):

    #     return self.env.ref('vit_sales_payment_kas.action_report_struk').report_action(self)
        