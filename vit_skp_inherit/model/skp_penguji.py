#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class skp_penguji(models.Model):
    _name = "vit.skp_penguji"
    _inherit = "vit.skp_penguji"

    ak_ketua_penguji = fields.Float( string="Ak ketua penguji",  help="")
    ak_anggota_penguji = fields.Float( string="Ak anggota penguji",  help="")
    ak_total = fields.Float( string="Ak total",  help="")
