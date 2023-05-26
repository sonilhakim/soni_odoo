#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
import time
from odoo.exceptions import UserError, Warning

class vit_informasi(models.Model):

    _name = "vit.informasi"
    _description = "vit.informasi"
    _inherit = ['mail.thread']
    name = fields.Char( required=True, string="Nama Informasi",  help="")
    jenis_informasi = fields.Char( string="Jenis Informasi",  help="")
    tanggal = fields.Date( string="Tanggal", default=lambda self:time.strftime("%Y-%m-%d"), help="")
	
