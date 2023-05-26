#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft','Draft'),('open','Confirm'),('done','Done')]
from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class referensi_aset(models.Model):
    _name = "vit.referensi_aset"
    _inherit = "vit.referensi_aset"

    name = fields.Char( required=True, default="New", readonly=True,  string="Name", states={"draft" : [("readonly",False)]}, help="")
    data_file = fields.Binary(string='Referensi File', help='')

    # @api.model
    # def create(self, vals):
    #     if not vals.get("name", False) or vals["name"] == "New":
    #         vals["name"] = self.env["ir.sequence"].next_by_code("vit.referensi_aset") or "Error Number!!!"
    #     return super(referensi_aset, self).create(vals)

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
