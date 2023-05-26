#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class skp_rekapitulasi_mengembangkan_bahan_kuliah(models.Model):
    _name = "vit.skp_rekapitulasi_mengembangkan_bahan_kuliah"
    _inherit = "vit.skp_rekapitulasi_mengembangkan_bahan_kuliah"

    naskah = fields.Integer( string="Naskah",  help="")
