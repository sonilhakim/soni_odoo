from odoo import tools
from odoo import models, fields, api
import odoo.addons.decimal_precision as dp
import time
import logging
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)
CASHFLOW_STATES =[('draft','Draft'),('open','Verifikasi'), ('reject','Ditolak'),
				 ('done','Disetujui')]


class cashflow_coa(models.Model):
	_name 		= 'anggaran.cashflow.coa'

	code		= fields.Char('Code')
	parent_id	= fields.Many2one('anggaran.cashflow.coa', 'Parent')
	name		= fields.Char('Name')

class cashflow(models.Model):
	_name 		= 'anggaran.cashflow'

	name				= fields.Char('No', default= '/', required=True)
	tanggal				= fields.Date('Tanggal', default=lambda self: time.strftime("%Y-%m-%d"))
	fakultas_id			= fields.Many2one(comodel_name='vit.fakultas', string='Fakultas')
	jurusan_id			= fields.Many2one(comodel_name='vit.jurusan', string='Jurusan')
	unit_id				= fields.Many2one(comodel_name='vit.unit_kerja', string='SUBSATKER', required=True)
	tahun_id			= fields.Many2one(comodel_name='account.fiscal.year', string='Tahun', required=True)
	cashflow_line_ids	= fields.One2many(comodel_name='anggaran.cashflow.line',inverse_name='cashflow_id',string='Lines', ondelete="cascade")
	state             	= fields.Selection(selection=CASHFLOW_STATES, string='Status', readonly=True ,required=True, default=CASHFLOW_STATES[0][0])
	user_id				= fields.Many2one(comodel_name='res.users', string='Create By', default=lambda self: self.env.uid)
	show_actual			= fields.Boolean('Show Actual', default=True)
	show_deviasi		= fields.Boolean('Show Deviation', default=True)
	revision			= fields.Integer('Revision')

	@api.multi
	def action_draft(self):
		#set to "draft" state
		return self.write({'state':CASHFLOW_STATES[0][0]})
	
	@api.multi
	def action_confirm(self):
		#set to "confirmed" state
		return self.write({'state':CASHFLOW_STATES[1][0]})
	
	@api.multi
	def action_reject(self):
		#set to "done" state
		return self.write({'state':CASHFLOW_STATES[2][0]})
	
	@api.multi
	def action_done(self):
		#set to "done" state
		return self.write({'state':CASHFLOW_STATES[3][0]})

	@api.model
	def create(self, vals):
		vals['name']    = self.env['ir.sequence'].next_by_code('anggaran.cashflow')
		return super(cashflow, self).create(vals)

	@api.multi
	def action_recalculate(self):
		divider = 1000

		sql = "delete from anggaran_cashflow_line where cashflow_id=%s"
		self.env.cr.execute(sql, (self.id,))

		# cf = self
		coa_obj = self.env['anggaran.cashflow.coa']
		line_obj = self.env['anggaran.cashflow.line']

		coa_ids = coa_obj.search([])

		p_line_ids = {}
		a_line_ids = {}
		v_line_ids = {}

		saldo_akhir = {}

		for m in range(1,13):

			p_total_income = 0.0
			p_total_biaya_unit = 0.0
			p_total_biaya_adm = 0.0
			p_total_pengeluaran = 0.0
			p_total_pendanaan = 0.0


			for coa in coa_obj:

				p_mfield = 0
				a_mfield = 0
				v_mfield = 0

				if coa.code == '1':
					p_mfield = saldo_akhir.get(m-1, 0)
					saldo_awal = saldo_akhir.get(m-1, 0)
				
				if coa.code == '2.1':
					if (m in range(1,5)) or (m in range(7,11)) :
						p_mfield = self.cari_bpp_mhs(self)/4
					p_total_income += p_mfield 

				if coa.code == '2.2':
					if m == 1:
						p_mfield = self.cari_spp_mhs(self) 
					p_total_income += p_mfield

				if coa.code == '2.3':
					p_mfield = self.cari_tagihan_lain(self)
					p_total_income += p_mfield

				if coa.code == '2.4':
					p_mfield = self.cari_income_lain(self)
					p_total_income += p_mfield

				if coa.code == '2.100':
					p_mfield = saldo_awal+ p_total_income


				if coa.code == '3.1':
					hasil = self.cari_bahan_habis_pakai(self, m)
					p_mfield = hasil[0]
					a_mfield = hasil[1]
					v_mfield = hasil[2]
					p_total_biaya_unit += p_mfield

				if coa.code == '3.2':
					hasil = self.cari_gaji(self, m)
					p_mfield = hasil[0]
					a_mfield = hasil[1]
					v_mfield = hasil[2]
					p_total_biaya_unit += p_mfield

				if coa.code == '3.3':
					hasil = self.cari_sewa(self, m)
					p_mfield = hasil[0]
					a_mfield = hasil[1]
					v_mfield = hasil[2]
					p_total_biaya_unit += p_mfield

				if coa.code == '3.4':
					hasil = self.cari_outsourcing(self, m)
					p_mfield = hasil[0]
					a_mfield = hasil[1]
					v_mfield = hasil[2]
					p_total_biaya_unit += p_mfield

				if coa.code == '3.5':
					hasil = self.cari_overhead(self, m)
					p_mfield = hasil[0]
					a_mfield = hasil[1]
					v_mfield = hasil[2]
					p_total_biaya_unit += p_mfield

				if coa.code == '3.100':
					p_mfield = p_total_biaya_unit 


				if coa.code == '3.6':
					p_mfield = self.cari_biaya_adm(self, m)
					p_total_pengeluaran += p_mfield

				if coa.code == '3.7':
					hasil = self.cari_investasi(self, m)
					p_mfield = hasil[0]
					a_mfield = hasil[1]
					v_mfield = hasil[2]
					p_total_pengeluaran += p_mfield

				if coa.code == '3.8':
					p_mfield = self.cari_biaya_prepaid(self, m)
					p_total_pengeluaran += p_mfield

				if coa.code == '3.9':
					p_mfield = self.cari_pajak(self,m)
					p_total_pengeluaran += p_mfield

				if coa.code == '3.10':
					hasil = self.cari_uudp(self, m)
					p_mfield = hasil[0]
					a_mfield = hasil[1]
					v_mfield = hasil[2]
					p_total_pengeluaran += p_mfield

				if coa.code == '3.11':
					p_mfield = self.cari_saving(self,m)
					p_total_pengeluaran += p_mfield

				if coa.code == '3.200':
					p_mfield = p_total_pengeluaran

				if coa.code == '3.300':
					p_mfield = saldo_awal + p_total_income - p_total_biaya_unit - p_total_pengeluaran


				if coa.code == '4.1':
					p_mfield = self.cari_pinjaman(self,m)
					p_total_pendanaan += p_mfield

				if coa.code == '4.2':
					p_mfield = self.cari_pembayaran_pinjaman(self,m)
					p_total_pendanaan += p_mfield

				if coa.code == '4.3':
					p_mfield = self.cari_bunga_pinjaman(self,m)
					p_total_pendanaan += p_mfield

				if coa.code == '4.100':
					p_mfield = p_total_pendanaan 

				if coa.code == '5':
					p_mfield =  saldo_awal + p_total_income - p_total_biaya_unit - p_total_pengeluaran + p_total_pendanaan
					saldo_akhir[m] = p_mfield


				p_data = {
					'cashflow_id' : self.id ,
					'cashflow_coa_id'	: coa.id,
					'type' : 'p',
					('m%s' % m) : p_mfield / divider,
				}
				a_data = {
					'cashflow_id' : self.id ,
					# 'cashflow_coa_id'	: coa.id,
					'type' : 'a',
					('m%s' % m) : a_mfield / divider,
				}

				v_data = {
					'cashflow_id' : self.id ,
					# 'cashflow_coa_id'	: coa.id,
					'type' : 'v',
					('m%s' % m) : v_mfield / divider,
				}

				if m == 1:
					p_line_id = line_obj.create(p_data)
					p_line_ids.update({ coa.id: p_line_id })

					if self.show_actual:
						a_line_id = line_obj.create(a_data)
						a_line_ids.update({ coa.id: a_line_id })
					if self.show_deviasi:
						v_line_id = line_obj.create(v_data)
						v_line_ids.update({ coa.id: v_line_id })

				else:
					line_obj.write(p_line_ids[ coa.id ], p_data)
					if self.show_actual:
						line_obj.write(a_line_ids[ coa.id ], a_data)
					if self.show_deviasi:
						line_obj.write(v_line_ids[ coa.id ], v_data)


		self.write({'revision':self.revision+1})
		return

	#cari dari jurusan_income total record total
	def cari_spp_mhs(self):
		jurusan_id = self.jurusan_id
		total = 0.0
		for inc in jurusan_id.income_ids:
			total += inc.total_spp
		return total 

	def cari_bpp_mhs(self):
		jurusan_id = self.jurusan_id
		total = 0.0
		for inc in jurusan_id.income_ids:
			total += inc.total_bpp
		return total 

	def cari_income_lain(self):
		total = 0.0
		return total

	def cari_tagihan_lain(self):
		total = 0.0
		return total 

	def query_rka_coa(self, cost_type_code , m):
		total_p = 0.0
		total_a = 0.0
		total_v = 0.0

		tahun = int(self.tahun_id.code)
		tahun,m = self.map_month_to_period(cr, uid, m, tahun )

		sql = "SELECT sum(rka_coa.total), sum(rka_coa.realisasi), sum(rka_coa.total)-sum(coalesce(rka_coa.realisasi,0)) "
		sql += "FROM anggaran_rka rka "
		# sql += "LEFT JOIN account_period per ON rka.period_id = per.id "
		sql += "LEFT JOIN anggaran_rka_kegiatan rka_keg ON rka.id = rka_keg.rka_id "
		sql += "LEFT JOIN anggaran_rka_coa rka_coa ON rka_keg.id = rka_coa.rka_kegiatan_id "
		sql += "LEFT JOIN anggaran_mata_anggaran_kegiatan mak ON rka_coa.mak_id = mak.id "
		sql += "LEFT JOIN anggaran_cost_type ct ON mak.cost_type_id = ct.id "
		sql += "WHERE rka.unit_id = %s " % (self.unit_id.id)
		sql += "AND rka.tahun = %s " % (self.tahun_id.id)
		sql += "AND ct.code = '%s' " % (cost_type_code)
		sql += "AND rka.state = 'done' "
		sql += "AND per.code = '%02d/%s' " % ( m, tahun) 
		
		cr.execute(sql)
		hasil = cr.fetchone()

		# print sql
		# print hasil

		if hasil[0] != None:
			total_p = hasil[0]

		if hasil[1] != None:
			total_a = hasil[1]

		if hasil[2] != None:
			total_v = hasil[2]
			
		return (total_p, total_a, total_v)


	def cari_bahan_habis_pakai(self, m):
		total = self.query_rka_coa(self, "1",m)
		return total 

	def cari_gaji(self, m):
		total = self.query_rka_coa(self, "2",m)
		return total 

	def cari_sewa(self, m):
		total = self.query_rka_coa(self, "3",m)
		return total 

	def cari_outsourcing(self, m):
		total = self.query_rka_coa(self, "4",m)
		return total 

	def cari_overhead(self, m):
		total = self.query_rka_coa(self, "5",m)
		return total 

	def cari_biaya_adm(self, m):
		total = 0.0
		return total 

	def map_month_to_period(self, m, tahun):
		m = m + 8
		if m > 12:
			m = m - 12
			tahun = tahun + 1

		return tahun, m

	def cari_investasi(self, m):
		# m : 1=Sep, 2=Oct, dst..
		# period : 01=Jan, 02=Feb
		tahun = int(self.tahun_id.code)

		tahun,m = self.map_month_to_period(m, tahun )

		p_total = 0.0
		a_total = 0.0
		v_total = 0.0

		sql = "SELECT sum(total),0,0 from anggaran_investasi inv "
		# sql += "LEFT JOIN account_period per ON inv.period_id = per.id "
		sql += "WHERE unit_id = %s " % (self.unit_id.id)
		sql += "AND tahun_id = %s " % (self.tahun_id.id) 
		sql += "AND per.code = '%02d/%s' " % ( m, tahun) 
		sql += "AND inv.state = 'done'"


		cr.execute(sql)
		hasil = cr.fetchone()

		# print sql 
		# print hasil

		if hasil[0] != None:
			p_total = hasil[0]
		if hasil[1] != None:
			a_total = hasil[1]
		if hasil[2] != None:
			v_total = hasil[2]
		return (p_total, a_total, v_total)

	def cari_biaya_prepaid(self,m):
		total = 0.0
		return total 

	def cari_pajak(self, m):
		total = 0.0
		return total 

	def cari_uudp(self, m):
		# m : 1=Sep, 2=Oct, dst..
		# period : 01=Jan, 02=Feb
		tahun = int(self.tahun_id.code)

		tahun,m = self.map_month_to_period(m, tahun )
		
		p_total = 0.0
		a_total = 0.0
		v_total = 0.0

		sql = "SELECT sum(jumlah),0,0 from anggaran_sup sup "
		# sql += "LEFT JOIN account_period per ON sup.period_id = per.id "
		sql += "WHERE unit_id = %s " % (self.unit_id.id)
		sql += "AND tahun_id = %s " % (self.tahun_id.id) 
		sql += "AND per.code = '%02d/%s' " % ( m, tahun) 
		sql += "AND sup.state = 'done'"


		cr.execute(sql)
		hasil = cr.fetchone()

		# print sql 
		# print hasil

		if hasil[0] != None:
			p_total = hasil[0]
		if hasil[1] != None:
			a_total = hasil[1]
		if hasil[2] != None:
			v_total = hasil[2]

		return (p_total, a_total, v_total)

	def cari_saving(self, m):
		total = 0.0
		return total 

	def cari_pinjaman(self, m):
		total = 0.0
		return total 

	def cari_pembayaran_pinjaman(self, m):
		total = 0.0
		return total 

	def cari_bunga_pinjaman(self, m):
		total = 0.0
		return total 



class cashflow_line(models.Model):
	_name 		= 'anggaran.cashflow.line'

	cashflow_id		= fields.Many2one('anggaran.cashflow', 'Cashflow')
	cashflow_coa_id	= fields.Many2one('anggaran.cashflow.coa', 'Rincian')
	code 			= fields.Char(comodel_name="anggaran.cashflow_coa", related='cashflow_coa_id.code', string="Code", store=False)
	type			= fields.Char('Type')
	m1 				= fields.Float('Sep')
	m2 				= fields.Float('Oct')
	m3 				= fields.Float('Nov')
	m4 				= fields.Float('Dec')
	m5 				= fields.Float('Jan')
	m6 				= fields.Float('Feb')
	m7 				= fields.Float('Mar')
	m8				= fields.Float('Apr')
	m9 				= fields.Float('May')
	m10 			= fields.Float('Jun')
	m11 			= fields.Float('Jul')
	m12 			= fields.Float('Aug')

	m1a 			= fields.Float('Sep (a)')
	m2a 			= fields.Float('Oct (a)')
	m3a 			= fields.Float('Nov (a)')
	m4a 			= fields.Float('Dec (a)')
	m5a 			= fields.Float('Jan (a)')
	m6a 			= fields.Float('Feb (a)')
	m7a 			= fields.Float('Mar (a)')
	m8a 			= fields.Float('Apr (a)')
	m9a 			= fields.Float('May (a)')
	m10a 			= fields.Float('Jun (a)')
	m11a 			= fields.Float('Jul (a)')
	m12a 			= fields.Float('Aug (a)')

	m1s 			= fields.Float('Sep (s)')
	m2s 			= fields.Float('Oct (s)')
	m3s 			= fields.Float('Nov (s)')
	m4s 			= fields.Float('Dec (s)')
	m5s 			= fields.Float('Jan (s)')
	m6s 			= fields.Float('Feb (s)')
	m7s 			= fields.Float('Mar (s)')
	m8s 			= fields.Float('Apr (s)')
	m9s 			= fields.Float('May (s)')
	m10s 			= fields.Float('Jun (s)')
	m11s 			= fields.Float('Jul (s)')
	m12s 			= fields.Float('Aug (s)')

