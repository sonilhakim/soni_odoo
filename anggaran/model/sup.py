from odoo import tools
from odoo import fields, models, api
import odoo.addons.decimal_precision as dp
import time
import logging
from odoo.tools.translate import _
from odoo.exceptions import UserError, Warning

_logger = logging.getLogger(__name__)
SUP_STATES =[ 	('draft','Draft'),
				('open','Verifikasi'), 
				('reject','Ditolak'),
				('done','Disetujui')]

class sup(models.Model):
	_name 		= 'anggaran.sup'

	def _spm_exists(self):
		for sup in self:
			sup.spm_exists = False
			if sup.spm_ids:
				sup.spm_exists = True

	name 				= fields.Char('Nomor' , readonly=True, required=True, default='/')
	tanggal 			= fields.Date('Tanggal', required=True, default=lambda self: time.strftime("%Y-%m-%d"))
	tahun_id		    = fields.Many2one(comodel_name='account.fiscal.year', string='Tahun')
	period_id		    = fields.Many2one(comodel_name='account.period', string='Period', compute='_fperiode', store=True,)
	lampiran			= fields.Integer('Lampiran')
	perihal 			= fields.Char('Perihal', required=True, default='Permohonan Uang Persediaan')
	kepada  			= fields.Text('Kepada', required=True, default='Bendahara Pusat')
	# 'dasar_rkat' 		= fields.Char('Dasar RKAT Nomor/Tanggal', required=True),
	dasar_rkat 			= fields.Many2one(comodel_name='anggaran.rka', string='Dasar ROA', required=True)
	jumlah  			= fields.Float('Jumlah', required=True)
	unit_id 			= fields.Many2one(comodel_name='vit.unit_kerja', string='Atas Nama', required=True)
	nomor_rek 			= fields.Char('Nomor Rekening')
	nama_bank 			= fields.Char('Nama Bank')
	pumkc_id     		= fields.Many2one(comodel_name='hr.employee', string='PUMKC')
	nip_pumkc 			= fields.Char(comodel_name='hr.employee', related='pumkc_id.nip', string='NIP PUMKC', store=True, readonly=True)
	atasan_pumkc_id		= fields.Many2one(comodel_name='hr.employee', string='Atasan Langsung PUMKC')
	nip_atasan_pumkc 	= fields.Char(comodel_name='hr.employee', related='atasan_pumkc_id.nip', string='NIP Atasan PUMKC', store=True, readonly=True)
	state       	    = fields.Selection(selection=SUP_STATES, string='Status', readonly=True, required=True, default=SUP_STATES[0][0])
	user_id		    	= fields.Many2one(comodel_name='res.users', string='Created', default=lambda self: self.env.uid)
	spm_ids				= fields.One2many(comodel_name='anggaran.spm',inverse_name='sup_id',string='SPM')
	spm_exists			= fields.Boolean(compute=_spm_exists, string='SPM Sudah Tercatat', help="Apakah UP ni sudah dicatatkan SPM-nya.")

	@api.depends('tahun_id')
	def _fperiode(self):
		periode = ''
		for sup in self:
			periode = int(sup.tahun_id.name) + 1
			acc_periode = sup.env['account.period'].search([('name','=',str(periode))])
			# import pdb; pdb.set_trace()
			if acc_periode:
				sup.period_id = acc_periode.id

	@api.model
	def create(self, vals):
		vals['name'] = self.env['ir.sequence'].next_by_code('anggaran.sup')
		return super(sup, self).create(vals)
		
	@api.multi
	def action_draft(self):
		#set to "draft" state
		return self.write({'state':SUP_STATES[0][0]})
	@api.multi
	def action_confirm(self):
		#set to "confirmed" state
		return self.write({'state':SUP_STATES[1][0]})
	@api.multi
	def action_reject(self):
		#set to "reject" state
		return self.write({'state':SUP_STATES[2][0]})	
	@api.multi	
	def action_done(self):
		#set to "done" state
		return self.write({'state':SUP_STATES[3][0]})
	@api.multi
	def action_create_spm(self):
		for sup in self:

	# 	#############################################################
	# 	# cari rka utk unit_id
	# 	#############################################################
			rka_obj = self.env["anggaran.rka"]
			rka_ids = rka_obj.search([('unit_id.id','=', sup.unit_id.id)])
			for rka in rka_ids:	
				spm_line_ids = []
				for keg in rka.rka_kegiatan_ids:
					# kegiatan_ids += keg.indikator

					spm_line_ids.append((0,0,{
						'kegiatan'	: keg.indikator,
						'pagu'		: keg.anggaran,
						'sisa_dana'	: keg.sisa
					}))
					# spm_line_ids = [(0,0,{
					# 	'kebijakan_id' : bij.id
					# }) for bij 
					# in set(kebijakan_ids) ]

				spm_obj = self.env["anggaran.spm"]
				data = {
					'name' 			: '/',
					'tanggal' 		: time.strftime("%Y-%m-%d") ,
					'cara_bayar'    : 'up',
					'unit_id'	 	: sup.unit_id.id,
					'tahun_id'		: sup.tahun_id.id,
					'jumlah' 		: sup.jumlah,
					'sisa' 			: rka.sisa,
					'user_id'	    : self.env.uid, 
					'state'         : 'draft',
					'sup_id'		: sup.id,
					'spm_line_ids'	: spm_line_ids
				}
			spm_id = spm_obj.create(data)
			return spm_id

	@api.multi
	def action_view_spm(self):
		spms = self.mapped('spm_ids')
		action = self.env.ref('anggaran.action_spm_list').read()[0]
		# if len(spms) > 1:
		# 	action['domain'] = [('id', 'in', ["+','.join(map(str, spms))+"])]
		if len(spms) == 1:
			form_view = [(self.env.ref('anggaran.view_spm_form').id, 'form')]
			if 'views' in action:
				action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
			else:
				action['views'] = form_view
			action['res_id'] = spms.ids[0]
		else:
			action = {'type': 'ir.actions.act_window_close'}
		return action


	@api.multi
	def unlink(self):
		for me_id in self :
			if me_id.state != SUP_STATES[0][0]:
				raise UserError("Tidak bisa dihapus selain dalam status Rancangan!")
		return super(sup, self).unlink()