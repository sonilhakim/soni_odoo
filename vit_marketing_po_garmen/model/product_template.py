#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class ProductTemplatePO(models.Model):
    _inherit = "product.template"

    default_code_c = fields.Char('Product Code', store=True)