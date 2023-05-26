#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class kelompok_aset(models.Model):

    _name = "vit.kelompok_aset"
    _description = "vit.kelompok_aset"
    
    name = fields.Char( required=True, string="Name",  help="")
    description = fields.Text( string="Description",  help="")


