#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft', 'Draft'),('open','Confirm'),('done','Done')]
from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class mutasi_barang(models.Model):

    _name = "vit.mutasi_barang"
    _description = "vit.mutasi_barang"
    name = fields.Char( required=True, default="New", readonly=True,  string="Name",  help="")
    date = fields.Date( string="Date",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    start_date = fields.Date( string="Start date",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    end_date = fields.Date( string="End date",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    state = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",  help="")


    def action_reload(self, ):
        pass


    detail_ids = fields.One2many(comodel_name="vit.mutasi_detail",  inverse_name="mutasi_id",  string="Detail",  readonly=True, states={"draft" : [("readonly",False)]},  help="")

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
        return super(mutasi_barang, self).unlink()
