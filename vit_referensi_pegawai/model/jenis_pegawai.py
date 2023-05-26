#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class jenis_pegawai(models.Model):

    _name = "vit.jenis_pegawai"
    _description = "vit.jenis_pegawai"
    name = fields.Char( required=True, string="Name",  help="")


