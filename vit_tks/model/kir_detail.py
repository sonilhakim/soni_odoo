#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class kir_detail(models.Model):

    _name = "vit.kir_detail"
    _description = "vit.kir_detail"
    name = fields.Char( required=True, string="Name",  help="")
    merk_model = fields.Char( string="Merk model",  help="")
    no_seri_pbr = fields.Char( string="No seri pbr",  help="")
    thn_pembuatan = fields.Char( string="Thn pembuatan",  help="")
    code = fields.Char( string="Code",  help="")
    jumlah = fields.Float( string="Jumlah",  help="")
    harga = fields.Float( string="Harga",  help="")
    kondisi = fields.Char( string="Kondisi",  help="")
    keterangan = fields.Char( string="Keterangan",  help="")


    kir_id = fields.Many2one(comodel_name="vit.kir",  string="Kir",  help="")
    asset_id = fields.Many2one(comodel_name="account.asset.asset",  string="Asset",  help="")
