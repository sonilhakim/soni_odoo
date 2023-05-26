#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
import time
from odoo.exceptions import UserError, Warning

class vit_remunerasi(models.Model):

    _name = "vit.remunerasi"
    _description = "vit.remunerasi"
    name = fields.Char( required=True, string="Nama Remunerasi",  help="")
    jenis_remunerasi = fields.Char( string="Jenis Remunerasi",  help="")
    tanggal = fields.Date( string="Tanggal", default=lambda self:time.strftime("%Y-%m-%d"), help="")
	
