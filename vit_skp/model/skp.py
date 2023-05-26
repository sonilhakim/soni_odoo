#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft','Draft'),('open','Diperiksa'),('done','Selesai')]
from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class skp(models.Model):

    _name = "vit.skp"
    _description = "vit.skp"
    name = fields.Char( required=True, default="New", readonly=True,  string="Name",  help="")
    state = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",  help="")
    jumlah_10_sks_pertama = fields.Float( string="Jumlah 10 sks pertama",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    jumlah_sks_berikutnya = fields.Float( string="Jumlah sks berikutnya",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    tanggal = fields.Date( string="Tanggal",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    pns_nip = fields.Char( string="Pns nip",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    pns_pangkat_gol_ruang = fields.Char( string="Pns pangkat gol ruang",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    pejabat_penilai_nip = fields.Char( string="Pejabat penilai nip",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    pejabat_penilai_pangkat_gol_ruang = fields.Char( string="Pejabat penilai pangkat gol ruang",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    lokasi = fields.Char( string="Lokasi",  readonly=True, states={"draft" : [("readonly",False)]},  help="")


    def action_print_pengukuran(self, ):
        pass


    def action_print_penilaian(self, ):
        pass


    def action_print_skp(self, ):
        pass


    def action_hitung_rekapitulasi(self, ):
        pass


    tahun_akademik_id = fields.Many2one(comodel_name="vit.tahun_akademik",  string="Tahun akademik",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    pns_id = fields.Many2one(comodel_name="hr.employee",  string="Pns",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    pejabat_penilai_id = fields.Many2one(comodel_name="hr.employee",  string="Pejabat penilai",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    pns_jabatan_id = fields.Many2one(comodel_name="vit.jabatan",  string="Pns jabatan",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    pns_unit_kerja_id = fields.Many2one(comodel_name="vit.unit_kerja",  string="Pns unit kerja",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    pejabat_penilai_unit_kerja_id = fields.Many2one(comodel_name="vit.unit_kerja",  string="Pejabat penilai unit kerja",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    pejabat_penilai_jabatan_id = fields.Many2one(comodel_name="vit.jabatan",  string="Pejabat penilai jabatan",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    perkuliahan_ids = fields.One2many(comodel_name="vit.skp_perkuliahan",  inverse_name="skp_id",  string="Perkuliahan",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    seminar_ids = fields.One2many(comodel_name="vit.skp_seminar",  inverse_name="skp_id",  string="Seminar",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    kkn_pkn_pkl_ids = fields.One2many(comodel_name="vit.skp_kkn_pkn_pkl",  inverse_name="skp_id",  string="Kkn pkn pkl",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    disertasi_thesis_skripsi_ids = fields.One2many(comodel_name="vit.skp_disertasi",  inverse_name="skp_id",  string="Disertasi thesis skripsi",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    penguji_ids = fields.One2many(comodel_name="vit.skp_penguji",  inverse_name="skp_id",  string="Penguji",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    membina_ids = fields.One2many(comodel_name="vit.skp_membina",  inverse_name="skp_id",  string="Membina",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    mengembangkan_program_kuliah_ids = fields.One2many(comodel_name="vit.skp_mengembangkan_program_kuliah",  inverse_name="skp_id",  string="Mengembangkan program kuliah",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    mengembangkan_bahan_kuliah_ids = fields.One2many(comodel_name="vit.skp_mengembangkan_bahan_kuliah",  inverse_name="skp_id",  string="Mengembangkan bahan kuliah",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    orasi_ilmiah_ids = fields.One2many(comodel_name="vit.skp_orasi_ilmiah",  inverse_name="skp_id",  string="Orasi ilmiah",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    jabatan_pt_ids = fields.One2many(comodel_name="vit.skp_jabatan_pt",  inverse_name="skp_id",  string="Jabatan pt",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    membimbing_dosen_ids = fields.One2many(comodel_name="vit.skp_membimbing_dosen",  inverse_name="skp_id",  string="Membimbing dosen",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    detasering_ids = fields.One2many(comodel_name="vit.skp_detasering",  inverse_name="skp_id",  string="Detasering",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    pengembangan_diri_ids = fields.One2many(comodel_name="vit.skp_pengembangan_diri",  inverse_name="skp_id",  string="Pengembangan diri",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    penelitian_ids = fields.One2many(comodel_name="vit.skp_penelitian",  inverse_name="skp_id",  string="Penelitian",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    pengabdian_ids = fields.One2many(comodel_name="vit.skp_pengabdian",  inverse_name="skp_id",  string="Pengabdian",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    rekapitulasi_ids = fields.One2many(comodel_name="vit.skp_rekapitulasi_perkuliahan",  inverse_name="skp_id",  string="Rekapitulasi",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    rekapitulasi_mengembangkan_bahan_kuliah_ids = fields.One2many(comodel_name="vit.skp_rekapitulasi_mengembangkan_bahan_kuliah",  inverse_name="skp_id",  string="Rekapitulasi mengembangkan bahan kuliah",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    rekapitulasi_jabatan_pt_ids = fields.One2many(comodel_name="vit.skp_rekapitulasi_jabatan_pt",  inverse_name="skp_id",  string="Rekapitulasi jabatan pt",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
