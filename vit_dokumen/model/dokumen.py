#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class dokumen(models.Model):

    _name = "vit.dokumen"
    _description = "vit.dokumen"
    name = fields.Char( required=True, string="Name",  help="")


    jenis_id = fields.Many2one(comodel_name="vit.jenis_dokumen",  string="Jenis",  help="")
    dokumen_satuan_kerja_id = fields.Many2one(comodel_name="vit.dokumen_satuan_kerja",  string="Dokumen satuan kerja",  help="")
    unit_id = fields.Many2one(comodel_name="vit.unit_kerja",  string="Unit",  help="")
