# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResPartner(models.Model):
	_inherit = "res.partner"

	@api.multi
	@api.depends('name', 'street')
	def name_get(self):
		res = []
		for rec in self:
			name = '['+ (rec.name or '') + '] ' + (rec.street2 or '')
			res.append((rec.id, street2))
		return res

	@api.model
	def name_search(self, name, args=None, operator='ilike', limit=100):
		args = args or []
		recs = self.browse()
		if not recs:
			recs = self.search([
				'|','|',
				('name', operator, name),
				('street2', operator, name)
			] + args, limit=limit)
		return recs.name_get()