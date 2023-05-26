#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class jenis_pendidikan(models.Model):

    _name = "vit.jenis_pendidikan"
    _description = "vit.jenis_pendidikan"
    name = fields.Char( required=True, string="Name",  help="")


