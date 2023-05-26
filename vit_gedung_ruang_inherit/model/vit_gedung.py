#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft','Draft'),('open','Confirmed'),('done','Done')]
from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class vit_gedung(models.Model):
    _name = "vit.vit_gedung"
    _inherit = "vit.vit_gedung"

    name = fields.Char( required=True, default="New", readonly=False,  string="Name",  help="")

    # @api.model
    # def create(self, vals):
    #     if not vals.get("name", False) or vals["name"] == "New":
    #         vals["name"] = self.env["ir.sequence"].next_by_code("vit.vit_gedung") or "Error Number!!!"
    #     return super(vit_gedung, self).create(vals)

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
        return super(vit_gedung, self).unlink()

    @api.onchange('asset_id')
    def onchange_kir(self):
        for gd in self:
            if gd.asset_id:
                gd.penanggung_jawab_id = gd.asset_id.responsible_id
