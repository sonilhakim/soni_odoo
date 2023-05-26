#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
import time
from odoo.exceptions import UserError, ValidationError
STATES=[('draft', 'Draft'), ('open', 'Open'), ('cancel', 'Cancel'), ('proposal', 'Proposal')]

class marketing_inquery_garmen(models.Model):

    _name = "vit.marketing_inquery_garmen"
    _description = "vit.marketing_inquery_garmen"
    _order = 'date desc, id desc'
    _inherit = ['mail.thread']

    name                = fields.Char( readonly=True, required=True, default='New', string="Name", copy=False)
    state               = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",track_visibility='onchange',  help="")
    date                = fields.Date( string="Date", required=False, default=lambda self: time.strftime("%Y-%m-%d"), readonly=True, states={"draft" : [("readonly",False)]}, help="")
    source              = fields.Char( string="Source", required=True, help="", readonly=True, states={"draft" : [("readonly",False)]} )
    project             = fields.Text( string="Project", required=True, help="", readonly=True, states={"draft" : [("readonly",False)]} )
    notes               = fields.Text( string="Notes",  help="", readonly=True, states={"draft" : [("readonly",False)]} )    
    due_date            = fields.Date(string="Due Date", required=True, readonly=True, states={"draft" : [("readonly",False)]}, help="")
    pic_marketing       = fields.Char( string="PIC Marketing", required=True, help="", readonly=True, states={"draft" : [("readonly",False)]} )
    # total_qty           = fields.Float( string="Total", store=True,compute='_compute_total',  help="")

    partner_id          = fields.Many2one( required=True, comodel_name="res.partner",  string="Buyer", readonly=True, states={"draft" : [("readonly",False)]},  help="")
    user_id             = fields.Many2one("res.users", "User", default=lambda self: self.env.uid, track_visibility='onchange', readonly=True)
    company_id          = fields.Many2one( comodel_name="res.company",  string="Company", related='user_id.company_id', readonly=True,  help="")
    line_ids            = fields.One2many(comodel_name="vit.inquery_garmen_line",  inverse_name="inquery_id",  string="Lines",  help="", readonly=True, states={"draft" : [("readonly",False)]} )
    doc_ids             = fields.One2many(comodel_name="vit.inquery_garmen_doc",  inverse_name="inquery_id",  string="Docs",  help="", readonly=True, states={"draft" : [("readonly",False)]} )
    # proposal_id         = fields.Many2one(comodel_name="vit.marketing_proposal",  string="Proposal", help="")
    proposal            = fields.Char( string="Proposal")

    @api.multi
    def _cek_name(self):
        for po in self:
            x = self.env['vit.marketing_inquery_garmen'].search([('name','=',po.name),('id','!=',po.id)])
            if x:
                return False

        return True

    _constraints = [(_cek_name, 'Name of Marketing Inquery must be Unique!', ['name'])]
    
    @api.model
    def create(self, vals):
        partner = self.env['res.partner'].search([('id','=',vals['partner_id'])])
        if not partner.ref:
            raise UserError(_('Referensi Buyer belum diisi'))
        inq = self.env['vit.marketing_inquery_garmen'].search([('partner_id','=',vals['partner_id'])])
        if not vals.get('name', False) or vals['name'] == 'New':
            # vals['name'] = self.env['ir.sequence'].next_by_code('vit.marketing_inquery_garmen') or 'Error Number!!!'
            seq = len(inq)
            if len(str(seq)) == 1:
                vals['name'] = partner.ref + '0' + str(seq + 1)
            else:
                vals['name'] = partner.ref + str(seq + 1)
        return super(marketing_inquery_garmen, self).create(vals)

    
    @api.multi 
    def action_draft(self):
        self.state = STATES[0][0]

    @api.multi 
    def action_confirm(self):
        if not self.line_ids or not self.doc_ids:
            raise UserError(_('BOQ dan Attachment harus diisi'))
        else:
            self.state = STATES[1][0]

    @api.multi 
    def action_cancel(self):
        self.state = STATES[2][0]

    @api.multi 
    def action_proposal(self):
        self.ensure_one()
        prop = self.env["vit.marketing_proposal"]
        cr = self.env.cr
        cr1 = self.env.cr
        for ic in self:            
            sql = """SELECT il.name, il.qty, u.id
                    FROM vit_inquery_garmen_line il
                    -- LEFT JOIN product_product pp ON il.product_id = pp.id
                    LEFT JOIN uom_uom u ON il.uom = u.id
                    WHERE il.inquery_id = %s
                    """
            cr.execute(sql, (ic.id,))
            result = cr.fetchall()
            line_ids = []
            for res in result:
                line_ids.append((0,0,{
                        'name'   : res[0],
                        'qty'    : res[1],
                        'uom'    : res[2],
                    }))

            # sql1 = """SELECT doc_name, doc, date, name
            #         FROM vit_inquery_garmen_doc
            #         WHERE inquery_id = %s
            #         """
            # cr1.execute(sql1, (ic.id,))
            # result1 = cr1.fetchall()
            doc_ids = []
            # for res1 in result1:
            for doc in ic.doc_ids:
                doc_ids.append((0,0,{
                        'doc_name'   : doc.doc_name,
                        'doc'        : doc.doc,
                        'date'       : doc.date,
                        'name'       : doc.name,
                    }))
            
            data = {
                'inquery_id' : ic.id,
                'partner_id' : ic.partner_id.id ,
                'project'    : ic.project,
                'notes'      : ic.notes,
                'line_ids'   : line_ids,
                'doc_ids'    : doc_ids,
            }
            if prop.search([('inquery_id', '=', ic.id)]):
                pass
            else:
                prop_id = prop.create(data)
                ic.proposal = prop_id.name
            # import pdb;pdb.set_trace()
        self.state = STATES[3][0]

    @api.multi
    def unlink(self):
        for rec in self:
            if rec.state != 'draft':
                raise UserError(_('Data yang bisa dihapus hanya yang berstatus draft!'))
        return super(marketing_inquery_garmen, self).unlink()

    
    # @api.depends('line_ids.qty')
    # def _compute_total(self):
    #     self.total_qty = sum(line.qty for line in self.line_ids)
