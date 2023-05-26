#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class doc_history(models.Model):
    _name = "vit.doc_history"
    _inherit = "vit.doc_history"
