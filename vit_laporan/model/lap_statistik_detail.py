#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class lap_statistik_detail(models.Model):

    _name = "vit.lap_statistik_detail"
    _description = "vit.lap_statistik_detail"
    name = fields.Char( required=True, string="Name",  help="")
    nip = fields.Char( string="Nip",  help="")
    golongan = fields.Char( string="Golongan",  help="")
    jabatan = fields.Char( string="Jabatan",  help="")


    statistik_id = fields.Many2one(comodel_name="vit.laporan_statistik_pegawai",  string="Statistik",  help="")
