# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MrpWorkorder(models.Model):
	_inherit = 'mrp.workorder'

	spec_type = fields.Selection([('Normal','Normal'), ('SP','SP')], string="Spec Type", default='Normal')
