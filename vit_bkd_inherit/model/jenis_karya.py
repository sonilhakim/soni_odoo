#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class jenis_karya(models.Model):

    _name = "vit.jenis_karya"
    _description = "vit.jenis_karya"
    name = fields.Char( required=True, string="Name",  help="")
