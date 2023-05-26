#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class anggaran_detail(models.Model):

    _name = "vit.anggaran_detail"
    _description = "vit.anggaran_detail"

    target_capaian      = fields.Float( string="Target capaian",  help="")
    anggaran            = fields.Float( string="Anggaran",  help="")
    realisasi           = fields.Float( string="Realisasi",  help="")
    sisa                = fields.Float( string="Sisa",  help="")
    definitif           = fields.Float( string="Definitif",  help="")
    kegiatan            = fields.Text(string='Kegiatan')


    # kegiatan_id = fields.Many2one(comodel_name="anggaran.kegiatan",  string="Kegiatan",  help="")
    rekapitulasi_id     = fields.Many2one(comodel_name="vit.rekapitulasi_anggaran_program_dan_kegiatan_unit",  string="Rekapitulasi",  help="")
    satuan_target       = fields.Char(string='Satuan Target')
