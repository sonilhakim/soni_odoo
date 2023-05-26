#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class anggaran_unit(models.Model):

    _name = "vit.anggaran_unit"
    _description = "vit.anggaran_unit"
    alokasi = fields.Float( string="Alokasi",  help="")
    anggaran = fields.Float( string="Anggaran",  help="")
    realisasi = fields.Float( string="Realisasi",  help="")
    sisa = fields.Float( string="Sisa",  help="")
    definitif = fields.Float( string="Definitif",  help="")


    unit_id = fields.Many2one(comodel_name="vit.unit_kerja",  string="SUBSATKER",  help="")
    rka_id = fields.Many2one(comodel_name="anggaran.rka",  string="RKA",  help="")
    rekap_unit_id = fields.Many2one(comodel_name="vit.rekap_unit",  string="Rekap unit",  help="")
