#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class skp_penguji(models.Model):

    _name = "vit.skp_penguji"
    _description = "vit.skp_penguji"
    name = fields.Char( required=True, string="Name",  help="")
    jumlah_mhs_ketua_penguji = fields.Integer( string="Jumlah mhs ketua penguji",  help="")
    jumlah_mhs_anggota_penguji = fields.Integer( string="Jumlah mhs anggota penguji",  help="")
    ak_ketua_penguji = fields.Integer( string="Ak ketua penguji",  help="")
    ak_anggota_penguji = fields.Integer( string="Ak anggota penguji",  help="")
    ak_total = fields.Integer( string="Ak total",  help="")


    skp_id = fields.Many2one(comodel_name="vit.skp",  string="Skp",  help="")
    semester_id = fields.Many2one(comodel_name="vit.semester",  string="Semester",  help="")
