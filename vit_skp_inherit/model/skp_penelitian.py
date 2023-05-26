#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class skp_penelitian(models.Model):
    _name = "vit.skp_penelitian"
    _inherit = "vit.skp_penelitian"

    ak_jumlah_peneliti_mandiri = fields.Float( string="Ak jumlah peneliti mandiri",  help="")
    ak_jumlah_peneliti_utama = fields.Float( string="Ak jumlah peneliti utama",  help="")
    ak_jumlah_peneliti_anggota = fields.Float( string="Ak jumlah peneliti anggota",  help="")
    ak_jumlah = fields.Float( string="Ak jumlah",  help="")
