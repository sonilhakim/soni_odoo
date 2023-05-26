#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class kinerja_bidang_penelitian(models.Model):

    _name = "vit.kinerja_bidang_penelitian"
    _description = "vit.kinerja_bidang_penelitian"
    name = fields.Char( required=True, string="Name",  help="")
    uraian_jenis_kegiatan = fields.Char( string="Uraian jenis kegiatan",  help="")
    bukti_penugasan = fields.Char( string="Bukti penugasan",  help="")
    file_bukti_penugasan = fields.Binary( string="File bukti penugasan",  help="")
    file_bukti_penugasan_filename = fields.Char( string="File bukti penugasan filename",  help="")
    beban_sks = fields.Float( string="Beban sks",  help="")
    masa_penugasan = fields.Char( string="Masa penugasan",  help="")
    bukti_dokumen = fields.Char( string="Bukti dokumen",  help="")
    file_bukti_dokumen = fields.Binary( string="File bukti dokumen",  help="")
    file_bukti_dokumen_filename = fields.Char( string="File bukti dokumen filename",  help="")
    kinerja_sks = fields.Float( string="Kinerja sks",  help="")
    kinerja_sks_persen = fields.Float( string="Kinerja sks persen",  help="")


    bkd_id = fields.Many2one(comodel_name="vit.bkd",  string="Bkd",  help="")
    jenis_kegiatan_id = fields.Many2one(comodel_name="vit.jenis_kegiatan_penelitian",  string="Jenis kegiatan",  help="")
    rekomendasi_id = fields.Many2one(comodel_name="vit.rekomendasi",  string="Rekomendasi",  help="")
