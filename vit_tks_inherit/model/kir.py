#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft', 'Draft'),('open','Confirm'),('done','Done')]
from odoo import models, fields, api, _
import time
import datetime
from odoo.exceptions import UserError, Warning

class kir(models.Model):
    _name = "vit.kir"
    _inherit = "vit.kir"

    date  = fields.Date(string="Tanggal Pembukuan", required=False,
                              default=lambda self:time.strftime("%Y-%m-%d"))
    ruang = fields.Many2one( "vit.vit_ruang", string="Ruang",  readonly=True, states={"draft" : [("readonly",False)]}, help="")
    gedung = fields.Many2one( "vit.vit_gedung", string="Gedung",  readonly=True, states={"draft" : [("readonly",False)]},  help="")

    @api.model
    def create(self, vals):
        if not vals.get("name", False) or vals["name"] == "New":
            vals["name"] = self.env["ir.sequence"].next_by_code("vit.kir") or "Error Number!!!"
        return super(kir, self).create(vals)

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
