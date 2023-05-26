#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class account_period(models.Model):

    _name = "account.period"
    _description = "account.period"

    _inherit = "account.period"


