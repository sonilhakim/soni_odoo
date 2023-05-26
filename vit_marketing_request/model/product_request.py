#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class VitProductRequest(models.Model):
    _inherit = "vit.product.request"

    partner_id          = fields.Many2one(comodel_name="res.partner",  string="Buyer", readonly=True, states={'draft': [('readonly', False)]}, help="")
    project_description = fields.Text(string="Project Description", readonly=True, states={'draft': [('readonly', False)]}, help="")
