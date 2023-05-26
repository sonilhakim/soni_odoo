#!/usr/bin/python
#-*- coding: utf-8 -*-
import base64
import time
from odoo import models, fields, api, _

class inquery_garmen_doc(models.Model):

    _name = "vit.inquery_garmen_doc"
    _description = "vit.inquery_garmen_doc"
    
    name 		= fields.Char( required=False, string="Description",  help="")
    date 		= fields.Date( string="Date", default=lambda self: time.strftime("%Y-%m-%d"), help="")
    doc 		= fields.Binary( string="Document Name",  help="")
    doc_name 	= fields.Char( string="Document Name",)


    inquery_id 	= fields.Many2one(comodel_name="vit.marketing_inquery_garmen",  string="Inquery",  help="")
