from odoo import tools
from odoo import models, fields, api
import odoo.addons.decimal_precision as dp
import time
import logging
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)
BIAYA_STATES =[('draft','Draft'),('open','Verifikasi'), ('reject','Ditolak'),
                 ('done','Disetujui')]

class biaya(models.Model):
	_name 		= 'anggaran.biaya'

	name 				= fields.Char('Nomor', default='/', required=True, readonly=True)
	tanggal 			= fields.Date('Tanggal', required=True, default=lambda self: time.strftime("%Y-%m-%d"))
	unit_id	 			= fields.Many2one(comodel_name='vit.unit_kerja', string='SUBSATKER')
	tahun_id		    = fields.Many2one(comodel_name='account.fiscal.year', string='Tahun')
	kas_id		    	= fields.Many2one(comodel_name='anggaran.kas', string='Kas Keluar', domain=[('type','=','out')])
	keperluan  			= fields.Many2one(comodel_name='anggaran.rka_kegiatan', string='Untuk Keperluan')
	total 				= fields.Float("Total Biaya")
	kepada_partner_id	= fields.Many2one(comodel_name='res.partner', string='Dibayarkan Kepada', help="Partner (Supplier/Perorangan) penerima")
	biaya_line_ids 		= fields.One2many(comodel_name='anggaran.biaya_line',inverse_name='biaya_id',string='Penjelasan', ondelete="cascade")
	pumkc_id     		= fields.Many2one(comodel_name='hr.employee', string='PUMKC')
	nip_pumkc 			= fields.Char(related='pumkc_id.nip', string='NIP PUMKC', store=True, readonly=True)
	atasan_pumkc_id  	= fields.Many2one(comodel_name='hr.employee', string='Atasan Langsung PUMKC')
	nip_atasan_pumkc 	= fields.Char(related='atasan_pumkc_id.nip', string='NIP Atasan PUMKC', store=True, readonly=True)
	user_id	    		= fields.Many2one(comodel_name='res.users', string='Created', default=lambda self: self.env.uid, required=True,readonly=True)
	state             	= fields.Selection(string="Status", selection=BIAYA_STATES, required=True, readonly=True, default=BIAYA_STATES[0][0])

	@api.multi
	def action_draft(self):
		#set to "draft" state
		return self.write({'state':BIAYA_STATES[0][0]})
	
	@api.multi
	def action_confirm(self):
		#set to "confirmed" state
		return self.write({'state':BIAYA_STATES[1][0]})
	
	@api.multi
	def action_reject(self):
		#set to "done" state
		return self.write({'state':BIAYA_STATES[2][0]})
	
	@api.multi
	def action_done(self):
		#set to "done" state
		return self.write({'state':BIAYA_STATES[3][0]})

	@api.model
	def create(self, vals):
		vals['name']    = self.env['ir.sequence'].next_by_code('anggaran.biaya')
		return super(biaya, self).create(vals)



class biaya_line(models.Model):
	_name 		= "anggaran.biaya_line"

	# @api.onchange('sptb_line_ids')
	# def _sudah_sptb(self):
	# 	for biaya_line in self:
	# 		if biaya_line.sptb_line_ids:
	# 			biaya_line.sudah_sptb = True

	biaya_id		= fields.Many2one(comodel_name='anggaran.biaya', string='Biaya')
	rka_coa_id	 	= fields.Many2one(comodel_name='anggaran.rka_coa', string='COA Bersangkutan')
	biaya_ini	  	= fields.Float("Jumlah")
	uraian  		= fields.Char('Uraian')
	sptb_line_ids	= fields.One2many(comodel_name='anggaran.sptb_line',inverse_name='biaya_line_id',string='SPTB Item')
	sudah_sptb		= fields.Boolean(string='Sudah di-SPTB-kan', help="Apakah biaya ini sudah dicatatkan ke SPTB.")


