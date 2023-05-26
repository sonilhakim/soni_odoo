#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class account_asset(models.Model):

    _name = "account.asset.asset"
    _description = "account.asset.asset"

    _inherit = "account.asset.asset"

    kelompok_asset_id = fields.Many2one(comodel_name="vit.kelompok_aset",  string="Kelompok Asset",  help="")

    parent_kategori = fields.Char(string='Parent Category', related="category_id.parent_id.parent_id.parent_id.name", store=True)
    # parent_kategori = fields.Char(string='Parent Category')

    # @api.onchange('category_id')
    # def onchange_parent_kategori(self):
    # 	for rec in self:
    # 		rec.parent_kategori = rec.category_id.parent_id.parent_id.parent_id.name