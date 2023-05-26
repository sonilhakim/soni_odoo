#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class riwayat_seminar(models.Model):
    _name = "vit.riwayat_seminar"
    _inherit = "vit.riwayat_seminar"

    tingkat_seminar = fields.Many2one(comodel_name="vit.tingkat_seminar",  string="Tingkat Seminar",  help="")
