from odoo import fields, api, models

class AccountJournal(models.Model):
	_inherit = 'account.journal'

	is_wesel = fields.Boolean('Wesel')
	is_virtual_account = fields.Boolean('Virtual Account')
	is_transfer = fields.Boolean('Transfer Cash')

AccountJournal()