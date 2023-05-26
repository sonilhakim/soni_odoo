# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import time
from datetime import datetime
from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError


class SaleInvPaymentKas(models.TransientModel):
    _name = "sale.inv.payment.kas"
    _description = "Sales Payment Invoice Kas"

    
    @api.model
    def _default_total_harga(self):
        sale_order = self.env['sale.order'].browse(self._context.get('active_ids', []))
        total_harga = sale_order.amount_total
        return total_harga


    amount_total = fields.Float('Total Harga', digits=dp.get_precision('Account'), default=_default_total_harga, help="")
    amount_kas = fields.Float('Kas', digits=dp.get_precision('Account'), help="")
    change = fields.Float('Kembalian', digits=dp.get_precision('Account'), compute='get_change', store= True, help="")
    
    @api.depends('amount_kas')
    def get_change(self):
        if self.amount_kas:
            self.change = self.amount_kas - self.amount_total

    
    @api.multi
    def create_invoices(self):
        sale_order = self.env['sale.order'].browse(self._context.get('active_ids', []))
        sale_order.change = self.change
        sale_order.action_invoice_create()

        invoice = self.env['account.invoice'].search([('id', 'in', sale_order.invoice_ids.ids)])
        invoice.write({            
            'total_item' : len(invoice.invoice_line_ids),
            'total_qty' : sum(l.quantity for l in invoice.invoice_line_ids),
            'change' : self.change,
            'tunai' : True,
            'discount_global_amount' : sale_order.discount_global_amount
            })

        invoice.action_invoice_open()
        payment_id = self.env['account.payment']
        journal = self.env['account.journal'].search([('type','=','cash')], limit=1)
        payment_methods = journal.inbound_payment_method_ids
        payment_methods_list = payment_methods.ids

        payment_methode = self.env['account.payment.method'].search([('payment_type','=','inbound'),('id', 'in', payment_methods_list)])

        if invoice.state == 'open':
            # import pdb;pdb.set_trace()
            data = {
                    'journal_id': journal.id,
                    'payment_method_id': payment_methode.id,
                    'payment_date': datetime.now(),
                    'communication': invoice.number,
                    'invoice_ids': [(6, 0, invoice.ids)],
                    'payment_type': 'inbound',
                    'amount': abs(invoice.amount_total),
                    'currency_id': invoice.currency_id.id,
                    'partner_id': invoice.partner_id.id,
                    'partner_type': 'customer',
                    'multi': False,
                    'payment_difference_handling': 'reconcile',
                    }
            payment = payment_id.create(data)
            payment.post()

        report_action = self.env.ref('vit_sales_payment_kas.action_report_struk').report_action(invoice)

        # return {'type': 'ir.actions.act_window_close'}
        report_action['close_on_report_download']=True

        return report_action