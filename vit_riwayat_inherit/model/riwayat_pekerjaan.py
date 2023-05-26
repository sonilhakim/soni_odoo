#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class riwayat_pekerjaan(models.Model):
    _name = "vit.riwayat_pekerjaan"
    _inherit = "vit.riwayat_pekerjaan"

    pekerjaan_id = fields.Many2one( "hr.job","Pekerjaan",  help="")
