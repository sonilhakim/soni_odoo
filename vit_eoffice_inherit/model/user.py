#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class user(models.Model):
    _name = "res.users"
    _inherit = "res.users"