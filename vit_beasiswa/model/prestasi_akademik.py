#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class prestasi_akademik(models.Model):

    _name = "vit.prestasi_akademik"
    _description = "vit.prestasi_akademik"
    name = fields.Char( required=True, string="Name",  help="")
    tahun = fields.Integer( string="Tahun",  help="")
    tingkat = fields.Char( string="Tingkat",  help="")
    prestasi = fields.Char( string="Prestasi",  help="")
    upload_bukti = fields.Binary( string="Upload bukti",  help="")


    penerima_beasiswa_id = fields.Many2one(comodel_name="vit.penerima_beasiswa",  string="Penerima beasiswa",  help="")
