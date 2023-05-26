from odoo import tools
from odoo import fields, models, api
import odoo.addons.decimal_precision as dp
import time
import logging
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)
INVESTASI_STATES =[('draft','Draft'),('open','Verifikasi'), ('reject','Ditolak'),
                 ('done','Disetujui')]

class investasi(models.Model):
	_name 		= 'anggaran.investasi'

	name				= fields.Char('Nomor', default='/', required=True, readonly=True)
	tanggal				= fields.Date('Tanggal', required=True, default=lambda self: time.strftime("%Y-%m-%d"))
	unit_id				= fields.Many2one(comodel_name='vit.unit_kerja', string='SUBSATKER')
	tahun_id			= fields.Many2one(comodel_name='account.fiscal.year', string='Tahun')
	period_id			= fields.Many2one(comodel_name='account.period', string='Perioda')
	# 'keperluan'  		: fields.Many2one('anggaran.rka_kegiatan', 'Untuk Keperluan'),
	kepada_partner_id	= fields.Many2one(comodel_name='res.partner', string='Dibayarkan Kepada', help="Partner (Supplier/Perorangan) penerima")
	keperluan			= fields.Text("Keperluan")
	total				= fields.Float("Total Biaya")
	pumkc_id			= fields.Many2one(comodel_name='hr.employee', string='PUMKC')
	nip_pumkc			= fields.Char(related='pumkc_id.nip', string='NIP PUMKC', store=True, readonly=True)
	atasan_pumkc_id		= fields.Many2one(comodel_name='hr.employee', string='Atasan Langsung PUMKC')
	nip_atasan_pumkc 	= fields.Char(related='atasan_pumkc_id.nip', string='NIP Atasan PUMKC', store=True, readonly=True)
	user_id	    		= fields.Many2one(comodel_name='res.users', string='Created', required=True, readonly=True, default=lambda self: self.env.uid)
	state             	= fields.Selection(string="Status", selection=INVESTASI_STATES, required=True, readonly=True, default=INVESTASI_STATES[0][0])

	@api.multi
	def action_draft(self):
		#set to "draft" state
		return self.write({'state':INVESTASI_STATES[0][0]})
	
	@api.multi
	def action_confirm(self):
		#set to "confirmed" state
		return self.write({'state':INVESTASI_STATES[1][0]})
	
	@api.multi
	def action_reject(self):
		#set to "done" state
		return self.write({'state':INVESTASI_STATES[2][0]})
	
	@api.multi
	def action_done(self):
		#set to "done" state
		return self.write({'state':INVESTASI_STATES[3][0]})

	
	@api.model
	def create(self, vals):
		vals['name']    = self.env['ir.sequence'].next_by_code('anggaran.investasi')
		return super(investasi, self).create(vals)



class investasi_line(models.Model):
	_name 		= "anggaran.investasi_line"

	# def _sudah_sptb_search(self, cr, uid, obj, name, args, context=None):
	# 	#########################################################
	# 	# return list of tuples [('id','in',[1,2,3,4])]
	# 	# dimana 1,2,3,4 adalah id record yang mathcing dengan 
	# 	# yang dicari (misalnya yang sudah di-sptb, mana aja id nya)
	# 	#########################################################
	# 	data = [('sptb_line_ids','!=',False)]
	# 	res = self.search(cr, uid, data, context=context)
	# 	if not res:
	# 		return [('id', '=', 0)]
	# 	return [('id', 'in', [x[0] for x in res])]

	investasi_id	= fields.Many2one(comodel_name='anggaran.investasi', string='Biaya')
	rka_coa_id	 	= fields.Many2one(comodel_name='anggaran.rka_coa', string='COA Bersangkutan')
	investasi_ini  	= fields.Float("Jumlah")
	uraian  		= fields.Char('Uraian')

