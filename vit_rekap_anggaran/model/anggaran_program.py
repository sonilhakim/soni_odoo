#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class anggaran_program(models.Model):

    _name = "vit.anggaran_program"
    _description = "vit.anggaran_program"
    target_capaian = fields.Float( string="Target capaian",  help="")
    anggaran = fields.Float( string="Anggaran",  help="")
    realisasi = fields.Float( string="Realisasi",  help="")
    sisa = fields.Float( string="Sisa",  help="")
    definitif = fields.Float( string="Definitif",  help="")


    satuan_target = fields.Char(string='Satuan Target')
    # program_id = fields.Many2one(comodel_name="anggaran.program",  string="Program",  help="")
    indikator        = fields.Text(string='Kegiatan', required=True, )
    rekap_anggaran_id = fields.Many2one(comodel_name="vit.rekap_anggaran_program",  string="Rekap anggaran",  help="")
