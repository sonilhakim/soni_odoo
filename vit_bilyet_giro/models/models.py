from odoo import models, fields, api, _
import time
import logging
import odoo.addons.decimal_precision as dp
from datetime import datetime, timedelta
from odoo.exceptions import UserError
# from datetime import datetime, timedelta, date, time

STATES = [('draft', 'Draft'), ('open', 'Open'),
		  ('close', 'Close'), ('reject', 'Reject')]


class vit_bilyet_giro(models.Model):
	_name = "vit.vit_bilyet_giro"
	_inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']


	def post_mesages_giro(self):
		# import pdb;pdb.set_trace();
		ir_model_data_sudo = self.env['ir.model.data'].sudo()

		user    = ir_model_data_sudo.get_object('vit_bilyet_giro', 'group_user')
		manager = ir_model_data_sudo.get_object('vit_bilyet_giro', 'group_manager')
		billing = ir_model_data_sudo.get_object('account', 'group_account_invoice')

		user_partner_ids     = user.users.mapped('partner_id')
		manager_partner_ids  = manager.users.mapped('partner_id')
		bill_partner_ids = billing.users.mapped('partner_id.id')

		user_partners    =  user_partner_ids.ids
		manager_partners =  manager_partner_ids.ids
		bill_partners    =  bill_partner_ids

		receivers = user_partners + manager_partners + bill_partners

		subject = _("Bilyet Giro")
		body = _('Giro %s Closed, journal payment %s were created.') % (self.name, self.payment_id.name,)
		messages = self.message_post(body=body, subject=subject)
		messages.update({'needaction_partner_ids' : [(6, 0, list(set(receivers)))]})

		
		return True

	def _invoice_names(self):
		# results = {}
		for giro in self:
			invoice_names = []
			for gi in giro.giro_invoice_ids:
				invoice_names.append( "%s " % (gi.invoice_id.number or "") )
				results = ", ".join(invoice_names)
		# import pdb; pdb.set_trace()
				giro.invoice_names = results

	name = fields.Char(string="Number", help="Nomor Giro",
					   required=True, states={'draft': [('readonly', False)]})
	due_date = fields.Date(string="Due Date", required=True, readonly=True, states={
							   'draft': [('readonly', False)]})
	receive_date = fields.Date(string="Receive Date", readonly=True, states={
								   'draft': [('readonly', False)]})
	submit_date = fields.Date(string="Submit Date", readonly=True, states={
								   'draft': [('readonly', False)]})
	clearing_date = fields.Datetime(string="Clearing Date", readonly=True,)
	amount = fields.Float(string="Amount", readonly=True, states={
						  'draft': [('readonly', False)]})
	amount_difference = fields.Float(string="Amount Difference", compute="_cek_total",)
	partner_id = fields.Many2one(comodel_name="res.partner", string="Partner", readonly=True, states={
								 'draft': [('readonly', False)]})
	journal_id = fields.Many2one(comodel_name="account.journal", string="Bank Journal", domain=[
								 ('type', '=', 'bank')], readonly=True, states={'draft': [('readonly', False)]})
	payment_id = fields.Many2one(comodel_name="account.payment", string="Payment", readonly=True)
	giro_invoice_ids = fields.One2many(comodel_name="vit.giro_invoice", inverse_name="giro_id", required=True, readonly=True, states={
									   'draft': [('readonly', False)]})
	invoice_names = fields.Char(compute="_invoice_names", string="Allocated Invoices")
	type = fields.Selection([('payment', 'Payment'), ('receipt', 'Receipt')], default='payment',
							string="Type", readonly=True, required=True, states={'draft': [('readonly', False)]})
	invoice_type = fields.Char(string="Invoice Type", default='in_invoice', readonly=True, states={
							   'draft': [('readonly', False)]})
	state = fields.Selection(string="State", selection=STATES,
							 required=True, readonly=True, default=STATES[0][0])
	user_id = fields.Many2one("res.users", string="User", default=lambda self: self.env.user)
	param_id = fields.Many2one(comodel_name="vit.vit_config_giro", string="Submit Term")
	_sql_constraints = [('name_uniq', 'unique(name)',
						 _('Nomor Giro tidak boleh sama!'))]
						 
	# @api.multi
	# def _cek_total(self):
	# 	inv_total = 0.0
	# 	for giro in self:
	# 		for gi in giro.giro_invoice_ids:
	# 			inv_total += gi.amount
	# 		# import pdb; pdb.set_trace()
	# 		if giro.amount == inv_total:
	# 			return True
	# 	return False
	
	# _constraints = [(_cek_total, _(
	# 	'Total amount allocated untuk invoices harus sama dengan total Giro amount'), ['amount'])]
	def _cek_total(self):
		inv_total = 0.0
		for giro in self:
			for gi in giro.giro_invoice_ids:
				inv_total += gi.amount_invoice
				giro.amount_difference = giro.amount - inv_total

	@api.multi
	def action_cancel(self):
		self.write({'state': STATES[0][0]})

	@api.model
	def create(self, values):        
		res = super(vit_bilyet_giro, self).create(values)
		start = res.due_date + timedelta(days=1)
		receive_date = str(res.receive_date)
		submit_date = str(res.submit_date)
		due_date = str(start)
		param = res.param_id
		store = start - timedelta(days=(param.term)+2)
		if res.giro_invoice_ids.ids == []:
			raise UserError(_('Invoice harus terisi!'))
		if res.amount == 0.0:
			raise UserError(_('Amount harus terisi!'))
		if receive_date >= due_date:
			raise UserError(_('Receive Date tidak boleh lebih dari Due Date!'))
		if submit_date <= str(store):
			raise UserError(_('Submit Date tidak boleh lebih dari %s hari sebelum Due Date!')  % (param.term))
		if submit_date >= due_date:
			raise UserError(_('Submit Date tidak boleh lebih dari Due Date!'))
		return res

	def write(self, values):        
		result = super(vit_bilyet_giro, self).write(values)
		start = self.due_date + timedelta(days=1)
		due_date = str(start)
		receive_date = str(self.receive_date)
		submit_date = str(self.submit_date)
		# start = datetime.strptime(due_date, '%Y-%m-%d').date()
		store = start - timedelta(days=(self.param_id.term)+2)
		if self.giro_invoice_ids.ids == []:
			raise UserError(_('Invoice harus terisi!'))
		if self.amount == 0.0:
			raise UserError(_('Amount harus terisi!'))
		if receive_date >= due_date:
			raise UserError(_('Receive Date tidak boleh lebih dari Due Date!'))
		if submit_date <= str(store):
			raise UserError(_('Submit Date tidak boleh lebih dari %s hari sebelum Due Date!')  % (self.param_id.term))
		if submit_date >= due_date:
			raise UserError(_('Submit Date tidak boleh lebih dari Due Date!'))
		return result

	@api.multi
	def action_confirm(self):
		# import pdb; pdb.set_trace()	
		# due_date = str(self.due_date)
		# receive_date = str(self.receive_date)
		# start = datetime.strptime(due_date, '%Y-%m-%d %H:%M:%S')
		# sub = datetime.strptime(receive_date, '%Y-%m-%d %H:%M:%S')
		# end = self.param_id.search([('id','=', 1)])
		# par = start-sub
		# print(int(end.name_parameter))
		# print('=========================')
		# if (str(par)[0:3]) <= (str(end.name_parameter)) :
		# if due_date <= receive_date :
		#     raise UserError(_('Tanggal Due Date harus lebih besar dari tanggal Receive Date'))

		# self.write({'state': STATES[1][0], 'submit_date': (start - timedelta(days=end.name_parameter))})
		self.write({'state': STATES[1][0]})
		

	@api.multi
	def action_clearing(self):
		for giro in self:
			payment = giro.env['account.payment']
			company_id = giro._context.get(
				'company_id', giro.env.user.company_id.id)
			#payment supplier
			if giro.type == 'payment':
				pay_type = 'outbound'
				partner_type = 'supplier'
				# payment_method = giro.journal_id.outbound_payment_method_ids.id
			#receive customer
			else:
				pay_type = 'inbound'
				partner_type = 'customer'
				# payment_method = giro.journal_id.inbound_payment_method_ids.id

			payment_id = payment.create({
				'payment_type': pay_type,
				'partner_id': giro.partner_id.id,
				'partner_type': partner_type,
				'journal_id': giro.journal_id.id,
				'amount': giro.amount,
				'communication': 'Payment giro ' + giro.name,
				'company_id': company_id,
				'payment_method_id': 1,

			})
			# import pdb; pdb.set_trace()
			payment.browse(payment_id.id).post()
			giro.write({'state': STATES[2][0], 'clearing_date': time.strftime("%Y-%m-%d %H:%M:%S"), 'payment_id': payment_id.id})
			giro.post_mesages_giro()
			# messages = giro.message_post(body=_('Giro %s Closed, journal payment %s were created.') % (self.name, self.payment_id.name,))
			# messages.update({'needaction_partner_ids' : [(6, 0, [self.user_id.partner_id.id])]})

	@api.multi
	def action_reject(self):
		self.write({'state': STATES[3][0]})

	@api.onchange('type')
	def on_change_type(self):
		inv_type = 'in_invoice'
		if self.type == 'payment':
			inv_type = 'in_invoice'
		elif self.type == 'receipt':
			inv_type = 'out_invoice'
		self.invoice_type = inv_type

	@api.onchange('param_id')
	def on_change_submit_date(self):
		if self.due_date != False:
			# due_date = str(self.due_date)
			# start = datetime.strptime(due_date, '%Y-%m-%d %H:%M:%S')
			# start = datetime.strptime(due_date, '%Y-%m-%d').date()
			end = self.param_id
			self.submit_date = (self.due_date - timedelta(days=end.term))

class vit_config_giro(models.Model):
	_name = "vit.vit_config_giro"

	name = fields.Char(string="Name", help="Nama Submit term",
					   required=True)
	# date = fields.Date(string="Term Date")
	term = fields.Integer(string="Term", help="parameter", required=True)
	category = fields.Char(string="Type", readonly=True, default='Days')

class vit_giro_invoice(models.Model):
	_name = "vit.giro_invoice"

	giro_id = fields.Many2one(
		comodel_name="vit.vit_bilyet_giro", string="Giro")
	invoice_id = fields.Many2one(comodel_name="account.invoice", string="Invoice",
								 help="Invoice to be paid", domain=[('state', '=', 'open')])
	amount_invoice = fields.Float(string="Invoice Amount")
	amount = fields.Float(string="Giro Amount", related="giro_id.amount")

	@api.onchange('invoice_id')
	def on_change_invoice_id(self):
		self.amount_invoice = self.invoice_id.residual

	# @api.multi
	# def _cek_total(self):
	# 	inv_total = 0.0
	# 	for gi in self:
	# 		giro = gi.giro_id			
	# 		inv_total += gi.amount
	# 		total = inv_total
	# 		# import pdb; pdb.set_trace()
	# 		if total == giro.amount:
	# 			return True
	# 	return False
	
	# _constraints = [(_cek_total, _(
	# 	'Total amount allocated untuk invoice harus sama dengan total Giro amount'), ['amount'])]


class account_invoice(models.Model):
	_name = "account.invoice"
	_inherit = 'account.invoice'

	giro_invoice_ids = fields.One2many(
		comodel_name="vit.giro_invoice", inverse_name="invoice_id", string="Giro")
