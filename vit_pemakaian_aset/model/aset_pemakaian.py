#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class aset_pemakaian(models.Model):

    _name = "vit.aset_pemakaian"
    _description = "vit.aset_pemakaian"
    _rec_name   = "aset_id"
    # name = fields.Char( required=True, string="Name",  help="")
    reference = fields.Char( string="Reference",  help="")
    qty = fields.Integer( string="Qty",  help="")


    aset_id = fields.Many2one(comodel_name="account.asset.asset",  string="Aset",  help="")
    pemakaian_id = fields.Many2one(comodel_name="vit.pemakaian_aset",  string="Pemakaian",  help="")
    kategori_id = fields.Many2one(comodel_name="account.asset.category",  string="Kategori",  help="")
    lokasi_id = fields.Many2one(comodel_name="vit.location",  string="Lokasi",  help="")
