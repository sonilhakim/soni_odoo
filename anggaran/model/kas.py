from odoo import tools
from odoo import fields, models, api
from odoo.exceptions import UserError
import odoo.addons.decimal_precision as dp
import time
import logging
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)
KAS_STATES =[('draft','Draft'),('open','Verifikasi'), ('reject','Ditolak'),
				 ('done','Disetujui')]

class kas(models.Model):
	_name       = "anggaran.kas"

	def _biaya_exists(self):
		for kas in self:
			if kas.biaya_ids:
				kas.biaya_exists = True

	name                = fields.Char("Nomor", default='/', readonly=True )
	tanggal             = fields.Date("Tanggal", required=True, default=lambda self: time.strftime("%Y-%m-%d"))
	tahun_id            = fields.Many2one(comodel_name='account.fiscal.year', string='Tahun', required=True)
	unit_id             = fields.Many2one(comodel_name='vit.unit_kerja', string='SUBSATKER', required=True, help="Unit Kerja yang memiliki transaksi ini")
	sumber_uang         = fields.Selection([('up','UP'),('tup','TUP'),('gup','GUP')],
							'Sumber Uang', help="Dari UP, TUP, atau GUP")
	type                = fields.Selection([('in','Masuk'),('out','Keluar')],'Jenis Kas',required=True)
	jenis_item          = fields.Selection([('um','Uang Muka'),('def','Definitif')],'Jenis Item',required=True)
	journal_id          = fields.Many2one(comodel_name='account.journal', string='Journal')
	kepada_unit_id      = fields.Many2one(comodel_name='vit.unit_kerja', string='Dibayarkan Kepada Unit', help="Unit penerima uang kas keluar")
	dari_unit_id        = fields.Many2one(comodel_name='vit.unit_kerja', string='Diterima Dari', help="Unit pengirim uang kas masuk")
	kepada_partner_id   = fields.Many2one(comodel_name='res.partner', string='Dibayarkan Kepada Partner', help="Partner (Supplier/Perorangan) penerima kas keluar")
	jumlah              = fields.Float("Jumlah", required=True)
	cheque_nomor        = fields.Char("Cheque Nomor")
	rek_nomor           = fields.Char("Rekening Nomor")
	rka_id				= fields.Many2one(comodel_name='anggaran.rka', string='Dasar Anggaran')
	kegiatan_id         = fields.Many2one(comodel_name='anggaran.rka_kegiatan', string='Untuk Keperluan')
	dasar_pembayaran    = fields.Char("Dasar Pembayaran")
	bendahara_id        = fields.Many2one(comodel_name='hr.employee', string='Bendahara Penerima')
	nip_bendahara       = fields.Char(related='bendahara_id.nip', string='NIP Bendahara Penerima', store=True, readonly=True)
	kadiv_anggaran_id   = fields.Many2one(comodel_name='hr.employee', string='Kepala Divisi Anggaran')
	nip_kadiv_anggaran  = fields.Char(related='kadiv_anggaran_id.nip', string='NIP Kepala Divisi Anggaran', store=True, readonly=True)
	kadiv_akuntansi_id  = fields.Many2one(comodel_name='hr.employee', string='Kepala Divisi Akuntansi')
	nip_kadiv_akuntansi = fields.Char(related='kadiv_akuntansi_id.nip', string='NIP Kepala Divisi Akuntansi', store=True, readonly=True)
	dirkeu_id           = fields.Many2one(comodel_name='hr.employee', string='Direktur Direktorat Keuangan')
	nip_dirkeu_id       = fields.Char(related='dirkeu_id.nip', string='NIP Direktur Direktorat Keuangan', store=True, readonly=True)
	state               = fields.Selection(string="Status", selection=KAS_STATES, required=True, readonly=True, default=KAS_STATES[0][0])
	user_id             = fields.Many2one(comodel_name='res.users', string='Created', default=lambda self: self.env.uid)
	spm_id              = fields.Many2one(comodel_name='anggaran.spm', string='SPM Asal', help="SPM untuk Pengeluaran Kas")
	biaya_ids           = fields.One2many(comodel_name='anggaran.biaya',inverse_name='kas_id',string='Biaya')
	biaya_exists        = fields.Boolean(string='Biaya Sudah Tercatat',compute='_biaya_exists', help="Apakah kas keluar ini sudah dicatatkan bukti biayanya.")

	@api.multi
	def action_view_biaya(self):
		biayas = self.mapped('biaya_ids')
		action = self.env.ref('anggaran.action_biaya_list').read()[0]
		if len(biayas) > 1:
			action['domain'] = [('id', 'in', ["+','.join(map(str, biayas))+"])]
		elif len(biayas) == 1:
			form_view = [(self.env.ref('anggaran.view_biaya_form').id, 'form')]
			if 'views' in action:
				action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
			else:
				action['views'] = form_view
			action['res_id'] = biayas.ids[0]
		else:
			action = {'type': 'ir.actions.act_window_close'}
		return action
	
	@api.model
	def create(self, vals):
		vals['name'] = self.env['ir.sequence'].next_by_code('anggaran.kas.%s' % vals['type'])
		return super(kas, self).create(vals)

	@api.multi
	def action_draft(self):
		#set to "draft" state
		return self.write({'state':KAS_STATES[0][0]})
	@api.multi
	def action_confirm(self):
		#set to "confirmed" state
		return self.write({'state':KAS_STATES[1][0]})
	@api.multi
	def action_done(self, context=None):
		#set to "done" state

		# bentuk kas masuk di unit tujuan
		# kas = self.browse(cr, uid, ids[0], context=context)
		# if kas.kepada_unit_id:
		for kas in self :
			if kas.kepada_unit_id:
				context.update({
					'tahun_id'          : kas.tahun_id.id, 
					'dasar_pembayaran'  : kas.dasar_pembayaran, 
					'jumlah'            : kas.jumlah, 
					'unit_id'           : kas.kepada_unit_id.id, 
					'contra_unit'       : kas.unit_id.id, 
					'kegiatan_id'       : kas.kegiatan_id.id,
					'jenis_item'        : kas.jenis_item,
					'sumber_uang'       : kas.sumber_uang,
					'spm_id'            : kas.spm_id.id,
				})
				kas_id = self.create_kas('in', context)
		return self.write({'state':KAS_STATES[3][0]})
	@api.multi
	def action_reject(self):
		#set to "reject" state
		return self.write({'state':KAS_STATES[2][0]})
	@api.multi
	def create_kas(self, type, context):

		#################################################################
		# cari journal kas keluar
		#################################################################
		journal_ids = False
		if type=='out':
			journal_ids = self.env["account.journal"].search([('code','=','BNK1')])
			if not journal_ids:
				raise UserError(_("Journal untuk transaksi Kas Keluar tidak ditemukan") ) 
		elif type=='in':
			journal_ids = self.env["account.journal"].search([('code','=','BNK1')])
			if not journal_ids:
				raise UserError(_("Journal untuk transaksi Kas Masuk tidak ditemukan") ) 

		data = {
			'name'              : '/',
			'tanggal'           : time.strftime("%Y-%m-%d") ,
			'tahun_id'          : context['tahun_id'],
			'unit_id'           : context['unit_id'],
			'type'              : type,
			'dasar_pembayaran'  : context['dasar_pembayaran'], 
			'kegiatan_id'       : context['kegiatan_id'], 
			'journal_id'        : journal_ids.id,
			'kepada_unit_id'    : context['contra_unit'] if type=='out' else False,
			'dari_unit_id'      : context['contra_unit'] if type=='in' else False,
			'jumlah'            : context['jumlah'],
			'jenis_item'        : context['jenis_item'],
			'sumber_uang'       : context['sumber_uang'],
			'spm_id'            : context['spm_id'],
			'cheque_nomor'      : '',
			'rek_nomor'         : '',
			'state'             : 'draft',
			'user_id'           : self.env.uid, 
		}
		kas_id = self.create(data)
		return kas_id 
	@api.multi
	def action_create_biaya(self):
		# kas = self.browse(cr, uid, ids[0], context=context)
		for kas in self:
			biaya = kas.env["anggaran.biaya"]
			data = {
				'name'              : '/',
				'tanggal'           : time.strftime("%Y-%m-%d") ,
				'biaya_line_ids'    : False,
				'tahun_id'          : kas.tahun_id.id,
				'unit_id'           : kas.kepada_unit_id.id,     
				'kepada_partner_id' : kas.kepada_partner_id.id,   
				'total'             : kas.jumlah,
				'kas_id'            : kas.id,
				'user_id'           : kas.env.uid, 
				'state'             : 'draft'
			}
			biaya_id = biaya.create(data)
		return biaya_id
