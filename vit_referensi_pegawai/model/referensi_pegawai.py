#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
import time
from odoo.exceptions import UserError, Warning

class referensi_pegawai(models.Model):

    _name = "vit.referensi_pegawai"
    _description = "vit.referensi_pegawai"
    name = fields.Char( required=True, string="Nama Referensi",  help="")
    jenis_referensi = fields.Char( string="Jenis Referensi",  help="")
    tanggal = fields.Date( string="Tanggal", default=lambda self:time.strftime("%Y-%m-%d"), help="")
	
