#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class asets(models.Model):

	_name = "vit.asets_pemilik"
	_description = "vit.asets_pemilik"
	_rec_name = "asset_id"

	lokasi_aset = fields.Char( string="Lokasi aset",  help="")
	status_aset = fields.Char( string="Status aset",  help="")
	tgl_awal 	= fields.Date( string="Awal kepemilikan",  help="")
	tgl_akhir 	= fields.Date( string="Akhir kepemilikan",  help="")
	asset_id 	= fields.Many2one(comodel_name="account.asset.asset",  string="Asset",  help="")
	partner_id 	= fields.Many2one(comodel_name="res.partner",  string="Partner",  help="")

	@api.onchange('asset_id')
	def onchange_data(self):
		if self.asset_id:
			self.lokasi_aset = self.asset_id.last_location_id.name
			self.status_aset = self.asset_id.state



class Partneraset(models.Model):

	_name = "res.partner"
	_description = "res.partner"

	_inherit = "res.partner"

	pemilik_asset = fields.Boolean( string="Pemilik Asset",  help="")
	asets_pemilik = fields.One2many(comodel_name="vit.asets_pemilik",  inverse_name="partner_id",  string="Asets", readonly=True, help="")

	# @api.model
	# def create(self, values):
	# 	res = super(Partneraset, self).create(values)
	# 	if self.asets_pemilik:
	# 		for ap in self.asets_pemilik:
	# 			self.env.cr.execute("update account_asset_asset set pemilik_id=%s where id = %s",( self.id, ap.asset_id.id ))
	# 	return res

	# def write(self, values):
	# 	res = super(Partneraset, self).write(values)
	# 	if self.asets_pemilik:
	# 		for ap in self.asets_pemilik:
	# 			self.env.cr.execute("update account_asset_asset set pemilik_id=%s where id = %s",( self.id, ap.asset_id.id ))
	# 			self.env.cr.execute("update account_asset_asset set pemilik_id = null where pemilik_id = %s and id <> %s",( self.id, self.asets_pemilik.asset_id.id ))
	# 	else:
	# 		self.env.cr.execute("update account_asset_asset set pemilik_id = null where pemilik_id = %s",( self.id, ))
	# 		self.pemilik_asset = False
	# 	return res