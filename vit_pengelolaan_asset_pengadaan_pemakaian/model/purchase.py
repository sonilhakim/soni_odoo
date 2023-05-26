from odoo import api, fields, models
from odoo.exceptions import UserError, AccessError


class PurchaseOrderAnggaran(models.Model):
	_name = "purchase.order"
	_inherit = "purchase.order"

	unit_id	= fields.Many2one(comodel_name='vit.unit_kerja', string='SUBSATKER')
	rka_id	= fields.Many2one(comodel_name='anggaran.rka', string='Dasar Anggaran')
	rka_kegiatan_id	= fields.Many2one(comodel_name='anggaran.rka_kegiatan', string='Kegiatan')
	mak_id 			= fields.Many2one(comodel_name='anggaran.rka_coa', string='MAK')
	sisa_anggaran	= fields.Float(string="Sisa Anggaran")

	@api.onchange('mak_id')
	def onchange_anggaran(self):
		for po in self:
			po.sisa_anggaran = po.mak_id.sisa

	@api.multi
	def button_confirm(self):
		res = super(PurchaseOrderAnggaran, self).button_confirm()
		for po in self:
			if po.amount_total >= po.sisa_anggaran + 0.01:
				raise UserError('Total Pengadaan tidak boleh lebih besar dari Sisa Anggaran')
			else :
				sql = "UPDATE anggaran_rka_coa SET realisasi = coalesce(realisasi,0) + '%s', sisa = coalesce(sisa,0) - '%s' WHERE id = '%s'" % (po.amount_total, po.amount_total, po.mak_id.id)
				self.env.cr.execute(sql)
				sql1 = "UPDATE anggaran_rka_kegiatan SET realisasi = coalesce(realisasi,0) + '%s', sisa = coalesce(sisa,0) - '%s' WHERE id = '%s'" % (po.amount_total, po.amount_total, po.rka_kegiatan_id.id)
				self.env.cr.execute(sql1)
				sql2 = "UPDATE anggaran_rka SET realisasi = coalesce(realisasi,0) + '%s', sisa = coalesce(sisa,0) - '%s' WHERE id = '%s'" % (po.amount_total, po.amount_total, po.rka_id.id)
				self.env.cr.execute(sql2)


# class PurchaseOrderLineAnggaran(models.Model):
# 	_name = 'purchase.order.line'
# 	_inherit = "purchase.order.line"

# 	rka_kegiatan_id	= fields.Many2one(comodel_name='anggaran.rka_kegiatan', string='Kegiatan')
# 	mak_id 			= fields.Many2one(comodel_name='anggaran.rka_coa', string='MAK')
# 	sisa_anggaran	= fields.Float(string="Sisa Anggaran")

# 	@api.onchange('mak_id')
# 	def onchange_anggaran(self):
# 		for po in self:
# 			po.sisa_anggaran = po.mak_id.sisa