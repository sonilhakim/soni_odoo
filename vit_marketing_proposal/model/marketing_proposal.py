#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
import time
from odoo.exceptions import UserError, ValidationError
STATES=[('draft', 'Draft'), ('open', 'Open'), ('cancel', 'Cancel'), ('done','Presentasi')]

class marketing_proposal(models.Model):
    _name = "vit.marketing_proposal"
    _description = "vit.marketing_proposal"
    _order = 'date desc, id desc'
    _inherit = ['mail.thread']

    name                = fields.Char( readonly=True, required=True, default='New', string="Name",  help="")
    state               = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",track_visibility='onchange',  help="")
    date                = fields.Date( string="Date", required=False, default=lambda self: time.strftime("%Y-%m-%d"), readonly=True, states={"draft" : [("readonly",False)]}, help="")
    partner_id          = fields.Many2one( required=True, comodel_name="res.partner",  string="Buyer", readonly=True, states={"draft" : [("readonly",False)]},  help="")
    user_id             = fields.Many2one("res.users", "User", default=lambda self: self.env.uid, track_visibility='onchange', readonly=True)
    company_id          = fields.Many2one( comodel_name="res.company",  string="Company", related='user_id.company_id', readonly=True,  help="")
    inquery_id          = fields.Many2one( required=True, comodel_name="vit.marketing_inquery_garmen",  string="No Inquery",  help="")
    due_date            = fields.Date(string="Due Date", readonly=True, states={"draft" : [("readonly",False)]}, help="")
    project             = fields.Text( string="Project Description", required=True, help="", readonly=True, states={"draft" : [("readonly",False)]} )
    notes               = fields.Text( string="Notes",  help="", readonly=True, states={"draft" : [("readonly",False)]} )
    line_ids            = fields.One2many(comodel_name="vit.proposal_line",  inverse_name="proposal_id",  string="Lines",  help="", readonly=True, states={"draft" : [("readonly",False)]} )
    # total_qty           = fields.Float( string="Total", store=True,compute='_compute_total',  help="")
    doc_ids             = fields.One2many(comodel_name="vit.proposal_doc",  inverse_name="proposal_id",  string="Docs",  help="", readonly=True, states={"draft" : [("readonly",False)]} )
    sph                 = fields.Char( string="SPH")

    @api.model
    def create(self, vals):
        if not vals.get('name', False) or vals['name'] == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('vit.marketing_proposal') or 'Error Number!!!'
        return super(marketing_proposal, self).create(vals)

    # @api.onchange('inquery_id')
    # def inquery_onchange(self):
    #     if not self.inquery_id:
    #         return
    #     self.project        = self.inquery_id.project
    #     self.partner_id     = self.inquery_id.partner_id
    #     obj = self.env['vit.inquery_garmen_line'].search([('inquery_id','=',self.inquery_id.id)])
    #     doc = self.env['vit.inquery_garmen_doc'].search([('inquery_id','=',self.inquery_id.id)])
    #     line_data = []
    #     doc_data = []
    #     for record in self:
    #         record.update({"line_ids": False})
    #         for x in obj:
    #             line_data = [(0, 0, {
    #                 'product_id'   : x.product_id.id,
    #                 'qty'          : x.qty,
    #                 'uom'          : x.uom.id,
    #                 })]
    #             record.update({"line_ids": line_data})
            
    #         record.update({"doc_ids": False})
    #         for k in doc:
    #             doc_data = [(0, 0, {
    #                 "name": k.name,
    #                 "date":k.date,
    #                 "doc": k.doc,
    #                 "doc_name" : k.doc_name,
    #                 })]
    #             record.update({"doc_ids": doc_data})
    
    @api.multi 
    def action_draft(self):
        self.state = STATES[0][0]

    @api.multi 
    def action_confirm(self):
        if not self.line_ids or not self.doc_ids:
            raise UserError(_('BOQ dan Document harus diisi'))
        else:
            self.state = STATES[1][0]

    @api.multi 
    def action_cancel(self):
        self.state = STATES[2][0]

    @api.multi 
    def action_done(self):
        self.ensure_one()
        sph = self.env["vit.marketing_sph_garmen"]
        cr = self.env.cr
        cr1 = self.env.cr
        for prop in self:            
            sql = """SELECT pl.name, pl.qty, u.id
                    FROM vit_proposal_line pl
                    -- LEFT JOIN product_product pp ON pl.product_id = pp.id
                    LEFT JOIN uom_uom u ON pl.uom = u.id
                    WHERE pl.proposal_id = %s
                    """
            cr.execute(sql, (prop.id,))
            result = cr.fetchall()
            line_ids = []
            for res in result:
                line_ids.append((0,0,{
                        'name'   : res[0],
                        'qty'    : res[1],
                        'uom_id' : res[2],
                    }))

            doc_ids = []
            for doc in prop.doc_ids:
                doc_ids.append((0,0,{
                        'doc_name'   : doc.doc_name,
                        'doc'        : doc.doc,
                        'date'       : doc.date,
                        'name'       : doc.name,
                    }))
            
            data = {
                'proposal_id'   : prop.id,
                'partner_id'    : prop.partner_id.id ,
                'project'       : prop.project,
                'notes'         : prop.notes,
                'boq_ids'       : line_ids,
                'doc_ids'       : doc_ids,
            }
            if sph.search([('proposal_id', '=', prop.id)]):
                pass
            else:
                sph_id = sph.create(data)
                prop.sph = sph_id.name
            # import pdb;pdb.set_trace()
        self.state = STATES[3][0]

    # @api.depends('line_ids.qty')
    # def _compute_total(self):
    #     self.total_qty = sum(line.qty for line in self.line_ids)