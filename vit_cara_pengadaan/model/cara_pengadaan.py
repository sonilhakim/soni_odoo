#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class cara_pengadaan(models.Model):

    _name = "vit.cara_pengadaan"
    _description = "vit.cara_pengadaan"
    name = fields.Char( required=True, string="Name",  help="")
    code = fields.Char( string="Kode",  help="")


