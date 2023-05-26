#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.addons import decimal_precision as dp
from io import StringIO
import base64
import time
from odoo.exceptions import UserError, ValidationError
STATES=[('draft', 'Draft'), ('open', 'Open'), ('created', 'Product Created'), ('mo', 'MO On Progress'), ('done_mo', 'MO Done'), ('approved', 'Approved')]

class sample_approval_line(models.Model):

    _name = "vit.sample_approval_line"
    _description = "vit.sample_approval_line"
    _order = 'id desc'
    _inherit = ['mail.thread']

    name            = fields.Char( required=True, string="Style",  help="")
    state           = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State", track_visibility='onchange', help="")
    qty             = fields.Float( string="Qty", digits=dp.get_precision('Product Unit of Measure'), default=1.0,  help="")
    kain            = fields.Char( string="Kain",  help="")
    uom             = fields.Many2one(comodel_name="uom.uom", string="Satuan")
    size            = fields.Many2one( "product.attribute.value",string="Size")
    desc            = fields.Char( string="Description",  help="")
    harga_cm        = fields.Float( string="Harga CM / PC",  help="")
    
    # xsample_id      = fields.Many2one( comodel_name="product.template",  string="XSample",  help="")
    product_sample_id = fields.Many2one( comodel_name="product.template", string="Product Sample", required=False,  help="")
    sample_approval_id = fields.Many2one(comodel_name="vit.sample_approval",  string="Sample Approval",  help="")
    material_ids    = fields.One2many(comodel_name="vit.approval_material_list",  inverse_name="approval_line_id",  string="Material List",  help="" )
    bom_id          = fields.Many2one(comodel_name="mrp.bom", string="Bill of Material")
    routing_id      = fields.Many2one(comodel_name="mrp.routing", string="Routing")
    mo_ids          = fields.One2many(comodel_name="mrp.production", inverse_name="approval_line_id", string="MO Sample")
    design_ids      = fields.One2many(comodel_name="vit.approval_desain",  inverse_name="approval_line_id",  string="Desain",  help="" )
    boq_jo_id       = fields.Many2one( comodel_name="vit.boq_po_garmen_line", string="BOQ", help="")
    
    @api.multi
    def create_product_sample(self):
        for sl in self:
            categ = self.env['product.category'].search([('name','=','Barang Sample')])
            if not categ:
                raise UserError(_('Kategori Product Barang Jadi belum ada!'))
            else:
                product_tmp = self.env['product.template']
                p_product_tmp = self.env['product.product']
                bom_tmp = self.env['mrp.bom']
                datas = {
                    'name'          : sl.name + '[Sample Approval]',
                    'type'          : 'product',
                    'categ_id'      : categ.id,
                    'uom_id'        : sl.uom.id,
                    'uom_po_id'     : sl.uom.id,
                    'sample'        : True,
                    'list_price'    : 0.0,
                    'standard_price': 0.0,
                    'taxes_id'          : False,
                    'supplier_taxes_id' : False,
                    'tracking'      : 'none',
                    'sale_ok'       : False,
                    'purchase_ok'   : False,
                    'company_id'    : sl.sample_approval_id.company_id.id,
                    'partner_id'    : sl.sample_approval_id.partner_id.id,
                    # 'image_medium'  : rd.gbr,
                }
                # import pdb;pdb.set_trace()
                # create product sample
                sample = product_tmp.create(datas)                
                sample_variant = p_product_tmp.search([('product_tmpl_id', '=', sample.id)], limit=1)
                # create BoM
                bom_line_ids = []
                for mt in sl.material_ids:
                    bom_line_ids.append((0,0,{
                            'product_id'    : mt.material.id,
                            'product_qty'   : mt.cons,
                            'product_uom_id': mt.uom.id,
                        }))
                bom_datas = {
                    'product_tmpl_id'           : sample.id,
                    'product_id'                : sample_variant.id,
                    'product_qty'               : sl.qty,
                    'product_uom_id'            : sample.uom_id.id,
                    'routing_id'                : sl.routing_id.id,
                    'bom_line_ids'              : bom_line_ids,
                }
                bom = bom_tmp.create(bom_datas)
            return sl.write({'state': 'created','product_sample_id': sample.id,'bom_id': bom.id})

    @api.multi 
    def action_approved(self):
        self.state = STATES[5][0]
            

class approval_material_list(models.Model):

    _name = "vit.approval_material_list"
    _description = "vit.approval_material_list"
    _rec_name = "material"

    name        = fields.Char( required=False, string="Material List",  help="")
    qty         = fields.Float( string="Qty", digits=dp.get_precision('Product Unit of Measure'), default=0.0,  help="")
    spec        = fields.Char( string="Spec", help="")
    colour      = fields.Char( string="Colour", help="" )
    uom         = fields.Many2one(comodel_name="uom.uom", string="Unit",)
    cons        = fields.Float( string="Cons", digits=dp.get_precision('Product Unit of Measure'), default=0.0,  help="")
    
    material    = fields.Many2one( comodel_name="product.product", string="Material",  help="")
    approval_line_id   = fields.Many2one( comodel_name="vit.sample_approval_line", string="Sample Approval Line",  help="")

    @api.onchange('material')
    def onchange_uom(self):
        for lis in self:
            if lis.material:
                lis.uom = lis.material.uom_id
    

class approval_desain(models.Model):

    _name = "vit.approval_desain"
    _description = "vit.approval_desain"
    
    name        = fields.Char( string="Description",  help="")
    date        = fields.Date( string="Date", default=lambda self: time.strftime("%Y-%m-%d"), help="")
    doc         = fields.Binary( string="Designn",  help="")
    doc_name    = fields.Char( string="Document Name",)

    approval_line_id   = fields.Many2one( comodel_name="vit.sample_approval_line", string="Sample Approval Line",  help="")
