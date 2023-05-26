#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
import time

class spk_product_pengukuran(models.Model):

    _name = "vit.spk_product_pengukuran"
    _description = "vit.spk_product_pengukuran"
    
    name            = fields.Char( string="Code",  help="")
    variant_id      = fields.Many2one( "product.attribute",string="Variant")
    # size_id         = fields.Many2one( "product.attribute.value",string="Size", required=True)
    size_ids        = fields.Many2many( "product.attribute.value",string="Size(s)")
    
    product_id      = fields.Many2one( required=True, comodel_name="product.template",  string="Style",  help="")
    # template_id     = fields.Many2one( comodel_name="vit.template_pengukuran", required=False, string="Template Pengukuran",)
    spk_id          = fields.Many2one(comodel_name="vit.spk_pengukuran",  string="SPK Pengukuran",  help="")

    @api.onchange('variant_id')
    def onchange_sizes(self):
    	for pp in self:
    		if pp.variant_id:
    			pp.size_ids = pp.variant_id.value_ids