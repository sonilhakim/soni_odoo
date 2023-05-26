#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class pbi(models.Model):

    _name = "vit.pbi"
    _description = "vit.pbi"
    name = fields.Char( required=True, string="Name",  help="")
    kode = fields.Integer( string="Kode",  help="")


    pebin_id = fields.Many2one(comodel_name="vit.pebin",  string="Pebin",  help="")
