#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class employee(models.Model):

    _name = "hr.employee"
    _description = "hr.employee"

    _inherit = "hr.employee"
    nomor_sertifikat = fields.Char( string="Nomor sertifikat",  help="")
    nip = fields.Char( string="Nip",  help="")
    nidn = fields.Char( string="Nidn",  help="")
    s1 = fields.Char( string="S1",  help="")
    s2 = fields.Char( string="S2",  help="")
    s3 = fields.Char( string="S3",  help="")
    s1_ijasah = fields.Binary( string="S1 ijasah",  help="")
    s2_ijasah = fields.Binary( string="S2 ijasah",  help="")
    s3_ijasah = fields.Binary( string="S3 ijasah",  help="")
    s1_ijasah_filename = fields.Char( string="S1 ijasah filename",  help="")
    s2_ijasah_filename = fields.Char( string="S2 ijasah filename",  help="")
    s3_ijasah_filename = fields.Char( string="S3 ijasah filename",  help="")
    bidang_ilmu = fields.Char( string="Bidang ilmu",  help="")
    ktp = fields.Binary( string="Ktp",  help="")
    ktp_filename = fields.Binary( string="Ktp filename",  help="")


    bkd_ids = fields.One2many(comodel_name="vit.bkd",  inverse_name="employee_id",  string="Bkd",  help="")
    status_dosen_id = fields.Many2one(comodel_name="vit.status_dosen",  string="Status dosen",  help="")
    fakultas_id = fields.Many2one(comodel_name="vit.fakultas",  string="Fakultas",  help="")
    jurusan_id = fields.Many2one(comodel_name="vit.jurusan",  string="Jurusan",  help="")
    program_studi_id = fields.Many2one(comodel_name="vit.program_studi",  string="Program studi",  help="")
    jabatan_fungsional_id = fields.Many2one(comodel_name="vit.jabatan",  string="Jabatan fungsional",  help="")
    golongan_id = fields.Many2one(comodel_name="vit.golongan",  string="Golongan",  help="")
    asesor1_id = fields.Many2one(comodel_name="hr.employee",  string="Asesor1",  help="")
    asesor2_id = fields.Many2one(comodel_name="hr.employee",  string="Asesor2",  help="")
