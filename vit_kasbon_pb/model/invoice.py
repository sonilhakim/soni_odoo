#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class invoice(models.Model):

    _name = "account.invoice"
    _description = "account.invoice"

    _inherit = "account.invoice"


    kasbon_id = fields.Many2one(comodel_name="vit.kasbon_pb",  string="Kasbon",  help="", )
