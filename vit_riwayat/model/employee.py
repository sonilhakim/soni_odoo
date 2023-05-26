#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class employee(models.Model):

    _name = "hr.employee"
    _description = "hr.employee"

    _inherit = "hr.employee"


    riwayat_izin_belajar_ids = fields.One2many(comodel_name="vit.riwayat_izin_belajar",  inverse_name="employee_id",  string="Riwayat izin belajars",  help="")
    riwayat_tugas_belajar_ids = fields.One2many(comodel_name="vit.riwayat_tugas_belajar",  inverse_name="employee_id",  string="Riwayat tugas belajars",  help="")
    riwayat_study_lanjutan_ids = fields.One2many(comodel_name="vit.riwayat_study_lanjutan",  inverse_name="employee_id",  string="Riwayat study lanjutans",  help="")
    riwayat_membimbing_ids = fields.One2many(comodel_name="vit.riwayat_membimbing",  inverse_name="employee_id",  string="Riwayat membimbings",  help="")
    riwayat_mengajar_ids = fields.One2many(comodel_name="vit.riwayat_mengajar",  inverse_name="employee_id",  string="Riwayat mengajars",  help="")
    riwayat_beasiswa_ids = fields.One2many(comodel_name="vit.riwayat_beasiswa",  inverse_name="employee_id",  string="Riwayat beasiswas",  help="")
    riwayat_pekerjaan_ids = fields.One2many(comodel_name="vit.riwayat_pekerjaan",  inverse_name="employee_id",  string="Riwayat pekerjaans",  help="")
    riwayat_pengabdian_masyarakat_ids = fields.One2many(comodel_name="vit.riwayat_pengabdian_masyarakat",  inverse_name="employee_id",  string="Riwayat pengabdian masyarakats",  help="")
    riwayat_bkd_ids = fields.One2many(comodel_name="vit.riwayat_bkd",  inverse_name="employee_id",  string="Riwayat bkds",  help="")
    riwayat_kunjungan_ke_luar_negeri_ids = fields.One2many(comodel_name="vit.riwayat_kunjungan_ke_luar_negeri",  inverse_name="employee_id",  string="Riwayat kunjungan ke luar negeris",  help="")
    riwayat_pelatihan_ids = fields.One2many(comodel_name="vit.riwayat_pelatihan",  inverse_name="employee_id",  string="Riwayat pelatihans",  help="")
    riwayat_kepakaran_dosen_ids = fields.One2many(comodel_name="vit.riwayat_kepakaran_dosen",  inverse_name="employee_id",  string="Riwayat kepakaran dosens",  help="")
    riwayat_diklat_ids = fields.One2many(comodel_name="vit.riwayat_diklat",  inverse_name="employee_id",  string="Riwayat diklats",  help="")
    riwayat_pendidikan_ids = fields.One2many(comodel_name="vit.riwayat_pendidikan",  inverse_name="employee_id",  string="Riwayat pendidikans",  help="")
    riwayat_penghargaan_ids = fields.One2many(comodel_name="vit.riwayat_penghargaan",  inverse_name="employee_id",  string="Riwayat penghargaans",  help="")
    riwayat_seminar_ids = fields.One2many(comodel_name="vit.riwayat_seminar",  inverse_name="employee_id",  string="Riwayat seminars",  help="")
    riwayat_organisasi_pegawai_ids = fields.One2many(comodel_name="vit.riwayat_organisasi_pegawai",  inverse_name="employee_id",  string="Riwayat organisasi pegawais",  help="")
    riwayat_penelitian_karya_imliah_ids = fields.One2many(comodel_name="vit.riwayat_penelitian_karya_imliah",  inverse_name="employee_id",  string="Riwayat penelitian karya imliahs",  help="")
    riwayat_dosen_mengajar_diluar_ids = fields.One2many(comodel_name="vit.riwayat_dosen_mengajar_diluar",  inverse_name="employee_id",  string="Riwayat dosen mengajar diluars",  help="")
    riwayat_perjalanan_dinas_ids = fields.One2many(comodel_name="vit.riwayat_perjalanan_dinas",  inverse_name="employee_id",  string="Riwayat perjalanan dinass",  help="")
