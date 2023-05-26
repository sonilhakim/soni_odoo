#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class daftar_detail(models.Model):

    _name = "vit.daftar_detail"
    _description = "vit.daftar_detail"
    name = fields.Char( required=True, string="Name",  help="")
    nip = fields.Char( string="Nip",  help="")
    tgl_lahir = fields.Date( string="Tgl lahir",  help="")
    tmp_lahir = fields.Char( string="Tmp lahir",  help="")


    riwayat_hidup_id = fields.Many2one(comodel_name="vit.daftar_riwayat_hidup",  string="Riwayat hidup",  help="")
