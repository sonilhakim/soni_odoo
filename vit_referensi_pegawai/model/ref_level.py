#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class ref_level(models.Model):

    _name = "vit.ref_level"
    _description = "vit.ref_level"
    name = fields.Char( required=True, string="Level",  help="")


