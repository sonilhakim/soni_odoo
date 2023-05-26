#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft','Draft'),('open','Confirm'),('done','Done')]
from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class referensi_aset(models.Model):

    _name = "vit.referensi_aset"
    _description = "vit.referensi_aset"
    name = fields.Char( required=True, default="New", readonly=True,  string="Name",  help="")
    description = fields.Text( string="Description",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    state = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",  help="")


    ikhtisar_ids = fields.One2many(comodel_name="vit.ikhtisar",  inverse_name="ref_id",  string="Ikhtisar",  readonly=True, states={"draft" : [("readonly",False)]},  help="")

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
        return super(referensi_aset, self).unlink()
