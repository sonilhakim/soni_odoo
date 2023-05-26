#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class duk_detail(models.Model):

    _name = "vit.duk_detail"
    _description = "vit.duk_detail"
    name = fields.Char( required=True, string="Name",  help="")
    pangkat = fields.Char( string="Pangkat",  help="")


    duk_id = fields.Many2one(comodel_name="vit.duk",  string="Duk",  help="")
