#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
import time
from odoo.exceptions import UserError, Warning

class referensi_rekomendasi_bkd(models.Model):

    _name = "vit.referensi_rekomendasi_bkd"
    _description = "vit.referensi_rekomendasi_bkd"
    name = fields.Char( required=True, string="Nama Rekomendasi",  help="")
    bkd = fields.Many2one( "vit.bkd", "BKD",  help="")
    tanggal = fields.Date( string="Tanggal Rekomendasi", default=lambda self:time.strftime("%Y-%m-%d"), help="")
	
