#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.addons import decimal_precision as dp
import time
from odoo.exceptions import UserError, ValidationError

class boq_po_garmen_line(models.Model):
    _name = "vit.boq_po_garmen_line"
    _description = "vit.boq_po_garmen_line"

    name            = fields.Char( string="Style",  help="")
    qty             = fields.Float( string="Quantity", digits=dp.get_precision('Product Unit of Measure'),  help="")
    tax_id          = fields.Many2one('account.tax', string='PPN', domain=[('type_tax_use','!=','none'), '|', ('active', '=', False), ('active', '=', True)])
    price           = fields.Monetary( string="Unit Price",  help="")
    tax_val         = fields.Monetary( string="Nilai Pajak", help="")
    total_price     = fields.Monetary( string="Sub Total Price", help="")
    currency_id     = fields.Many2one('res.currency', related='po_id.company_id.currency_id', string="Currency", readonly=True)
    kain            = fields.Char( string="Kain",  help="")
    colour          = fields.Char( string="Colour",  help="")

    product_id      = fields.Many2one( required=False, comodel_name="product.template",  string="Product Style",  help="")
    sample_id       = fields.Many2one( required=True, comodel_name="product.template",  string="Sample",  help="")
    product_name    = fields.Char( string="Product Description", help="")
    uom_id          = fields.Many2one(comodel_name="uom.uom",  string="Uom", help="")
    po_id           = fields.Many2one(comodel_name="vit.purchase_order_garmen",  string="Po",  help="")
    material_ids    = fields.One2many(comodel_name="vit.or_material_list",  inverse_name="boq_id",  string="Material List", help="")
    design_ids      = fields.One2many(comodel_name="vit.or_line_doc",  inverse_name="boq_id",  string="Design", help="")
    is_po_payung    = fields.Boolean('Po Payung')
    doc_count       = fields.Integer(string='Hitung Doc', compute='_get_doc')
    
    
    @api.onchange('qty','price','tax_id')
    def onchange_total_price(self):
        for boq in self:
            if boq.tax_id:
                boq.tax_val = boq.price * (boq.tax_id.amount / 100.0)
                boq.total_price = boq.qty * (boq.price + boq.tax_val)
            else:
                boq.total_price = boq.qty * boq.price

    def _get_doc(self):
        for boq in self:
            doc_ids = self.env["vit.or_line_doc"].search([('boq_id','=',boq.id)])
            if doc_ids:
                boq.doc_count = len(set(doc_ids.ids))

    @api.multi
    def action_view_doc(self):
        for boq in self:
            doc_ids = self.env["vit.or_line_doc"].search([('boq_id','=',boq.id)])
            action = self.env.ref('vit_marketing_po_garmen.action_vit_or_line_doc').read()[0]
            action['domain'] = [('id', 'in', doc_ids.ids)]
            return action

    

class or_material_list(models.Model):

    _name = "vit.or_material_list"
    _description = "vit.or_material_list"
    _rec_name = "material"

    name        = fields.Char( string="Material List", default="Material List", store=True, help="")
    acc_no      = fields.Char( string="ACC NO",  help="")
    qty         = fields.Float( string="Qty", digits=dp.get_precision('Product Unit of Measure'), default=0.0,  help="")
    spec        = fields.Char( string="Spec", help="")
    colour      = fields.Char( string="Colour", help="" )
    uom         = fields.Many2one(comodel_name="uom.uom", string="Unit",)
    cons        = fields.Float( string="Cons", digits=dp.get_precision('Product Unit of Measure'), default=0.0,  help="")
    
    material    = fields.Many2one( comodel_name="product.product", string="Item", required=True,  help="")
    boq_id      = fields.Many2one( comodel_name="vit.boq_po_garmen_line", string="Nama Style", help="")


class or_line_doc(models.Model):

    _name = "vit.or_line_doc"
    _description = "vit.or_line_doc"

    @api.model
    def _get_default_boq_id(self):
        if self._context.get('active_id'):
            boq_id_obj = self.env['vit.purchase_order_garmen']
            boq_id = boq_id_obj.browse(self._context.get('active_id'))
            return boq_id
    
    name        = fields.Char( string="Description",  help="")
    date        = fields.Date( string="Date", default=lambda self: time.strftime("%Y-%m-%d"), help="")
    doc         = fields.Binary( string="Document Name",  help="")
    doc_name    = fields.Char( string="Document Name",)

    boq_id      = fields.Many2one( comodel_name="vit.boq_po_garmen_line", string="BOQ", default=_get_default_boq_id, help="")
