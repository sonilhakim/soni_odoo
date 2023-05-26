#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class skp_pengembangan_diri(models.Model):
    _name = "vit.skp_pengembangan_diri"
    _inherit = "vit.skp_pengembangan_diri"

    ak = fields.Float( string="Ak",  help="")
    jumlah_ak = fields.Float( string="Jumlah ak",  help="")
