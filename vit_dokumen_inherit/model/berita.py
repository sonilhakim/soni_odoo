#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class berita(models.Model):
    _name = "vit.berita"
    _inherit = ['vit.berita','mail.thread']
