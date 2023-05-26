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

_logger = logging.getLogger(__name__)
RKA_STATES =[('draft','Draft'),('open','Konfirmasi'),('submit','Verifikasi'),('cancel','Dibatalkan'),('done','Disahkan'),('notdone','Tidak Disetujui'),('lock','Selesai')]

###########################################################################
#Level 1 : RKA
###########################################################################
class rka(models.Model):
	_name 		= "anggaran.rka"
	_description = "anggaran.rka"
	_inherit 	= ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
	_order		= "no asc"
	# _rec_name	= "name"

	@api.depends('rka_kegiatan_ids')
	# @api.multi 
	def _anggaran(self):
		total = 0.0
		# total2 = 0.0
		# total3 = 0.0
		# total4 = 0.0
		for rka in self:
			for keg in rka.rka_kegiatan_ids:
				total = total + keg.anggaran
			# for keg in rka.rka_kegiatan_ids2:
			# 	total2 = total2 + keg.anggaran
			# for keg in rka.rka_kegiatan_ids3:
			# 	total3 = total3 + keg.anggaran
			# for keg in rka.rka_kegiatan_ids4:
			# 	total4 = total4 + keg.anggaran
		# print total 
			rka.anggaran = total
	
	# def hitung_realisasi(self, array_coas):
	# 	realisasi = 0 
	# 	for ar in array_coas:
	# 		realisasi = realisasi + ar['realisasi']
	# 	return realisasi 	

	# def hitung_anggaran(self, array_coas):
	# 	realisasi = 0 
	# 	for ar in array_coas:
	# 		realisasi = realisasi + ar['anggaran']
	# 	return realisasi 

	# @api.depends('rka_kegiatan_ids.realisasi', 'rka_kegiatan_ids2.realisasi', 'rka_kegiatan_ids3.realisasi', 'rka_kegiatan_ids4.realisasi')
	# def _frealisasi(self):
		
	# 	realisasi   = 0.0
	# 	realisasi1 	= 0.0
	# 	realisasi2	= 0.0
	# 	realisasi3	= 0.0
	# 	realisasi4	= 0.0
	# 	for rka in self:
	# 		if rka.rka_kegiatan_ids :
	# 			realisasi1 = sum(map(lambda x: x.realisasi, rka.rka_kegiatan_ids))
	# 		if rka.rka_kegiatan_ids2 :
	# 			realisasi2 = sum(map(lambda x: x.realisasi, rka.rka_kegiatan_ids2))
	# 		if rka.rka_kegiatan_ids3 :
	# 			realisasi3 = sum(map(lambda x: x.realisasi, rka.rka_kegiatan_ids3))
	# 		if rka.rka_kegiatan_ids4 :
	# 			realisasi4 = sum(map(lambda x: x.realisasi, rka.rka_kegiatan_ids4))

	# 		realisasi = realisasi1 + realisasi2 + realisasi3 + realisasi4
	# 		rka.realisasi = realisasi

	# def _fanggaran(self):
	# 	results = {}
	# 	rkas = self.browse(cr, uid, ids, context=context) 
	# 	for rka in rkas:
	# 		rka_kegiatan_ids = rka.rka_kegiatan_ids
	# 		self.realisasi = self.hitung_anggaran(rka_kegiatan_ids)
	@api.depends("anggaran","realisasi")
	def _fsisa(self):
		for rka in self:
			rka.sisa = rka.anggaran - rka.realisasi


	name				= fields.Char(string='nama', required=True)
	unit_id				= fields.Many2one(comodel_name='vit.unit_kerja', string='SUBSATKER', required=True, states={"lock" : [("readonly",True)]})
	fakultas_id			= fields.Many2one(comodel_name='vit.fakultas', related='unit_id.fakultas_id', string="Fakultas", store=True, states={"lock" : [("readonly",True)]})
	tahun				= fields.Many2one(comodel_name='account.fiscal.year', string='Tahun', required=True, states={"lock" : [("readonly",True)]})
	period_id			= fields.Many2one(comodel_name='account.period', string='Periode' , compute='_fperiode', store=True, )
	user_id	    		= fields.Many2one(comodel_name='res.users', string='User', default=lambda self: self.env.uid, readonly=True)
	ttd_id     			= fields.Many2one(comodel_name="hr.employee",  string="Penandatangan", states={"lock" : [("readonly",True)]}, help="")
	pos_ttd    			= fields.Char(string="Posisi Penandatangan", states={"lock" : [("readonly",True)]}, help="")
	alokasi				= fields.Float(string='Alokasi', states={"lock" : [("readonly",True)]})
	anggaran			= fields.Float('Total Anggaran', compute='_anggaran', store=True)
	realisasi			= fields.Float("Realisasi", store=True)
	sisa		 		= fields.Float(compute='_fsisa',string="Sisa", store=True)
	definitif			= fields.Float("Definitif", states={"lock" : [("readonly",True)]})
	rka_kegiatan_ids	= fields.One2many(comodel_name='anggaran.rka_kegiatan',inverse_name='rka_id', 
							string='Kegiatan', ondelete="cascade", states={"lock" : [("readonly",True)]})
	# rka_kegiatan_ids2  	= fields.One2many(comodel_name='anggaran.rka_kegiatan',inverse_name='rka_id', 
	# 						string=_('Pemasaran'), ondelete="cascade", domain=[('category_id','like','PEMASARAN')], states={"lock" : [("readonly",True)]})
	# rka_kegiatan_ids3  	= fields.One2many(comodel_name='anggaran.rka_kegiatan',inverse_name='rka_id', 
	# 						string=_('Investasi'), ondelete="cascade", domain=[('category_id','like','INVESTASI')], states={"lock" : [("readonly",True)]})
	# rka_kegiatan_ids4  	= fields.One2many(comodel_name='anggaran.rka_kegiatan',inverse_name='rka_id', 
	# 						string=_('Overhead'), ondelete="cascade", domain=[('category_id','like','OVERHEAD')], states={"lock" : [("readonly",True)]})
	state			 	= fields.Selection(selection=RKA_STATES,string='Status',readonly=True,required=True,default=RKA_STATES[0][0])
	note		 		= fields.Text(string='Note', states={"lock" : [("readonly",True)]})
	mak_terisi			= fields.Boolean('MAK Terisi', default=False)
	no					= fields.Integer(string='No', readonly=True, related='unit_id.no', store=True)
	date_open 			= fields.Datetime( string="Tanggal Submit",  readonly=True, help="")
	
	# def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
	# 	args = args or []
	# 	domain = []
	# 	if name:
	# 		domain = ['|', ('code', operator, name), ('name', operator, name)]
	# 		if operator in expression.NEGATIVE_TERM_OPERATORS:
	# 			domain = ['&', '!'] + domain[1:]
	# 	rec_ids = self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)
	# 	return self.browse(rec_ids).name_get()
	
	# @api.multi
	# def name_get(self):
	# 	result = []
	# 	for rec in self:
	# 		name = rec.unit_id.name
	# 		result.append((rec.id, name))
	# 	return result

	@api.onchange('unit_id')
	def name_onchange(self):
		for rec in self:
			rec.name = rec.unit_id.name

	@api.depends('tahun')
	def _fperiode(self):
		periode = ''
		for rka in self:
			periode = int(rka.tahun.name) + 1
			acc_periode = rka.env['account.period'].search([('name','=',str(periode))])
			# import pdb; pdb.set_trace()
			if acc_periode:
				rka.period_id = acc_periode.id


	@api.multi
	def action_draft(self):
		#set to "draft" state
		return self.write({'state':RKA_STATES[0][0]})

	@api.multi
	def action_cancel(self):
		#set to "draft" state
		return self.write({'state':RKA_STATES[3][0]})

	@api.multi
	def action_confirm(self):
		for rka in self:
		#apakah ada rka dengna perioda yang sama utk tahun ini
			rkas = rka.search([('tahun','=',rka.tahun.id ), ('period_id','=',rka.period_id.id ), ('unit_id','=',rka.unit_id.id), ('state','!=','cancel' )])
			if len(rkas) > 1:
				raise UserError(_("Ada lebih dari satu RENBUT pada perioda yang sama") ) 

			# if rka.alokasi < rka.anggaran and rka.state not in ['draft','open']:
			# 	raise UserError(_("Total Anggaran Melebihi Alokasi") )

			# if rka.alokasi > rka.anggaran and rka.state not in ['draft','open']:
			# 	raise UserError(_("Total Anggaran Kurang Dari Alokasi") )

			# if rka.state not in ['draft','open'] and (rka.alokasi == 0.0 or rka.anggaran == 0.0):
			# 	raise UserError(_("Mohon dilengkapi data Alokasi dan Total Anggaran") )
		#set to "open" state
		return self.write({'state':RKA_STATES[1][0]})
	
	@api.multi
	def action_submit(self):
		#set to "submit" state
		for rka in self:
		#apakah ada rka dengna perioda yang sama utk tahun ini
			rkas = rka.search([('tahun','=',rka.tahun.id ), ('period_id','=',rka.period_id.id ), ('unit_id','=',rka.unit_id.id), ('state','!=','cancel' )])
			if len(rkas) > 1:
				raise UserError(_("Ada lebih dari satu RARENJA pada perioda yang sama") ) 

			# if rka.alokasi < rka.anggaran:
			# 	raise UserError(_("Total Anggaran Melebihi Alokasi") )

			# if rka.alokasi > rka.anggaran:
			# 	raise UserError(_("Total Anggaran Kurang Dari Alokasi") )

			# if rka.alokasi == 0.0 or rka.anggaran == 0.0:
			# 	raise UserError(_("Mohon dilengkapi data Alokasi dan Total Anggaran") )

			rka.date_open =	datetime.now()

		return rka.write({'state':RKA_STATES[2][0]})
	
	@api.multi
	def action_done(self):
		for rka in self:
		#apakah ada rka dengna perioda yang sama utk tahun ini
			rkas = rka.search([('tahun','=',rka.tahun.id ), ('period_id','=',rka.period_id.id ), ('unit_id','=',rka.unit_id.id), ('state','!=','cancel' )])
			if len(rkas) > 1:
				raise UserError(_("Ada lebih dari satu RENJA pada perioda yang sama") ) 

			if rka.alokasi < rka.anggaran:
				raise UserError(_("Total Anggaran Melebihi Alokasi") )

			if rka.alokasi > rka.anggaran:
				raise UserError(_("Total Anggaran Kurang Dari Alokasi") )

			if rka.alokasi == 0.0 or rka.anggaran == 0.0:
				raise UserError(_("Mohon dilengkapi data Alokasi dan Total Anggaran") )
		#set to "done" state
		return self.write({'state':RKA_STATES[4][0]})

	@api.multi
	def action_notdone(self):
			#set to "tidak disetujui" state
		return self.write({'state':RKA_STATES[5][0]})

	@api.multi
	def action_lock(self):
		#set to "lock" state
		return self.write({'state':RKA_STATES[6][0]})


	# ######################################################################
	# # looping Kebijakan, Program, Kegiatan, MAK
	# # isi ke RKA, RKA Kegiatan, dst, sd rka_coa
	# ######################################################################
	@api.multi
	def action_fill_mak(self):		
		# rka = self

		kbj_obj	= self.env['anggaran.kebijakan']
		prg_obj	= self.env['anggaran.program']
		keg_obj	= self.env['anggaran.kegiatan']
		mak_obj	= self.env['anggaran.mata_anggaran_kegiatan']
		rka_keg_obj	= self.env['anggaran.rka_kegiatan']

		rka_kegiatan_ids	= []
		
		keg_ids = keg_obj.search([])
		
		for keg in keg_ids:			
			rka_coa_ids = []

			mak_ids = mak_obj.search([('kegiatan_id','=', keg.id),('unit_id','=', self.unit_id.id)])
			for mak in mak_ids:
				rka_coa_ids.append( (0,0, {
					'mak_id'			: mak.id,
				}) )

	# 		#kalau sudah ada record rka_kegiatan_ids utk kegiatan ini, tidak usah diinsert

			exist = rka_keg_obj.search([('rka_id','=', self.id),('kegiatan_id','=',keg.id)])
			# import pdb; pdb.set_trace()
			if not exist:
				rka_kegiatan_ids.append( (0,0,{ 
					# 'kebijakan_id' 		: keg.kebijakan_id.id,
					# 'program_id' 		: keg.program_id.id,
					'kegiatan_id' 		: keg.id,
					'indikator' 		: '',
					'target_capaian' 	: 0.0,
					'target_capaian_uom': False,
					'anggaran' 			: 0.0,
					'rka_coa_ids'		: rka_coa_ids
				}) )
			# import pdb; pdb.set_trace()
		data = {
			'alokasi'			: 0.0,
			'anggaran'			: 0.0,
			'realisasi'			: 0.0,
			'sisa'		 		: 0.0, 
			'definitif'			: 0.0,
			'rka_kegiatan_ids'  : rka_kegiatan_ids,
			'state'			 	: RKA_STATES[0][0],
			'note'		 		: '',
			'mak_terisi' 		: True 
		}
		# import pdb; pdb.set_trace()
		self.write(data)	
		return

	def copy(self):
		default = {}
		rka_kegiatan_ids = []

		for fd in self.rka_kegiatan_ids:

			rka_coa_ids = []
			for rc in fd.rka_coa_ids:

				rka_detail_ids = []
				for rd in rc.rka_detail_ids:
					rka_volume_ids = []
					for rv in rd.rka_volume_ids:
						rka_volume_ids.append((0,0,{
							# 'rka_detail_id'  : rv.rka_detail_id,
							'volume' 		 : rv.volume,
							'volume_uom'	 : rv.volume_uom
						}))
					rka_detail_ids.append( (0,0,{
						# 'rka_coa_id' 	: rd.rka_coa_id,
						'keterangan'	: rd.keterangan,
						'tarif'		 	: rd.tarif,
						'jumlah'		: rd.jumlah,
						'volume_total' 	: rd.volume_total,
						'rka_volume_ids': rka_volume_ids
					}))

				rka_coa_ids.append( (0,0, {
					# 'rka_kegiatan_id' 	: rc.rka_kegiatan_id.id,
					'mak_id'			: rc.mak_id.id,
					'total'		 		: rc.total,
					'komponen_id'		: rc.komponen_id.id,
					'subkomponen_id'	: rc.subkomponen_id.id,
					'rka_detail_ids'	: rka_detail_ids

				}) )

			rka_kegiatan_ids.append( (0,0,{ 
				# 'kebijakan_id' 		: fd.kebijakan_id.id,
				# 'program_id' 		: fd.program_id.id,
				'tridharma_id'		: fd.tridharma_id.id,
				'category_id' 		: fd.category_id.id,
				'indikator' 		: fd.indikator,
				'target_capaian' 	: fd.target_capaian,
				'target_capaian_uom': fd.target_capaian_uom or False,
				'anggaran' 			: fd.anggaran,
				'rka_coa_ids'		: rka_coa_ids
			}) )
		
		default.update({'rka_kegiatan_ids' : rka_kegiatan_ids })
		return super(rka, self).copy(default)

	# ######################################################################
	# # duplikat RKA untuk revisi
	# ######################################################################

	revised_notes   = fields.Text(string="Keterangan Revisi", readonly=True, required=False, )
	revised_date    = fields.Datetime(string="Tanggal Revisi", readonly=True, required=False, )
	revised_by_id  	= fields.Many2one(comodel_name="res.users", string="Direvisi oleh", readonly=True, required=False, )
	source_rka_id 	= fields.Many2one(comodel_name="anggaran.rka", string="Revisi Dari", readonly=True, required=False, )
	dest_rka_id 	= fields.Many2one(comodel_name="anggaran.rka", string="Dokumen Revisi", readonly=True, required=False, )
	is_revisi		= fields.Boolean('Revisi', default=False, readonly=True)
	no_revisi		= fields.Integer(string='Revisi ke', readonly=True)
	origin 			= fields.Many2one(comodel_name="anggaran.rka", string="Dokumen Asal", readonly=True)
	revisi_count	= fields.Integer(string='Hitung Revisi', compute='_get_revisi', readonly=True)

	def action_revised(self):
		self.ensure_one()

		########## create new picking with the same name and rename the old one
		new_rec = self.duplicate()

		########## cancel the old one
		self.cancel()
		self.dest_rka_id = new_rec.id

		return new_rec


	def duplicate(self):
		old_name = self.name
		origin_name = self.origin.name
		# import pdb; pdb.set_trace()
		if self.origin :
			new_name = origin_name + ' REVISI ' + str(self.no_revisi + 1)
			origin = self.origin.id
		else :
			new_name = old_name + ' REVISI ' + str(self.no_revisi + 1)
			origin = self.id

		rka_kegiatan_ids = []
		for fd in self.rka_kegiatan_ids:

			rka_coa_ids = []
			for rc in fd.rka_coa_ids:

				rka_detail_ids = []
				for rd in rc.rka_detail_ids:
					rka_volume_ids = []
					for rv in rd.rka_volume_ids:
						rka_volume_ids.append((0,0,{
							'volume' 		 : rv.volume,
							'volume_uom'	 : rv.volume_uom
						}))
					rka_detail_ids.append( (0,0,{
						'keterangan'	: rd.keterangan,
						'tarif'		 	: rd.tarif,
						'jumlah'		: rd.jumlah,
						'volume_total' 	: rd.volume_total,
						'rka_volume_ids': rka_volume_ids
					}))

				rka_coa_ids.append( (0,0, {
					'mak_id'			: rc.mak_id.id,
					'total'		 		: rc.total,
					'realisasi'			: rc.realisasi,
					'komponen_id'		: rc.komponen_id.id,
					'subkomponen_id'	: rc.subkomponen_id.id,
					'rka_detail_ids'	: rka_detail_ids

				}) )

			rka_kegiatan_ids.append( (0,0,{ 
				# 'kebijakan_id' 		: fd.kebijakan_id.id,
				# 'program_id' 		: fd.program_id.id,
				'tridharma_id'		: fd.tridharma_id.id,
				'category_id' 		: fd.category_id.id,
				'indikator' 		: fd.indikator,
				'target_capaian' 	: fd.target_capaian,
				'target_capaian_uom': fd.target_capaian_uom or False,
				'anggaran' 			: fd.anggaran,
				'realisasi'			: fd.realisasi,
				'rka_coa_ids'		: rka_coa_ids
			}) )

		default={
			'name': new_name,
			'revised_notes': self.revised_notes,
			'revised_date': self.revised_date,
			'revised_by_id': self.revised_by_id.id,
			'source_rka_id': self.id,
			'unit_id': self.unit_id.id,
			'tahun': self.tahun.id,
			# 'period_id'  : self.period_id.id,
			'alokasi' : self.alokasi,
			'anggaran' : self.anggaran,
			'realisasi'    : self.realisasi,
			'definitif'    : self.definitif,
			'rka_kegiatan_ids' : rka_kegiatan_ids,
			'no' : self.no,
			'date_open': self.date_open,
			'no_revisi' : self.no_revisi + 1,
			'is_revisi': True,
			'origin' : origin,
			'state'     : 'submit',
		}
		new_rec = self.create(default)
		return new_rec

	def cancel(self):
		## update state to cancel
		self.state= 'cancel'

	@api.multi
	def action_view_revisi(self):
		anggarans = self.env['anggaran.rka'].search(['|',('origin','=',self.origin.id),('id','=',self.origin.id)])
		action = self.env.ref('anggaran.action_rka_revisi_list').read()[0]
		
		if len(anggarans) >= 1:
			action['domain'] = [('id', 'in', anggarans.ids)]
		# elif len(anggarans) == 1:
		# 	form_view = [(self.env.ref('anggaran.view_rka_form').id, 'form')]
		# 	if 'views' in action:
		# 		action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
		# 	else:
		# 		action['views'] = form_view
		# 	action['res_id'] = anggarans.ids[0]
		else:
			action = {'type': 'ir.actions.act_window_close'}
		return action

	def _get_revisi(self):
		anggarans = self.env['anggaran.rka'].search([('origin','=',self.origin.id)])
		self.revisi_count = len(set(anggarans.ids))

	@api.multi
	def get_current_date(self):
		date = ''
		for ra in self:
			now = datetime.now()
			user = ra.env['res.users'].browse(ra.env.uid)
			tz   = pytz.timezone(user.tz) or pytz.utc
			date_new = pytz.utc.localize(now).astimezone(tz)
			tgl    = datetime.strftime(date_new, '%d')
			bln    = datetime.strftime(date_new, '%m')
			thn    = datetime.strftime(date_new, '%Y')
			b = ''
			if bln == '01':
				b = 'Januari'
			if bln == '02':
				b = 'Februari'
			if bln == '03':
				b = 'Maret'
			if bln == '04':
				b = 'April'
			if bln == '05':
				b = 'Mei'
			if bln == '06':
				b = 'Juni'
			if bln == '07':
				b = 'Juli'
			if bln == '08':
				b = 'Agustus'
			if bln == '09':
				b = 'September'
			if bln == '10':
				b = 'Oktober'
			if bln == '11':
				b = 'November'
			if bln == '12':
				b = 'Desember'
			date = str(tgl) +" "+ b +" "+ str(thn)
		return date

###########################################################################
#Level 2 : RKA Kegiatan
###########################################################################
class rka_kegiatan(models.Model):
	_name 		= "anggaran.rka_kegiatan"
	_rec_name   = "indikator"
	_order		= "id asc"

	@api.depends('rka_coa_ids') 
	def _total_anggaran(self):
		for rka_kegiatan in self:
			total = 0.0
			for coa in rka_kegiatan.rka_coa_ids:
				total = total + coa.total
			# print total 
			rka_kegiatan.anggaran = total 

	
	# @api.depends('rka_coa_ids.realisasi')
	# def _frealisasi(self):
		# results = {}
		# rka_kegiatans = self.browse(cr, uid, ids, context=context) 

		# ambil satu-per-satu sesion object 
		# for rka_kegiatan in self:
		# 	rka_kegiatan.realisasi = sum(map(lambda x: x.realisasi, rka_kegiatan.rka_coa_ids))
			# array_coas = rka_kegiatan.rka_coa_ids
			# rka_kegiatan.realisasi = self.hitung_realisasi(array_coas)
		# return results

	@api.depends('anggaran','realisasi')
	def _fsisa(self):
		# ambil satu-per-satu sesion object 
		for rka_kegiatan in self:
			rka_kegiatan.sisa = rka_kegiatan.anggaran - rka_kegiatan.realisasi

	rka_id				= fields.Many2one(comodel_name='anggaran.rka', string='RKA')
	kebijakan_id	  	= fields.Many2one(comodel_name='anggaran.kebijakan', string='Kebijakan')
	category_id  		= fields.Many2one(comodel_name='anggaran.category', string="KRO", required=True, )
	program_id			= fields.Many2one(comodel_name='anggaran.program', string='Program')
	tridharma_id		= fields.Many2one(comodel_name='anggaran.tridharma', string='Tri Dharma PT', required=True, )
	kegiatan_id	   		= fields.Many2one(comodel_name='anggaran.kegiatan', string='Kegiatans')
	unit_id		  		= fields.Many2one(comodel_name='vit.unit_kerja', related='rka_id.unit_id', string="SUBSATKER", readonly=True )
	indikator		 	= fields.Text(string='Kegiatan', required=True, )
	target_capaian		= fields.Float(string='Target Capaian')
	# target_capaian_uom	= fields.Many2one(comodel_name='uom.uom', string='Satuan Target')
	target_capaian_uom	= fields.Char(string='Satuan Target')
	anggaran			= fields.Float("Total Anggaran", compute='_total_anggaran', store=True)
	realisasi			= fields.Float("Realisasi")
	sisa		 		= fields.Float(compute='_fsisa', string="Sisa", store=True)
	definitif			= fields.Float("Definitif")
	rka_coa_ids	   		= fields.One2many(comodel_name='anggaran.rka_coa',inverse_name='rka_kegiatan_id',
		string='Rincian', ondelete="cascade")



###########################################################################
#Level 3 : RKA Rincian MAK
###########################################################################
class rka_coa(models.Model):
	_rec_name   = "mak_id"
	_name 		= "anggaran.rka_coa"
	_order		= "id asc"

	@api.depends('rka_detail_ids') 
	def _total(self):
		for mak in self:
			total = 0.0
			for det in mak.rka_detail_ids:
				total = total + det.volume_total
			# print total 
			mak.total = total

	@api.depends('total','realisasi')
	def _fsisa(self): 
		for rka_coa in self:
			rka_coa.sisa = rka_coa.total - rka_coa.realisasi
			
	rka_kegiatan_id	= fields.Many2one(comodel_name='anggaran.rka_kegiatan', string='Kegiatan')
	mak_id			= fields.Many2one(comodel_name='anggaran.mata_anggaran_kegiatan', string='Kode')
	total		 	= fields.Float('Total', compute='_total', store=True)

	#diupdate waktu SPP confirm
	realisasi		= fields.Float('Realisasi')
	sisa		 	= fields.Float(compute='_fsisa', string="Sisa", store=True)

	definitif	 	= fields.Float('Definitif Biaya')
	sumber_dana_id	= fields.Many2one(comodel_name='anggaran.sumber_dana', string='Sumber Dana')
	komponen_id		= fields.Many2one(comodel_name='anggaran.komponen', string='Komponen')
	subkomponen_id	= fields.Many2one(comodel_name='anggaran.subkomponen', string='Sub Komponen')
	rka_detail_ids	= fields.One2many(comodel_name='anggaran.rka_detail',inverse_name='rka_coa_id',string='Detail', ondelete="cascade")

	




###########################################################################
#Level 4: detail MAK
###########################################################################
class rka_detail(models.Model):
	_rec_name   = "keterangan"
	_name 		= "anggaran.rka_detail"
	_order		= "id asc"

	@api.onchange('rka_volume_ids','tarif') 
	def on_change_rka_volume_ids(self):
		total = 1
		gab_vol = []
		# count = len(set(self.rka_volume_ids.ids))
		# i=0
		for vol in self.rka_volume_ids:
			total = total * vol.volume
			if vol.volume != False and vol.volume_uom != False:
				# if count != i:
				# 	gab_vol.append(str(vol.volume) +" "+ vol.volume_uom + " x ")
				# else:
				gab_vol.append(str(vol.volume) +" "+ vol.volume_uom)
			# i += 1
		self.jumlah = total 	
		self.volume_total = total * self.tarif
		satuan_volume = ' '.join(map(str, gab_vol))
		self.satuan_volume = satuan_volume.replace(".", ",")

	rka_coa_id 		= fields.Many2one(comodel_name='anggaran.rka_coa', string='MAK')
	keterangan		= fields.Text(string='Detail', required=True)
	satuan_volume	= fields.Char(string="Satuan Keterangan")
	tarif		 	= fields.Float(string='Harga Satuan', required=True)
	jumlah			= fields.Float(string='Volume', required=True)

	volume_total 	= fields.Float(string='Jumlah' , required=True)
	uom_volume		= fields.Char(string='Satuan', required=True)
	rka_volume_ids	= fields.One2many(comodel_name='anggaran.rka_volume',inverse_name='rka_detail_id',
		string='Volume Satuan', ondelete="cascade")


###########################################################################
#Level 5: detail volumes
###########################################################################
class rka_volume(models.Model):
	_name 		= "anggaran.rka_volume"

	rka_detail_id	= fields.Many2one(comodel_name='anggaran.rka_detail', string='RKA Detail')
	volume	 		= fields.Float('Volume')
	# volume_uom		= fields.Many2one(comodel_name='uom.uom', string='Satuan Volume')
	volume_uom		= fields.Char(string='Satuan Volume')
	
