#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft','Draft'),('open','Perlu Approval'),('read','Read'),('unread','Unread')]
from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class doc(models.Model):

    _name = "vit.doc"
    _description = "vit.doc"
    name = fields.Char( required=True, default="New", readonly=True,  string="Name",  help="")
    state = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",  help="")
    subject = fields.Char( string="Subject",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    body = fields.Text( string="Body",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    date = fields.Date( string="Date",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    read_status = fields.Boolean( string="Read status",  readonly=True, states={"draft" : [("readonly",False)]},  help="")


    user_id = fields.Many2one(comodel_name="res.users",  string="User",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    to_user_ids = fields.One2many(comodel_name="vit.to_user",  inverse_name="doc_id",  string="To user",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    cc_user_ids = fields.One2many(comodel_name="vit.cc_user",  inverse_name="doc_id",  string="Cc user",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    doc_type_id = fields.Many2one(comodel_name="vit.doc_type",  string="Doc type",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    doc_template_id = fields.Many2one(comodel_name="vit.doc_template",  string="Doc template",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    doc_history_ids = fields.One2many(comodel_name="vit.doc_history",  inverse_name="doc_id",  string="Doc history",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    parent_id = fields.Many2one(comodel_name="vit.doc",  string="Parent",  readonly=True, states={"draft" : [("readonly",False)]},  help="")

    def action_confirm(self):
        self.state = STATES[1][0]

    def action_done(self):
        self.state = STATES[2][0]

    def action_draft(self):
        self.state = STATES[0][0]

    @api.multi
    def unlink(self):
        for me_id in self :
            if me_id.state != STATES[0][0]:
                raise UserError("Cannot delete non draft record!")
        return super(doc, self).unlink()
