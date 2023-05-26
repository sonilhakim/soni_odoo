#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class details_naik_pangkat(models.Model):

    _name = "vit.details_naik_pangkat"
    _description = "vit.details_naik_pangkat"
    name = fields.Char( required=True, string="Name",  help="")
    nip = fields.Char( string="Nip",  help="")
    pangkat_awal = fields.Char( string="Pangkat awal",  help="")
    pangkat_akhir = fields.Char( string="Pangkat akhir",  help="")


    kenaikan_pangkat_id = fields.Many2one(comodel_name="vit.kenaikan_pangkat",  string="Kenaikan pangkat",  help="")
