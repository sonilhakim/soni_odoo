#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class jenis_buku(models.Model):

    _name = "vit.jenis_buku"
    _description = "vit.jenis_buku"
    name = fields.Char( required=True, string="Name",  help="")


