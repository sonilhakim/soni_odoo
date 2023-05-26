#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class skp_jabatan_pt(models.Model):

    _name = "vit.skp_jabatan_pt"
    _description = "vit.skp_jabatan_pt"
    name = fields.Char( required=True, string="Name",  help="")
    hasil = fields.Integer( string="Hasil",  help="")
    satuan_hasil = fields.Char( string="Satuan hasil",  help="")
    angka_kredit = fields.Integer( string="Angka kredit",  help="")
    jumlah_angka_kredit = fields.Integer( string="Jumlah angka kredit",  help="")


    skp_id = fields.Many2one(comodel_name="vit.skp",  string="Skp",  help="")
    semester_id = fields.Many2one(comodel_name="vit.semester",  string="Semester",  help="")
