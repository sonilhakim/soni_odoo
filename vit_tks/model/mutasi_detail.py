#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class mutasi_detail(models.Model):

    _name = "vit.mutasi_detail"
    _description = "vit.mutasi_detail"
    name = fields.Char( required=True, string="Name",  help="")
    kode_barang = fields.Char( string="Kode barang",  help="")
    nama_barang = fields.Char( string="Nama barang",  help="")
    type = fields.Char( string="Type",  help="")
    no_sertifikat = fields.Char( string="No sertifikat",  help="")
    asal = fields.Char( string="Asal",  help="")
    tahun_perolehan = fields.Char( string="Tahun perolehan",  help="")
    kondisi = fields.Char( string="Kondisi",  help="")
    lokasi_awal = fields.Char( string="Lokasi awal",  help="")
    lokasi_akhir = fields.Char( string="Lokasi akhir",  help="")
    jumlah_awal = fields.Float( string="Jumlah awal",  help="")
    jumlah_akhir = fields.Float( string="Jumlah akhir",  help="")
    keterangan = fields.Text( string="Keterangan",  help="")


    transfer_id = fields.Many2one(comodel_name="vit.transfer",  string="Transfer",  help="")
    mutasi_id = fields.Many2one(comodel_name="vit.mutasi_barang",  string="Mutasi",  help="")
