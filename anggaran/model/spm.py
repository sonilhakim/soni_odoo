from odoo import tools
from odoo import fields,models, api
from odoo.exceptions import UserError
import odoo.addons.decimal_precision as dp
import time
import logging
from odoo.tools.translate import _
from odoo.exceptions import UserError, Warning

_logger = logging.getLogger(__name__)
SPM_STATES =[('draft','Draft'),('open','Verifikasi'), 
				('reject','Ditolak'),
				 ('done','Disetujui')]

class spm(models.Model):
	_name 		= "anggaran.spm"

	def _kas_exists(self):
		for spm in self:
			spm.kas_exists = False
			if spm.kas_ids:
				spm.kas_exists = True

	name 			= fields.Char("Nomor", default='/', readonly=True)
	tanggal 		= fields.Date("Tanggal", default=lambda self: time.strftime("%Y-%m-%d"))
	cara_bayar      = fields.Selection([('up','UP'),('gup','GUP'),('tup','TUP'),('ls','LS')],
							'Cara Bayar',required=True)
	unit_id	 		= fields.Many2one(comodel_name='vit.unit_kerja', string='Atas Nama')
	tahun_id		= fields.Many2one(comodel_name='account.fiscal.year', string='Tahun')

	sup_id		    = fields.Many2one(comodel_name='anggaran.sup', string='UP Asal')
	tup_id		    = fields.Many2one(comodel_name='anggaran.tup', string='TUP Asal')
	spp_id		    = fields.Many2one(comodel_name='anggaran.spp', string='SPP Asal')

	pengguna_id  	= fields.Many2one(comodel_name='hr.employee', string='Pengguna Dana')
	nip_pengguna 	= fields.Char(comodel_name='hr.employee', related='pengguna_id.nip', string='NIP Pengguna Dana', store=True, readonly=True)
	dirkeu_id    	= fields.Many2one(comodel_name='hr.employee', string='Direktur Keuangan')
	nip_dirkeu 		= fields.Char(comodel_name='hr.employee', related='dirkeu_id.nip', string='NIP Direktur Keuangan', store=True, readonly=True)	

	spm_line_ids	= fields.One2many(comodel_name='anggaran.spm_line',inverse_name='spm_id',string='Rincian', ondelete="cascade")
	jumlah 			= fields.Float('Jumlah SPM')
	sisa 			= fields.Float('Sisa Anggaran')

	user_id	    	= fields.Many2one(comodel_name='res.users', string='Created', default=lambda self: self.env.uid,)
	state           = fields.Selection(selection=SPM_STATES, string='Status', readonly=True, required=True, default=SPM_STATES[0][0])
	kas_ids			= fields.One2many(comodel_name='anggaran.kas',inverse_name='spm_id',string='Kas Keluar')
	kas_exists		= fields.Boolean(compute='_kas_exists', string='Kas Keluar Sudah Tercatat', help="Apakah SPM ini sudah dicatatkan bukti kas keluar nya.")

	@api.model
	def create(self, vals):
		vals['name']    = self.env['ir.sequence'].next_by_code('anggaran.spm')
		return super(spm, self).create(vals)
	@api.multi	
	def action_draft(self):
		#set to "draft" state
		return self.write({'state':SPM_STATES[0][0]})
	@api.multi
	def action_confirm(self):
		#set to "confirmed" state
		return self.write({'state':SPM_STATES[1][0]})
	@api.multi
	def action_reject(self):
		#set to "done" state
		return self.write({'state':SPM_STATES[2][0]})
	@api.multi
	def action_done(self):
		#set to "done" state
		return self.write({'state':SPM_STATES[3][0]})
	@api.multi
	def action_create_kas_keluar(self, context=None):
	# 	#################################################################
	# 	# spm
	# 	#################################################################
		for spm in self:

		# 	#################################################################
		# 	# kas object
		# 	#################################################################
			kas_obj = self.env["anggaran.kas"]		
		# 	#################################################################
		# 	# cari unit pusat 
		# 	#################################################################
			unit_pusat_id =  self.env["vit.unit_kerja"].search([("name","=","BIRO RENKU")])
			# if not unit_pusat_id:
			# 	raise UserError(_("Unit Pusat tidak ditemukan") ) 

			context.update({
				'tahun_id' 			: spm.tahun_id.id, 
				# 'kegiatan_id' 		: spm.name, 
				'jumlah' 			: spm.jumlah, 
				'unit_id' 			: unit_pusat_id.id, 
				'contra_unit' 		: spm.unit_id.id, 
				'kegiatan_id' 		: False,
				'dasar_pembayaran' 	: '',
				'jenis_item'  		: 'um',
				'sumber_uang' 		: spm.cara_bayar,
				'spm_id' 			: spm.id,

			})
			kas_id = kas_obj.create_kas('out', context)
		
		return kas_id
	
	@api.multi
	def action_view_kas(self):
		kases = self.mapped('kas_ids')
		action = self.env.ref('anggaran.action_kas_keluar_list').read()[0]
		# if len(kases) > 1:
		# 	action['domain'] = [('id', 'in', ["+','.join(map(str, kases))+"])]
		if len(kases) == 1:
			form_view = [(self.env.ref('anggaran.view_kas_form').id, 'form')]
			if 'views' in action:
				action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
			else:
				action['views'] = form_view
			action['res_id'] = kases.ids[0]
		else:
			action = {'type': 'ir.actions.act_window_close'}
		return action

	@api.multi
	def unlink(self):
		for me_id in self :
			if me_id.state != SPM_STATES[0][0]:
				raise UserError("Tidak bisa dihapus selain dalam status Rancangan!")
		return super(spm, self).unlink()

class spm_line(models.Model):
	_name 		= "anggaran.spm_line"

	spm_id			= fields.Many2one(comodel_name='anggaran.spm', string='SPM')
	# kebijakan_id	= fields.Many2one(comodel_name='anggaran.kebijakan', string='Kebijakan')
	kegiatan 		= fields.Text(string='Kegiatan')
	pagu			= fields.Float('PAGU')
	up_sd_lalu		= fields.Float('UP/GUP sd yg Lalu')
	up_ini			= fields.Float('UP/GUP Ini')
	jumlah_up		= fields.Float('Jumlah sd UP/GUP Ini')
	sisa_dana		= fields.Float('Sisa Dana')

