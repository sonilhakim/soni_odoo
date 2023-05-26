#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class skp_penelitian(models.Model):

    _name = "vit.skp_penelitian"
    _description = "vit.skp_penelitian"
    name = fields.Char( required=True, string="Name",  help="")
    jumlah_peneliti_mandiri = fields.Integer( string="Jumlah peneliti mandiri",  help="")
    jumlah_peneliti_utama = fields.Integer( string="Jumlah peneliti utama",  help="")
    jumlah_peneliti_anggota = fields.Integer( string="Jumlah peneliti anggota",  help="")
    ak_karya_ilmiah_jurnal = fields.Integer( string="Ak karya ilmiah jurnal",  help="")
    ak_jumlah_peneliti_mandiri = fields.Integer( string="Ak jumlah peneliti mandiri",  help="")
    ak_jumlah_peneliti_utama = fields.Integer( string="Ak jumlah peneliti utama",  help="")
    ak_jumlah_peneliti_anggota = fields.Integer( string="Ak jumlah peneliti anggota",  help="")
    ak_jumlah = fields.Integer( string="Ak jumlah",  help="")


    skp_id = fields.Many2one(comodel_name="vit.skp",  string="Skp",  help="")
