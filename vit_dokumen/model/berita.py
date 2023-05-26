#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class berita(models.Model):

    _name = "vit.berita"
    _description = "vit.berita"
    name = fields.Char( required=True, string="Name",  help="")
    tanggal = fields.Date( string="Tanggal",  help="")


