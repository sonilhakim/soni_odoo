#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class detail_penilaian(models.Model):

    _name = "vit.detail_penilaian"
    _description = "vit.detail_penilaian"
    name = fields.Char( required=True, string="Name",  help="")
    nip = fields.Char( string="Nip",  help="")
    pekerjaan = fields.Char( string="Pekerjaan",  help="")
    nilai = fields.Float( string="Nilai",  help="")


    dp3_id = fields.Many2one(comodel_name="vit.dp3",  string="Dp3",  help="")
