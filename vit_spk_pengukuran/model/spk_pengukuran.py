#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
import time
from odoo.exceptions import UserError, ValidationError
STATES=[('draft', 'Draft'), ('open', 'Open'), ('cancel', 'Cancel'), ('done','Done')]

class spk_pengukuran(models.Model):

    _name = "vit.spk_pengukuran"
    _description = "vit.spk_pengukuran"
    _order = 'date desc, id desc'
    _inherit = ['mail.thread']

    name                = fields.Char( readonly=True, required=True, default='New', string="Instruksi No",  help="")
    state               = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State", track_visibility='onchange', help="")
    date                = fields.Date( string="Date", required=False, default=lambda self: time.strftime("%Y-%m-%d"), readonly=True, states={"draft" : [("readonly",False)]}, help="")
    partner_id          = fields.Many2one( required=True, comodel_name="res.partner",  string="Buyer", readonly=True, states={"draft" : [("readonly",False)]},  help="")
    user_id             = fields.Many2one("res.users", "User", default=lambda self: self.env.uid, track_visibility='onchange', readonly=True)
    company_id          = fields.Many2one( comodel_name="res.company",  string="Company", related='user_id.company_id', readonly=True,  help="")
    project             = fields.Text( string="Project Description",  help="", readonly=True, states={"draft" : [("readonly",False)]} )
    notes               = fields.Text( string="Notes",  help="", readonly=True, states={"draft" : [("readonly",False)]} )
    spk_line_ids        = fields.One2many(comodel_name="vit.spk_pengukuran_line",  inverse_name="spk_id",  string="Lines",  help="", readonly=True, states={"draft" : [("readonly",False)]} )
    doc_ids             = fields.One2many(comodel_name="vit.spk_pengukuran_doc",  inverse_name="spk_id",  string="Document",  help="", readonly=True, states={"draft" : [("readonly",False)]} )
    po_id               = fields.Many2one(comodel_name="vit.purchase_order_garmen", string="No. OR")
    spk_product_ids     = fields.One2many(comodel_name="vit.spk_product_pengukuran",  inverse_name="spk_id",  string="Product",  help="", readonly=True, states={"draft" : [("readonly",False)]} )
    
    @api.model
    def create(self, vals):
        if not vals.get('name', False) or vals['name'] == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('vit.spk_pengukuran') or 'Error Number!!!'
        return super(spk_pengukuran, self).create(vals)

    
    @api.multi 
    def action_draft(self):
        self.state = STATES[0][0]

    @api.multi 
    def action_confirm(self):
        if not self.spk_line_ids:
            raise UserError(_('Detail harus diisi'))
        else:
            self.state = STATES[1][0]

    @api.multi 
    def action_cancel(self):
        self.state = STATES[2][0]

    @api.multi 
    def action_done(self):
        self.state = STATES[3][0]
