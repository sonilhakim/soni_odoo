#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class ikhtisar(models.Model):

    _name = "vit.ikhtisar"
    _description = "vit.ikhtisar"
    name = fields.Char( required=True, string="Name",  help="")
    revisi = fields.Text( string="Revisi",  help="")
    lama = fields.Text( string="Lama",  help="")


    ref_id = fields.Many2one(comodel_name="vit.referensi_aset",  string="Ref",  help="")
