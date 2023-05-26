#!/usr/bin/python
#-*- coding: utf-8 -*-
import base64
import time
from odoo import models, fields, api, _

class request_doc(models.Model):

    _name = "vit.request_doc"
    _description = "vit.request_doc"
    
    name        = fields.Char( string="Description",  help="")
    date        = fields.Date( string="Date",  default=lambda self: time.strftime("%Y-%m-%d"), help="")
    doc         = fields.Binary( string="Document Name",  help="")
    doc_name    = fields.Char( string="Document Name",)


    request_id  = fields.Many2one(comodel_name="vit.marketing_request",  string="Request",  help="")
