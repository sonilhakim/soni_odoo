#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class skp_perkuliahan(models.Model):
	_name = "vit.skp_perkuliahan"
	_inherit = "vit.skp_perkuliahan"

	# totak_sks_per_smt = fields.Float( string="Total sks per smt", compute="compute_perkuliahan", help="")

	# @api.multi
 #    def compute_perkuliahan(self):
 #        for kul in self:
 #            kul.totak_sks_per_smt = (kul.sks * kul.jumlah_kelas)/kul.jumlah_dosen_pengampu
