#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class rekap_perguruan_tinggi_line(models.Model):
    _name = "vit.rekap_perguruan_tinggi_line"
    _inherit = "vit.rekap_perguruan_tinggi_line"

    name = fields.Char( required=False, string="Name",  help="")
    kewajiban_khusus = fields.Char( string="Kewajiban khusus",  help="")
