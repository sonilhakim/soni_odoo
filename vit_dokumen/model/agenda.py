#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class agenda(models.Model):

    _name = "vit.agenda"
    _description = "vit.agenda"
    name = fields.Char( required=True, string="Name",  help="")
    kegiatan = fields.Char( string="Kegiatan",  help="")
    tanggal = fields.Date( string="Tanggal",  help="")


    unit_id = fields.Many2one(comodel_name="vit.unit_kerja",  string="Unit",  help="")
