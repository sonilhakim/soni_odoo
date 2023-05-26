from odoo import api, fields, models, _
import time
import datetime
from odoo.tools.safe_eval import safe_eval
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)


class invoice(models.Model):
	_name = 'account.invoice'
	_inherit = 'account.invoice'

	order = fields.Many2one("sale.order", string="Order")
	truck_run = fields.Char(string="Run")

	# def get_order(self):
	# 	for inv in self:
	# 		if inv.origin:
	# 			sale_order = inv.env['sale.order'].search([('name','=',inv.origin)])
	# 			for so in sale_order:
	# 				r = so.truck_run_ids
	# 				inv.order = so.id
	# 				inv.truck_run = ",".join( [ x.name for x in r ] )

	@api.multi
	def generate_printer_data(self):
		tpl = self.env['mail.template'].search([('name', '=', 'Dot Matrix Customer Invoice')])
		data = tpl._render_template(tpl.body_html, 'account.invoice', self.id, post_process=False)
		self.printer_data = data

invoice()


class sales(models.Model):
	_name = 'sale.order'
	_inherit = 'sale.order'

	@api.multi
	def action_invoice_create(self, grouped=False, final=False):
		res = super(sales, self).action_invoice_create(grouped=False, final=False)        
		for so in self:
			for inv in so.env['account.invoice'].search([('origin', '=', so.name)]):
				r = so.truck_run_ids
				inv.order = so.id
				inv.truck_run = ",".join( [ x.name for x in r ] )

		return res

sales()