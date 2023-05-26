#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class doc_template(models.Model):

    _name = "vit.doc_template"
    _description = "vit.doc_template"
    name = fields.Char( required=True, string="Name",  help="")
    code = fields.Char( string="Code",  help="")
    body = fields.Text( string="Body",  help="")


