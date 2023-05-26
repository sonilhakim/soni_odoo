# -*- coding: utf-8 -*-

import time
from datetime import datetime, timedelta
import dateutil.parser
from dateutil import relativedelta
import pytz
from odoo import api, models, fields, _


class StickerKartonWizard(models.TransientModel):
    _name = "sticker.karton.wizard"

    package_id              = fields.Many2one(comodel_name="stock.quant.package", string="Package")
    partner_id              = fields.Many2one(comodel_name="res.partner",  string="Buyer",)
    lokasi_id               = fields.Many2one('vit.lokasi_karyawan', string='Lokasi')
    sticker_karyawan_ids    = fields.One2many('karton.karyawan.wizard','sticker_karton_id', 'Karton Karyawan')
    sticker_report_ids      = fields.One2many('karton.report.wizard','sticker_karton_id', 'Karton Karyawan')

    @api.multi
    def _compute_get_list(self):
        package_id = self._context.get('active_id', False)
        if package_id:
            pack_obj = self.env['stock.quant.package']
            pack = pack_obj.browse(package_id)
            sql = """
                SELECT rp.id, lk.id, pack.id
                FROM stock_quant_package pack
                LEFT JOIN stock_picking sp ON pack.picking_id = sp.id
                LEFT JOIN vit_purchase_order_garmen po ON sp.po_id = po.id
                LEFT JOIN res_partner rp ON po.partner_id = rp.id
                LEFT JOIN vit_lokasi_karyawan lk ON sp.lokasi_id = lk.id
                WHERE pack.id = %s
                """
            self.env.cr.execute(sql, (pack.id,))
            record = self.env.cr.fetchall()
            for rec in record:
                sqlk = """
                    SELECT lot.karyawan, lot.nik, lot.nama_bordir, lot.lot, lot.jabatan_id, lot.divisi_id
                    FROM stock_quant sq
                    LEFT JOIN stock_quant_package pack ON sq.package_id = pack.id
                    LEFT JOIN stock_production_lot lot ON sq.lot_id = lot.id
                    WHERE pack.id = %s
                    GROUP BY lot.karyawan, lot.nik, lot.nama_bordir, lot.lot, lot.jabatan_id, lot.divisi_id
                    """
                self.env.cr.execute(sqlk, (pack.id,))
                result = self.env.cr.fetchall()
                karyawan_ids = []
                i = 1
                for res in result:
                    if res[3]:
                        lot = str(res[3])
                    else:
                        lot = 0
                    sqls = """
                        SELECT pt.id, sz.id, count(sq.id)
                        FROM stock_production_lot lot
                        LEFT JOIN product_attribute_value sz ON lot.size_id = sz.id
                        LEFT JOIN product_product pp ON lot.product_id = pp.id
                        LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
                        LEFT JOIN stock_quant sq ON sq.lot_id = lot.id
                        LEFT JOIN stock_quant_package pack ON sq.package_id = pack.id
                        WHERE pack.id = %s AND lot.karyawan = %s AND lot.nik = %s AND lot.nama_bordir = %s AND lot.lot = %s AND lot.jabatan_id = %s AND lot.divisi_id = %s
                        GROUP BY pt.id, sz.id
                        """
                    self.env.cr.execute(sqls, (pack.id, res[0], res[1], res[2], lot, res[4], res[5]))
                    result1 = self.env.cr.fetchall()
                    style_ids = []
                    for res1 in result1:
                        style_ids.append((0,0,{
                            'style_id'          : res1[0],
                            'size_id'           : res1[1],
                            'qty'               : str(res1[2]),
                        }))
                    karyawan_ids.append((0,0,{
                            'nomor'             : i,
                            'karyawan'          : res[0],
                            'nik'               : res[1],
                            'nama_bordir'       : res[2],
                            'lot'               : str(res[3]),
                            'jabatan_id'        : res[4],
                            'divisi_id'         : res[5],
                            'sticker_style_ids' : style_ids,
                        }))
                    i += 1

                self.write({
                    'partner_id'            : rec[0],
                    'lokasi_id'             : rec[1],
                    'package_id'            : rec[2],
                    'sticker_karyawan_ids'  : karyawan_ids,
                })

    @api.multi
    def compute_report(self):
        self._compute_get_list()
        report_ids = []
        dat_nik = []
        for ky in self.sticker_karyawan_ids:
            # dat_size = []
            for st in ky.sticker_style_ids:
                if ky.nomor not in dat_nik:
                    dat_nik.append(ky.nomor)
                    nik = ky.nik
                    nomor = ky.nomor
                    karyawan = ky.karyawan
                    nama_bordir = ky.nama_bordir
                    lot = ky.lot
                    jabatan_id = ky.jabatan_id.id
                    divisi_id = ky.divisi_id.id
                else:
                    nik = ''
                    nomor = ''
                    karyawan = ''
                    nama_bordir = ''
                    lot = ''
                    jabatan_id = ''
                    divisi_id = ''

                # if st.size_id.id not in dat_size:
                # dat_size.append(st.size_id.id)
                style_id = st.style_id.id
                size_id = st.size_id.id
                qty = st.qty
                # else:
                #     style_id = ''
                #     size_id = ''
                #     qty = ''

                report_ids.append((0,0,{
                    'nomor'             : nomor,
                    'karyawan'          : karyawan,
                    'nik'               : nik,
                    'nama_bordir'       : nama_bordir,
                    'lot'               : lot,
                    'style_id'          : style_id,
                    'size_id'           : size_id,
                    'qty'               : qty,
                    'jabatan_id'        : jabatan_id,
                    'divisi_id'         : divisi_id,
                }))
        self.write({'sticker_report_ids'  : report_ids})
            
    @api.multi
    def action_print_report(self):
        self.compute_report()
        report_action = self.env.ref(
            'vit_sticker_polybag.report_sticker_karton'
        ).report_action(self)

        report_action['close_on_report_download']=True

        return report_action

StickerKartonWizard()

class KartonKaryawanWizard(models.TransientModel):
    _name = "karton.karyawan.wizard"

    nomor               = fields.Char( string="No",)
    karyawan            = fields.Char( string="Karyawan",)
    nik                 = fields.Char( string="NIK")
    nama_bordir         = fields.Char( string="Nama Bordir")
    lot                 = fields.Char( string="Lot")
    jabatan_id          = fields.Many2one( "vit.jabatan_karyawan",string="Jabatan")
    divisi_id           = fields.Many2one( "vit.divisi_karyawan",string="Divisi")
    sticker_karton_id   = fields.Many2one('sticker.karton.wizard', string='Karton Wizard')
    sticker_style_ids   = fields.One2many('karton.style.wizard','sticker_karyawan_id', 'Karton Style')
    
KartonKaryawanWizard()

class KartonStyleWizard(models.TransientModel):
    _name = "karton.style.wizard"

    style_id            = fields.Many2one('product.template', string='Style')
    size_id             = fields.Many2one( "product.attribute.value",string="Size")
    qty                 = fields.Char( string="Qty", )
    sticker_karyawan_id = fields.Many2one('sticker.karyawan.wizard', string='Sticker Karyawan')
    
KartonStyleWizard()

class KartonReportWizard(models.TransientModel):
    _name = "karton.report.wizard"

    nomor               = fields.Char( string="No",)
    karyawan            = fields.Char( string="Karyawan",)
    nik                 = fields.Char( string="NIK")
    nama_bordir         = fields.Char( string="Nama Bordir")
    lot                 = fields.Char( string="Lot")
    style_id            = fields.Many2one('product.template', string='Style')
    size_id             = fields.Many2one( "product.attribute.value",string="Size")
    jabatan_id          = fields.Many2one( "vit.jabatan_karyawan",string="Jabatan")
    divisi_id           = fields.Many2one( "vit.divisi_karyawan",string="Divisi")
    qty                 = fields.Char( string="Qty", )
    sticker_karton_id   = fields.Many2one('sticker.karton.wizard', string='Karton Wizard')

KartonReportWizard()
