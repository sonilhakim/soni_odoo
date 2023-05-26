#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class riwayat_penghargaan(models.Model):
    _name = "vit.riwayat_penghargaan"
    _inherit = "vit.riwayat_penghargaan"

    jenis_penghargaan = fields.Many2one(comodel_name="vit.jenis_penghargaan",  string="Jenis Penghargaan",  help="")
