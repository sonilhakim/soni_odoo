#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class buku_inventaris_detail(models.Model):

    _name = "vit.buku_inventaris_detail"
    _description = "vit.buku_inventaris_detail"
    name = fields.Char( required=True, string="Name",  help="")
    type = fields.Char( string="Type",  help="")
    tahun_perolehan = fields.Date( string="Tahun perolehan",  help="")
    jumlah = fields.Float( string="Jumlah",  help="")
    satuan = fields.Char( string="Satuan",  help="")
    kondisi = fields.Char( string="Kondisi",  help="")
    asal = fields.Char( string="Asal",  help="")
    keterangan = fields.Text( string="Keterangan",  help="")


    buku_inventaris_id = fields.Many2one(comodel_name="vit.buku_inventaris",  string="Buku inventaris",  help="")
