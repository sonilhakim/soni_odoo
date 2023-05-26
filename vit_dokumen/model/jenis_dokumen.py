#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class jenis_dokumen(models.Model):

    _name = "vit.jenis_dokumen"
    _description = "vit.jenis_dokumen"
    name = fields.Char( required=True, string="Name",  help="")


