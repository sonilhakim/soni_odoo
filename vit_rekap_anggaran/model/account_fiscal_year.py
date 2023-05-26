#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class account_fiscal_year(models.Model):

    _name = "account.fiscal.year"
    _description = "account.fiscal.year"

    _inherit = "account.fiscal.year"


