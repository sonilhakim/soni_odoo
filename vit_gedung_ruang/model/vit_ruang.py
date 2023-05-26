#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class vit_ruang(models.Model):

    _name = "vit.vit_ruang"
    _description = "vit.vit_ruang"
    name = fields.Char( required=True, string="Name",  help="")
    kode_ruang = fields.Char( string="Kode ruang",  help="")
    luas = fields.Float( string="Luas",  help="")
    lantai = fields.Char( string="Lantai",  help="")
    tanggal_awal = fields.Date( string="Tanggal awal",  help="")
    tanggal_akhir = fields.Date( string="Tanggal akhir",  help="")


    gedung_id = fields.Many2one(comodel_name="vit.vit_gedung",  string="Gedung",  help="")
    penanggung_jawab_id = fields.Many2one(comodel_name="res.users",  string="Penanggung jawab",  help="")
    pengguna_id = fields.Many2one(comodel_name="vit.unit_kerja",  string="Pengguna",  help="")
    jenis_penggunaan_id = fields.Many2one(comodel_name="vit.guna_ruang",  string="Jenis penggunaan",  help="")
