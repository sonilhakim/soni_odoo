from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.addons import decimal_precision as dp
from odoo import api, fields, models, _

class product_product(models.Model):
	_inherit = 'product.product'

	sequence 				= fields.Integer(string="Seq", required=True)
	discount_bertingkat_id 	= fields.Many2one('purchase.discount.bertingkat', 'Discount Bertingkat', ondelete="cascade")
	satuan_product 			= fields.Many2one('uom.uom','Satuans')
	min_stock 				= fields.Float('Stock Minimal')
	# harga_satuan 			= fields.Float( 'Harga Satuan', digits=dp.get_precision('Product Price'))
	harga_discount 			= fields.Float(compute='_compute_discount', string='Harga Discount', store=True)
	harga_beli 				= fields.Float( string='Harga Beli', digits=dp.get_precision('Product Price'))
	profit 					= fields.Float( string='Profit (%)', store=True)
	nilai_profit			= fields.Float( compute='_compute_profit', string='Nilai Profit', digits=dp.get_precision('Product Price'))
	# harga_jual 				= fields.Float( string='Harga Jual 1', digits=dp.get_precision('Product Price'))
	# harga_jual2				= fields.Float( string='Harga Jual 2', digits=dp.get_precision('Product Price'))
	# harga_jual3				= fields.Float( string='Harga Jual 3', digits=dp.get_precision('Product Price'))

	@api.depends('discount_bertingkat_id', 'standard_price')
	def _compute_discount(self):
		discount_summary = 0.0
		for pp in self:
			if pp.discount_bertingkat_id:
				discount_model = pp.env['purchase.discount.bertingkat'].search(
					[('id', '=', pp.discount_bertingkat_id.id), ('valid_until', '>=', fields.Datetime.now()), ('valid_from', '<=', fields.Datetime.now())])
				
				if discount_model:
					for discount in discount_model:
						for discount_detail in discount.line_ids:
							if discount_detail.calculate == "upper":
								if discount_summary != 0.0:
									discount_summary += discount_summary * discount_detail.discount / 100
							else:
								discount_summary += pp.standard_price * discount_detail.discount / 100

				discount_summary = pp.currency_id.round(discount_summary)
				pp.harga_discount = discount_summary
			else:
				pp.harga_discount = 0.0

	@api.onchange('standard_price', 'harga_discount')
	def _compute_harga_beli(self):
		for pp in self:
			pp.harga_beli = pp.standard_price - pp.harga_discount


	@api.depends('profit', 'harga_beli')
	def _compute_profit(self):
		for pp in self:
			# selisih = pp.harga_jual - pp.standard_price
			# if pp.standard_price:
			# 	pp.profit = (selisih / pp.standard_price) * 100
			if pp.profit:
				pp.nilai_profit = pp.harga_beli * (pp.profit / 100)
			else:
				pp.nilai_profit = 0.0

	# @api.onchange('standard_price','profit','nilai_profit')
	# def _onchange_harga_jual(self):
	# 	for pp in self:
	# 		pp.harga_jual = pp.standard_price + pp.nilai_profit

	@api.onchange('sequence')
	def _onchange_conv(self):
		for pp in self:
			if pp.sequence == 1:
				pp.conv_value = 1.0