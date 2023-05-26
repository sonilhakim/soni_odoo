#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
import time
from odoo.exceptions import UserError, Warning

class vit_kerja_dosen(models.Model):

    _name = "vit.kerja_dosen"
    _description = "vit.kerja_dosen"
    name = fields.Char( required=True, string="Nama Kerja Dosen",  help="")
    jenis_kerja_dosen = fields.Char( string="Jenis Kerja Dosen",  help="")
    tanggal = fields.Date( string="Tanggal", default=lambda self:time.strftime("%Y-%m-%d"), help="")
	
