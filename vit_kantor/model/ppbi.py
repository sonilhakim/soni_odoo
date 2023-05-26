#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class ppbi(models.Model):

    _name = "vit.ppbi"
    _description = "vit.ppbi"
    name = fields.Char( required=True, string="Name",  help="")
    kode = fields.Integer( string="Kode",  help="")


    pebin_id = fields.Many2one(comodel_name="vit.pebin",  string="Pebin",  help="")
    pbi_id = fields.Many2one(comodel_name="vit.pbi",  string="Pbi",  help="")
