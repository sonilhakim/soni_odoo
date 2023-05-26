#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
import time
from odoo.exceptions import UserError, ValidationError
STATES=[('draft', 'Draft'), ('open', 'Open'), ('approve', 'Approve Sample'), ('cancel', 'Cancel'), ('done','Done')]

class sample_approval(models.Model):

    _name = "vit.sample_approval"
    _description = "vit.sample_approval"
    _order = 'date desc, id desc'
    _inherit = ['mail.thread']

    name                = fields.Char( readonly=True, required=True, default='New', string="Name",  help="")
    state               = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State", track_visibility='onchange', help="")
    date                = fields.Date( string="Date", required=True, default=lambda self: time.strftime("%Y-%m-%d"), readonly=True, states={"draft" : [("readonly",False)]}, help="")
    requester           = fields.Char( string="Request", required=True, help="", readonly=True, states={"draft" : [("readonly",False)]} )
    project             = fields.Text( string="Project Description", required=True, help="", readonly=True, states={"draft" : [("readonly",False)]} )
    recipient           = fields.Char( string="Recipient", required=True, help="", readonly=True, states={"draft" : [("readonly",False)]} )
    notes               = fields.Text( string="Notes",  help="", readonly=True, states={"draft" : [("readonly",False)]} )    
    due_date            = fields.Date(string="Due Date", required=True, readonly=True, states={"draft" : [("readonly",False)]}, help="")
    
    partner_id          = fields.Many2one( required=True, comodel_name="res.partner",  string="Buyer", readonly=True, states={"draft" : [("readonly",False)]},  help="")
    user_id             = fields.Many2one("res.users", "User", default=lambda self: self.env.uid, track_visibility='onchange', readonly=True)
    company_id          = fields.Many2one( comodel_name="res.company",  string="Company", related='user_id.company_id', readonly=True,  help="")
    product_request_id  = fields.Many2one( comodel_name="vit.product.request", string="Product Request", help="")
    line_approval_ids   = fields.One2many(comodel_name="vit.sample_approval_line",  inverse_name="sample_approval_id",  string="Lines",  help="", readonly=True, states={"draft": [("readonly", False)],"open": [("readonly", False)]} )
    jo_id               = fields.Char( string="No JO",  help="", readonly=True)
    or_id               = fields.Many2one( comodel_name="vit.purchase_order_garmen",  string="No. OR", readonly=True,  help="")
    
    
    @api.model
    def create(self, vals):
        if not vals.get('name', False) or vals['name'] == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('vit.sample_approval') or 'Error Number!!!'
            
        return super(sample_approval, self).create(vals)


    @api.multi 
    def action_draft(self):
        for line in self.line_approval_ids:
            line.write({'state': 'draft'})
        self.state = STATES[0][0]

    @api.multi 
    def action_confirm(self):
        for sa in self:
            for line in sa.line_approval_ids:
                line.write({'state': 'open'})
        self.state = STATES[1][0]
    
    @api.multi 
    def action_approve(self):
        self.state = STATES[2][0]

    @api.multi 
    def action_cancel(self):
        self.state = STATES[3][0]
    
    
    @api.multi 
    def action_done(self):
        for sa in self:
            jo = self.env["vit.purchase_order_garmen"].search([('id','=',sa.or_id.id)])
            for sal in sa.line_approval_ids:
                # import pdb;pdb.set_trace()
                if sal.state != 'approved':
                    raise UserError(_('Ada sample yang belum di approve'))
                boq = self.env["vit.boq_po_garmen_line"].search([('id','=',sal.boq_jo_id.id),('po_id','=',jo.id)])
                if sal.state != 'approved':
                    raise UserError(_('Ada sample yang belum di approve'))
                sql = "delete from vit_or_material_list where boq_id = %s"
                self.env.cr.execute(sql, (sal.boq_jo_id.id,)) 
                materials = self.env['vit.approval_material_list'].search([('approval_line_id','=',sal.id)])
                mat_data = []
                for mat in materials:
                    mat_data.append((0,0,{
                        'acc_no'   : mat.material.product_tmpl_id.default_code,
                        'material' : mat.material.id,
                        'qty'      : mat.qty,
                        'uom'      : mat.uom,
                        'spec'     : mat.spec,
                        'colour'   : mat.colour,
                        'cons'     : mat.cons,
                        'boq_id'   : mat.approval_line_id.boq_jo_id.id,
                        }))
                sql1 = "delete from vit_or_line_doc where boq_id = %s"
                self.env.cr.execute(sql1, (sal.boq_jo_id.id,))
                designs = self.env['vit.approval_desain'].search([('approval_line_id','=',sal.id)])
                ds_data = []
                for ds in designs:
                    ds_data.append((0,0,{
                        'doc_name'   : ds.doc_name,
                        'doc'        : ds.doc,
                        'date'       : ds.date,
                        'name'       : ds.name,
                        'boq_id'     : mat.approval_line_id.boq_jo_id.id,
                        }))
                boq.update({
                        'sample_approv_id' : sal.product_sample_id.id,
                        # 'routing_id'       : sal.routing_id.id,
                        'harga_cm'         : sal.harga_cm,
                        'material_ids'     : mat_data,
                        'design_ids'       : ds_data,
                    })
            jo.update({'sample_done'   : True})
        self.state = STATES[4][0]

 