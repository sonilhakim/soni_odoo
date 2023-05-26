#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
import time
from odoo.exceptions import UserError, ValidationError

class SummaryPolybagStore(models.Model):

    _name = "vit.summary_polybag_store"
    _description = "vit.summary_polybag_store"

    polybag_name   = fields.Char(string="Polybag Sumber")
    date           = fields.Datetime( string="Time Tracking")
    qty_polybag    = fields.Float('Qty Polybag')
    store_id       = fields.Many2one('vit.kasir_store', string='Kasir Store')
    