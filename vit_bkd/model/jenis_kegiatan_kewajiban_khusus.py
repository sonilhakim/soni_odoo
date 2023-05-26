#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class jenis_kegiatan_kewajiban_khusus(models.Model):

    _name = "vit.jenis_kegiatan_kewajiban_khusus"
    _description = "vit.jenis_kegiatan_kewajiban_khusus"
    name = fields.Char( required=True, string="Name",  help="")


