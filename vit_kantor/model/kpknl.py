#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class kpknl(models.Model):

    _name = "vit.kpknl"
    _description = "vit.kpknl"
    name = fields.Char( required=True, string="Name",  help="")
    kode = fields.Integer( string="Kode",  help="")
    alamat = fields.Char( string="Alamat",  help="")


    lokasi_id = fields.Many2one(comodel_name="vit.location",  string="Lokasi",  help="")
