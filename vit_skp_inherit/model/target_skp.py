#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft','Draft'),('proses','Diproses'),('open','Diperiksa'),('done','Selesai'),('reject','Ditolak')]
from odoo import models, fields, api, _
import time
import datetime
from odoo.exceptions import UserError, Warning

class targetskp(models.Model):

	_name = "vit.target_skp"
	_description = "vit.target_skp"
	name = fields.Char( required=True, default="Baru", readonly=True,  string="Name",  help="")
	state = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",  help="")
	tanggal = fields.Date( string="Tanggal",  readonly=True, states={"draft" : [("readonly",False)]}, default=lambda self:time.strftime("%Y-%m-%d"), help="")
	pns_id = fields.Many2one(comodel_name="hr.employee",  string="Pns",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
	pns_nip = fields.Char( string="Pns nip", related='pns_id.nip', readonly=True, help="")
	pns_pangkat_gol_ruang = fields.Char( comodel_name="hr.employee", string="Pns pangkat gol ruang", related='pns_id.pangkat_gol_ruang', readonly=True, states={"draft" : [("readonly",True)]})
	pns_jabatan_id = fields.Many2one(comodel_name="vit.jabatan",  string="Pns jabatan", related='pns_id.jabatan_id', readonly=True, states={"draft" : [("readonly",True)]})
	pns_unit_kerja_id = fields.Many2one(comodel_name="vit.unit_kerja",  string="Pns unit kerja" , related='pns_id.unit_kerja_id',  readonly=True, states={"draft" : [("readonly",True)]})
	pejabat_penilai_id = fields.Many2one(comodel_name="hr.employee",  string="Pejabat penilai",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
	pejabat_penilai_nip = fields.Char( string="Pejabat penilai nip", related='pejabat_penilai_id.nip', readonly=True, help="")
	pejabat_penilai_pangkat_gol_ruang = fields.Char( comodel_name="hr.employee", string="Pejabat penilai pangkat gol ruang", related='pejabat_penilai_id.pangkat_gol_ruang', readonly=True, states={"draft" : [("readonly",True)]})
	pejabat_penilai_jabatan_id = fields.Many2one(comodel_name="vit.jabatan",  string="Pejabat penilai jabatan", related='pejabat_penilai_id.jabatan_id', readonly=True, states={"draft" : [("readonly",True)]})
	pejabat_penilai_unit_kerja_id = fields.Many2one(comodel_name="vit.unit_kerja",  string="Pejabat penilai unit kerja" , related='pejabat_penilai_id.unit_kerja_id',  readonly=True, states={"draft" : [("readonly",True)]})
	def action_print_pengukuran(self, ):
		pass


	def action_print_penilaian(self, ):
		pass


	def action_print_skp(self, ):
		pass


	def action_hitung_rekapitulasi(self, ):
		pass

	tahun_akademik_id = fields.Many2one(comodel_name="vit.tahun_akademik",  string="Tahun akademik",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
	target_val_ids = fields.One2many(comodel_name="vit.skp_target_val",  inverse_name="target_skp_id",  string="Rincian Target", readonly=True, states={"draft" : [("readonly",False)],"proses" : [("readonly",False)]},  help="")
	jumlah_nilai = fields.Float(string='Jumlah',
		store=True, readonly=True, compute='_compute_nilai', track_visibility='always')
	nilai_capaian_skp = fields.Float(string='Nilai Capaian SKP',
		store=True, readonly=True, compute='_compute_nilai', track_visibility='always')
	
	@api.model
	def create(self, vals):
		if not vals.get("name", False) or vals["name"] == "New":
			vals["name"] = self.env["ir.sequence"].next_by_code("vit.target_skp") or "Error Number!!!"
		return super(targetskp, self).create(vals)

	@api.multi
	def action_confirm(self):
		self.state = STATES[2][0]

	@api.multi
	def action_done(self):
		self.state = STATES[3][0]

	def action_reject(self):
		self.state = STATES[4][0]

	@api.multi
	def action_draft(self):
		self.state = STATES[0][0]

	@api.multi
	def unlink(self):
		for me_id in self :
			if me_id.state != STATES[0][0]:
				raise UserError("Cannot delete non draft record!")
		return super(targetskp, self).unlink()

	@api.multi
	def action_realisasi(self):
		# import pdb; pdb.set_trace()
		if ((self.pns_id.id==False) or (self.pejabat_penilai_id.id==False) or (self.tahun_akademik_id.id==False)):
			raise UserError("Pns, Pejabat Penilai dan Tahun Akademik tidak boleh kosong!")

		skp = self.env['vit.skp'].search([('pns_id','=',self.pns_id.id),('pejabat_penilai_id','=',self.pejabat_penilai_id.id),('tahun_akademik_id','=',self.tahun_akademik_id.id),('state','=','done')])
		if not skp:
			raise UserError(("SKP untuk %s belum dibuat atau belum disetujui!") % (self.pns_id.name))
		else:
			cr = self.env.cr
			sql = """
					select sum(kul.ak_jumlah), sum(kul.sks_riil)
					from vit_skp skp
					left join vit_skp_rekapitulasi_perkuliahan kul on kul.skp_id = skp.id
					left join hr_employee pns on skp.pns_id = pns.id
					left join hr_employee pjb on skp.pejabat_penilai_id = pjb.id
					left join vit_tahun_akademik tak on skp.tahun_akademik_id = tak.id
					where pns.id = %s and pjb.id = %s and tak.id = %s and skp.state = 'done'
					"""
			# import pdb; pdb.set_trace()
			cr.execute(sql, (self.pns_id.id, self.pejabat_penilai_id.id, self.tahun_akademik_id.id))
			result = cr.fetchall()
			for res in result:
				cr.execute("update vit_skp_target_val set real_ak=%s, real_kuantitas=%s where name='perkuliahan' and target_skp_id = %s",( res[0],res[1],self.id, ))
			
			sql1 = """
					select sum(sem.ak), sum(sem.semester_id)
					from vit_skp skp
					left join vit_skp_seminar sem on sem.skp_id = skp.id
					left join hr_employee pns on skp.pns_id = pns.id
					left join hr_employee pjb on skp.pejabat_penilai_id = pjb.id
					left join vit_tahun_akademik tak on skp.tahun_akademik_id = tak.id
					where pns.id = %s and pjb.id = %s and tak.id = %s and skp.state = 'done'
					"""
			cr.execute(sql1, (self.pns_id.id, self.pejabat_penilai_id.id, self.tahun_akademik_id.id))
			result1 = cr.fetchall()
			for res1 in result1:
				cr.execute("update vit_skp_target_val set real_ak=%s, real_kuantitas=%s where name='seminar' and target_skp_id = %s",( res1[0],res1[1],self.id, ))

			sql2 = """
					select sum(kkn.ak), sum(kkn.jumlah)
					from vit_skp skp
					left join vit_skp_kkn_pkn_pkl kkn on kkn.skp_id = skp.id
					left join hr_employee pns on skp.pns_id = pns.id
					left join hr_employee pjb on skp.pejabat_penilai_id = pjb.id
					left join vit_tahun_akademik tak on skp.tahun_akademik_id = tak.id
					where pns.id = %s and pjb.id = %s and tak.id = %s and skp.state = 'done'
					"""
			cr.execute(sql2, (self.pns_id.id, self.pejabat_penilai_id.id, self.tahun_akademik_id.id))
			result2 = cr.fetchall()
			for res2 in result2:
				cr.execute("update vit_skp_target_val set real_ak=%s, real_kuantitas=%s where name='kkn_pkn_pkl' and target_skp_id = %s",( res2[0],res2[1],self.id, ))

			sql3 = """
					select sum(dis.ak_total), sum(dis.jumlah_lulusan_pembimbing_utama), sum(dis.jumlah_lulusan_pembimbing_pembantu)
					from vit_skp_disertasi dis
					left join vit_skp skp on dis.skp_id = skp.id
					left join hr_employee pns on skp.pns_id = pns.id
					left join hr_employee pjb on skp.pejabat_penilai_id = pjb.id
					left join vit_tahun_akademik tak on skp.tahun_akademik_id = tak.id
					where pns.id = %s and pjb.id = %s and tak.id = %s and skp.state = 'done'
					"""
			cr.execute(sql3, (self.pns_id.id, self.pejabat_penilai_id.id, self.tahun_akademik_id.id))
			result3 = cr.fetchall()
			for res3 in result3:
				if res3[1] or res3[2]:
					cr.execute("update vit_skp_target_val set real_ak=%s, real_kuantitas=%s where name='disertasi_thesis_skripsi' and target_skp_id = %s",( res3[0],(res3[1]+res3[2]),self.id, ))

			sql4 = """
					select sum(uji.ak_total), sum(uji.jumlah_mhs_ketua_penguji), sum(uji.jumlah_mhs_anggota_penguji)
					from vit_skp skp
					left join vit_skp_penguji uji on uji.skp_id = skp.id
					left join hr_employee pns on skp.pns_id = pns.id
					left join hr_employee pjb on skp.pejabat_penilai_id = pjb.id
					left join vit_tahun_akademik tak on skp.tahun_akademik_id = tak.id
					where pns.id = %s and pjb.id = %s and tak.id = %s and skp.state = 'done'
					"""
			cr.execute(sql4, (self.pns_id.id, self.pejabat_penilai_id.id, self.tahun_akademik_id.id))
			result4 = cr.fetchall()
			for res4 in result4:
				if res4[1] or res4[2]:
					cr.execute("update vit_skp_target_val set real_ak=%s, real_kuantitas=%s where name='penguji' and target_skp_id = %s",( res4[0],(res4[1]+res4[2]),self.id, ))

			sql5 = """
					select sum(bna.ak), sum(bna.jumlah)
					from vit_skp skp
					left join vit_skp_membina bna on bna.skp_id = skp.id
					left join hr_employee pns on skp.pns_id = pns.id
					left join hr_employee pjb on skp.pejabat_penilai_id = pjb.id
					left join vit_tahun_akademik tak on skp.tahun_akademik_id = tak.id
					where pns.id = %s and pjb.id = %s and tak.id = %s and skp.state = 'done'
					"""
			cr.execute(sql5, (self.pns_id.id, self.pejabat_penilai_id.id, self.tahun_akademik_id.id))
			result5 = cr.fetchall()
			for res5 in result5:
				cr.execute("update vit_skp_target_val set real_ak=%s, real_kuantitas=%s where name='membina' and target_skp_id = %s",( res5[0],res5[1],self.id, ))

			sql6 = """
					select sum(mpk.ak), sum(mpk.jumlah)
					from vit_skp skp
					left join vit_skp_mengembangkan_program_kuliah mpk on mpk.skp_id = skp.id
					left join hr_employee pns on skp.pns_id = pns.id
					left join hr_employee pjb on skp.pejabat_penilai_id = pjb.id
					left join vit_tahun_akademik tak on skp.tahun_akademik_id = tak.id
					where pns.id = %s and pjb.id = %s and tak.id = %s and skp.state = 'done'
					"""
			cr.execute(sql6, (self.pns_id.id, self.pejabat_penilai_id.id, self.tahun_akademik_id.id))
			result6 = cr.fetchall()
			for res6 in result6:
				cr.execute("update vit_skp_target_val set real_ak=%s, real_kuantitas=%s where name='mengembangkan_program_kuliah' and target_skp_id = %s",( res6[0],res6[1],self.id, ))

			sql7 = """
					select sum(mbk.ak), sum(mbk.naskah)
					from vit_skp skp
					left join vit_skp_rekapitulasi_mengembangkan_bahan_kuliah mbk on mbk.skp_id = skp.id
					left join hr_employee pns on skp.pns_id = pns.id
					left join hr_employee pjb on skp.pejabat_penilai_id = pjb.id
					left join vit_tahun_akademik tak on skp.tahun_akademik_id = tak.id
					where pns.id = %s and pjb.id = %s and tak.id = %s and skp.state = 'done'
					"""
			cr.execute(sql7, (self.pns_id.id, self.pejabat_penilai_id.id, self.tahun_akademik_id.id))
			result7 = cr.fetchall()
			for res7 in result7:
				cr.execute("update vit_skp_target_val set real_ak=%s, real_kuantitas=%s where name='mengembangkan_bahan_kuliah' and target_skp_id = %s",( res7[0],res7[1],self.id, ))

			sql8 = """
					select sum(oil.ak), sum(oil.jumlah)
					from vit_skp skp
					left join vit_skp_orasi_ilmiah oil on oil.skp_id = skp.id
					left join hr_employee pns on skp.pns_id = pns.id
					left join hr_employee pjb on skp.pejabat_penilai_id = pjb.id
					left join vit_tahun_akademik tak on skp.tahun_akademik_id = tak.id
					where pns.id = %s and pjb.id = %s and tak.id = %s and skp.state = 'done'
					"""
			cr.execute(sql8, (self.pns_id.id, self.pejabat_penilai_id.id, self.tahun_akademik_id.id))
			result8 = cr.fetchall()
			for res8 in result8:
				cr.execute("update vit_skp_target_val set real_ak=%s, real_kuantitas=%s where name='orasi_ilmiah' and target_skp_id = %s",( res8[0],res8[1],self.id, ))

			sql9 = """
					select sum(jpt.jumlah_angka_kredit), sum(jpt.satuan_hasil)
					from vit_skp skp
					left join vit_skp_rekapitulasi_jabatan_pt jpt on jpt.skp_id = skp.id
					left join hr_employee pns on skp.pns_id = pns.id
					left join hr_employee pjb on skp.pejabat_penilai_id = pjb.id
					left join vit_tahun_akademik tak on skp.tahun_akademik_id = tak.id
					where pns.id = %s and pjb.id = %s and tak.id = %s and skp.state = 'done'
					"""
			cr.execute(sql9, (self.pns_id.id, self.pejabat_penilai_id.id, self.tahun_akademik_id.id))
			result9 = cr.fetchall()
			for res9 in result9:
				cr.execute("update vit_skp_target_val set real_ak=%s, real_kuantitas=%s where name='jabatan_pt' and target_skp_id = %s",( res9[0],res9[1],self.id, ))

			sql10 = """
					select sum(bim.ak), sum(bim.jumlah)
					from vit_skp skp
					left join vit_skp_membimbing_dosen bim on bim.skp_id = skp.id
					left join hr_employee pns on skp.pns_id = pns.id
					left join hr_employee pjb on skp.pejabat_penilai_id = pjb.id
					left join vit_tahun_akademik tak on skp.tahun_akademik_id = tak.id
					where pns.id = %s and pjb.id = %s and tak.id = %s and skp.state = 'done'
					"""
			cr.execute(sql10, (self.pns_id.id, self.pejabat_penilai_id.id, self.tahun_akademik_id.id))
			result10 = cr.fetchall()
			for res10 in result10:
				cr.execute("update vit_skp_target_val set real_ak=%s, real_kuantitas=%s where name='membimbing_dosen' and target_skp_id = %s",( res10[0],res10[1],self.id, ))

			sql11 = """
					select sum(det.ak), sum(det.jumlah)
					from vit_skp skp
					left join vit_skp_detasering det on det.skp_id = skp.id
					left join hr_employee pns on skp.pns_id = pns.id
					left join hr_employee pjb on skp.pejabat_penilai_id = pjb.id
					left join vit_tahun_akademik tak on skp.tahun_akademik_id = tak.id
					where pns.id = %s and pjb.id = %s and tak.id = %s and skp.state = 'done'
					"""
			cr.execute(sql11, (self.pns_id.id, self.pejabat_penilai_id.id, self.tahun_akademik_id.id))
			result11 = cr.fetchall()
			for res11 in result11:
				cr.execute("update vit_skp_target_val set real_ak=%s, real_kuantitas=%s where name='detasering' and target_skp_id = %s",( res11[0],res11[1],self.id, ))

			sql12 = """
					select  sum(pd.jumlah_ak), sum(pd.jumlah)
					from vit_skp skp
					left join vit_skp_pengembangan_diri pd on pd.skp_id = skp.id
					left join hr_employee pns on skp.pns_id = pns.id
					left join hr_employee pjb on skp.pejabat_penilai_id = pjb.id
					left join vit_tahun_akademik tak on skp.tahun_akademik_id = tak.id
					where pns.id = %s and pjb.id = %s and tak.id = %s and skp.state = 'done'
					"""
			cr.execute(sql12, (self.pns_id.id, self.pejabat_penilai_id.id, self.tahun_akademik_id.id))
			result12 = cr.fetchall()
			for res12 in result12:
				cr.execute("update vit_skp_target_val set real_ak=%s, real_kuantitas=%s where name='pengembangan_diri' and target_skp_id = %s",( res12[0],res12[1],self.id, ))

			sql13 = """
					select sum(plt.ak_jumlah), sum(plt.jumlah_peneliti_mandiri), sum(plt.jumlah_peneliti_utama), sum(plt.jumlah_peneliti_anggota)
					from vit_skp skp
					left join vit_skp_penelitian plt on plt.skp_id = skp.id
					left join hr_employee pns on skp.pns_id = pns.id
					left join hr_employee pjb on skp.pejabat_penilai_id = pjb.id
					left join vit_tahun_akademik tak on skp.tahun_akademik_id = tak.id
					where pns.id = %s and pjb.id = %s and tak.id = %s and skp.state = 'done'
					"""
			cr.execute(sql13, (self.pns_id.id, self.pejabat_penilai_id.id, self.tahun_akademik_id.id))
			result13 = cr.fetchall()
			for res13 in result13:
				if res13[1] or res13[2] or res13[3]:
					jumlah_plt = res13[1]+res13[2]+res13[3]
					cr.execute("update vit_skp_target_val set real_ak=%s, real_kuantitas=%s where name='penelitian' and target_skp_id = %s",( res13[0],jumlah_plt,self.id, ))

			sql14 = """
					select  sum(abd.ak_jumlah), sum(abd.jumlah_program)
					from vit_skp skp
					left join vit_skp_pengabdian abd on abd.skp_id = skp.id
					left join hr_employee pns on skp.pns_id = pns.id
					left join hr_employee pjb on skp.pejabat_penilai_id = pjb.id
					left join vit_tahun_akademik tak on skp.tahun_akademik_id = tak.id
					where pns.id = %s and pjb.id = %s and tak.id = %s and skp.state = 'done'
					"""
			cr.execute(sql14, (self.pns_id.id, self.pejabat_penilai_id.id, self.tahun_akademik_id.id))
			result14 = cr.fetchall()
			for res14 in result14:
				cr.execute("update vit_skp_target_val set real_ak=%s, real_kuantitas=%s where name='pengabdian' and target_skp_id = %s",( res14[0],res14[1],self.id, ))

			sql15 = """
					select  sum(tgs.ak), sum(tgs.jumlah)
					from vit_skp skp
					left join vit_skp_tugas_tambahan tgs on tgs.skp_id = skp.id
					left join hr_employee pns on skp.pns_id = pns.id
					left join hr_employee pjb on skp.pejabat_penilai_id = pjb.id
					left join vit_tahun_akademik tak on skp.tahun_akademik_id = tak.id
					where pns.id = %s and pjb.id = %s and tak.id = %s and skp.state = 'done'
					"""
			cr.execute(sql15, (self.pns_id.id, self.pejabat_penilai_id.id, self.tahun_akademik_id.id))
			result15 = cr.fetchall()
			for res15 in result15:
				cr.execute("update vit_skp_target_val set real_ak=%s, real_kuantitas=%s where name='tugas_tambahan' and target_skp_id = %s",( res15[0],res15[1],self.id, ))

			self.state = STATES[1][0]

	@api.one
	@api.depends('target_val_ids.nilai_capaian')
	def _compute_nilai(self):
		self.jumlah_nilai = sum(line.nilai_capaian for line in self.target_val_ids)
		i = 0
		for line in self.target_val_ids:
			i += 1
			self.nilai_capaian_skp = self.jumlah_nilai / i


class skp_target_val(models.Model):
	_name = "vit.skp_target_val"
	_description = "vit.skp_target_val"

	name = fields.Selection(
			selection=[ ('perkuliahan', 'Perkuliahan'),
						('seminar', 'Seminar'),
						('kkn_pkn_pkl', 'Kkn pkn pkl'),
						('disertasi_thesis_skripsi', 'Disertasi thesis skripsi'),
						('penguji', 'Penguji'),
						('membina', 'Membina'),
						('mengembangkan_program_kuliah', 'Mengembangkan program kuliah'),
						('mengembangkan_bahan_kuliah', 'Mengembangkan bahan kuliah'),
						('orasi_ilmiah', 'Orasi ilmiah'),
						('jabatan_pt', 'Jabatan pt'),
						('membimbing_dosen', 'Membimbing dosen'),
						('detasering', 'Detasering'),
						('pengembangan_diri', 'Pengembangan diri'),
						('penelitian', 'Penelitian'),
						('pengabdian', 'Pengabdian'),
						('tugas_tambahan', 'Tugas Tambahan') ],
			required=True, string="Nama",  help="")
	company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string="Company Currency", readonly=True)
	company_id = fields.Many2one('res.company', string='Company', change_default=True,
		required=True, default=lambda self: self.env['res.company']._company_default_get('account.invoice'))

	target_ak = fields.Float( string="Target AK")
	target_kuantitas = fields.Integer( string="Target Kuantitas/Output", default=0)
	target_satuan_kuant = fields.Char(string="Satuan Kuantitas/Output")
	target_kualitas = fields.Integer( string="Target Kualitas", default=0)
	target_waktu = fields.Integer( string="Target Waktu", default=0)
	target_satuan_waktu = fields.Char(string="Target Satuan Waktu")    
	target_biaya = fields.Monetary('Target Biaya', currency_field='company_currency_id', default=0.0)

	real_ak = fields.Float( string="Realisasi AK")
	real_kuantitas = fields.Integer( string="Realisasi Kuantitas/Output", default=0)
	real_satuan_kuant = fields.Char(string="Satuan Kuantitas/Output")
	real_kualitas = fields.Integer( string="Realisasi Kualitas", default=0)
	real_waktu = fields.Integer( string="Realisasi Waktu", default=0)
	real_satuan_waktu = fields.Char(string="Satuan Waktu")
	real_biaya = fields.Monetary('Realisasi Biaya', currency_field='company_currency_id', default=0.0)

	penghitungan = fields.Float('Penghitungan', compute='compute_nilai', store=True,)
	nilai_capaian = fields.Float('Nilai Capaian SKP', compute='compute_nilai', store=True,)

	target_skp_id = fields.Many2one('vit.target_skp', string='Target SKP')

	@api.onchange('target_satuan_kuant')
	def onchange_satuan_kuant(self):
		if self.target_satuan_kuant:
			self.real_satuan_kuant = self.target_satuan_kuant

	@api.onchange('target_satuan_waktu')
	def onchange_satuan_waktu(self):
		if self.target_satuan_waktu:
			self.real_satuan_waktu = self.target_satuan_waktu

	@api.depends('real_kuantitas','target_kuantitas','real_kualitas','target_kualitas','target_waktu','real_waktu')
	def compute_nilai(self):
		kuan = 0
		kual = 0
		waktu = 0
		biaya = 0
		for val in self:
			if val.target_kuantitas != 0:                    
				kuan = (val.real_kuantitas / val.target_kuantitas) * 100
			if val.target_kualitas != 0:
				kual = (val.real_kualitas / val.target_kualitas) * 100
			if val.target_waktu != 0:
				waktu = (((1.76 * val.target_waktu) - val.real_waktu) / val.target_waktu) * 100
			if val.target_biaya != 0.0:
				biaya = (((1.76 * val.target_biaya) - val.real_biaya) / val.target_biaya) * 100            
			# import pdb; pdb.set_trace()           
			val.penghitungan = kuan + kual + waktu + biaya
			val.nilai_capaian = val.penghitungan / 3
