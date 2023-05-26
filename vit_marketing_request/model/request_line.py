#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.addons import decimal_precision as dp
from io import StringIO
import base64
import time
from odoo.exceptions import UserError, ValidationError
STATES=[('draft', 'Draft'), ('open', 'Open'), ('created', 'Product Created'), ('mo', 'MO On Progress'), ('done_mo', 'MO Done'), ('approved', 'Approved')]

class request_line(models.Model):

    _name = "vit.request_line"
    _description = "vit.request_line"
    _order = 'id desc'

    name            = fields.Char( required=True, string="Item",  help="")
    # state           = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",  help="")
    qty             = fields.Float( string="Qty", digits=dp.get_precision('Product Unit of Measure'), default=1.0,  help="")
    uom             = fields.Many2one(comodel_name="uom.uom", string="Satuan")
    
    request_id      = fields.Many2one(comodel_name="vit.marketing_request",  string="Request",  help="")
    boq_sph_id      = fields.Many2one(comodel_name="vit.boq_sph_garmen_line", string="Boq SPH")
    detail_ids      = fields.One2many(comodel_name="vit.request_detail",  inverse_name="request_line_id",  string="Request Line",  help="" )
    # doc_line_ids    = fields.One2many(comodel_name="vit.request_line_doc",  inverse_name="request_line_id",  string="Request Line",  help="" )
    
    # def write(self, vals):        
    #     result = super(request_line, self).write(vals)
    #     for line in self:
    #         # import pdb;pdb.set_trace()
    #         if line.doc_line_ids.ids == []:
    #             raise UserError(_('Dokumen Desain %s belum diisi') % (line.name))

    #         return result

class request_detail(models.Model):

    _name = "vit.request_detail"
    _description = "vit.request_detail"
    _order = 'id desc'
    _inherit = ['mail.thread']

    name            = fields.Char( required=True, string="Style",  help="")
    state           = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",track_visibility='onchange',  help="")
    qty             = fields.Float( string="Qty", digits=dp.get_precision('Product Unit of Measure'), default=1.0,  help="")
    kain            = fields.Char( string="Kain",  help="")
    # desain          = fields.Char( string="Desain", compute="add_desain", store=True,  help="" )
    uom             = fields.Many2one(comodel_name="uom.uom", string="Satuan")
    size            = fields.Many2one( "product.attribute.value",string="Size")
    desc            = fields.Char( string="Description",  help="")
    # gbr             = fields.Binary( string="Gambar",  help="")
    # doc_name        = fields.Char( string="Document",)
    
    product_id      = fields.Many2one( comodel_name="product.template", string="Product", required=False,  help="")
    request_line_id = fields.Many2one(comodel_name="vit.request_line",  string="Request Line",  help="")
    material_ids    = fields.One2many(comodel_name="vit.request_material_list",  inverse_name="request_detail_id",  string="Material List",  help="" )
    # routing_id      = fields.Many2one(comodel_name="mrp.routing", string="Routing")
    bom_id          = fields.Many2one(comodel_name="mrp.bom", string="Bill of Material")
    # mo_id           = fields.Many2one(comodel_name="mrp.production", string="MO Sample")
    mo_ids          = fields.One2many(comodel_name="mrp.production", inverse_name="request_detail_id", string="MO Sample")
    doc_line_ids    = fields.One2many(comodel_name="vit.request_line_doc",  inverse_name="detail_id",  string="Desain",  help="" )
    
        
    # @api.depends('doc')
    # def add_desain(self):
    #     for rq in self:
    #         if rq.doc:
    #             rq.desain = 'Terlampir'
    @api.onchange('product_id')
    def onchange_material(self):
        if self.product_id:
            # import pdb;pdb.set_trace()
            bom = self.env['mrp.bom'].search([('product_tmpl_id','=',self.product_id.id)], limit=1)
            if bom:
                materials = []
                for mat in bom.bom_line_ids:
                    materials.append((0,0,{
                                'material'      : mat.product_id.id,
                                'qty'           : mat.product_qty,
                                'uom'           : mat.product_uom_id.id,
                            }))
                self.material_ids = materials
    
    @api.multi
    def create_product_sample(self):
        for rd in self:
            categ = self.env['product.category'].search([('name','=','Barang Sample')])
            if not categ:
                raise UserError(_('Kategori Barang Sample belum ada!'))
            else:
                product_tmp = self.env['product.template']
                p_product_tmp = self.env['product.product']
                bom_tmp = self.env['mrp.bom']
                datas = {
                    'name'          : rd.name + '[Sample Marketing]',
                    'type'          : 'product',
                    'categ_id'      : categ.id,
                    'uom_id'        : rd.uom.id,
                    'uom_po_id'     : rd.uom.id,
                    'sample'        : True,
                    'list_price'    : 0.0,
                    'standard_price': 0.0,
                    'taxes_id'          : False,
                    'supplier_taxes_id' : False,
                    'tracking'      : 'none',
                    'sale_ok'       : False,
                    'purchase_ok'   : False,
                    'company_id'    : rd.request_line_id.request_id.company_id.id,
                    'partner_id'    : rd.request_line_id.request_id.partner_id.id,
                    # 'image_medium'  : rd.gbr,
                }
                # import pdb;pdb.set_trace()
                # create product sample
                sample = product_tmp.create(datas)                
                sample_variant = p_product_tmp.search([('product_tmpl_id', '=', sample.id)], limit=1)
                # create BoM
                bom_line_ids = []
                for mt in rd.material_ids:
                    bom_line_ids.append((0,0,{
                            'product_id'    : mt.material.id,
                            'product_qty'   : mt.qty,
                            'product_uom_id': mt.uom.id,
                        }))
                bom_datas = {
                    'product_tmpl_id'           : sample.id,
                    'product_id'                : sample_variant.id,
                    'product_qty'               : rd.qty,
                    'product_uom_id'            : sample.uom_id.id,
                    # 'routing_id'                : rd.routing_id.id,
                    'bom_line_ids'              : bom_line_ids,
                }
                bom = bom_tmp.create(bom_datas)
            return rd.write({'state': 'created','product_id': sample.id,'bom_id': bom.id})

    @api.multi 
    def action_confirm(self):
        self.state = STATES[1][0]

    @api.multi 
    def action_approved(self):
        self.state = STATES[5][0]
            

class request_material_list(models.Model):

    _name = "vit.request_material_list"
    _description = "vit.request_material_list"
    _rec_name = "material"

    name        = fields.Char( required=False, string="Material List",  help="")
    qty         = fields.Float( string="Qty", digits=dp.get_precision('Product Unit of Measure'), default=0.0,  help="")
    spec        = fields.Char( string="Spec", help="")
    colour      = fields.Char( string="Colour", help="" )
    uom         = fields.Many2one(comodel_name="uom.uom", string="Unit",)
    # cons        = fields.Float( string="Cons", digits=dp.get_precision('Product Unit of Measure'), default=0.0,  help="")
    
    material    = fields.Many2one( comodel_name="product.product", string="Material",  help="")
    request_detail_id   = fields.Many2one( comodel_name="vit.request_detail", string="Detail",  help="")

    @api.onchange('material')
    def onchange_uom(self):
        for lis in self:
            if lis.material:
                lis.uom = lis.material.uom_id
    

class request_line_doc(models.Model):

    _name = "vit.request_line_doc"
    _description = "vit.request_line_doc"
    
    name        = fields.Char( string="Description",  help="")
    date        = fields.Date( string="Date", default=lambda self: time.strftime("%Y-%m-%d"), help="")
    doc         = fields.Binary( string="Document Name",  help="")
    doc_name    = fields.Char( string="Document Name",)

    detail_id   = fields.Many2one(comodel_name="vit.request_detail",  string="Detail",  help="")
    # request_line_id = fields.Many2one(comodel_name="vit.request_line",  string="Request Line",  help="")
    