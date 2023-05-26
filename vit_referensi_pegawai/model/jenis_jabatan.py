#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class JenisJabatan(models.Model):

    _name = "vit.jenis.jabatan"
    _description = "vit.jenis.jabatan"
    name = fields.Char( required=True, string="Name",  help="")
    code = fields.Char( string="Kode",  help="")
