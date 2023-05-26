# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
import datetime
import sys
import logging
_logger = logging.getLogger(__name__)

class AccountInvoiceLine(models.Model):
	_inherit = 'account.invoice.line'


	@api.onchange('product_id')
	def _onchange_analytic_tag(self):
		if not self.invoice_id:
			return

		for line in self:
			product = line.product_id
			if product.analytic_tag_id:
				line.analytic_tag_ids = [(6,0,[product.analytic_tag_id.id])]
