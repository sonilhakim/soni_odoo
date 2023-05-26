#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class kinerja_kewajiban_khusus(models.Model):
	_name = "vit.kinerja_kewajiban_khusus"
	_inherit = "vit.kinerja_kewajiban_khusus"

	@api.model
	def year_selection(self):
		year = 2000 # replace 2000 with your a start year
		year_list = []
		while year != 2100: # replace 2030 with your end year
			year_list.append((str(year), str(year)))
			year += 1
		return year_list	

	tahun = fields.Selection( selection="year_selection", string="Tahun")
	ceklist_asesor = fields.Selection([('memenuhi','Memenuhi'),('tidak_memenuhi','Tidak Memenuhi')],'Ceklist Asesor')

	nama_jurnal = fields.Char( string="Nama Jurnal", help="")
	volume_nomor = fields.Integer( string="Volume, Nomor", help="")
	impact_factor = fields.Char( string="Impact Factor", help="")
	alamat_url = fields.Char( string="Alamat URL",  help="")

	nama_seminar = fields.Char( string="Nama Seminar", help="")
	tempat_seminar = fields.Char( string="Tempat Seminar", help="")
	penyelenggara = fields.Char( string="Penyelenggara", help="")

	bahasa_jurnal = fields.Selection([('indonesia','Indonesia'),('arab','Arab'),('inggris','Inggris'),('perancir','Perancis'),('rusia','Rusia'),('spanyol','Spanyol'),('tiongkok','Tiongkok')], string="Bahasa Jurnal", help="")
	akreditasi = fields.Selection([('a','A'),('b','B')],'Akreditasi')
	status_doaj = fields.Selection([('tidak_terindeks','Tidak Terindeks'),('green_thick','Green Thick')],'Status DOAJ')
	
	terindeks = fields.Selection([('sinta','Sinta'),('arjuna','Arjuna')],'Terindeks')
	standart_tatakelola = fields.Selection([('q1','Q1'),('q2','Q2'),('q3','Q3'),('q4','Q4'),('q5','Q5'),('q6','Q6')],'Standart Tatakelola')
	
	jenis_hki = fields.Selection([('nasional','Nasional'),('internasional','Internasional')],'Jenis HKI')
	no_sertifikat = fields.Char( string="No. Sertifikat",  help="")

	lingkup_kegiatan = fields.Selection([('nasional','Nasional'),('internasional','Internasional')],'Lingkup Kegiatan')
	tempat_publikasi = fields.Char( string="Tempat Publikasi",  help="")	
	
	artikel = fields.Binary( string="Artikel",  help="")
	cover_depan = fields.Binary( string="Cover Depan",  help="")
	daftar_isi = fields.Binary( string="Daftar Isi",  help="")
	sertifikat = fields.Binary( string="Sertifikat",  help="")
	deskripsi_paten = fields.Binary( string="Deskripsi Paten",  help="")
	bukti_karya = fields.Binary( string="Bukti Karya",  help="")
	peer_reviewer = fields.Binary( string="Peer Riviewer",  help="")
	lain_lain = fields.Binary( string="Lain-Lain",  help="")

	jenis_karya_id = fields.Many2one(comodel_name="vit.jenis_karya",  string="Jenis Karya",  help="")
	jenis_karya_name = fields.Char(related="jenis_karya_id.name",  string="nama Jenis Karya",  help="")
	# kinerja_sks_persen = fields.Float( string="Kinerja sks persen", compute="compute_sks", store=True, help="")

	# @api.depends("beban_sks","kinerja_sks")
	# def compute_sks(self):
	# 	for kinerja in self:
	# 		if kinerja.beban_sks != 0:
	# 			kinerja.kinerja_sks_persen = (kinerja.kinerja_sks / kinerja.beban_sks) * 100
	