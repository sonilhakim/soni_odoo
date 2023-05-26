#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class riwayat_kunjungan_ke_luar_negeri(models.Model):
    _name = "vit.riwayat_kunjungan_ke_luar_negeri"
    _inherit = "vit.riwayat_kunjungan_ke_luar_negeri"

    jenis_kunjungan_luar = fields.Many2one(comodel_name="vit.jenis_kunjungan_luar",  string="Jenis Kunjungan Luar",  help="")
