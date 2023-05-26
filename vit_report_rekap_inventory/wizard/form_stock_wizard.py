# -*- coding: utf-8 -*-

import time
from datetime import datetime, timedelta
import dateutil.parser
from dateutil import relativedelta
import pytz
from odoo import api, models, fields, _


class FormStockWizard(models.TransientModel):
    _name = "form.stock.wizard"

   
    style_id     = fields.Many2one( comodel_name="product.template",  string="Style",  help="")
    product_name = fields.Char( string="Product Description", compute='get_datas', store=True, help="")
    partner_id   = fields.Many2one( comodel_name="res.partner",  string="Buyer", compute='get_datas', store=True, help="")
    date         = fields.Date( string="Date", default=lambda self: time.strftime("%Y-%m-%d"), help="")
    
    
    @api.depends('style_id')
    def get_datas(self):
        for ra in self:
            if ra.style_id:
                sql = """SELECT rp.id, boq.product_name
                        FROM product_template pt
                        LEFT JOIN vit_boq_po_garmen_line boq ON boq.product_id = pt.id
                        LEFT JOIN vit_purchase_order_garmen po ON boq.po_id = po.id
                        LEFT JOIN res_partner rp ON po.partner_id = rp.id
                        WHERE pt.id = %s
                        """

                self.env.cr.execute(sql, (ra.style_id.id,))
                result = self.env.cr.fetchall()
                for res in result:
                    ra.partner_id = res[0]
                    ra.product_name = res[1]
        

    @api.multi
    def action_print_report(self):
        data = {
            'style_id': self.style_id.id,
        }
        report_action = self.env.ref(
            'vit_report_rekap_inventory.action_form_stock'
        ).report_action(self, data=data)
        report_action['close_on_report_download']=True

        return report_action



