#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft','Draft'),('open','Confirm'),('done','Done')]
from odoo import models, fields, api, _
import time
from odoo.exceptions import UserError, Warning

class pemakaian_aset(models.Model):
    _name = "vit.pemakaian_aset"
    _inherit = "vit.pemakaian_aset"

    date = fields.Date( string="Tanggal",  readonly=True, default=lambda self: time.strftime("%Y-%m-%d"), states={"draft" : [("readonly",False)]},  help="")

    @api.model
    def create(self, vals):
        if not vals.get("name", False) or vals["name"] == "New":
            vals["name"] = self.env["ir.sequence"].next_by_code("vit.pemakaian_aset") or "Error Number!!!"
        return super(pemakaian_aset, self).create(vals)

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
        return super(pemakaian_aset, self).unlink()
