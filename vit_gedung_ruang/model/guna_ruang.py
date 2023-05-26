#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class guna_ruang(models.Model):

    _name = "vit.guna_ruang"
    _description = "vit.guna_ruang"
    name = fields.Char( required=True, string="Name",  help="")
    description = fields.Text( string="Description",  help="")


