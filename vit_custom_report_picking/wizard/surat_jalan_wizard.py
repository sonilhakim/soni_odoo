# -*- coding: utf-8 -*-

import time
from datetime import datetime, timedelta
import dateutil.parser
from dateutil import relativedelta
import pytz
from odoo.addons import decimal_precision as dp
from odoo import api, models, fields, _


class SuratJalanWizard(models.TransientModel):
    _name = "surat.jalan.wizard"

    picking_id         = fields.Many2one(comodel_name="stock.picking", string="Picking")
    sj_move_wizard_ids = fields.One2many('sj.move.wizard','sj_wizard_id', 'Surat Jalan Move')
    
    @api.multi
    def _compute_get_move(self):
        picking_id = self._context.get('active_id', False)
        if picking_id:
            pick_obj = self.env['stock.picking']
            pick = pick_obj.browse(picking_id)
            sql = """
                SELECT pt.name, stl.product_name, uom.id, sum(sm.quantity_done)
                FROM stock_move sm
                LEFT JOIN stock_picking sp ON sm.picking_id = sp.id
                LEFT JOIN product_product pp ON sm.product_id = pp.id
                LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
                LEFT JOIN vit_boq_po_garmen_line stl ON stl.product_id = pt.id
                LEFT JOIN vit_purchase_order_garmen po ON sp.po_id = po.id
                LEFT JOIN uom_uom uom ON sm.product_uom = uom.id
                WHERE sp.id = %s AND stl.po_id = po.id
                GROUP BY pt.id, stl.product_name, uom.id
                """
            self.env.cr.execute(sql, (pick.id,))
            record = self.env.cr.fetchall()
            move_ids = []
            desc = ""
            for rec in record:
                if not rec[1]:
                    desc = ""
                else :
                    desc = rec[1]
                move_ids.append((0,0,{
                        'item_description'  : rec[0],
                        'faktur_item_description'  : desc,
                        'quantity_done'     : rec[3],
                        'product_uom'       : rec[2],
                    }))

            self.write({
                'picking_id'          : pick.id,
                'sj_move_wizard_ids'  : move_ids,
            })
            
    @api.multi
    def action_print_report(self):
        self._compute_get_move()
        report_action = self.env.ref(
            'vit_custom_report_delivery_slip.surat_jalan_style'
        ).report_action(self)

        report_action['close_on_report_download']=True

        return report_action

SuratJalanWizard()

class SJMoveWizard(models.TransientModel):
    _name = "sj.move.wizard"

    quantity_done       = fields.Float('Quantity Done', digits=dp.get_precision('Product Unit of Measure'))
    product_uom         = fields.Many2one('uom.uom', 'Unit of Measure')
    item_description    = fields.Char( string="Item Description")
    faktur_item_description    = fields.Char( string="Faktur Item Description")
    sj_wizard_id        = fields.Many2one('surat.jalan.wizard', string='Surat Jalan Wizard')
    
SJMoveWizard()
