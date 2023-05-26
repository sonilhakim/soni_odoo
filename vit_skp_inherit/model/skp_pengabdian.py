#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class skp_pengabdian(models.Model):
    _name = "vit.skp_pengabdian"
    _inherit = "vit.skp_pengabdian"

    ak_program = fields.Float( string="Ak program",  help="")
    ak_jumlah = fields.Float( string="Ak jumlah",  help="")
