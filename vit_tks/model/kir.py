#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft', 'Draft'),('open','Confirm'),('done','Done')]
from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class kir(models.Model):

    _name = "vit.kir"
    _description = "vit.kir"
    name = fields.Char( required=True, default="New", readonly=True,  string="Name",  help="")
    ruang = fields.Char( string="Ruang",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    state = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",  help="")
    date = fields.Date( string="Date",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    gedung = fields.Char( string="Gedung",  readonly=True, states={"draft" : [("readonly",False)]},  help="")


    kir_detail_ids = fields.One2many(comodel_name="vit.kir_detail",  inverse_name="kir_id",  string="Kir detail",  readonly=True, states={"draft" : [("readonly",False)]},  help="")

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
        return super(kir, self).unlink()
