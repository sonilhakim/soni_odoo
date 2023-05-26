#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class skp_rekapitulasi_jabatan_pt(models.Model):

    _name = "vit.skp_rekapitulasi_jabatan_pt"
    _description = "vit.skp_rekapitulasi_jabatan_pt"
    name = fields.Char( required=True, string="Name",  help="")
    satuan_hasil = fields.Integer( string="Satuan hasil",  help="")
    jumlah_angka_kredit = fields.Integer( string="Jumlah angka kredit",  help="")


    skp_id = fields.Many2one(comodel_name="vit.skp",  string="Skp",  help="")
