#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class vit_data_mahasiswa(models.Model):

    _name = "vit.vit_data_mahasiswa"
    _description = "vit.vit_data_mahasiswa"
    name = fields.Char( required=True, string="Name",  help="")
    tahun = fields.Char( string="Tahun",  help="")
    semester = fields.Char( string="Semester",  help="")
    jumlah_mahasiswa = fields.Integer( string="Jumlah mahasiswa",  help="")
    jumlah_ditawarkan = fields.Integer( string="Jumlah ditawarkan",  help="")
    co_hort = fields.Char( string="Cohort")


    fakultas_id = fields.Many2one(comodel_name="vit.fakultas",  string="Fakultas",  help="")
    jurusan_id = fields.Many2one(comodel_name="vit.jurusan",  string="Jurusan",  help="")
    prodi_id = fields.Many2one(comodel_name="vit.program_studi",  string="Prodi",  help="")
