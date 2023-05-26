#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class agenda(models.Model):
    _name = "vit.agenda"
    _inherit = ['vit.agenda','mail.thread']
