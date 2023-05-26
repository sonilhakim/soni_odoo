from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.osv import expression
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.float_utils import float_compare
from odoo.exceptions import UserError, AccessError
from odoo.tools.misc import formatLang
from odoo.addons import decimal_precision as dp

import logging
_logger = logging.getLogger(__name__)

class purchase_order(models.Model):
	_inherit 	= "purchase.order"

	@api.depends('order_line')
	def _compute_discount(self):
		sum_discount_total = 0.0

		for order in self:
			for line in order.order_line:
				sum_discount_total += line.harga_discount

			order.update({
				'discount_total': order.currency_id.round(sum_discount_total),
			})
			
	@api.depends('order_line')
	def _amount_all(self):
		for order in self:
			amount_untaxed = amount_tax = amount_subtotal = 0.0
			for line in order.order_line:
				amount_untaxed += line.price_subtotal
				amount_tax += line.price_tax
				amount_subtotal += (line.price_unit * line.product_qty)

			order.update({
				'amount_untaxed': order.currency_id.round(amount_untaxed),
				'amount_tax': order.currency_id.round(amount_tax),
				'amount_total': amount_untaxed + amount_tax,
				'amount_subtotal': amount_subtotal
			})

	discount_total = fields.Float(compute='_compute_discount', string='Discount Total', store=True, readonly=True)
	amount_subtotal = fields.Monetary(string='Subtotal', store=True, readonly=True, compute='_amount_all', track_visibility='always')

	# termin		= fields.Float('Termin', readonly=True, states={"draft" : [("readonly",False)]})
	cara_bayar 	= fields.Selection([('cash', 'Cash'), ('transfer', 'Transfer')], string='Cara Bayar', default='cash')
	up			= fields.Char('Up')
	expedisi	= fields.Char('Ekspedisi')

class purchase_order_line(models.Model):
	_inherit 	= "purchase.order.line"

	default_code 			= fields.Char('SKU', index=True)
	price_subtotal 			= fields.Monetary(compute='_compute_amount', string='Subtotal', store=True)
	satuan_product 			= fields.Many2one('uom.uom','Satuan', compute='_compute_satuan',store=True)
	# harga_satuan 			= fields.Float( 'Harga Satuan', digits=dp.get_precision('Product Price'))
	discount_bertingkat_id 	= fields.Many2one('purchase.discount.bertingkat', 'Discount Bertingkat')
	harga_discount 			= fields.Float( string='Discount')
	discount1				= fields.Float( compute='_compute_disc', string='Discount 1', store=True)
	discount2				= fields.Float( compute='_compute_disc', string='Discount 2', store=True)
	discount3				= fields.Float( compute='_compute_disc', string='Discount 3', store=True)

	pack_set1				= fields.Float( compute='_compute_pack', string='set1', store=True)
	pack_set2				= fields.Float( compute='_compute_pack', string='set2', store=True)
	pack_set3				= fields.Float( compute='_compute_pack', string='set3', store=True)
	satuan_set1 			= fields.Many2one('uom.uom','Satuan1', compute='_compute_pack', store=True)
	satuan_set2 			= fields.Many2one('uom.uom','Satuan2', compute='_compute_pack', store=True)
	satuan_set3 			= fields.Many2one('uom.uom','Satuan3', compute='_compute_pack', store=True)

	@api.depends('product_qty', 'price_unit', 'taxes_id', 'harga_discount')
	def _compute_amount(self):
		for line in self:
			vals = line._prepare_compute_all_values()

			taxes = line.taxes_id.compute_all(
				vals['price_unit'],
				vals['currency_id'],
				vals['product_qty'],
				vals['product'],
				vals['partner'])

			line.update({
				'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
				'price_total': taxes['total_included'],
				'price_subtotal': taxes['total_excluded'],
				'harga_discount': vals['discount_summary']
			})

	def _prepare_compute_all_values(self):
		self.ensure_one()

		discount_summary = 0.0
		discount_val = 0.0

		if self.product_qty < 1 or self.price_unit < 1:
			discount_per_product = 0.0
			price_after_discount = self.price_unit
		else:
			# hitung discount bertingkat disini
			base_price = self.price_unit * self.product_qty

			discount_model = self.env['purchase.discount.bertingkat'].search(
				[('id', '=', self.discount_bertingkat_id.id), ('valid_until', '>=', self.order_id.date_order.date()), ('valid_from', '<=', self.order_id.date_order.date())])

			if discount_model:
				for discount in discount_model:
					for discount_detail in discount.line_ids:
						if discount_detail.calculate == "upper":
							if discount_summary != 0.0:
								discount_summary += discount_val * discount_detail.discount / 100
								discount_val = base_price - discount_summary
						else:
							discount_summary += base_price * discount_detail.discount / 100
							discount_val = base_price - discount_summary

			discount_summary = self.order_id.currency_id.round(discount_summary) 
		

			discount_per_product = discount_summary / self.product_qty
			price_after_discount = self.price_unit - discount_per_product
			

		return {
			'price_unit': price_after_discount,
			'currency_id': self.order_id.currency_id,
			'product_qty': self.product_qty,
			'product': self.product_id,
			'partner': self.order_id.partner_id,
			'discount_summary': discount_summary
		}

	@api.onchange('product_id', 'product_qty', 'product_uom')
	def onchange_product_product_id(self):
		res = super(purchase_order_line, self)._onchange_quantity()
		for line in self:
			line.default_code = line.product_id.default_code
			line.discount_bertingkat_id = line.product_id.discount_bertingkat_id
			line.price_unit = line.product_id.standard_price

		return res

	@api.depends('product_id')
	def _compute_satuan(self):
		for line in self:
			line.satuan_product = line.product_id.satuan_product

	@api.depends('discount_bertingkat_id')
	def _compute_disc(self):
		for line in self:
			disc1 = line.env['purchase.discount.bertingkat.line'].search([('purchase_discount_bertingkat_id','=',line.discount_bertingkat_id.id),('sequence','=',1)])
			disc2 = line.env['purchase.discount.bertingkat.line'].search([('purchase_discount_bertingkat_id','=',line.discount_bertingkat_id.id),('sequence','=',2)])
			disc3 = line.env['purchase.discount.bertingkat.line'].search([('purchase_discount_bertingkat_id','=',line.discount_bertingkat_id.id),('sequence','=',3)])
			if disc1:
				line.discount1 = disc1.discount
			if disc2:
				line.discount2 = disc2.discount
			if disc3:
				line.discount3 = disc3.discount

	@api.depends('product_qty')
	def _compute_pack(self):
		
		for line in self:
			product = line.env['product.product'].search([('product_tmpl_id','=',line.product_id.product_tmpl_id.id)])
			# import pdb; pdb.set_trace()
			if line.product_id.sequence == 1:
				line.pack_set1 = line.product_qty
				line.satuan_set1 = line.satuan_product
				for prod in product:
					# p2 = prod.search([('sequence','=',2)])
					# p3 = prod.search([('sequence','=',3)])
					if prod.sequence == 2:
						line.pack_set2 = line.product_qty * prod.conv_value
						line.satuan_set2 = prod.satuan_product
					if prod.sequence == 3:
						line.pack_set3 = line.product_qty * prod.conv_value
						line.satuan_set3 = prod.satuan_product
			if line.product_id.sequence == 2:
				line.pack_set1 = 0.0
				line.satuan_set1 = False
				line.pack_set2 = line.product_qty
				line.satuan_set2 = line.satuan_product
				for prod in product:
					# p3 = prod.search([('sequence','=',3)])
					if prod.sequence == 3:
						line.pack_set3 = line.product_qty * prod.conv_value / prod.conv_value
						line.satuan_set3 = prod.satuan_product
			if line.product_id.sequence == 3:
				line.pack_set1 = 0.0
				line.satuan_set1 = False
				line.pack_set2 = 0.0
				line.satuan_set2 = False
				line.pack_set3 = line.product_qty
				line.satuan_set2 = line.satuan_product
