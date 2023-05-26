#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class skp_pengabdian(models.Model):

    _name = "vit.skp_pengabdian"
    _description = "vit.skp_pengabdian"
    name = fields.Char( required=True, string="Name",  help="")
    jumlah_program = fields.Integer( string="Jumlah program",  help="")
    ak_program = fields.Integer( string="Ak program",  help="")
    ak_jumlah = fields.Integer( string="Ak jumlah",  help="")


    skp_id = fields.Many2one(comodel_name="vit.skp",  string="Skp",  help="")
