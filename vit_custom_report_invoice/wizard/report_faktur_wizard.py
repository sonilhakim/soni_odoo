# -*- coding: utf-8 -*-

import time
from datetime import datetime, timedelta
import dateutil.parser
from dateutil import relativedelta
import pytz
from odoo.addons import decimal_precision as dp
from odoo import api, models, fields, _


class ReportFakturWizard(models.TransientModel):
    _name = "report.faktur.wizard"

    inv_id          = fields.Many2one('account.invoice', string='Invoice')
    dp_total        = fields.Monetary(string='DP', help="Total DP")
    currency_id     = fields.Many2one('res.currency', related='inv_id.currency_id', store=True, related_sudo=False, readonly=False)
    lines_wizard    = fields.One2many('report.faktur.wizard.line', 'inv_wiz_id', string='Inv Lines')


    @api.multi
    def _compute_get_lines(self):
        invoice_id = self._context.get('active_id', False)
        if invoice_id:
            inv_obj = self.env['account.invoice']
            invoice = inv_obj.browse(invoice_id)
            cr = self.env.cr
            sql = """SELECT stl.product_name, sum(il.quantity), il.uom_id, il.price_unit, sum(il.price_subtotal), sum(il.price_total)
                FROM account_invoice_line il
                LEFT JOIN account_invoice inv ON il.invoice_id = inv.id
                LEFT JOIN product_product pp ON il.product_id = pp.id
                LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
                LEFT JOIN vit_boq_po_garmen_line stl ON stl.product_id = pt.id
                LEFT JOIN vit_purchase_order_garmen po ON stl.po_id = po.id
                WHERE inv.id = %s AND po.po_payung_id IS NULL
                GROUP BY stl.id, il.uom_id, il.price_unit
                """
            cr.execute(sql, (invoice.id,))
            record = cr.fetchall()
            line_ids = []
            for rec in record:
                line_ids.append((0,0,{
                        'item_desc'     : rec[0],
                        'quantity'      : rec[1],
                        'uom_id'        : rec[2],
                        'price_unit'    : rec[3],
                        'price_subtotal': rec[4],
                        'price_total'   : rec[5]
                    }))

            data = {
                'inv_id'  : invoice.id,
                'dp_total': invoice.amount_total - invoice.residual,
                'lines_wizard': line_ids,
            }
            self.write(data)

   
    @api.multi
    def action_print_report(self):
        # import pdb;pdb.set_trace()
        self._compute_get_lines()
        report_action = self.env.ref(
            'vit_custom_report_invoice.account_report_faktur'
        ).report_action(self)
        report_action['close_on_report_download']=True

        return report_action

ReportFakturWizard()

class ReportFakturWizardLine(models.TransientModel):
    _name = "report.faktur.wizard.line"

    item_desc   = fields.Char(string='Item Description')
    quantity    = fields.Float(string='Quantity', digits=dp.get_precision('Product Unit of Measure'))
    uom_id      = fields.Many2one('uom.uom', string='Unit of Measure', index=True, oldname='uos_id')
    price_unit  = fields.Float(string='Unit Price', digits=dp.get_precision('Product Price'))
    price_subtotal = fields.Monetary(string='Amount (without Taxes)', help="Total amount without taxes")
    price_total = fields.Monetary(string='Amount (with Taxes)', help="Total amount with taxes")
    inv_wiz_id  = fields.Many2one('report.faktur.wizard', string='Inv Wizard')

    currency_id = fields.Many2one('res.currency', related='inv_wiz_id.inv_id.currency_id', store=True, related_sudo=False, readonly=False)
    
ReportFakturWizardLine()
