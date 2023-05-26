#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class details_gaji(models.Model):

    _name = "vit.details_gaji"
    _description = "vit.details_gaji"
    name = fields.Char( required=True, string="Name",  help="")
    nip = fields.Char( string="Nip",  help="")
    gaji_awal = fields.Float( string="Gaji awal",  help="")
    gaji_sekarang = fields.Float( string="Gaji sekarang",  help="")


    kenaikan_id = fields.Many2one(comodel_name="vit.kenaikan_gaji",  string="Kenaikan",  help="")
