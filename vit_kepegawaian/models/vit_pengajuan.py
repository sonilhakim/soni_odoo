#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
import time
from odoo.exceptions import UserError, Warning

class vit_pengajuan(models.Model):

    _name = "vit.pengajuan"
    _description = "vit.pengajuan"
    name = fields.Char( required=True, string="Nama Pengajuan",  help="")
    jenis_pengajuan = fields.Char( string="Jenis Pengajuan",  help="")
    tanggal = fields.Date( string="Tanggal", default=lambda self:time.strftime("%Y-%m-%d"), help="")
	
