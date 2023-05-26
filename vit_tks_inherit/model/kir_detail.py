#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class kir_detail(models.Model):
	_name = "vit.kir_detail"
	_inherit = "vit.kir_detail"

	name = fields.Char( required=False, string="Name",  help="")

	@api.onchange('asset_id')
	def onchange_kir(self):
		for kir in self:
			if kir.asset_id:
				kir.merk_model = kir.asset_id.tipe_barang
				kir.thn_pembuatan = kir.asset_id.tahun_pembuatan
				kir.code = kir.asset_id.code
				kir.jumlah = kir.asset_id.qty
				kir.harga = kir.asset_id.value
				kir.kondisi = kir.asset_id.condition
				kir.name = kir.asset_id.name