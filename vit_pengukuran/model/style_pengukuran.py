#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class style_pengukuran(models.Model):
    _name = "vit.style_pengukuran"
    _description = "Style Pengukuran"
    
    name        = fields.Many2one( comodel_name="product.template", required=True, string="Style Name",domain=[('sale_ok','=',True)])
    user_id      = fields.Many2one("res.users", "User", default=lambda self: self.env.uid, track_visibility='onchange')
    size_ids     = fields.One2many(comodel_name="vit.style_pengukuran_size",  inverse_name="style_id",  string="Size Pengukuran",  copy=True )
    pengukuran_id   = fields.Many2one( comodel_name="vit.pengukuran",  string="Pengukuran")
    pengukuran_header_id   = fields.Many2one( comodel_name="vit.pengukuran.header",  string="SPK Pengukuran")
    karyawan_id     = fields.Many2one( comodel_name="vit.pengukuran_karyawan", required=True, string="Karyawan",)

class style_pengukuran_size(models.Model):
    _name = "vit.style_pengukuran_size"
    _description = "Style Pengukuran Size"

    name        = fields.Char( required=True, string="Size",  help="")
    style_id    = fields.Many2one("vit.style_pengukuran", "Style", required=True)
    item_ids    = fields.One2many(comodel_name="vit.style_pengukuran_item",  inverse_name="size_id",  string="Item Pengukuran",  copy=True )

class style_pengukuran_item(models.Model):
    _name = "vit.style_pengukuran_item"
    _description = "Style Peengukuran Item"

    name    = fields.Char( required=True, string="Item Pengukuran",  help="")
    size    = fields.Float( string="Size", required=True, help="")
    size_id = fields.Many2one("vit.style_pengukuran_size", "Size Style")