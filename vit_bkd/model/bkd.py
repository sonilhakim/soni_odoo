#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft','Draft'),('open','Diperiksa'),('done','Disetujui')]
from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class bkd(models.Model):

    _name = "vit.bkd"
    _description = "vit.bkd"
    name = fields.Char( required=True, default="New", readonly=True,  string="Name",  help="")
    date = fields.Date( string="Date",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    nip = fields.Char( string="Nip",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    nidn = fields.Char( string="Nidn",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    s1 = fields.Char( string="S1",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    s2 = fields.Char( string="S2",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    s3 = fields.Char( string="S3",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    bidang_ilmu = fields.Char( string="Bidang ilmu",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    mobile = fields.Char( string="Mobile",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    email = fields.Char( string="Email",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    state = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",  help="")


    employee_id = fields.Many2one(comodel_name="hr.employee",  string="Employee",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    institusi_id = fields.Many2one(comodel_name="res.company",  string="Institusi",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    tahun_akademik_id = fields.Many2one(comodel_name="vit.tahun_akademik",  string="Tahun akademik",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    semester_id = fields.Many2one(comodel_name="vit.semester",  string="Semester",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    wakil_dekan_id = fields.Many2one(comodel_name="hr.employee",  string="Wakil dekan",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    status_dosen_id = fields.Many2one(comodel_name="vit.status_dosen",  string="Status dosen",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    jabatan_fungsional_id = fields.Many2one(comodel_name="vit.jabatan",  string="Jabatan fungsional",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    fakultas_id = fields.Many2one(comodel_name="vit.fakultas",  string="Fakultas",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    jurusan_id = fields.Many2one(comodel_name="vit.jurusan",  string="Jurusan",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    program_studi_id = fields.Many2one(comodel_name="vit.program_studi",  string="Program studi",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    golongan_id = fields.Many2one(comodel_name="vit.golongan",  string="Golongan",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    kinerja_bidang_pendidikan_ids = fields.One2many(comodel_name="vit.kinerja_bidang_pendidikan",  inverse_name="bkd_id",  string="Kinerja bidang pendidikan",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    kinerja_bidang_penelitian_ids = fields.One2many(comodel_name="vit.kinerja_bidang_penelitian",  inverse_name="bkd_id",  string="Kinerja bidang penelitian",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    kinerja_bidang_pengabdian_ids = fields.One2many(comodel_name="vit.kinerja_bidang_pengabdian",  inverse_name="bkd_id",  string="Kinerja bidang pengabdian",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    kinerja_kewajiban_khusus_ids = fields.One2many(comodel_name="vit.kinerja_kewajiban_khusus",  inverse_name="bkd_id",  string="Kinerja kewajiban khusus",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
