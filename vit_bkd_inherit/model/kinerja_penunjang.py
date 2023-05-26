#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class kinerja_penunjang(models.Model):

    _name = "vit.kinerja_penunjang"
    _description = "vit.kinerja_penunjang"
    
    name = fields.Char( required=True, string="Name",  help="")
    uraian_jenis_kegiatan = fields.Char( string="Uraian jenis kegiatan",  help="")
    bukti_penugasan = fields.Char( string="Bukti penugasan",  help="")
    file_bukti_penugasan = fields.Binary( string="File bukti penugasan",  help="")
    file_bukti_penugasan2 = fields.Binary( string="File bukti penugasan",  help="")
    file_bukti_penugasan_filename = fields.Char( string="File bukti penugasan filename",  help="")
    beban_sks = fields.Float( string="Beban sks",  help="")
    masa_penugasan = fields.Char( string="Masa penugasan",  help="")
    bukti_dokumen = fields.Char( string="Bukti dokumen",  help="")
    file_bukti_dokumen = fields.Binary( string="File bukti dokumen",  help="")
    file_bukti_dokumen2 = fields.Binary( string="File bukti dokumen",  help="")
    file_bukti_dokumen3 = fields.Binary( string="File bukti dokumen",  help="")
    file_bukti_dokumen_filename = fields.Char( string="File bukti dokumen filename",  help="")
    kinerja_sks = fields.Float( string="Kinerja sks",  help="")
    kinerja_sks_persen = fields.Float( string="Kinerja sks persen",  help="")


    bkd_id = fields.Many2one(comodel_name="vit.bkd",  string="Bkd",  help="")
    jenis_kegiatan_id = fields.Many2one(comodel_name="vit.jenis_kegiatan_kewajiban_khusus",  string="Jenis kegiatan",  help="")
    rekomendasi_id = fields.Many2one(comodel_name="vit.rekomendasi",  string="Rekomendasi",  help="")
    # kinerja_sks_persen = fields.Float( string="Kinerja sks persen", compute="compute_sks", store=True, help="")

    # @api.depends("beban_sks","kinerja_sks")
    # def compute_sks(self):
    #     for kinerja in self:
    #         if kinerja.beban_sks != 0:
    #             kinerja.kinerja_sks_persen = (kinerja.kinerja_sks / kinerja.beban_sks) * 100
