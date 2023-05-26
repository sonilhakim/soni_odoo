#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class ProductTemplateMR(models.Model):
    _inherit = "product.template"

    spec        = fields.Char( string="Spec",  help="")
    colour      = fields.Char( string="Colour",  help="" )
    sample 		= fields.Boolean( string="Sample")
    partner_id  = fields.Many2one( comodel_name="res.partner",  string="Customer", help="")
    inquery_id  = fields.Many2one( comodel_name="vit.marketing_inquery_garmen", string="No. Inquery")