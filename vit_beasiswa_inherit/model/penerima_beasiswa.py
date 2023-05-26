#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft','Draft'),('open','Verifikasi'),('lolos_akademik','Lolos Akademik'),('done','Lolos PTN'),('reject','Ditolak')]
from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class penerima_beasiswa(models.Model):
    _name = "vit.penerima_beasiswa"
    _inherit = "vit.penerima_beasiswa"

    @api.model
    def create(self, vals):
        if not vals.get("name", False) or vals["name"] == "New":
            vals["name"] = self.env["ir.sequence"].next_by_code("vit.penerima_beasiswa") or "Error Number!!!"
        return super(penerima_beasiswa, self).create(vals)

    def action_confirm(self):
        self.state = STATES[1][0]

    def action_pass(self):
        self.state = STATES[2][0]

    def action_done(self):
        self.state = STATES[3][0]

    def action_reject(self):
        self.state = STATES[4][0]

    def action_draft(self):
        self.state = STATES[0][0]

    @api.multi
    def unlink(self):
        for me_id in self :
            if me_id.state != STATES[0][0]:
                raise UserError("Cannot delete non draft record!")
        return super(penerima_beasiswa, self).unlink()
