#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
import time
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, ValidationError
STATES=[('draft', 'Draft'), ('open', 'Open'), ('cancel', 'Cancel'), ('approved','Approved'), ('jo_onprogress','JO Onprogress'), ('jo_done','JO Done')]
# STATES_ST=[('draft', 'Draft'), ('open', 'Open'), ('worksheet','Worksheet')]

class purchase_order_md_garmen(models.Model):
    _name = "vit.purchase_order_garmen"
    _inherit = "vit.purchase_order_garmen"
        
    name_jo            = fields.Char( readonly=True, required=True, default='New', string="Name",  help="")
    state              = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",  help="")
    product_request_id = fields.Many2one( comodel_name="vit.product.request", string="Product Request", help="")
    sample_approval_id = fields.Char( string="No. Sample Approval")
    sample_done        = fields.Boolean( string="Sample Approval Done", default=False)
    
    @api.multi
    def action_submit_jo(self):
        for po in self:
            po.name_jo = self.env['ir.sequence'].next_by_code('vit.job_order_garmen') or 'Error Number!!!'
                   
        self.state = STATES[4][0]
        
    @api.multi 
    def action_job_done(self):
        self.state = STATES[5][0]

class boq_po_md_garmen_line(models.Model):
    _name = "vit.boq_po_garmen_line"
    _inherit = ['vit.boq_po_garmen_line','mail.thread']
    _order = 'id desc'
    
    harga_cm         = fields.Float( string="Harga CM / PC",  help="")
    # state            = fields.Selection(selection=STATES_ST,  readonly=True, default=STATES_ST[0][0],  string="State",  help="")
    jo_name          = fields.Char( string="No. JO", related="po_id.name_jo", store=True)
    sample_approv_id = fields.Many2one( comodel_name="product.template",  string="Sample Approval",  help="")
    sample_done      = fields.Boolean( string="Sample Approval Done", related="po_id.sample_done")
    routing_id       = fields.Many2one(comodel_name="mrp.routing", string="Routing")
    ws_count         = fields.Integer(string='Hitung Worksheet', compute='_get_ws')
    pengukuran_id    = fields.Many2one( comodel_name="vit.pengukuran",  string="No. Pengukuran",  help="")
    # bom_qty          = fields.Float( string="Qty", digits=dp.get_precision('Product Unit of Measure'), default=1.0,  help="")
    lot_selected = fields.Char(string="Lot Selected")

    def _get_ws(self):
        for boq in self:
            mrp_ids = self.env["mrp.production"].search([('boq_po_line_id','=',boq.id)])
            if mrp_ids:
                boq.ws_count = len(set(mrp_ids.ids))

    @api.multi
    def action_view_worksheet(self):
        for boq in self:
            mrp_ids = self.env["mrp.production"].search([('boq_po_line_id','=',boq.id)])
            action = self.env.ref('mrp.mrp_production_action').read()[0]
            if len(mrp_ids) > 1:
                action['domain'] = [('id', 'in', mrp_ids.ids)]
            elif len(mrp_ids) == 1:
                form_view = [(self.env.ref('mrp.mrp_production_form_view').id, 'form')]
                if 'views' in action:
                    action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
                else:
                    action['views'] = form_view
                action['res_id'] = mrp_ids.ids[0]
            else:
                action = {'type': 'ir.actions.act_window_close'}
            return action

class or_material_list_md(models.Model):
    _name = "vit.or_material_list"
    _inherit = "vit.or_material_list"

    qty_style = fields.Float( string="Qty Style", digits=dp.get_precision('Product Unit of Measure'), related="boq_id.qty", store=True,  help="")
    jo_name   = fields.Char( string="JO", related="boq_id.po_id.name_jo", store=True)
    po_id     = fields.Many2one( string="PO", related="boq_id.po_id", store=True)
    total     = fields.Float( string="Total", digits=dp.get_precision('Product Unit of Measure'), compute="_compute_total", store=True, help="")
    pr        = fields.Boolean( string="Purchase Request")
    

    @api.depends('qty_style','cons')
    def _compute_total(self):
        for mat in self:
            mat.total = mat.qty_style * mat.cons