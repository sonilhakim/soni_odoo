# -*- coding: utf-8 -*-

import time
from datetime import datetime, timedelta
import dateutil.parser
from dateutil import relativedelta
import pytz
from odoo import api, models, fields, _


class RekapMutasiStockWizard(models.TransientModel):
    _name = "rekap.mutasi.stock.wizard"

   
    location_id = fields.Many2one('stock.location', "Lokasi Gudang", required=True,)
    date_from   = fields.Date( string="Dari", default=lambda self: time.strftime("%Y-%m-%d"), help="")
    date_to     = fields.Date( string="Ke", default=lambda self: time.strftime("%Y-%m-%d"), help="")
    mutasi_lines    = fields.One2many('rincian.mutasi.stock.wizard', 'mutasi_id', string='Rincian')

    @api.model
    def _compute_mutasi_stock(self):
        # cr = self.env.cr
        cr1 = self.env.cr
        # sql = """SELECT pp.id
        #         FROM stock_move sm
        #         LEFT JOIN product_product pp ON sm.product_id = pp.id
        #         LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
        #         LEFT JOIN stock_picking sp ON sm.picking_id = sp.id
        #         LEFT JOIN stock_location sl ON sp.location_id = sl.id
        #         WHERE sp.state = 'done' AND sl.id = %s AND sp.date_done BETWEEN %s AND %s
        #         GROUP BY pp.id
        #         """
        # cr.execute(sql, (self.location_id.id,self.date_from,self.date_to,))
        # result = cr.fetchall()
        # for res in result:
            # product = self.env['product.product'].search([('id','=',res[0])])
        sqlr = """SELECT pp.id,
                (SELECT sum(smb.quantity_done)
                 FROM stock_move smb
                 LEFT JOIN stock_picking spb ON smb.picking_id = spb.id
                 LEFT JOIN stock_location slb ON spb.location_id = slb.id
                 LEFT JOIN product_product ppb ON smb.product_id = ppb.id
                 WHERE spb.state = 'done' AND slb.id = %s AND spb.date_done < %s AND ppb.id = pp.id
                 GROUP BY ppb.id
                ) as openingb,
                (SELECT sum(sma.quantity_done)
                 FROM stock_move sma
                 LEFT JOIN stock_picking spa ON sma.picking_id = spa.id
                 LEFT JOIN stock_location sla ON spa.location_dest_id = sla.id
                 LEFT JOIN product_product ppa ON sma.product_id = ppa.id
                 WHERE spa.state = 'done' AND sla.id = %s AND spa.date_done < %s AND ppa.id = pp.id
                 GROUP BY ppa.id
                ) as openinga,
                (SELECT sum(smi.quantity_done)
                 FROM stock_move smi
                 LEFT JOIN stock_picking spi ON smi.picking_id = spi.id
                 LEFT JOIN stock_location sli ON spi.location_dest_id = sli.id
                 LEFT JOIN product_product ppi ON smi.product_id = ppi.id
                 WHERE spi.state = 'done' AND sli.id = %s AND spi.date_done BETWEEN %s AND %s AND ppi.id = pp.id
                 GROUP BY ppi.id
                ) as masuk,
                (SELECT sum(smo.quantity_done)
                 FROM stock_move smo
                 LEFT JOIN stock_picking spo ON smo.picking_id = spo.id
                 LEFT JOIN stock_location slo ON spo.location_id = slo.id
                 LEFT JOIN product_product ppo ON smo.product_id = ppo.id
                 WHERE spo.state = 'done' AND slo.id = %s AND spo.date_done BETWEEN %s AND %s AND ppo.id = pp.id
                 GROUP BY ppo.id
                 ) as keluar
                FROM product_product pp
                LEFT JOIN stock_move sm ON sm.product_id = pp.id
                LEFT JOIN stock_picking sp ON sm.picking_id = sp.id
                WHERE sp.state = 'done' AND sp.date_done BETWEEN %s AND %s
                GROUP BY pp.id
            """
        cr1.execute(sqlr, (self.location_id.id,self.date_from,self.location_id.id,self.date_from,self.location_id.id,self.date_from,self.date_to,self.location_id.id,self.date_from,self.date_to,self.date_from,self.date_to))
        record = cr1.fetchall()
        mutasi_lines = []
        for rec in record:
            # import pdb;pdb.set_trace()
            product = self.env['product.product'].search([('id','=',rec[0])])
            if rec[1] == None:
                op1 = 0.0
            else:
                op1 = rec[1]
            if rec[2] == None:
                op2 = 0.0
            else:
                op2 = rec[2]
            if rec[3] == None:
                km = 0.0
            else:
                km = rec[3]
            if rec[4] == None:
                kk = 0.0
            else:
                kk = rec[4]
            mutasi_lines.append((0,0,{
                    'no_stock'   : product.default_code,
                    'des_stock'  : product.display_name,
                    'opening'    : op2 - op1,
                    'kts_masuk'  : km,
                    'kts_out'    : kk,
                    'balance'    : ((op2 - op1) + km) - kk,
                }))

        self.write({
                    'mutasi_lines': mutasi_lines,
                })
    
    @api.multi
    def action_print_report(self):
        self._compute_mutasi_stock()
        report_action = self.env.ref(
            'vit_report_rekap_inventory.action_mutasi_stock'
        ).report_action(self)
        report_action['close_on_report_download']=True

        return report_action


class RincianMutasiStockWizard(models.TransientModel):
    _name = "rincian.mutasi.stock.wizard"

   
    no_stock = fields.Char('No. Barang')
    des_stock = fields.Char('Deskripsi Barang')
    opening = fields.Float('Opening Balance')
    kts_masuk = fields.Float('Kts Masuk')
    kts_out = fields.Float('Kts Masuk')
    balance = fields.Float('Balance')
    mutasi_id = fields.Many2one('rekap.mutasi.stock.wizard', "Ringkasan Mutasi",)

