#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class riwayat_pelatihan(models.Model):
    _name = "vit.riwayat_pelatihan"
    _inherit = "vit.riwayat_pelatihan"

    jenis_pelatihan = fields.Many2one(comodel_name="vit.jenis_pelatihan",  string="Jenis Pelatihan",  help="")
