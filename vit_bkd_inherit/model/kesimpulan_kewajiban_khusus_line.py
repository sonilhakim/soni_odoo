#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class kesimpulan_kewajiban_khusus_line(models.Model):

	_name = "vit.kesimpulan_kewajiban_khusus_line"
	_description = "vit.kesimpulan_kewajiban_khusus_line"

	@api.model
	def year_selection(self):
		year = 2000 # replace 2000 with your a start year
		year_list = []
		while year != 2100: # replace 2030 with your end year
			year_list.append((str(year), str(year)))
			year += 1
		return year_list

	# name = fields.Char( required=True, string="Judul Karya",  help="")
	kewajiban_khusus_id = fields.Many2one(comodel_name="vit.kinerja_kewajiban_khusus",  string="Judul Karya",  help="")
	tahun = fields.Selection( selection="year_selection", string="Tahun")
	ceklist_asesor = fields.Selection([('memenuhi','Memenuhi'),('tidak_memenuhi','Tidak Memenuhi')],'Ceklist Asesor')


	kesimpulan_id = fields.Many2one(comodel_name="vit.kesimpulan_kinerja_dosen",  string="Kesimpulan",  help="")
