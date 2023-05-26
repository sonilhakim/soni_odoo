#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class jenis_disertasi(models.Model):

    _name = "vit.jenis_disertasi"
    _description = "vit.jenis_disertasi"
    name = fields.Char( required=True, string="Name",  help="")


