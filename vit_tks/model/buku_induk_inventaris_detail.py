#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class buku_induk_inventaris_detail(models.Model):

    _name = "vit.buku_induk_inventaris_detail"
    _description = "vit.buku_induk_inventaris_detail"
    name = fields.Char( required=True, string="Name",  help="")
    code = fields.Char( string="Code",  help="")
    date = fields.Date( string="Date",  help="")
    type = fields.Char( string="Type",  help="")
    jumlah = fields.Float( string="Jumlah",  help="")
    satuan = fields.Char( string="Satuan",  help="")
    tahun_pembuatan = fields.Char( string="Tahun pembuatan",  help="")
    asal = fields.Char( string="Asal",  help="")
    kelengkapan_dokumen = fields.Char( string="Kelengkapan dokumen",  help="")
    tanggal_penyerahan_barang = fields.Date( string="Tanggal penyerahan barang",  help="")
    kondisi = fields.Char( string="Kondisi",  help="")
    harga = fields.Float( string="Harga",  help="")
    keterangan = fields.Text( string="Keterangan",  help="")


    buku_induk_id = fields.Many2one(comodel_name="vit.buku_induk_inventaris",  string="Buku induk",  help="")
