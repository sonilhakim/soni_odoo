#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class rekomendasi(models.Model):

    _name = "vit.rekomendasi"
    _description = "vit.rekomendasi"
    name = fields.Char( required=True, string="Name",  help="")


