#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class skp_disertasi(models.Model):
    _name = "vit.skp_disertasi"
    _inherit = "vit.skp_disertasi"

    ak_pembimbing_utama = fields.Float( string="Ak pembimbing utama",  help="")
    ak_pembimbing_pembantu = fields.Float( string="Ak pembimbing pembantu",  help="")
    ak_total = fields.Float( string="Ak total",  help="")

    