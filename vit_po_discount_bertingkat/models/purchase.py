# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

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

class PurchaseOrder(models.Model):
	_inherit = "purchase.order"

	@api.depends('order_line.discount_amount')
	def _compute_discount(self):
		sum_discount_total = 0.0

		for order in self:
			for line in order.order_line:
				sum_discount_total += line.discount_amount

			order.update({
				'discount_total': order.currency_id.round(sum_discount_total),
			})
			
	@api.depends('order_line.price_total')
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


class PurchaseOrderLine(models.Model):
	_inherit = "purchase.order.line"

	price_subtotal = fields.Monetary(compute='_compute_amount', string='Subtotal', store=True)
	discount_amount = fields.Float(string="Discount Amount")

	@api.depends('product_qty', 'price_unit', 'taxes_id', 'discount_amount')
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
				'discount_amount': vals['discount_summary']
			})

	def _prepare_compute_all_values(self):
		# Hook method to returns the different argument values for the
		# compute_all method, due to the fact that discounts mechanism
		# is not implemented yet on the purchase orders.
		# This method should disappear as soon as this feature is
		# also introduced like in the sales module.
		self.ensure_one()

		discount_summary = 0.0

		if self.product_qty < 1 or self.price_unit < 1:
			discount_per_product = 0.0
			price_after_discount = self.price_unit
		else:
			# hitung discount bertingkat disini
			base_price = self.price_unit * self.product_qty

			discount_model = self.env['purchase.discount.bertingkat'].search(
				[('partner_id', '=', self.partner_id.id), ('valid_until', '>=', self.order_id.date_order.date()), ('valid_from', '<=', self.order_id.date_order.date())])

			if discount_model:
				for discount in discount_model:
					for discount_detail in discount.line_ids:
						if discount_detail.calculate == "upper":
							if discount_summary != 0.0:
								discount_summary += discount_summary * discount_detail.discount / 100
						else:
							discount_summary += base_price * discount_detail.discount / 100

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

	# @api.onchange('product_qty', 'product_uom')
	# def _onchange_quantity(self):
	# 	if not self.product_id:
	# 		return
	# 	params = {'order_id': self.order_id}
	# 	seller = self.product_id._select_seller(
	# 		partner_id=self.partner_id,
	# 		quantity=self.product_qty,
	# 		date=self.order_id.date_order and self.order_id.date_order.date(),
	# 		uom_id=self.product_uom,
	# 		params=params)

	# 	if seller or not self.date_planned:
	# 		self.date_planned = self._get_date_planned(seller).strftime(DEFAULT_SERVER_DATETIME_FORMAT)

	# 	if not seller:
	# 		if self.product_id.seller_ids.filtered(lambda s: s.name.id == self.partner_id.id):
	# 			self.price_unit = 0.0
	# 		return

	# 	price_unit = self.env['account.tax']._fix_tax_included_price_company(seller.price, self.product_id.supplier_taxes_id, self.taxes_id, self.company_id) if seller else 0.0
	# 	if price_unit and seller and self.order_id.currency_id and seller.currency_id != self.order_id.currency_id:
	# 		price_unit = seller.currency_id._convert(
	# 			price_unit, self.order_id.currency_id, self.order_id.company_id, self.date_order or fields.Date.today())

	# 	if seller and self.product_uom and seller.product_uom != self.product_uom:
	# 		price_unit = seller.product_uom._compute_price(price_unit, self.product_uom)

	# 	self.price_unit = price_unit

	# 	# check discount for selected vendor
	# 	if price_unit > 0:
	# 		base_price = price_unit * self.product_qty
	# 		discount_summary = 0.0

	# 		discount_model = self.env['purchase.discount.bertingkat'].search(
	# 			[('partner_id', '=', self.partner_id.id), ('valid_until', '>=', self.order_id.date_order.date()), ('valid_from', '<=', self.order_id.date_order.date())])

	# 		if discount_model:
	# 			for discount in discount_model:
	# 				for discount_detail in discount.line_ids:
	# 					if discount_detail.calculate == "upper":
	# 						if discount_summary != 0.0:
	# 							discount_summary += discount_summary * discount_detail.discount / 100
	# 					else:
	# 						discount_summary += base_price * discount_detail.discount / 100

	# 		self.discount_amount = self.order_id.currency_id.round(discount_summary) 
	# 	else:
	# 		self.discount_amount = 0.0