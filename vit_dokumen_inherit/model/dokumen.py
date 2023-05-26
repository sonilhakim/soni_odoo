#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class dokumen(models.Model):
    _name = "vit.dokumen"
    _inherit = ['vit.dokumen','mail.thread']
