#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class kinerja_bidang_penelitian(models.Model):
	_name = "vit.kinerja_bidang_penelitian"
	_inherit = "vit.kinerja_bidang_penelitian"

	# kinerja_sks_persen = fields.Float( string="Kinerja sks persen", compute="compute_sks", store=True, help="")
	file_bukti_penugasan2 = fields.Binary( string="File bukti penugasan",  help="")
	file_bukti_dokumen2 = fields.Binary( string="File bukti dokumen",  help="")
	file_bukti_dokumen3 = fields.Binary( string="File bukti dokumen",  help="")

	# @api.depends("beban_sks","kinerja_sks")
	# def compute_sks(self):
	# 	for kinerja in self:
	# 		if kinerja.beban_sks != 0:
	# 			kinerja.kinerja_sks_persen = (kinerja.kinerja_sks / kinerja.beban_sks) * 100
