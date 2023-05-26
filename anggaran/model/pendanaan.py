from odoo import tools
from odoo import fields, models, api
import odoo.addons.decimal_precision as dp
import time
import logging
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)
PENDANAAN_STATES =[('draft','Draft'),('open','Verifikasi'), ('reject','Ditolak'),
                 ('done','Disetujui')]

class pendanaan(models.Model):
	_name 		= 'anggaran.pendanaan'

	name 				= fields.Char('Nomor', required=True, readonly=True)
	tanggal 			= fields.Date('Tanggal', required=True, default=lambda self: time.strftime("%Y-%m-%d"))
	unit_id	 			= fields.Many2one(comodel_name='vit.unit_kerja', string='SUBSATKER')
	tahun_id			= fields.Many2one(comodel_name='account.fiscal.year', string='Tahun')
	period_id			= fields.Many2one(comodel_name='account.period', string='Period')
	keperluan  			= fields.Many2one(comodel_name='anggaran.rka_kegiatan', string='Untuk Keperluan')
	total 				= fields.Float("Total Pendanaan")
	pendanaan_line_ids	= fields.One2many(comodel_name='anggaran.pendanaan_line',inverse_name='pendanaan_id',string='Penjelasan', 
							ondelete="cascade")
	pumkc_id     		= fields.Many2one(comodel_name='hr.employee', string='PUMKC')
	nip_pumkc 			= fields.Char(related='pumkc_id.nip', string='NIP PUMKC', store=True, readonly=True)
	atasan_pumkc_id 	= fields.Many2one(comodel_name='hr.employee', string='Atasan Langsung PUMKC')
	nip_atasan_pumkc 	= fields.Char(related='atasan_pumkc_id.nip', string='NIP Atasan PUMKC', store=True, readonly=True)
	user_id	    		= fields.Many2one(comodel_name='res.users', string='Created', required=True,readonly=True)
	state           	= fields.Selection(selection=PENDANAAN_STATES, string='Status',readonly=True,required=True,default=PENDANAAN_STATES[0][0])

	def action_draft(self):
		#set to "draft" state
		return self.write({'state':PENDANAAN_STATES[0][0]})
	
	def action_confirm(self):
		#set to "confirmed" state
		return self.write({'state':PENDANAAN_STATES[1][0]})
	
	def action_reject(self):
		#set to "done" state
		return self.write({'state':PENDANAAN_STATES[2][0]})
	
	def action_done(self):
		#set to "done" state
		return self.write({'state':PENDANAAN_STATES[3][0]})

	def create(self,vals):
		vals['name']    = self.env['ir.sequence'].next_by_code('anggaran.pendanaan')
		return super(biaya, self).create(vals)



class pendanaan_line(models.Model):
	_name 		= "anggaran.pendanaan_line"


	pendanaan_id	= fields.Many2one(comodel_name='anggaran.pendanaan', string='Pendanaan')
	pendanaan_ini  	= fields.Float("Jumlah")
	uraian  		= fields.Char('Uraian')
	sudah_sptb		= fields.Boolean(string='Sudah di-SPTB-kan', type='boolean', help="Apakah pendanaan ini sudah dicatatkan ke SPTB."),


