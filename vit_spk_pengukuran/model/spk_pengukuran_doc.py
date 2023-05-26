#!/usr/bin/python
#-*- coding: utf-8 -*-
import base64
import time
from odoo import models, fields, api, _

class spk_pengukuran_doc(models.Model):

    _name = "vit.spk_pengukuran_doc"
    _description = "vit.spk_pengukuran_doc"
    
    name 		= fields.Char( required=False, string="Description",  help="")
    date 		= fields.Date( string="Date", default=lambda self: time.strftime("%Y-%m-%d"), help="")
    doc 		= fields.Binary( string="Document Name",  help="")
    doc_name 	= fields.Char( string="Document Name",)


    spk_id = fields.Many2one(comodel_name="vit.spk_pengukuran",  string="SPK Pengukuran",  help="")
