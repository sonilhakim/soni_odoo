#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class laporan_detail(models.Model):

    _name = "vit.laporan_detail"
    _description = "vit.laporan_detail"
    name = fields.Char( required=True, string="Name",  help="")
    nip = fields.Char( string="Nip",  help="")
    golongan = fields.Char( string="Golongan",  help="")
    jabatan = fields.Char( string="Jabatan",  help="")


    lap_daftar_pegawai_id = fields.Many2one(comodel_name="vit.laporan_daftar_pegawai",  string="Lap daftar pegawai",  help="")
