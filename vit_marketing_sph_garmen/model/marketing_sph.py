#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
import time
import datetime
STATES=[('draft', 'Draft'), ('open', 'Open'), ('cancel', 'Cancel'), ('purchase_approved', 'Purchase Approved'), ('ppic_approved', 'PPIC Approved'), ('tender', 'Tender'), ('close','Closed')]

class marketing_sph_garmen(models.Model):

    _name = "vit.marketing_sph_garmen"
    _description = "vit.marketing_sph_garmen"
    _order = 'date desc, id desc'
    _inherit = ['mail.thread']
    
    name                = fields.Char( readonly=True, required=True, default='New', string="No. SPH",  help="")
    state               = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State", track_visibility='onchange', help="")
    date                = fields.Date( string="Date", required=False, default=lambda self: time.strftime("%Y-%m-%d"), readonly=True, states={"draft" : [("readonly",False)]}, help="")
    due_date            = fields.Date(string="Due Date", readonly=True, states={"draft" : [("readonly",False)]}, help="")
    # deadline_date       = fields.Date(string="Deadline Production", readonly=True, states={"draft" : [("readonly",False)]}, help="")
    project             = fields.Text( string="Project", required=True, readonly=True, states={"draft" : [("readonly",False)]},  help="")
    notes               = fields.Text( string="Notes",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    total_qty           = fields.Float( string="Total Qty", store=True, compute='_compute_total_qty',  help="")
    time_production     = fields.Char(string="Time Production", readonly=True, states={"draft" : [("readonly",False)]}, help="")
    total_price         = fields.Monetary( compute="_compute_total_price", string="Total Price", store=True, help="")

    partner_id          = fields.Many2one(required=True, comodel_name="res.partner",  string="Buyer", readonly=True, states={"draft" : [("readonly",False)]}, help="")
    user_id             = fields.Many2one("res.users", "User", default=lambda self: self.env.uid, track_visibility='onchange', readonly=True)
    company_id          = fields.Many2one( comodel_name="res.company",  string="Company", related='user_id.company_id', readonly=True,  help="")
    currency_id         = fields.Many2one('res.currency', related='company_id.currency_id', string="Currency", readonly=True)
    proposal_id         = fields.Many2one( comodel_name="vit.marketing_proposal",  string="No. Proposal", help="")
    boq_ids             = fields.One2many(comodel_name="vit.boq_sph_garmen_line",  inverse_name="sph_id",  string="Boqs",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    doc_ids             = fields.One2many(comodel_name="vit.doc_sph_garmen_line",  inverse_name="sph_id",  string="Docs",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    
    po                  = fields.Char("No. OR")
    sample              = fields.Boolean("Product Sample", default=False)
    request             = fields.Char("No. Request Desain")
    condition           = fields.Text( string="Kondisi Penawaran",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    
    @api.model
    def create(self, vals):
        if not vals.get('name', False) or vals['name'] == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('vit.marketing_sph_garmen') or 'Error Number!!!'
        return super(marketing_sph_garmen, self).create(vals)

    @api.depends('boq_ids.qty')
    def _compute_total_qty(self):
        for sph in self:
            sph.total_qty = sum(line.qty for line in sph.boq_ids)

    @api.depends('boq_ids.total_price')
    def _compute_total_price(self):
        for sph in self:
            sph.total_price = sum(line.total_price for line in sph.boq_ids)
   
    @api.multi 
    def action_draft(self):
        self.state = STATES[0][0]

    @api.multi 
    def action_confirm(self):
        if not self.boq_ids or not self.doc_ids:
            raise UserError(_('BOQ dan Document harus diisi'))
        else:
            self.state = STATES[1][0]

    @api.multi 
    def action_cancel(self):
        pog = self.env["vit.purchase_order_garmen"].search([('name', '=', self.po)])
        if pog:
            if pog.state not in ['draft','cancel']:
                raise UserError(_('Cancel hanya bisa dilakukan jika OR belum dibuat atau masih berstatus Draft.'))
            else:
                pog.state = 'cancel'
                pog.sph_id = False
                self.po = False

        # for boq in self.boq_ids:
        #     if boq.sample_ids:
        #         sql = "delete from vit_boq_sph_sample where boq_id = %s"
        #         self.env.cr.execute(sql, (boq.id,))

        self.state = STATES[2][0]

    @api.multi 
    def action_approve_purchase(self):
        self.state = STATES[3][0]

    @api.multi 
    def action_approve_ppic(self):
        self.state = STATES[4][0]

    @api.multi 
    def action_tender(self):
        self.ensure_one()
        po = self.env["vit.purchase_order_garmen"]
        cr = self.env.cr
        for sph in self:
            line_ids = []
            for boq in sph.boq_ids:
                # import pdb;pdb.set_trace()                
                sphsam = self.env['vit.boq_sph_sample'].search([('boq_id','=',boq.id)])
                for sam in sphsam:
                    cr = self.env.cr
                    sql = """SELECT pp.default_code, pp.id, pt.spec, pt.colour, bl.product_qty, um.id
                            FROM mrp_bom_line bl
                            LEFT JOIN product_product pp ON bl.product_id = pp.id
                            LEFT JOIN mrp_bom bm ON bl.bom_id = bm.id
                            LEFT JOIN product_template pt ON bm.product_tmpl_id = pt.id
                            LEFT JOIN uom_uom um ON bl.product_uom_id = um.id
                            WHERE pt.id = %s
                            """
                    cr.execute(sql, (sam.product_id.id,))
                    result = cr.fetchall()
                    mat_data = []
                    for res in result:
                        mat_data.append((0, 0, {
                            "acc_no"   : res[0],
                            "material" : res[1],
                            "spec"     : res[2],
                            "colour"   : res[3],
                            "qty"      : res[4],
                            "uom"      : res[5],
                            }))
                    desain = self.env['vit.sample_line_doc'].search([('sample_id','=',sam.id)])
                    dsn_data = []
                    for dsn in desain:
                        dsn_data.append((0,0,{
                            'doc_name'   : dsn.doc_name,
                            'doc'        : dsn.doc,
                            'date'       : dsn.date,
                            'name'       : dsn.name,
                            }))
                    line_ids.append((0,0,{
                        "name"          : sam.name,
                        "sample_id"     : sam.product_id.id,
                        "kain"          : sam.kain,
                        "uom_id"        : boq.uom_id.id,
                        "price"         : boq.price,
                        "tax_id"        : boq.tax_id.id,
                        "product_name"  : sam.product_name,
                        "material_ids"  : mat_data,
                        "design_ids"    : dsn_data,
                        "is_po_payung"  : True,
                        }))
            doc_ids = []
            for doc in sph.doc_ids:
                doc_ids.append((0,0,{
                        'doc_name'   : doc.doc_name,
                        'doc'        : doc.doc,
                        'date'       : doc.date,
                        'name'       : doc.name,
                    }))
            
            data = {
                'sph_id'         : sph.id,
                'partner_id'     : sph.partner_id.id ,
                'project'        : sph.project,
                'note'           : sph.notes,
                'time_production': sph.time_production,
                'boq_line_ids'   : line_ids,
                'doc_line_ids'   : doc_ids,
            }
            if po.search([('sph_id', '=', sph.id)]):
                pass
            else:
                po_id = po.create(data)
                sph.po = po_id.name
        self.state = STATES[5][0]

    @api.multi 
    def action_close(self):
        self.state = STATES[6][0]

   