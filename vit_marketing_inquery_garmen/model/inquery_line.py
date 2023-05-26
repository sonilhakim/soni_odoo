#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.addons import decimal_precision as dp

class inquery_garmen_line(models.Model):

    _name = "vit.inquery_garmen_line"
    _description = "vit.inquery_garmen_line"

    name = fields.Char( required=True, string="Item",  help="")
    qty = fields.Float( string="Quantity", digits=dp.get_precision('Product Unit of Measure'), default=0.0,  help="")
    uom = fields.Many2one(comodel_name="uom.uom", string="Unit of Measure")

    # product_id = fields.Many2one( comodel_name="product.product", string="Product", required=True,  help="")
    inquery_id = fields.Many2one(comodel_name="vit.marketing_inquery_garmen",  string="Inquery",  help="")

    # @api.onchange('product_id')
    # def onchange_product(self):
    # 	for iq in self:
    # 		iq.uom = iq.product_id.uom_id.id