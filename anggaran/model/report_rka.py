from odoo import tools
from odoo import fields, models
from odoo import api
from odoo.exceptions import UserError
import odoo.addons.decimal_precision as dp
import time
from datetime import datetime, timedelta
import dateutil.parser
import pytz
import logging
from odoo.tools.translate import _
from odoo.osv import expression

###########################################################################
#Level 1 : RKA
###########################################################################
class reportrka(models.Model):
	_name		= "anggaran.rka"
	_inherit	= "anggaran.rka"

	rka_tridharma_ids	= fields.One2many(comodel_name='anggaran.rka_tridharma',inverse_name='report_rka_id', string='Tridharma')

	
	def action_report(self, ):

		for rka in self:
			sqld = "delete from anggaran_rka_tridharma where report_rka_id = %s"
			rka.env.cr.execute(sqld, (rka.id,))
			for td in rka.rka_tridharma_ids:
				sqld1 = "delete from anggaran_rka_kro where rka_tridharma_id = %s"
				rka.env.cr.execute(sqld1, (td.id,))
				for kro in td.rka_kro_ids:
					sqld2 = "delete from anggaran_rka_ro where rka_kro_id = %s"
					rka.env.cr.execute(sqld2, (kro.id,))
					for ro in kro.rka_ro_ids:
						sqld3 = "delete from anggaran_rka_komponen where rka_ro_id = %s"
						rka.env.cr.execute(sqld3, (ro.id,))
						for kom in ro.rka_komp_ids:
							sqld4 = "delete from anggaran_rka_subkomponen where rka_komp_id = %s"
							rka.env.cr.execute(sqld4, (kom.id,))
							for sub in kom.rka_sub_ids:
								sqld5 = "delete from anggaran_rka_mak where rka_subkomp_id = %s"
								rka.env.cr.execute(sqld5, (sub.id,))
								for mak in sub.rka_mak_ids:
									sqld6 = "delete from anggaran_rka_det where rka_mak_id = %s"
									rka.env.cr.execute(sqld6, (mak.id,))
			sql = """
				insert into anggaran_rka_tridharma (tridharma_id, anggaran, report_rka_id)
				select td.id, sum(keg.anggaran), %s
				from anggaran_rka_kegiatan keg
				left join anggaran_tridharma td on keg.tridharma_id = td.id
				left join anggaran_rka rka on keg.rka_id = rka.id
				where rka.id = %s
				group by td.id
				"""
			cr = rka.env.cr
			cr.execute(sql, (rka.id,rka.id,))
			sqltd = """
				select td.id, td.anggaran, td.tridharma_id
				from anggaran_rka_tridharma td
				left join anggaran_rka rka on td.report_rka_id = rka.id
				where rka.id = %s
				"""
			crtd = rka.env.cr
			crtd.execute(sqltd, (rka.id,))
			tridharma = crtd.fetchall()

			for td in tridharma:
				sql1 = """
					insert into anggaran_rka_kro (category_id, anggaran, rka_tridharma_id)
					select kro.id, sum(keg.anggaran), %s
					from anggaran_rka_kegiatan keg
					left join anggaran_tridharma td on keg.tridharma_id = td.id
					left join anggaran_category kro on keg.category_id = kro.id
					left join anggaran_rka rka on keg.rka_id = rka.id
					where rka.id = %s and td.id = %s
					group by kro.id
					"""
				cr1 = rka.env.cr
				cr1.execute(sql1, (td[0],rka.id,td[2]))

				sqlkro = """
					select kro.id, kro.anggaran, kro.category_id
					from anggaran_rka_kro kro
					left join anggaran_rka_tridharma td on kro.rka_tridharma_id = td.id
					where td.id = %s
					"""
				crkro = rka.env.cr
				crkro.execute(sqlkro, (td[0],))
				category = crkro.fetchall()

				for kro in category:
					sql2 = """
						insert into anggaran_rka_ro (indikator, anggaran, rka_kro_id)
						select keg.indikator, keg.anggaran, %s
						from anggaran_rka_kegiatan keg
						left join anggaran_tridharma td on keg.tridharma_id = td.id
						left join anggaran_category kro on keg.category_id = kro.id
						left join anggaran_rka rka on keg.rka_id = rka.id
						where rka.id = %s and td.id = %s and kro.id = %s
						group by keg.id
						"""
					cr2 = rka.env.cr
					cr2.execute(sql2, (kro[0],rka.id,td[2],kro[2]))

					sqlro = """
						select ro.id, ro.anggaran, ro.indikator
						from anggaran_rka_ro ro
						left join anggaran_rka_kro kro on ro.rka_kro_id = kro.id
						where kro.id = %s
						"""
					crro = rka.env.cr
					crro.execute(sqlro, (kro[0],))
					kegiatan = crro.fetchall()
					for keg in kegiatan:
						sql3 = """
							insert into anggaran_rka_komponen (komponen_id, total, rka_ro_id)
							select kom.id, sum(coa.total), %s
							from anggaran_rka_coa coa
							left join anggaran_komponen kom on coa.komponen_id = kom.id
							left join anggaran_rka_kegiatan keg on coa.rka_kegiatan_id = keg.id
							left join anggaran_tridharma td on keg.tridharma_id = td.id
							left join anggaran_category kro on keg.category_id = kro.id
							left join anggaran_rka rka on keg.rka_id = rka.id
							where rka.id = %s and td.id = %s and kro.id = %s and keg.indikator = %s
							group by kom.id
							"""
						cr3 = rka.env.cr
						cr3.execute(sql3, (keg[0],rka.id,td[2],kro[2],keg[2]))

						sqlkom = """
							select kom.id, kom.total, kom.komponen_id
							from anggaran_rka_komponen kom
							left join anggaran_rka_ro ro on kom.rka_ro_id = ro.id
							where ro.id = %s
							"""
						crkom = rka.env.cr
						crkom.execute(sqlkom, (keg[0],))
						komponen = crkom.fetchall()
						for kom in komponen:
							if kom[2]:
								sql4 = """
									insert into anggaran_rka_subkomponen (subkomponen_id, total, rka_ro_id, rka_komp_id)
									select sub.id, sum(coa.total), %s, %s
									from anggaran_rka_coa coa
									left join anggaran_komponen kom on coa.komponen_id = kom.id
									left join anggaran_subkomponen sub on coa.subkomponen_id = sub.id
									left join anggaran_rka_kegiatan keg on coa.rka_kegiatan_id = keg.id
									left join anggaran_tridharma td on keg.tridharma_id = td.id
									left join anggaran_category kro on keg.category_id = kro.id
									left join anggaran_rka rka on keg.rka_id = rka.id
									where rka.id = %s and td.id = %s and kro.id = %s and keg.indikator = %s and kom.id = %s
									group by sub.id
									"""
								cr4 = rka.env.cr
								cr4.execute(sql4, (keg[0],kom[0],rka.id,td[2],kro[2],keg[2],kom[2]))
							else:
								sql4 = """
									insert into anggaran_rka_subkomponen (subkomponen_id, total, rka_ro_id, rka_komp_id)
									select sub.id, sum(coa.total), %s, %s
									from anggaran_rka_coa coa
									left join anggaran_subkomponen sub on coa.subkomponen_id = sub.id
									left join anggaran_rka_kegiatan keg on coa.rka_kegiatan_id = keg.id
									left join anggaran_tridharma td on keg.tridharma_id = td.id
									left join anggaran_category kro on keg.category_id = kro.id
									left join anggaran_rka rka on keg.rka_id = rka.id
									where rka.id = %s and td.id = %s and kro.id = %s and keg.indikator = %s
									group by sub.id
									"""
								cr4 = rka.env.cr
								cr4.execute(sql4, (keg[0],kom[0],rka.id,td[2],kro[2],keg[2]))

							crsub = rka.env.cr
							sqlsub = """
								select sub.id, sub.total, sub.subkomponen_id
								from anggaran_rka_subkomponen sub
								left join anggaran_rka_komponen kom on sub.rka_komp_id = kom.id
								where kom.id = %s
								"""
							crsub.execute(sqlsub, (kom[0],))
							subkomponen = crsub.fetchall()

							for sub in subkomponen:
								if kom[2]:
									if sub[2]:
										sql5 = """
											insert into anggaran_rka_mak (mak_id, total, rka_ro_id, rka_komp_id, rka_subkomp_id)
											select mak.id, sum(coa.total), %s, %s, %s
											from anggaran_rka_coa coa
											left join anggaran_komponen kom on coa.komponen_id = kom.id
											left join anggaran_subkomponen sub on coa.subkomponen_id = sub.id
											left join anggaran_mata_anggaran_kegiatan mak on coa.mak_id = mak.id
											left join anggaran_rka_kegiatan keg on coa.rka_kegiatan_id = keg.id
											left join anggaran_tridharma td on keg.tridharma_id = td.id
											left join anggaran_category kro on keg.category_id = kro.id
											left join anggaran_rka rka on keg.rka_id = rka.id
											where rka.id = %s and td.id = %s and kro.id = %s and keg.indikator = %s and kom.id = %s and sub.id = %s
											group by mak.id
											"""
										cr5 = rka.env.cr
										cr5.execute(sql5, (keg[0],kom[0],sub[0],rka.id,td[2],kro[2],keg[2],kom[2],sub[2]))
									else :
										sql5 = """
											insert into anggaran_rka_mak (mak_id, total, rka_ro_id, rka_komp_id, rka_subkomp_id)
											select mak.id, sum(coa.total), %s, %s, %s
											from anggaran_rka_coa coa
											left join anggaran_komponen kom on coa.komponen_id = kom.id
											left join anggaran_mata_anggaran_kegiatan mak on coa.mak_id = mak.id
											left join anggaran_rka_kegiatan keg on coa.rka_kegiatan_id = keg.id
											left join anggaran_tridharma td on keg.tridharma_id = td.id
											left join anggaran_category kro on keg.category_id = kro.id
											left join anggaran_rka rka on keg.rka_id = rka.id
											where rka.id = %s and td.id = %s and kro.id = %s and keg.indikator = %s and kom.id = %s
											group by mak.id
											"""

										cr5 = rka.env.cr
										cr5.execute(sql5, (keg[0],kom[0],sub[0],rka.id,td[2],kro[2],keg[2],kom[2]))

								else:
									if sub[2]:
										sql5 = """
											insert into anggaran_rka_mak (mak_id, total, rka_ro_id, rka_komp_id, rka_subkomp_id)
											select mak.id, sum(coa.total), %s, %s, %s
											from anggaran_rka_coa coa
											left join anggaran_subkomponen sub on coa.subkomponen_id = sub.id
											left join anggaran_mata_anggaran_kegiatan mak on coa.mak_id = mak.id
											left join anggaran_rka_kegiatan keg on coa.rka_kegiatan_id = keg.id
											left join anggaran_tridharma td on keg.tridharma_id = td.id
											left join anggaran_category kro on keg.category_id = kro.id
											left join anggaran_rka rka on keg.rka_id = rka.id
											where rka.id = %s and td.id = %s and kro.id = %s and keg.indikator = %s and sub.id = %s
											group by mak.id
											"""
										cr5 = rka.env.cr
										cr5.execute(sql5, (keg[0],kom[0],sub[0],rka.id,td[2],kro[2],keg[2],sub[2]))
									else :
										sql5 = """
											insert into anggaran_rka_mak (mak_id, total, rka_ro_id, rka_komp_id, rka_subkomp_id)
											select mak.id, sum(coa.total), %s, %s, %s
											from anggaran_rka_coa coa
											left join anggaran_komponen kom on coa.komponen_id = kom.id
											left join anggaran_mata_anggaran_kegiatan mak on coa.mak_id = mak.id
											left join anggaran_rka_kegiatan keg on coa.rka_kegiatan_id = keg.id
											left join anggaran_tridharma td on keg.tridharma_id = td.id
											left join anggaran_category kro on keg.category_id = kro.id
											left join anggaran_rka rka on keg.rka_id = rka.id
											where rka.id = %s and td.id = %s and kro.id = %s and keg.indikator = %s
											group by mak.id
											"""

										cr5 = rka.env.cr
										cr5.execute(sql5, (keg[0],kom[0],sub[0],rka.id,td[2],kro[2],keg[2]))

								crmak = rka.env.cr
								sqlmak = """
									select mak.id, mak.total, mak.mak_id
									from anggaran_rka_mak mak
									left join anggaran_rka_subkomponen sub on mak.rka_subkomp_id = sub.id
									where sub.id = %s
									"""
								crmak.execute(sqlmak, (sub[0],))
								mak = crmak.fetchall()
								for m in mak:
									if kom[2]:
										if sub[2]:
											sql6 = """
												insert into anggaran_rka_det (keterangan, tarif, jumlah, volume_total, satuan_volume, uom_volume, rka_mak_id)
												select det.keterangan, det.tarif, det.jumlah, det.volume_total, det.satuan_volume, det.uom_volume, %s
												from anggaran_rka_detail det
												left join anggaran_rka_coa coa on det.rka_coa_id = coa.id
												left join anggaran_komponen kom on coa.komponen_id = kom.id
												left join anggaran_subkomponen sub on coa.subkomponen_id = sub.id
												left join anggaran_mata_anggaran_kegiatan mak on coa.mak_id = mak.id
												left join anggaran_rka_kegiatan keg on coa.rka_kegiatan_id = keg.id
												left join anggaran_tridharma td on keg.tridharma_id = td.id
												left join anggaran_category kro on keg.category_id = kro.id
												left join anggaran_rka rka on keg.rka_id = rka.id
												where rka.id = %s and td.id = %s and kro.id = %s and keg.indikator = %s and kom.id = %s and sub.id = %s and mak.id = %s
												"""

											cr6 = rka.env.cr
											cr6.execute(sql6, (m[0], rka.id,td[2],kro[2],keg[2],kom[2],sub[2], m[2]))
										else:
											sql6 = """
												insert into anggaran_rka_det (keterangan, tarif, jumlah, volume_total, satuan_volume, uom_volume, rka_mak_id)
												select det.keterangan, det.tarif, det.jumlah, det.volume_total, det.satuan_volume, det.uom_volume, %s
												from anggaran_rka_detail det
												left join anggaran_rka_coa coa on det.rka_coa_id = coa.id
												left join anggaran_komponen kom on coa.komponen_id = kom.id
												left join anggaran_mata_anggaran_kegiatan mak on coa.mak_id = mak.id
												left join anggaran_rka_kegiatan keg on coa.rka_kegiatan_id = keg.id
												left join anggaran_tridharma td on keg.tridharma_id = td.id
												left join anggaran_category kro on keg.category_id = kro.id
												left join anggaran_rka rka on keg.rka_id = rka.id
												where rka.id = %s and td.id = %s and kro.id = %s and keg.indikator = %s and kom.id = %s and mak.id = %s
												"""

											cr6 = rka.env.cr
											cr6.execute(sql6, (m[0], rka.id,td[2],kro[2],keg[2],kom[2], m[2]))
									else:
										if sub[2]:
											sql6 = """
												insert into anggaran_rka_det (keterangan, tarif, jumlah, volume_total, satuan_volume, uom_volume, rka_mak_id)
												select det.keterangan, det.tarif, det.jumlah, det.volume_total, det.satuan_volume, det.uom_volume, %s
												from anggaran_rka_detail det
												left join anggaran_rka_coa coa on det.rka_coa_id = coa.id
												left join anggaran_subkomponen sub on coa.subkomponen_id = sub.id
												left join anggaran_mata_anggaran_kegiatan mak on coa.mak_id = mak.id
												left join anggaran_rka_kegiatan keg on coa.rka_kegiatan_id = keg.id
												left join anggaran_tridharma td on keg.tridharma_id = td.id
												left join anggaran_category kro on keg.category_id = kro.id
												left join anggaran_rka rka on keg.rka_id = rka.id
												where rka.id = %s and td.id = %s and kro.id = %s and keg.indikator = %s and sub.id = %s and mak.id = %s
												"""

											cr6 = rka.env.cr
											cr6.execute(sql6, (m[0], rka.id,td[2],kro[2],keg[2],sub[2], m[2]))
										else:
											sql6 = """
												insert into anggaran_rka_det (keterangan, tarif, jumlah, volume_total, satuan_volume, uom_volume, rka_mak_id)
												select det.keterangan, det.tarif, det.jumlah, det.volume_total, det.satuan_volume, det.uom_volume, %s
												from anggaran_rka_detail det
												left join anggaran_rka_coa coa on det.rka_coa_id = coa.id
												left join anggaran_mata_anggaran_kegiatan mak on coa.mak_id = mak.id
												left join anggaran_rka_kegiatan keg on coa.rka_kegiatan_id = keg.id
												left join anggaran_tridharma td on keg.tridharma_id = td.id
												left join anggaran_category kro on keg.category_id = kro.id
												left join anggaran_rka rka on keg.rka_id = rka.id
												where rka.id = %s and td.id = %s and kro.id = %s and keg.indikator = %s and mak.id = %s
												"""

											cr6 = rka.env.cr
											cr6.execute(sql6, (m[0], rka.id,td[2],kro[2],keg[2], m[2]))

			# sql6 = """select det.keterangan, det.tarif, det.jumlah, det.volume_total, det.satuan_volume
			# 	from anggaran_rka_detail det
			# 	left join anggaran_rka_coa coa on det.rka_coa_id = coa.id
			# 	left join anggaran_rka_kegiatan keg on coa.rka_kegiatan_id = keg.id
			# 	left join anggaran_rka rka on keg.rka_id = rka.id
			# 	where rka.id = %s
			# 	"""

			# cr6 = rka.env.cr
			# cr6.execute(sql6, (rka.id,))
			# detail = cr6.fetchall()
			# import pdb; pdb.set_trace()
			# rka_tridharma_ids = []
			# for td in tridharma:
			# 	rka_kro_ids = []
			# 	for kro in category:
			# 		rka_ro_ids = []
			# 		for ro in kegiatan:
			# 			rka_komp_ids = []
			# 			rka_sub_ids = []
			# 			rka_mak_ids = []
			# 			for komp in komponen:
			# 				rka_sub_ids = []
			# 				rka_mak_ids = []
			# 				for sub in subkomponen:
			# 					rka_mak_ids = []
			# 					for m in mak:
			# 						rka_det_ids = []
			# 						for det in detail:
			# 							rka_det_ids.append( (0,0,{
			# 								'keterangan'	: det[0],
			# 								'tarif'		 	: det[1],
			# 								'jumlah'		: det[2],
			# 								'volume_total'	: det[3],
			# 								'satuan_volume' : det[4]
			# 							}))

			# 						rka_mak_ids.append( (0,0, {
			# 							'mak_id'		: m[0],
			# 							'total'		 	: m[1],
			# 							'rka_det_ids'	: rka_det_ids

			# 						}) )

			# 					rka_sub_ids.append( (0,0,{ 
			# 						'subkomponen_id'	: sub[0],
			# 						'total' 			: sub[1],
			# 						'rka_mak_ids' 		: rka_mak_ids
			# 					}) )

			# 				rka_komp_ids.append( (0,0,{ 
			# 					'komponen_id'		: komp[0],
			# 					'total' 			: komp[1],
			# 					'rka_sub_ids'		: rka_sub_ids,
			# 					'rka_mak_ids' 		: rka_mak_ids
			# 				}) )

			# 			rka_ro_ids.append( (0,0,{ 
			# 				'indikator'			: ro[0],
			# 				'anggaran' 			: ro[1],
			# 				'rka_komp_ids'		: rka_komp_ids,
			# 				'rka_sub_ids'		: rka_sub_ids,
			# 				'rka_mak_ids' 		: rka_mak_ids
			# 			}) )

			# 		rka_kro_ids.append( (0,0,{ 
			# 			'category_id'		: kro[0],
			# 			'anggaran' 			: kro[1],
			# 			'rka_ro_ids'		: rka_ro_ids,
			# 		}) )

			# 	rka_tridharma_ids.append( (0,0,{ 
			# 		'tridharma_id'		: td[0],
			# 		'anggaran' 			: td[1],
			# 		'rka_kro_ids'		: rka_kro_ids,
			# 	}) )

			# data = {
			# 		'unit_id'			: rka.unit_id.id,
			# 		'tahun'				: rka.tahun.id,
			# 		'name'				: rka.name,
			# 		'rka_tridharma_ids' : rka_tridharma_ids,
			# 	}
			# report_rka.create(data)

	@api.multi
	def print_renbut(self):
		self.action_report()
		return self.env.ref('anggaran.report_renbut').report_action(self)
	@api.multi
	def print_renbut_detail(self):
		self.action_report()
		return self.env.ref('anggaran.report_renbut_detail').report_action(self)
	@api.multi
	def print_rarenja(self):
		self.action_report()
		return self.env.ref('anggaran.report_rarenja').report_action(self)
	@api.multi
	def print_rarenja_detail(self):
		self.action_report()
		return self.env.ref('anggaran.report_rarenja_detail').report_action(self)
	@api.multi
	def print_renja(self):
		self.action_report()
		return self.env.ref('anggaran.report_renja').report_action(self)
	@api.multi
	def print_renja_detail(self):
		self.action_report()
		return self.env.ref('anggaran.report_renja_detail').report_action(self)
	@api.multi
	def print_rka(self):
		self.action_report()
		return self.env.ref('anggaran.report_rka').report_action(self)
	@api.multi
	def print_rka_detail(self):
		self.action_report()
		return self.env.ref('anggaran.report_rka_detail').report_action(self)


###########################################################################
#Level 2 : RKA Tridharma
###########################################################################
class rkatridharma(models.Model):
	_name			= "anggaran.rka_tridharma"
	_description	= "anggaran.rka_tridharma"

	tridharma_id	= fields.Many2one(comodel_name='anggaran.tridharma', string='Tri Dharma PT')
	anggaran		= fields.Float("Total Anggaran", compute='_total_anggaran', store=True)
	report_rka_id	= fields.Many2one(comodel_name='anggaran.rka', string='RKA')
	rka_kro_ids		= fields.One2many(comodel_name='anggaran.rka_kro',inverse_name='rka_tridharma_id', 
							string='Kegiatan KRO', ondelete="cascade")

###########################################################################
#Level 3 : RKA KRO
###########################################################################
class rkakro(models.Model):
	_name			= "anggaran.rka_kro"
	_description	= "anggaran.rka_kro"

	category_id	= fields.Many2one(comodel_name='anggaran.category', string="KRO")
	anggaran		= fields.Float("Total Anggaran", compute='_total_anggaran', store=True)

	rka_tridharma_id	= fields.Many2one(comodel_name='anggaran.rka_tridharma', string='RKA Tridharma')
	rka_ro_ids			= fields.One2many(comodel_name='anggaran.rka_ro',inverse_name='rka_kro_id', 
							string='Kegiatan RO', ondelete="cascade")

###########################################################################
#Level 4 : RKA RO
###########################################################################
class rkaro(models.Model):
	_name			= "anggaran.rka_ro"
	_description	= "anggaran.rka_ro"

	indikator		= fields.Text(string='Kegiatan')
	anggaran		= fields.Float("Total Anggaran", compute='_total_anggaran', store=True)

	rka_kro_id		= fields.Many2one(comodel_name='anggaran.rka_kro', string='RKA KRO')
	rka_komp_ids	= fields.One2many(comodel_name='anggaran.rka_komponen',inverse_name='rka_ro_id', 
							string='Kegiatan Komponen', ondelete="cascade")
	rka_sub_ids		= fields.One2many(comodel_name='anggaran.rka_subkomponen',inverse_name='rka_ro_id', 
							string='Kegiatan SubKomponen', ondelete="cascade")
	rka_mak_ids		= fields.One2many(comodel_name='anggaran.rka_mak',inverse_name='rka_ro_id', 
							string='Kegiatan MAK', ondelete="cascade")

###########################################################################
#Level 5 : RKA Komponen
###########################################################################
class rkakomponen(models.Model):
	_name			= "anggaran.rka_komponen"
	_description	= "anggaran.rka_komponen"

	komponen_id		= fields.Many2one(comodel_name='anggaran.komponen', string='Komponen')
	total			= fields.Float('Total', compute='_total', store=True)

	rka_ro_id	= fields.Many2one(comodel_name='anggaran.rka_ro', string='RKA RO')
	rka_sub_ids	= fields.One2many(comodel_name='anggaran.rka_subkomponen',inverse_name='rka_komp_id', 
							string='Sub Komponen', ondelete="cascade")
	rka_mak_ids	= fields.One2many(comodel_name='anggaran.rka_mak',inverse_name='rka_komp_id', 
							string='MAK', ondelete="cascade")

###########################################################################
#Level 6 : RKA Detail
###########################################################################
class rkasubkomponen(models.Model):
	_name			= "anggaran.rka_subkomponen"
	_description	= "anggaran.rka_subkomponen"

	subkomponen_id	= fields.Many2one(comodel_name='anggaran.subkomponen', string='Sub Komponen')
	total			= fields.Float('Total', compute='_total', store=True)

	rka_ro_id	= fields.Many2one(comodel_name='anggaran.rka_ro', string='RKA RO')
	rka_komp_id	= fields.Many2one(comodel_name='anggaran.rka_komponen', string='Komponen')
	rka_mak_ids	= fields.One2many(comodel_name='anggaran.rka_mak',inverse_name='rka_subkomp_id', 
							string='MAK', ondelete="cascade")

###########################################################################
#Level 5 : RKA MAK
###########################################################################
class rkamak(models.Model):
	_name			= "anggaran.rka_mak"
	_description	= "anggaran.rka_mak"

	mak_id			= fields.Many2one(comodel_name='anggaran.mata_anggaran_kegiatan', string='Kode')
	total			= fields.Float('Total', compute='_total', store=True)

	rka_ro_id	= fields.Many2one(comodel_name='anggaran.rka_ro', string='RKA RO')
	rka_komp_id	= fields.Many2one(comodel_name='anggaran.rka_komponen', string='Komponen')
	rka_subkomp_id	= fields.Many2one(comodel_name='anggaran.rka_subkomponen', string='Sub Komponen')
	rka_det_ids	= fields.One2many(comodel_name='anggaran.rka_det',inverse_name='rka_mak_id', 
							string='Detail MAK', ondelete="cascade")

###########################################################################
#Level 6 : RKA Detail
###########################################################################
class rkadet(models.Model):
	_name			= "anggaran.rka_det"
	_description	= "anggaran.rka_det"

	rka_mak_id	= fields.Many2one(comodel_name='anggaran.rka_mak', string='RKA KRO')
	keterangan		= fields.Text(string='Detail', required=True)
	satuan_volume	= fields.Char(string="Satuan Keterangan")
	tarif			= fields.Float(string='Harga Satuan', required=True)
	jumlah			= fields.Float(string='Volume', required=True)
	volume_total	= fields.Float(string='Jumlah' , required=True)
	uom_volume		= fields.Char(string='Satuan')
