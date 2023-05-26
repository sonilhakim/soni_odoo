#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class jenis_sub_insentif_kinerja(models.Model):

    _name = "vit.jenis_sub_insentif_kinerja"
    _description = "vit.jenis_sub_insentif_kinerja"
    name = fields.Char( required=True, string="Name",  help="")


