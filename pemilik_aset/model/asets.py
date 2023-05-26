#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class account_asset(models.Model):

	_name = "account.asset.asset"
	_description = "account.asset.asset"

	_inherit = "account.asset.asset"

	pemilik_id = fields.Many2one(comodel_name="res.partner", string="Pemilik",)
	tgl_awal 	= fields.Date( string="Awal kepemilikan",  help="")
	tgl_akhir 	= fields.Date( string="Akhir kepemilikan",  help="")

	@api.model
	def create(self, values):
		res = super(account_asset, self).create(values)
		for ast in self:
			if ast.pemilik_id:
				ast.env.cr.execute("update res_partner set pemilik_asset=True where id = %s",( self.pemilik_id.id,  ))
				sql = """
						insert into vit_asets_pemilik (lokasi_aset, status_aset, partner_id, asset_id, tgl_awal, tgl_akhir)
						select loc.name, ast.state, part.id, ast.id, ast.tgl_awal, ast.tgl_akhir
						from account_asset_asset ast
						left join vit_location loc on ast.last_location_id = loc.id
						left join res_partner part on ast.pemilik_id = part.id
						where ast.id = %s
						"""
				ast.env.cr.execute(sql, (ast.id,))
		return res

	def write(self, values):
		for ast in self:
			if ast.pemilik_id:
				ast.env.cr.execute("update res_partner set pemilik_asset=True where id = %s",( ast.pemilik_id.id,  ))
				ap = ast.env['vit.asets_pemilik'].search([('partner_id','=',ast.pemilik_id.id),('asset_id','=',ast.id)])
				if ap.id == False:
					sql = """
						insert into vit_asets_pemilik (lokasi_aset, status_aset, partner_id, asset_id, tgl_awal, tgl_akhir)
						select loc.name, ast.state, part.id, ast.id, ast.tgl_awal, ast.tgl_akhir
						from account_asset_asset ast
						left join vit_location loc on ast.last_location_id = loc.id
						left join res_partner part on ast.pemilik_id = part.id
						where ast.id = %s
						"""
					ast.env.cr.execute(sql, (ast.id,))			

			else:
				# self.env.cr.execute("DELETE FROM vit_asets_pemilik WHERE asset_id = %s",( self.id, ))
					# import pdb; pdb.set_trace()
				for part in ast.env['res.partner'].search([('pemilik_asset','=',True),('asets_pemilik','=',False)]):
					ast.env.cr.execute("update res_partner set pemilik_asset=False where id = %s",( part.id, ))
			
		return super(account_asset, self).write(values)