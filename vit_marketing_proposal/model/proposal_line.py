#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.addons import decimal_precision as dp

class proposal_line(models.Model):

    _name = "vit.proposal_line"
    _description = "vit.proposal_line"
    
    name 		= fields.Char( required=True, string="Item",  help="")
    qty 		= fields.Float( string="Quantity", digits=dp.get_precision('Product Unit of Measure'), default=0.0,  help="")
    
    # product_id 	= fields.Many2one( comodel_name="product.product", string="Product", required=True,  help="")
    proposal_id = fields.Many2one(comodel_name="vit.marketing_proposal",  string="Proposal",  help="")
    uom 		= fields.Many2one(comodel_name="uom.uom", string="Unit of Measure")
