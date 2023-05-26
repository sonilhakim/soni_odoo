#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class data_beasiswa(models.Model):

    _name = "vit.data_beasiswa"
    _description = "vit.data_beasiswa"
    name = fields.Char( required=True, string="Name",  help="")
    tahun = fields.Char( string="Tahun",  help="")
    semester = fields.Char( string="Semester",  help="")
    jumlah_beasiswa = fields.Float( string="Jumlah beasiswa",  help="")


    fakultas_id = fields.Many2one(comodel_name="vit.fakultas",  string="Fakultas",  help="")
    jurusan_id = fields.Many2one(comodel_name="vit.jurusan",  string="Jurusan",  help="")
    prodi_id = fields.Many2one(comodel_name="vit.program_studi",  string="Prodi",  help="")
