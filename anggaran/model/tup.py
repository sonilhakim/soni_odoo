from odoo import tools
from odoo import fields, models, api
import odoo.addons.decimal_precision as dp
import time
import logging
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)
TUP_STATES =[ 	('draft','Draft'),
				('open','Verifikasi'), 
				('reject','Ditolak'),
                ('done','Disetujui')]

class tup(models.Model):
	_name 		= 'anggaran.tup'

	name 				= fields.Char('Nomor' , readonly=True, required=True, default='/' )
	tanggal 			= fields.Date('Tanggal', required=True, default=lambda self: time.strftime("%Y-%m-%d"))
	tahun_id		    = fields.Many2one(comodel_name='account.fiscal.year', string='Tahun')
	lampiran			= fields.Integer('Lampiran')
	perihal 			= fields.Char('Perihal', required=True)
	kepada  			= fields.Text('Kepada', required=True)
	dasar_rkat 			= fields.Char('Dasar RKAT Nomor/Tanggal', required=True)
	jumlah  			= fields.Float('Jumlah', required=True)
	unit_id 			= fields.Many2one(comodel_name='vit.unit_kerja', string='Atas Nama', required=True)
	nomor_rek 			= fields.Char('Nomor Rekening')
	nama_bank 			= fields.Char('Nama Bank')
	pumkc_id     		= fields.Many2one(comodel_name='hr.employee', string='PUMKC')
	nip_pumkc 			= fields.Char(comodel_name='hr.employee', related='pumkc_id.nip', string='NIP PUMKC', store=True, readonly=True)
	atasan_pumkc_id   	= fields.Many2one(comodel_name='hr.employee', string='Atasan Langsung PUMKC')
	nip_atasan_pumkc	= fields.Char(comodel_name='hr.employee', related='atasan_pumkc_id.nip', string='NIP Atasan PUMKC', store=True, readonly=True)
	state             	= fields.Selection(selection=TUP_STATES, string='Status', readonly=True, required=True, default=TUP_STATES[0][0])
	user_id	    		= fields.Many2one(comodel_name='res.users', string='Created', default=lambda self: self.env.uid)

	
	def create(self, vals):
		vals['name']    = self.env['ir.sequence'].next_by_code('anggaran.tup')
		return super(tup, self).create(vals)
		
	def action_draft(self):
		#set to "draft" state
		return self.write({'state':TUP_STATES[0][0]})
	
	def action_confirm(self):
		#set to "confirmed" state
		return self.write({'state':TUP_STATES[1][0]})
	
	def action_reject(self):
		#set to "reject" state
		return self.write({'state':TUP_STATES[2][0]})	
		
	def action_done(self):
		#set to "done" state
		return self.write({'state':TUP_STATES[3][0]})

	def action_create_spm(self):
		for tup in self:
			spm_obj = self.env["anggaran.spm"]
			data = {
				'name' 			: '/',
				'tanggal' 		: time.strftime("%Y-%m-%d") ,
				'cara_bayar'    : 'up',
				'unit_id'	 	: tup.unit_id.id,
				'tahun_id'		: tup.tahun_id.id,
				'jumlah' 		: tup.jumlah,
				'sisa' 			: 0.0,
				'user_id'	    : self.env.uid, 
				'state'         : 'draft',
				'tup_id'		: tup.id
			}
		spm_id = spm_obj.create(data)
		return spm_id

