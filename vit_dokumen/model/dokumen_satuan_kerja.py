#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class dokumen_satuan_kerja(models.Model):

    _name = "vit.dokumen_satuan_kerja"
    _description = "vit.dokumen_satuan_kerja"
    name = fields.Char( required=True, string="Name",  help="")


    jenis_id = fields.Many2one(comodel_name="vit.jenis_dokumen",  string="Jenis",  help="")
    unit_id = fields.Many2one(comodel_name="vit.unit_kerja",  string="Unit",  help="")
