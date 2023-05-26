#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class jenis_kkn(models.Model):

    _name = "vit.jenis_kkn"
    _description = "vit.jenis_kkn"
    name = fields.Char( required=True, string="Name",  help="")


