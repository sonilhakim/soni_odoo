#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
import time
import base64

class doc_sph_garmen_line(models.Model):
    _name = "vit.doc_sph_garmen_line"
    _description = "vit.doc_sph_garmen_line"

    name 		= fields.Char( required=False, string="Description",  help="")
    doc 		= fields.Binary( string="Document Name",  help="")
    doc_name 	= fields.Char( string="Document Name",)
    date 		= fields.Date( string="Date", required=False, default=lambda self: time.strftime("%Y-%m-%d"),  help="")

    sph_id 		= fields.Many2one(comodel_name="vit.marketing_sph_garmen",  string="Sph",  help="")
