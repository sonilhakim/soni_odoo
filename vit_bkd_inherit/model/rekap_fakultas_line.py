#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class rekap_fakultas_line(models.Model):
    _name = "vit.rekap_fakultas_line"
    _inherit = "vit.rekap_fakultas_line"

    name = fields.Char( required=False, string="Name",  help="")
    kewajiban_khusus = fields.Char( string="Kewajiban khusus",  help="")
