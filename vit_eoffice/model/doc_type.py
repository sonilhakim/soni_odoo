#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class doc_type(models.Model):

    _name = "vit.doc_type"
    _description = "vit.doc_type"
    name = fields.Char( required=True, string="Name",  help="")
    code = fields.Char( string="Code",  help="")


