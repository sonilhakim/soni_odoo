#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class kesimpulan_kinerja_dosen_line(models.Model):

    _name = "vit.kesimpulan_kinerja_dosen_line"
    _description = "vit.kesimpulan_kinerja_dosen_line"
    name = fields.Char( required=True, string="Name",  help="")
    syarat = fields.Char( string="Syarat",  help="")
    kinerja = fields.Float( string="Kinerja",  help="")
    kesimpulan = fields.Char( string="Kesimpulan",  help="")


    kesimpulan_id = fields.Many2one(comodel_name="vit.kesimpulan_kinerja_dosen",  string="Kesimpulan",  help="")
