#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class aset_pemakaian(models.Model):
    _name = "vit.aset_pemakaian"
    _inherit = "vit.aset_pemakaian"

    reference = fields.Char( related='aset_id.code', string="Reference",  help="")
    kategori_id = fields.Many2one(comodel_name="account.asset.category", related='aset_id.category_id', string="Kategori",  help="")
    lokasi_id = fields.Many2one(comodel_name="vit.location", related='aset_id.last_location_id', string="Lokasi",  help="")
