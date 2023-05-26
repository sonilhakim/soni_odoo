#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class status_aset(models.Model):

    _name = "vit.status_aset"
    _description = "vit.status_aset"
    name = fields.Char( required=True, string="Name",  help="")
    description = fields.Text( string="Description",  help="")


