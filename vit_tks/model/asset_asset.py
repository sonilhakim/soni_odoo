#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class asset_asset(models.Model):

    _name = "account.asset.asset"
    _description = "account.asset.asset"

    _inherit = "account.asset.asset"
    tipe_barang = fields.Char( string="Tipe barang",  help="")
    tahun_pembuatan = fields.Char( string="Tahun pembuatan",  help="")
    asal = fields.Char( string="Asal",  help="")
    kelengkapan_dokumen = fields.Char( string="Kelengkapan dokumen",  help="")
    tgl_penyerahan_brg = fields.Date( string="Tgl penyerahan brg",  help="")


    satuan_id = fields.Many2one(comodel_name="uom.uom",  string="Satuan",  help="")
