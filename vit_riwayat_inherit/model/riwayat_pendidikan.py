#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class riwayat_pendidikan(models.Model):
    _name = "vit.riwayat_pendidikan"
    _inherit = "vit.riwayat_pendidikan"

    ref_pendidikan = fields.Many2one(comodel_name="vit.ref_pendidikan",  string="Pendidikan",  help="")

