from odoo import tools
from odoo import fields, models, api
import odoo.addons.decimal_precision as dp
import time
import logging
from odoo.tools.translate import _
from odoo.exceptions import UserError, Warning

_logger = logging.getLogger(__name__)
SPTB_STATES =[('draft','Draft'),('open','Verifikasi'), ('reject','Ditolak'),
				 ('done','Disetujui')]

class sptb(models.Model):
	_name 		= 'anggaran.sptb'

	def _spp_exists(self):
		for sptb in self:
			sptb.spp_exists = False
			if sptb.spp_ids:
				sptb.spp_exists = True

	def _total(self):
		for sptb in self:
			if sptb.sptb_line_ids:
				total = 0.0
				for sl in sptb.sptb_line_ids:
					total += sl.jumlah
				sptb.total = total

	name 				= fields.Char('Nomor', default='/', readonly=True)
	tanggal 			= fields.Date('Tanggal', readonly=True, default=lambda self: time.strftime("%Y-%m-%d"))
	tahun_id		   	= fields.Many2one(comodel_name='account.fiscal.year', string='Tahun', required=True)
	unit_id           	= fields.Many2one(comodel_name='vit.unit_kerja', string='SUBSATKER', required=True)
	jenis_belanja_id 	= fields.Many2one(comodel_name='account.account', string='Bagan Akun', required=True)
	rka_id				= fields.Many2one(comodel_name='anggaran.rka', string='Dasar Anggaran')
	rka_kegiatan_id 	= fields.Many2one(comodel_name='anggaran.rka_kegiatan', string='Kegiatan')
	program_id 			= fields.Many2one(comodel_name='anggaran.program', related='rka_kegiatan_id.kegiatan_id.program_id', string="Program",  readonly=True)
	kebijakan_id		= fields.Many2one(comodel_name='anggaran.kebijakan', related='program_id.kebijakan_id', string="Kebijakan",  readonly=True)
	sptb_line_ids     	= fields.One2many(comodel_name='anggaran.sptb_line',inverse_name='sptb_id',string='Penjelasan', ondelete="cascade")
	pumkc     			= fields.Many2one(comodel_name='hr.employee', string='PUMKC')
	nip_pumkc 			= fields.Char(comodel_name='hr.employee', related='pumkc.nip', string='NIP PUMKC', store=True, readonly=True)
	kasubag_aftik     	= fields.Many2one(comodel_name='hr.employee', string='Kasubag AFTIK')
	nip_kasubag_aftik 	= fields.Char(comodel_name='hr.employee', related='kasubag_aftik.nip', string='NIP Kasubag AFTIK', store=True, readonly=True)
	atasan_pumkc     	= fields.Many2one(comodel_name='hr.employee', string='Atasan Langsung PUMKC')
	nip_atasan_pumkc 	= fields.Char(comodel_name='hr.employee', related='atasan_pumkc.nip', string='NIP Atasan PUMKC', store=True, readonly=True)
	div_anggaran     	= fields.Many2one(comodel_name='hr.employee', string='Divisi Anggaran')
	nip_div_anggaran 	= fields.Char(comodel_name='hr.employee', related='div_anggaran.nip', string='NIP Divisi Anggaran', store=True, readonly=True)
	div_akuntansi     	= fields.Many2one(comodel_name='hr.employee', string='Divisi Akuntansi')
	nip_div_akuntansi	= fields.Char(comodel_name='hr.employee', related='div_akuntansi.nip', string='NIP Divisi Akuntansi', store=True, readonly=True)
	user_id	    		= fields.Many2one(comodel_name='res.users', string='Created', default=lambda self: self.env.uid)
	state             	= fields.Selection(selection=SPTB_STATES, string='Status', readonly=True, required=True, default=SPTB_STATES[0][0])
	spp_ids				= fields.One2many(comodel_name='anggaran.spp',inverse_name='sptb_id',string='SPP')
	spp_exists			= fields.Boolean(compute='_spp_exists', string='SPP Sudah Tercatat', help="Apakah SPTB ini sudah dicatatkan SPP nya.")
	total				= fields.Float(compute='_total', string='Total')

	@api.model
	def create(self, vals):
		vals['name']    = self.env['ir.sequence'].next_by_code('anggaran.sptb')
		return super(sptb, self).create(vals)

	@api.multi
	def action_draft(self):
		#set to "draft" state
		return self.write({'state':SPTB_STATES[0][0]})
	
	@api.multi
	def action_confirm(self):
		#set to "confirmed" state
		return self.write({'state':SPTB_STATES[1][0]})
	
	@api.multi
	def action_done(self):
		#set to "done" state
		return self.write({'state':SPTB_STATES[3][0]})	

	@api.multi
	def action_reject(self):
		#set to "done" state
		return self.write({'state':SPTB_STATES[2][0]})

	@api.multi
	def action_tarik_biaya(self):
		#######################################################################
		# tarik semua biaya_line_id yang blm di SPTB-kan
		# dan COA nya sama dengan jenis_belanja_id
		# dan yang ditujukan kepada partner / bukan unit kerja
		# dan biaya yang sudah done
		# dan milik unit kerja ybs
		#######################################################################
		for sptb in self:
			bl_obj = self.env["anggaran.biaya_line"]
			bl_ids = bl_obj.search([
				('rka_coa_id.mak_id.coa_id.id','=', sptb.jenis_belanja_id.id),
				('sptb_line_ids','=',False),
				('biaya_id.kepada_partner_id','!=', False),
				('biaya_id.unit_id.id', '=', sptb.unit_id.id),
				('biaya_id.state','=','done')])
			# import pdb; pdb.set_trace()

			#######################################################################
			# insert ke sptb_line
			# caranya, update field sptb_line_ids di sptb
			#######################################################################
			for bl in bl_ids:	
				sptb_lines = [(0,0,{
					'penerima_id'   : bl.biaya_id.kas_id.kepada_partner_id.id or False,
					'biaya_line_id' : bl.id,
					'uraian'        : bl.uraian,
					'bukti_no'      : "%s %s" % (bl.biaya_id.kas_id.name,bl.biaya_id.name) ,
					'bukti_tanggal' : bl.biaya_id.kas_id.tanggal,
					'jumlah' 		: bl.biaya_ini,
					})]

				data = {
					'sptb_line_ids': sptb_lines
				}
				self.write(data)
				bl.write({'sudah_sptb' : True})

		return True 


	# @api.multi
	# def action_tarik_sptb(self):
		#######################################################################
		# cari unit_ids dari unit kerja jurusan di bawah fakultas ini (unit_id)
		# cari sptb milik unit_ids tsb yg sudah done
		# dan belum di-sptb-kan 
		# copy sptb_line ke sptb ini
		#######################################################################		
		# for sptb in self:

		# 	sptb_lines = []
			# unit_ids = self.env["vit.unit_kerja"].search([('jurusan_id.fakultas_id','=',sptb.unit_id.fakultas_id.id)])
			# for unit_id in unit_ids:
		# 	sptb_ids = self.search([('unit_id','=', sptb.unit_id.id),('id','<>',sptb.id),('state','=','done')])
		# 	for sptb_unit in sptb_ids:
		# 		for sl in sptb_unit.sptb_line_ids:
		# 			if sl.sudah_sptb == False: # yang belum di-sptb-kan saja
		# 				sptb_lines += [(0,0,{
		# 					'penerima_id'   : sl.penerima_id.id or False,
		# 					'biaya_line_id' : sl.biaya_line_id.id,
		# 					'sptb_line_id'  : sl.id,
		# 					'uraian'        : sl.uraian,
		# 					'bukti_no'      : sl.bukti_no,
		# 					'bukti_tanggal' : sl.bukti_tanggal,
		# 					'jumlah' 		: sl.jumlah,
		# 				}) ]
		# 	data = {
		# 		'sptb_line_ids': sptb_lines
		# 	}
		# 	self.write(data)				
		# return True 

	@api.multi
	def action_create_spp(self):
		spp_lines = []
		for sptb in self:
			spp_lines = [(0,0,{
				'rka_kegiatan_id'   : sptb.rka_kegiatan_id.id,
				'pagu' : sptb.rka_kegiatan_id.anggaran,
				'spp_lalu' : sptb.rka_kegiatan_id.realisasi,
				'spp_ini' : sptb.total,
				'jumlah_spp' : sptb.rka_kegiatan_id.realisasi + sptb.total,
				'sisa_dana' : sptb.rka_kegiatan_id.anggaran - (sptb.rka_kegiatan_id.realisasi + sptb.total),
			}) ]
			spp  = self.env["anggaran.spp"]
			data = {
				'name' 				: '/',
				'tanggal' 			: time.strftime("%Y-%m-%d"),
				'kepada'  			: 'Direktorat Keuangan',
				'jumlah'  			: sptb.total,
				'keperluan' 		: '',
				'cara_bayar'      	: 'tup',
				'unit_id'  			: sptb.unit_id.id,
				'rka_id'   			: sptb.rka_id.id,
				'nomor_rek' 		: '',
				'nama_bank' 		: '',
				'tahun_id'			: sptb.tahun_id.id,
				# 'period_id'			: sptb.rka_kegiatan_id.rka_id.period_id.id,
				'spp_line_ids' 		: spp_lines,
				'user_id'	    	: self.env.uid,
				'state'           	: 'draft',
				'sptb_id'     		: sptb.id
			}
		spp_id = spp.create(data)
		return spp_id

	# def action_view_spp(self, cr, uid, ids, context=None):
	# 	'''
	# 	This function returns an action that display existing spp 
	# 	of given kas ids. It can either be a in a list or in a form view, 
	# 	if there is only one spp to show.
	# 	'''
	# 	mod_obj = self.pool.get('ir.model.data')
	# 	act_obj = self.pool.get('ir.actions.act_window')

	# 	result = mod_obj.get_object_reference(cr, uid, 'anggaran', 'action_spp_list')
	# 	id = result and result[1] or False
	# 	result = act_obj.read(cr, uid, [id], context=context)[0]
	# 	#compute the number of spp to display
	# 	spp_ids = []
	# 	for kas in self.browse(cr, uid, ids, context=context):
	# 		spp_ids += [spp.id for spp in kas.spp_ids]
	# 	#choose the view_mode accordingly
	# 	if len(spp_ids)>1:
	# 		result['domain'] = "[('id','in',["+','.join(map(str, spp_ids))+"])]"
	# 	else:
	# 		res = mod_obj.get_object_reference(cr, uid, 'anggaran', 'view_spp_form')
	# 		result['views'] = [(res and res[1] or False, 'form')]
	# 		result['res_id'] = spp_ids and spp_ids[0] or False
	# 	return result

	@api.multi
	def action_view_spp(self):
		spps = self.mapped('spp_ids')
		action = self.env.ref('anggaran.action_spp_list').read()[0]
		# if len(spps) > 1:
		# 	action['domain'] = [('id', 'in', ["+','.join(map(str, spps))+"])]
		if len(spps) == 1:
			form_view = [(self.env.ref('anggaran.view_spp_form').id, 'form')]
			if 'views' in action:
				action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
			else:
				action['views'] = form_view
			action['res_id'] = spps.ids[0]
		else:
			action = {'type': 'ir.actions.act_window_close'}
		return action

	@api.multi
	def unlink(self):
		for me_id in self :
			if me_id.state != SPTB_STATES[0][0]:
				raise UserError("Tidak bisa dihapus selain dalam status Rancangan!")
		return super(sptb, self).unlink()

class sptb_line(models.Model):
	_name 		= "anggaran.sptb_line"

	# @api.depends('sptb_line_ids')
	# def _sudah_sptb(self):
	# 	for sptb_line in self:
	# 		sptb_line.sudah_sptb = False
	# 		if sptb_line.sptb_line_ids:
	# 			sptb_line.sudah_sptb = True

	sptb_id 		= fields.Many2one(comodel_name='anggaran.sptb', string='SPTB')
	penerima_id   	= fields.Many2one(comodel_name='res.partner', string='Penerima')
	biaya_line_id 	= fields.Many2one(comodel_name='anggaran.biaya_line', string='Sumber Biaya Item')
	sptb_line_id  	= fields.Many2one(comodel_name='anggaran.sptb_line', string='Sumber SPTB Item')
	uraian        	= fields.Char('Uraian')
	bukti_no      	= fields.Char('No Bukti')
	bukti_tanggal 	= fields.Char('Tanggal Bukti')
	jumlah 			= fields.Float("Jumlah")
	sptb_line_ids	= fields.One2many(comodel_name='anggaran.sptb_line',inverse_name='sptb_line_id',string='SPTB Items')
	# sudah_sptb		= fields.Boolean(compute='_sudah_sptb', string='Sudah di-SPTB-kan', help="Apakah SPTB Jurusan ini sudah dicatatkan ke SPTB lain (Fakultas).")
