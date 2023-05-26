# -*- coding: utf-8 -*-

import time
from datetime import datetime, timedelta
import dateutil.parser
from dateutil import relativedelta
import pytz
from odoo.addons import decimal_precision as dp
from odoo import api, models, fields, _


class ReportWorksheetWizard(models.TransientModel):
    _name = "report.worksheet.wizard"

    worksheet_id  = fields.Many2one('mrp.production', string='Worksheet')
    total_finished_products = fields.Float(string='Total Finished Product', digits=dp.get_precision('Product Unit of Measure'))
    lines_wizard  = fields.One2many('report.worksheet.wizard.line', 'ws_wiz_id', string='Worksheet Lines')


    @api.multi
    def _compute_get_lines(self):
        worksheet_id = self._context.get('active_id', False)
        if worksheet_id:
            inv_obj = self.env['mrp.production']
            worksheet = inv_obj.browse(worksheet_id)
            cr = self.env.cr
            sql = """SELECT pp.id, sum(sm.product_uom_qty)
                FROM stock_move sm
                LEFT JOIN mrp_production ws ON sm.production_id = ws.id
                LEFT JOIN product_product pp ON sm.product_id = pp.id
                WHERE ws.id = %s
                GROUP BY pp.id
                """
            cr.execute(sql, (worksheet.id,))
            record = cr.fetchall()
            line_ids = []
            for rec in record:
                line_ids.append((0,0,{
                        'product_id'     : rec[0],
                        'product_uom_qty': rec[1],
                    }))

            data = {
                'worksheet_id': worksheet.id,                
                'lines_wizard': line_ids,
            }
            self.write(data)

   
    @api.multi
    def action_print_report(self):
        # import pdb;pdb.set_trace()
        self._compute_get_lines()
        self.total_finished_products = sum(l.product_uom_qty for l in self.lines_wizard)
        report_action = self.env.ref(
            'vit_custom_report_worksheet.action_report_worksheet'
        ).report_action(self)
        report_action['close_on_report_download']=True

        return report_action

ReportWorksheetWizard()

class ReportWorksheetWizardLine(models.TransientModel):
    _name = "report.worksheet.wizard.line"

    product_id = fields.Many2one('product.product', 'Product')
    product_uom_qty = fields.Float(string='Total Quantity', digits=dp.get_precision('Product Unit of Measure'))
    ws_wiz_id  = fields.Many2one('report.worksheet.wizard', string='Inv Wizard')

ReportWorksheetWizardLine()
