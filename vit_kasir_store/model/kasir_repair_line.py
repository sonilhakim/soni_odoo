#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, ValidationError

class KasirRepairLine(models.Model):

    _name = "vit.kasir_repair_line"
    _description = "vit.kasir_repair_line"

    lot_id_target   = fields.Many2one('stock.production.lot', string='Lots/Serial Numbers Target')
    karyawan_target = fields.Char( string="Nama Target",)
    nik_target      = fields.Char( string="NIK Target",)
    bordir_target   = fields.Char(string="Nama Bordir Target",)
    size_id_target  = fields.Many2one('product.attribute.value', string='Size Target',)
    style_id_target = fields.Many2one('vit.boq_po_garmen_line', string='Style Target',)
    pengukuran_karyawan_target = fields.Many2one('vit.pengukuran_karyawan', 'Pengukuran Target',)
    data_pengukuran_id_target = fields.Many2one('vit.data_pengukuran', string='Data Pengukuran Target',)
    polybag_target = fields.Char(string="Polybag Target",)
    divisi_target   = fields.Many2one( comodel_name="vit.divisi_karyawan", string="Divisi", )
    lokasi_target   = fields.Many2one( comodel_name='vit.lokasi_karyawan', string="Lokasi", )
    jabatan_target  = fields.Many2one("vit.jabatan_karyawan", "Jabatan", )
    location_id_target = fields.Many2one('stock.location', 'Last Location', )
    lot_target      = fields.Integer( string="LOT Target")
    
    is_swap         = fields.Boolean('Is Swap', default=False)
    store_id        = fields.Many2one('vit.kasir_store', string='Kasir Store')
    po_id           = fields.Many2one('vit.purchase_order_garmen', related='lot_id_target.po_id', string='No. OR', store=True)
    # state           = fields.Selection(string='Status', related='store_id.state', store=True)
    # unvalidate      = fields.Boolean('Unvalidate', default=False)

    location_id_sumber = fields.Many2one('stock.location', 'Last Location', )
    divisi_sumber   = fields.Many2one( comodel_name="vit.divisi_karyawan", string="Divisi", )
    lokasi_sumber   = fields.Many2one( comodel_name='vit.lokasi_karyawan', string="Lokasi", )
    jabatan_sumber  = fields.Many2one("vit.jabatan_karyawan", "Jabatan", )
    lot_id_sumber   = fields.Many2one('stock.production.lot', string='Lots/Serial Numbers Sumber')
    karyawan_sumber = fields.Char( string="Nama Sumber", )
    nik_sumber      = fields.Char( string="NIK Sumber", )
    bordir_sumber   = fields.Char(string="Nama Bordir Sumber", )
    size_id_sumber  = fields.Many2one('product.attribute.value', string='Size Sumber', )
    style_id_sumber = fields.Many2one('vit.boq_po_garmen_line', string='Style Sumber',)
    pengukuran_karyawan_sumber = fields.Many2one('vit.pengukuran_karyawan', 'Pengukuran Sumber', )
    data_pengukuran_id_sumber = fields.Many2one('vit.data_pengukuran', string='Data Pengukuran Sumber', )
    polybag_sumber     = fields.Char(string="Polybag Sumber", )
    lot_sumber      = fields.Integer( string="LOT Sumber")
    is_not_same      = fields.Boolean('Is_Not_Same', default=False)

    
    def check_data_double(self, lot_ids):
        lots = str(tuple(lot_ids.ids)).replace(",)",")")
        sql = "select ks.id from vit_kasir_repair_line ks left join stock_production_lot lot on ks.lot_id_target = lot.id where lot.id in %s and ks.store_id != %s and lot.store is true limit 1" % (lots, self.store_id.id)
        self.env.cr.execute(sql)
        datas = self.env.cr.fetchall()
        if datas and datas[0] != None :
            dupl = self.browse(datas[0][0])
            name = dupl.karyawan_sumber 
            if dupl.lot_id_target.name :
                name += ' / '+ dupl.karyawan_target
            lot = dupl.lot_id_sumber.name
            if dupl.lot_id_target.name :
                lot += ' / '+dupl.lot_id_target.name
            raise ValidationError('Data name: %s, lot: %s sudah ada di dokumen %s !' % (name,lot,dupl.store_id.name))

    @api.multi
    def swap_barcode(self):
        lot_ids = self.env['stock.production.lot']
        lot_ids |= self.lot_id_sumber
        lot_ids |= self.lot_id_target
        if lot_ids :
            self.check_data_double(lot_ids)

        if self.divisi_target:
            divisi_target = self.divisi_target.id
        else:
            divisi_target = 'Null'

        if self.lokasi_target:
            lokasi_target = self.lokasi_target.id
        else:
            lokasi_target = 'Null'

        if self.jabatan_target:
            jabatan_target = self.jabatan_target.id
        else:
            jabatan_target = 'Null'

        if self.bordir_target:
            bordir_target = self.bordir_target
        else:
            bordir_target = ''

        if self.lot_target:
            lot_target = self.lot_target
        else:                
            lot_target = 'Null'

        if self.divisi_sumber.id:
            divisi_sumber = self.divisi_sumber.id            
        else:
            divisi_sumber = 'Null'

        if self.lokasi_sumber:
            lokasi_sumber = self.lokasi_sumber.id
        else:
            lokasi_sumber = 'Null'

        if self.jabatan_sumber:
            jabatan_sumber = self.jabatan_sumber.id
        else:
            jabatan_sumber = 'Null'

        if self.bordir_sumber:
            bordir_sumber = self.bordir_sumber
        else:                
            bordir_sumber = ''

        if self.lot_sumber:
            lot_sumber = self.lot_sumber
        else:                
            lot_sumber = 'Null'

        # akalin jika ada nama karyawan yg mengandung tanda apostrof (')
        karyawan_target = self.karyawan_target
        if "'" in karyawan_target:
            new_karyawan_target = karyawan_target.split("'")
            karyawan_target = ''
            apostrof = False
            for new in new_karyawan_target:
                if not apostrof :
                    karyawan_target += new
                    apostrof = True
                else:
                    karyawan_target += "''"+new
                    apostrof = True
        karyawan_sumber = self.karyawan_sumber
        if "'" in karyawan_sumber:
            new_karyawan_sumber = karyawan_sumber.split("'")
            karyawan_sumber = ''
            apostrof = False
            for new in new_karyawan_sumber:
                if not apostrof :
                    karyawan_sumber += new
                    apostrof = True
                else:
                    karyawan_sumber += "''"+new
                    apostrof = True


        # update lot data tujuan
        self.env.cr.execute("""
            UPDATE stock_production_lot SET nik = '%s', karyawan = '%s', nama_bordir = '%s', pengukuran_karyawan = %s,
                    data_pengukuran_id = '%s', polybag = '%s', divisi_id = %s, lokasi_id = %s, jabatan_id = %s
            WHERE id = '%s'
            """ % (self.nik_target, karyawan_target, bordir_target, self.pengukuran_karyawan_target.id, self.data_pengukuran_id_target.id,
                   self.polybag_target, divisi_target, lokasi_target, jabatan_target, self.lot_id_sumber.id))
        # update lot data asal
        self.env.cr.execute("""
            UPDATE stock_production_lot SET nik = '%s', karyawan = '%s', nama_bordir = '%s', pengukuran_karyawan = %s,
                    data_pengukuran_id = '%s', polybag = '%s', divisi_id = %s, lokasi_id = %s, jabatan_id = %s
            WHERE id = '%s'
            """ % (self.nik_sumber, karyawan_sumber, bordir_sumber, self.pengukuran_karyawan_sumber.id, self.data_pengukuran_id_sumber.id,
                   self.polybag_sumber, divisi_sumber, lokasi_sumber, jabatan_sumber, self.lot_id_target.id))
        
        # create workorder history lot tujuan
        self.env.cr.execute("""
            INSERT INTO swap_history_barcode (id, karyawan, nik, swap_lot_id, store_doc, lot_id, date)
            VALUES (nextval('swap_history_barcode_id_seq'), '%s', '%s', %s, %s, %s, (now() at time zone 'UTC'))
            """ % (karyawan_target, self.nik_target, self.lot_id_sumber.id, self.store_id.id, self.lot_id_target.id))
        # create workorder history lot asal
        self.env.cr.execute("""
            INSERT INTO swap_history_barcode (id, karyawan, nik, swap_lot_id, store_doc, lot_id, date)
            VALUES (nextval('swap_history_barcode_id_seq'), '%s', '%s', %s, %s, %s, (now() at time zone 'UTC'))
            """ % (karyawan_sumber, self.nik_sumber, self.lot_id_target.id, self.store_id.id, self.lot_id_sumber.id))
        
        self.update({
                    'nik_target' : self.lot_id_target.nik,
                    'karyawan_target' : self.lot_id_target.karyawan,
                    'bordir_target' : self.lot_id_target.nama_bordir,
                    'pengukuran_karyawan_target' : self.lot_id_target.pengukuran_karyawan.id,
                    'data_pengukuran_id_target' : self.lot_id_target.data_pengukuran_id.id,
                    'polybag_target' : self.lot_id_target.polybag,
                    'divisi_target' : self.lot_id_target.divisi_id.id,
                    'lokasi_target' : self.lot_id_target.lokasi_id.id,
                    'jabatan_target': self.lot_id_target.jabatan_id.id,
                    'lot_target' : self.lot_id_target.lot,
                    'nik_sumber' : self.lot_id_sumber.nik,
                    'karyawan_sumber' : self.lot_id_sumber.karyawan,
                    'bordir_sumber' : self.lot_id_sumber.nama_bordir,
                    'pengukuran_karyawan_sumber' : self.lot_id_sumber.pengukuran_karyawan.id,
                    'data_pengukuran_id_sumber' : self.lot_id_sumber.data_pengukuran_id.id,
                    'polybag_sumber' : self.lot_id_sumber.polybag,
                    'divisi_sumber' : self.lot_id_sumber.divisi_id.id,
                    'lokasi_sumber' : self.lot_id_sumber.lokasi_id.id,
                    'jabatan_sumber': self.lot_id_sumber.jabatan_id.id,
                    'lot_sumber' : self.lot_id_sumber.lot,
                    'is_swap' : True,
                    })

