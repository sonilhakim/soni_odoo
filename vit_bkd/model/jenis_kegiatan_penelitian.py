#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class jenis_kegiatan_penelitian(models.Model):

    _name = "vit.jenis_kegiatan_penelitian"
    _description = "vit.jenis_kegiatan_penelitian"
    name = fields.Char( required=True, string="Name",  help="")


