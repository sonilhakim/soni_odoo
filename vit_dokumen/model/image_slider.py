#!/usr/bin/python
#-*- coding: utf-8 -*-
import base64
import time
from odoo import models, fields, api, _

class image_slider(models.Model):

    _name = "vit.image_slider"
    _description = "vit.image_slider"
    
    name 		= fields.Char( required=False, string="Description",  help="")
    date 		= fields.Date( string="Date", default=lambda self: time.strftime("%Y-%m-%d"), help="")
    img 		= fields.Binary( string="Image",  help="")
    img_name 	= fields.Char( string="Image Name",)
