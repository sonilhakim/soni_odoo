#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class riwayat_kepakaran_dosen(models.Model):
    _name = "vit.riwayat_kepakaran_dosen"
    _inherit = "vit.riwayat_kepakaran_dosen"

    bidang_kepakaran = fields.Many2one(comodel_name="vit.bidang_kepakaran",  string="Bidang Kepakaran",  help="")

