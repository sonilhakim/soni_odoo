#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class skp_rekapitulasi_mengembangkan_bahan_kuliah(models.Model):

    _name = "vit.skp_rekapitulasi_mengembangkan_bahan_kuliah"
    _description = "vit.skp_rekapitulasi_mengembangkan_bahan_kuliah"
    name = fields.Char( required=True, string="Name",  help="")
    naskah = fields.Char( string="Naskah",  help="")
    ak = fields.Integer( string="Ak",  help="")


    skp_id = fields.Many2one(comodel_name="vit.skp",  string="Skp",  help="")
