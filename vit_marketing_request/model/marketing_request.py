#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
import time
from odoo.exceptions import UserError, ValidationError
STATES=[('draft', 'Draft'), ('open', 'ACC TD'), ('mo_product', 'Create MO/Product'), ('approve', 'Approve Sample'), ('cancel', 'Cancel'), ('done','Done')]

class marketing_request(models.Model):

    _name = "vit.marketing_request"
    _description = "vit.marketing_request"
    _order = 'date desc, id desc'
    _inherit = ['mail.thread']

    name                = fields.Char( readonly=True, required=True, default='New', string="Name",  help="")
    state               = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",track_visibility='onchange',  help="")
    date                = fields.Date( string="Req Date", required=True, default=lambda self: time.strftime("%Y-%m-%d"), readonly=True, states={"draft" : [("readonly",False)]}, help="")
    requester           = fields.Char( string="Request", required=True, help="", readonly=True, states={"draft" : [("readonly",False)]} )
    project             = fields.Text( string="Project Description", required=True, help="", readonly=True, states={"draft" : [("readonly",False)]} )
    recipient           = fields.Char( string="Recipient", required=True, help="", readonly=True, states={"draft" : [("readonly",False)]} )
    notes               = fields.Text( string="Notes",  help="", readonly=True, states={"draft" : [("readonly",False)]} )    
    due_date            = fields.Date(string="Due Date", required=True, readonly=True, states={"draft" : [("readonly",False)]}, help="")
    # total_qty           = fields.Float( string="Total", store=True,compute='_compute_total',  help="")
    
    partner_id          = fields.Many2one( required=True, comodel_name="res.partner",  string="Buyer", readonly=True, states={"draft" : [("readonly",False)]},  help="")
    user_id             = fields.Many2one("res.users", "User", default=lambda self: self.env.uid, track_visibility='onchange', readonly=True)
    company_id          = fields.Many2one( comodel_name="res.company",  string="Company", related='user_id.company_id', readonly=True,  help="")
    line_request_ids    = fields.One2many(comodel_name="vit.request_line",  inverse_name="request_id",  string="Lines",  help="", readonly=True, states={"draft": [("readonly", False)],"open": [("readonly", False)]} )
    doc_request_ids     = fields.One2many(comodel_name="vit.request_doc",  inverse_name="request_id",  string="Docs",  help="", readonly=True, states={"draft" : [("readonly",False)]} )
    product_request_id  = fields.Many2one( comodel_name="vit.product.request", string="Product Request", help="")
    sph_id              = fields.Many2one(required=True, comodel_name="vit.marketing_sph_garmen",  string="No SPH",  help="", readonly=True, states={"draft" : [("readonly",False)]})
    
    @api.model
    def create(self, vals):
        if not vals.get('name', False) or vals['name'] == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('vit.marketing_request_desain') or 'Error Number!!!'
            # if type == 'design':
            #     vals['name'] = self.env['ir.sequence'].next_by_code('vit.marketing_request_design') or 'Error Number!!!'
            # else:
            #     vals['name'] = self.env['ir.sequence'].next_by_code('vit.marketing_request_sample') or 'Error Number!!!'
        return super(marketing_request, self).create(vals)

    @api.multi 
    def action_draft(self):
        for line in self.line_request_ids:
            line.write({'state': 'draft'})
        self.state = STATES[0][0]

    @api.multi 
    def action_confirm(self):
        for req in self:
            sph = self.env["vit.marketing_sph_garmen"].search([('id','=',req.sph_id.id)])
            if not req.line_request_ids or  not req.doc_request_ids :
                raise UserError(_('BOQ dan Attachment harus diisi'))
            else:
                for line in req.line_request_ids:
                    design = self.env['vit.request_detail'].search([('request_line_id','=',line.id)])
                    for d in design:
                        d.write({'state': 'open'})
                req.state = STATES[1][0]

    @api.multi 
    def action_acc(self):
        for req in self:
            sph = self.env["vit.marketing_sph_garmen"].search([('id','=',req.sph_id.id)])
            for rel in req.line_request_ids:
                boq = self.env["vit.boq_sph_garmen_line"].search([('id','=',rel.boq_sph_id.id),('sph_id','=',sph.id)])
                detail = self.env['vit.request_detail'].search([('request_line_id','=',rel.id)])
                if not detail:
                    raise UserError(_('Style belum dibuat'))
            req.state = STATES[2][0]

    @api.multi 
    def action_approve(self):
        self.state = STATES[3][0]

    @api.multi 
    def action_cancel(self):
        self.state = STATES[4][0]    

    @api.multi 
    def action_done(self):
        for req in self:
            sph = self.env["vit.marketing_sph_garmen"].search([('id','=',req.sph_id.id)])
            for rel in req.line_request_ids:
                boq = self.env["vit.boq_sph_garmen_line"].search([('id','=',rel.boq_sph_id.id),('sph_id','=',sph.id)])
                detail = self.env['vit.request_detail'].search([('request_line_id','=',rel.id)])
                for ds in detail:
                    if ds.state != 'approved':
                        raise UserError(_('Ada sample yang belum di approve'))
                    document = self.env['vit.request_line_doc'].search([('detail_id','=',ds.id)])
                    doc_data = []
                    for doc in document:
                        doc_data.append((0,0,{
                            'doc_name'   : doc.doc_name,
                            'doc'        : doc.doc,
                            'date'       : doc.date,
                            'name'       : doc.name,
                            }))
                    line_datas = [(0, 0, {
                            'product_id'    : ds.product_id.id,
                            'product_name'  : ds.desc,
                            'size'          : ds.size.id,
                            # 'gbr'           : ds.gbr,
                            'kain'          : ds.kain,
                            'name'          : ds.name,
                            # 'qty'           : rel.qty,
                            # 'uom_id'        : ds.uom.id,
                            'boq_id'        : rel.boq_sph_id.id,
                            'doc_line_ids'  : doc_data,

                        })]
                    boq.write({"sample_ids": line_datas})
            
            # sph.update({'sample'   : True,})
            # import pdb;pdb.set_trace()
            req.state = STATES[5][0]

    # @api.depends('line_request_ids.qty')
    # def _compute_total(self):
    #     self.total_qty = sum(line.qty for line in self.line_request_ids)
