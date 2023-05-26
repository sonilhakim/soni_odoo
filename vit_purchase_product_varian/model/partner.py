#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class Partners(models.Model):
	_inherit = "res.partner"

	fax = fields.Char()