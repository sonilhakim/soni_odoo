#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class pensiun_detail(models.Model):

    _name = "vit.pensiun_detail"
    _description = "vit.pensiun_detail"
    name = fields.Char( required=True, string="Name",  help="")
    nip = fields.Char( string="Nip",  help="")
    jabatan_terakhir = fields.Char( string="Jabatan terakhir",  help="")
    golongan_terakhir = fields.Char( string="Golongan terakhir",  help="")
    tmt_pensiun = fields.Date( string="Tmt pensiun",  help="")


    pensiun_id = fields.Many2one(comodel_name="vit.daftar_pegawai_pensiun",  string="Pensiun",  help="")
