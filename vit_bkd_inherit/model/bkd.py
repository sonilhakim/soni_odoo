#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft','Draft'),('open','Diperiksa Sesprodi'),('valid','BKD'),('asesor1','Diperiksa Asesor1'),('asesor2','Diperiksa Asesor2'),('done','Valid')]
from odoo import models, fields, api, _
import time
from odoo.exceptions import UserError, Warning

class bkd(models.Model):
    _name = "vit.bkd"
    _inherit = ['vit.bkd','portal.mixin', 'mail.thread', 'mail.activity.mixin']

    @api.model
    def year_selection(self):
        year = 2000 # replace 2000 with your a start year
        year_list = []
        while year != 2100: # replace 2030 with your end year
            year_list.append((str(year), str(year)))
            year += 1
        return year_list    

    name = fields.Char( required=True, default="Baru", readonly=True,  string="Name",  help="")
    state = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",  help="")
    date = fields.Date( string="Tanggal",  readonly=True, default=lambda self: time.strftime("%Y-%m-%d"), states={"draft" : [("readonly",False)]},  help="")
    no_sertifikat = fields.Char( comodel_name="hr.employee", string="No. Sertifikat", related='employee_id.nomor_sertifikat', readonly=True,  help="")
    file_sertifikat = fields.Binary( string="File Sertifikat",  help="")
    nip = fields.Char( comodel_name="hr.employee", string="Nip", related='employee_id.nip', readonly=True, states={"draft" : [("readonly",True)]},  help="")
    nidn = fields.Char( comodel_name="hr.employee", string="Nidn", related='employee_id.nidn', readonly=True, states={"draft" : [("readonly",True)]},  help="")
    s1 = fields.Char( string="S1", related='employee_id.s1',  readonly=True, states={"draft" : [("readonly",True)]},  help="")
    s2 = fields.Char( string="S2", related='employee_id.s2',  readonly=True, states={"draft" : [("readonly",True)]},  help="")
    s3 = fields.Char( string="S3", related='employee_id.s3',  readonly=True, states={"draft" : [("readonly",True)]},  help="")
    bidang_ilmu = fields.Char( string="Bidang ilmu", related='employee_id.bidang_ilmu',  readonly=True, states={"draft" : [("readonly",True)]}, store=True, help="")
    gelar_depan = fields.Char( string="Gelar Depan", related='employee_id.gelar_depan',  readonly=True, help="")
    gelar_belakang = fields.Char( string="Gelar Belakang", related='employee_id.gelar_belakang',  readonly=True, help="")
    mobile = fields.Char( comodel_name="hr.employee", string="Mobile", related='employee_id.mobile_phone', readonly=True, states={"draft" : [("readonly",True)]}, store=True, help="")
    email = fields.Char( comodel_name="hr.employee", string="Email", related='employee_id.work_email', readonly=True, states={"draft" : [("readonly",True)]}, store=True, help="")
    ktp = fields.Binary( string="KTP",  help="")
    is_bkd = fields.Boolean( string="BKD",  help="")

    institusi_id = fields.Many2one(comodel_name="res.company",  string="Institusi", related='employee_id.company_id', readonly=True, states={"draft" : [("readonly",True)]}, store=True, help="")
    status_dosen_id = fields.Many2one(comodel_name="vit.status_dosen", related='employee_id.status_dosen_id', string="Status dosen",  readonly=True, states={"draft" : [("readonly",True)]}, store=True,  help="")
    jabatan_fungsional_id = fields.Many2one(comodel_name="vit.jabatan", related='employee_id.jabatanf_id', string="Jabatan fungsional",  readonly=True, states={"draft" : [("readonly",True)]}, store=True, help="")
    jabatan_fungsional_name = fields.Char(related="jabatan_fungsional_id.name", string="Nama Jabatan fungsional",  readonly=True, store=True, help="")
    fakultas_id = fields.Many2one(comodel_name="vit.fakultas",  string="Fakultas", related='employee_id.fakultas_id', readonly=True, states={"draft" : [("readonly",True)]}, store=True,  help="")
    jurusan_id = fields.Many2one(comodel_name="vit.jurusan",  string="Jurusan", related='employee_id.jurusan_id', readonly=True, states={"draft" : [("readonly",True)]}, store=True, help="")
    program_studi_id = fields.Many2one(comodel_name="vit.program_studi", related='employee_id.program_studi_id', string="Program studi",  readonly=True, states={"draft" : [("readonly",True)]}, store=True, help="")
    golongan_id = fields.Many2one(comodel_name="vit.golongan",  string="Golongan", related='employee_id.golongan_id', readonly=True, states={"draft" : [("readonly",True)]}, store=True, help="")

    employee_id = fields.Many2one(comodel_name="hr.employee",  string="Karyawan",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    asesor1_id = fields.Many2one(comodel_name="hr.employee",  string="Asesor1",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    asesor2_id = fields.Many2one(comodel_name="hr.employee",  string="Asesor2",  readonly=True, states={"draft" : [("readonly",False)]},  help="")

    kinerja_bidang_pendidikan_ids = fields.One2many(comodel_name="vit.kinerja_bidang_pendidikan",  inverse_name="bkd_id",  string="Kinerja bidang pendidikan",  readonly=False, states={"done" : [("readonly",True)]},  help="")
    kinerja_bidang_penelitian_ids = fields.One2many(comodel_name="vit.kinerja_bidang_penelitian",  inverse_name="bkd_id",  string="Kinerja bidang penelitian",  readonly=False, states={"done" : [("readonly",True)]},  help="")
    kinerja_bidang_pengabdian_ids = fields.One2many(comodel_name="vit.kinerja_bidang_pengabdian",  inverse_name="bkd_id",  string="Kinerja bidang pengabdian",  readonly=False, states={"done" : [("readonly",True)]},  help="")
    kinerja_kewajiban_khusus_ids = fields.One2many(comodel_name="vit.kinerja_kewajiban_khusus",  inverse_name="bkd_id",  string="Kinerja kewajiban khusus",  readonly=False, states={"done" : [("readonly",True)]},  help="")
    kinerja_penunjang_ids = fields.One2many(comodel_name="vit.kinerja_penunjang",  inverse_name="bkd_id",  string="Kinerja penunjang lainnya",  readonly=False, states={"done" : [("readonly",True)]},  help="")

    periode_dari = fields.Selection( selection="year_selection", string="Periode Tahun dari")
    periode_sampai = fields.Char(compute="compute_sampai", string="Periode Tahun sampai")

    @api.model
    def create(self, vals):
        if not vals.get("name", False) or vals["name"] == "New":
            vals["name"] = self.env["ir.sequence"].next_by_code("vit.bkd") or "Error Number!!!"
        return super(bkd, self).create(vals)

    def action_confirm_rkd(self):
        self.state = STATES[1][0]

    def action_valid_rkd(self):
        self.is_bkd = True
        self.state = STATES[2][0]

    def action_novalid_rkd(self):
        self.state = STATES[0][0]

    def action_confirm_bkd(self):
        self.state = STATES[3][0]

    def action_asesor(self):
        self.state = STATES[4][0]

    def action_novalid_bkd(self):
        self.state = STATES[2][0]

    def action_done(self):
        self.state = STATES[5][0]

    def action_nodone_bkd(self):
        self.state = STATES[2][0]

    def action_draft(self):
        self.is_bkd = False
        self.state = STATES[0][0]

    @api.multi
    def unlink(self):
        for me_id in self :
            if me_id.state != STATES[0][0]:
                raise UserError("Cannot delete non draft record!")
        return super(bkd, self).unlink()
    
    @api.one
    @api.depends('asesor1_id','asesor2_id')
    def _get_current_user(self):
        # self.current_user = (self.env.user.id == self.asesor1_id.user_id.id)
        if self.env.user.id == self.asesor1_id.user_id.id:
            self.current_user1 = True

        if self.env.user.id == self.asesor2_id.user_id.id:
            self.current_user2 = True

    current_user1 = fields.Boolean('is current user1 ?', compute='_get_current_user')
    current_user2 = fields.Boolean('is current user2 ?', compute='_get_current_user')

    @api.depends("periode_dari")
    def compute_sampai(self):
        if self.periode_dari:
            periode_sampai = int(self.periode_dari) + 2

            self.periode_sampai = str(periode_sampai)