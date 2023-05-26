#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class wilayah(models.Model):

    _name = "vit.wilayah"
    _description = "vit.wilayah"
    name = fields.Char( required=True, string="Name",  help="")
    kode = fields.Integer( string="Kode",  help="")


