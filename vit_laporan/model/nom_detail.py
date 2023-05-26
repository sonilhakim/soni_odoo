#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class nom_detail(models.Model):

    _name = "vit.nom_detail"
    _description = "vit.nom_detail"
    name = fields.Char( required=True, string="Name",  help="")
    nip = fields.Char( string="Nip",  help="")
    pangkat_gol_ruang = fields.Char( string="Pangkat gol ruang",  help="")
    tmt_pangkat_gol_ruang = fields.Date( string="Tmt pangkat gol ruang",  help="")
    jabatan = fields.Char( string="Jabatan",  help="")
    tmt_jabatan = fields.Date( string="Tmt jabatan",  help="")


    nominatif_id = fields.Many2one(comodel_name="vit.lap_nominatif",  string="Nominatif",  help="")
