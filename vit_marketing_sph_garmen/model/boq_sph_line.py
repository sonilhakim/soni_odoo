#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class boq_sph_garmen_line(models.Model):
    _name = "vit.boq_sph_garmen_line"
    _description = "vit.boq_sph_garmen_line"
    
    name            = fields.Char( required=True, string="Item",  help="")
    qty             = fields.Float( string="Qty",  help="")
    # qty_or          = fields.Float( string="Qty OR",  help="")
    tax_id          = fields.Many2one('account.tax', string='Pajak', domain=[('type_tax_use','!=','none'), '|', ('active', '=', False), ('active', '=', True)])
    price           = fields.Monetary( string="Unit Price",  help="")
    tax_val         = fields.Monetary( string="Nilai Pajak", compute="_calc_total_price", store=True, help="")
    total_price     = fields.Monetary( string="Total Price", compute="_calc_total_price", store=True, help="")
    currency_id     = fields.Many2one('res.currency', related='sph_id.company_id.currency_id', string="Currency", readonly=True)
    bahan           = fields.Char( string="Bahan",  help="")
    
    # product_id      = fields.Many2one( required=False, comodel_name="product.template",  string="Product",  help="")
    uom_id          = fields.Many2one( comodel_name="uom.uom",  string="UOM",  help="")
    sph_id          = fields.Many2one(comodel_name="vit.marketing_sph_garmen",  string="Sph",  help="")
    sample_ids      = fields.One2many(comodel_name="vit.boq_sph_sample",  inverse_name="boq_id",  string="Sample",  help="")
    

    @api.depends('qty','price','tax_id')
    def _calc_total_price(self):
        for boq in self:
            if boq.tax_id:
                boq.tax_val = boq.price * (boq.tax_id.amount / 100.0)
                boq.total_price = boq.qty * (boq.price + boq.tax_val)
            else:
                boq.total_price = boq.qty * boq.price