# -*- coding: utf-8 -*-

import time
from datetime import datetime, timedelta
import dateutil.parser
from dateutil import relativedelta
import pytz
from odoo import api, models, fields, _


class ListStickerPolybagWizard(models.TransientModel):
    _name = "list.sticker.polybag.wizard"

    list_polybag = fields.One2many('list.sticker.polybag','list_wizard_id', 'List Polybag')

    @api.multi
    def _compute_get_list(self):
        context = dict(self._context or {})
        active_ids = context.get('active_ids', []) or []
        lot_ids = tuple(active_ids)
        # lots = self.env["stock.production.lot"].search([('id','in',lot_ids),('is_complete','=',True)])
        cr = self.env.cr
        sql = """
            SELECT ph.id, rp.id, dk.id, l1.id, l2.id, l3.id
            FROM stock_production_lot lot
            LEFT JOIN vit_pengukuran_header ph ON lot.project_id = ph.id
            LEFT JOIN res_partner rp ON ph.partner_id = rp.id
            LEFT JOIN vit_pengukuran_karyawan pk ON lot.pengukuran_karyawan = pk.id
            LEFT JOIN vit_divisi_karyawan dk ON pk.divisi_id = dk.id
            LEFT JOIN vit_lokasi_karyawan l1 ON pk.lokasi_id = l1.id
            LEFT JOIN vit_lokasi_karyawan l2 ON pk.lokasi2_id = l2.id
            LEFT JOIN vit_lokasi_karyawan l3 ON pk.lokasi3_id = l3.id
            WHERE lot.id IN %s
            GROUP BY ph.id, rp.id, dk.id, l1.id, l2.id, l3.id
            """
        cr.execute(sql, (lot_ids,))
        record = cr.fetchall()
        crl = self.env.cr
        for rec in record:
            sqll = """
                SELECT lot.nik, lot.karyawan, st.id, sz.id, count(lot.id)
                FROM stock_production_lot lot
                LEFT JOIN vit_pengukuran_header ph ON lot.project_id = ph.id
                LEFT JOIN res_partner rp ON ph.partner_id = rp.id
                LEFT JOIN vit_pengukuran_karyawan pk ON lot.pengukuran_karyawan = pk.id
                LEFT JOIN vit_divisi_karyawan dk ON pk.divisi_id = dk.id
                LEFT JOIN vit_lokasi_karyawan l1 ON pk.lokasi_id = l1.id
                LEFT JOIN vit_lokasi_karyawan l2 ON pk.lokasi2_id = l2.id
                LEFT JOIN vit_lokasi_karyawan l3 ON pk.lokasi3_id = l3.id
                LEFT JOIN vit_boq_po_garmen_line st ON lot.style_id = st.id
                LEFT JOIN product_attribute_value sz ON lot.size_id = sz.id
                WHERE lot.id IN %s AND ph.id = %s AND rp.id = %s AND dk.id = %s AND l1.id = %s AND l2.id = %s AND l3.id = %s
                GROUP BY lot.nik, lot.karyawan, st.id, sz.id
                """
            crl.execute(sqll, (lot_ids, rec[0], rec[1], rec[2], rec[3], rec[4], rec[5]))
            result = crl.fetchall()
            line_ids = []
            for res in result:
                line_ids.append((0,0,{
                        'nik'       : res[0],
                        'karyawan'  : res[1],
                        'style_id'  : res[2],
                        'size_id'   : res[3],
                        'qty'       : res[4],
                    }))

            data = {
                'pengukuran_header_id'  : rec[0],
                'partner_id'            : rec[1],
                'divisi_id'             : rec[2],
                'lokasi_id'             : rec[3],
                'lokasi2_id'            : rec[4],
                'lokasi3_id'            : rec[5],
                'line_ids'              : line_ids,
                'list_wizard_id'        : self.id,
            }
            self.list_polybag.create(data)

    @api.multi
    def action_print_report(self):
        # context = dict(self._context or {})
        # active_ids = context.get('active_ids', []) or []
        # lot_ids = tuple(active_ids)
        # data = {
        #     'lot_ids': lot_ids,
        # }
        # sql = """
        #     SELECT ph.id
        #     FROM stock_production_lot lot
        #     LEFT JOIN vit_pengukuran_header ph ON lot.project_id = ph.id
        #     WHERE lot.is_complete is True AND lot.id IN %s
        #     GROUP BY ph.id
        #     """
        # self.env.cr.execute(sql, (lot_ids,))
        # records = self.env.cr.fetchall()
        # ph_ids = [r[0] for r in records]
        # polybags = self.env['list.sticker.polybag'].sudo().search([('pengukuran_header_id','in',ph_ids)])
        # sqld = "delete from list_sticker_polybag where pengukuran_header_id in %s"
        # self.env.cr.execute(sqld, (tuple(ph_ids),))
        self._compute_get_list()
        report_action = self.env.ref(
            'vit_sticker_polybag.list_sticker_polybag_report'
        ).report_action(self)

        report_action['close_on_report_download']=True

        return report_action

ListStickerPolybagWizard()

class ListStickerPolybag(models.TransientModel):
    _name = "list.sticker.polybag"
    _description = "list.sticker.polybag"

    pengukuran_header_id    = fields.Many2one(comodel_name="vit.pengukuran.header",  string="Project",)
    partner_id              = fields.Many2one( comodel_name="res.partner", string="Buyer")
    divisi_id               = fields.Many2one( comodel_name="vit.divisi_karyawan",  string="Divisi")
    lokasi_id               = fields.Many2one( comodel_name='vit.lokasi_karyawan',string="Lokasi1")
    lokasi2_id              = fields.Many2one( comodel_name='vit.lokasi_karyawan',string="Lokasi2")
    lokasi3_id              = fields.Many2one( comodel_name='vit.lokasi_karyawan',string="Lokasi3")
    line_ids                = fields.One2many('list.sticker.polybag.line', 'list_id',string="List Line")
    list_wizard_id          = fields.Many2one('list.sticker.polybag.wizard', string='List Wizard')
    
ListStickerPolybag()


class ListStickerPolybagLine(models.TransientModel):
    _name = "list.sticker.polybag.line"
    _description = "list.sticker.polybag.line"

    style_id    = fields.Many2one('vit.boq_po_garmen_line', string='Style')
    karyawan    = fields.Char( string="Karyawan")
    nik         = fields.Char( string="NIK")
    size_id     = fields.Many2one('product.attribute.value', string='Size')
    qty         = fields.Integer( string="Qty")
    list_id     = fields.Many2one('list.sticker.polybag', string='List')

ListStickerPolybagLine()