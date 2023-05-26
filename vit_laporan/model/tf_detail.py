#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class tf_detail(models.Model):

    _name = "vit.tf_detail"
    _description = "vit.tf_detail"
    name = fields.Char( required=True, string="Name",  help="")
    nip = fields.Char( string="Nip",  help="")
    jabatan = fields.Char( string="Jabatan",  help="")
    golongan = fields.Char( string="Golongan",  help="")


    tf_id = fields.Many2one(comodel_name="vit.tenaga_fungsional",  string="Tf",  help="")
