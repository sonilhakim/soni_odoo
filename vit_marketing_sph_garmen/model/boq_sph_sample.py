#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.addons import decimal_precision as dp
from io import StringIO
import base64
import time
from odoo.exceptions import UserError, ValidationError


class boq_sph_sample(models.Model):
    _name = "vit.boq_sph_sample"
    _description = "vit.boq_sph_sample"
    
    name            = fields.Char( required=False, string="Style",  help="")
    # qty             = fields.Float( string="Qty",  help="")
    # qty_or          = fields.Float( string="Qty OR",  help="")
    kain            = fields.Char( string="Kain",  help="")
    # design          = fields.Char( string="Desain",  help="")
    # gbr             = fields.Binary( string="Gbr",  help="")
    size            = fields.Many2one( "product.attribute.value",string="Size")
    product_name    = fields.Char( string="Product Description", help="")

    product_id      = fields.Many2one( required=True, comodel_name="product.template",  string="Sample",  help="")
    # uom_id          = fields.Many2one( comodel_name="uom.uom",  string="UOM",  help="")
    # sph_id          = fields.Many2one( comodel_name="vit.marketing_sph_garmen", string="SPH")
    boq_id          = fields.Many2one( comodel_name="vit.boq_sph_garmen_line", string="BOQ")
    doc_line_ids    = fields.One2many(comodel_name="vit.sample_line_doc",  inverse_name="sample_id",  string="Desain",  help="" )
    

class sample_line_doc(models.Model):

    _name = "vit.sample_line_doc"
    _description = "vit.sample_line_doc"
    
    name        = fields.Char( string="Description",  help="")
    date        = fields.Date( string="Date", default=lambda self: time.strftime("%Y-%m-%d"), help="")
    doc         = fields.Binary( string="Document Name",  help="")
    doc_name    = fields.Char( string="Document Name",)

    sample_id   = fields.Many2one(comodel_name="vit.boq_sph_sample",  string="Request Line",  help="")
    
    