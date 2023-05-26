#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
import time
from odoo.addons import decimal_precision as dp

class spk_pengukuran_line(models.Model):

    _name = "vit.spk_pengukuran_line"
    _description = "vit.spk_pengukuran_line"
    
    name = fields.Char( required=False, string="Description",  help="")
    cabang = fields.Char( string="Cabang", required=False,)
    method = fields.Char( string="Metode", required=False,)
    jml_cabang = fields.Integer( string="Jml. Cabang", default= 1,)
    jml_karyawan = fields.Integer( string="Jml. Karyawan", default= 1,)
    date_start = fields.Date( string="Start Date", required=False, help="")
    date_end = fields.Date( string="End Date", required=False, help="")
    
    spk_id = fields.Many2one(comodel_name="vit.spk_pengukuran",  string="SPK Pengukuran",  help="")
