#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft','Rancangan'),('open','Proses'),('done','Valid')]
from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class capaian_kinerja_unit_kerja(models.Model):
    _name = "vit.capaian_kinerja_unit_kerja"
    _inherit = "vit.capaian_kinerja_unit_kerja"

    @api.model
    def create(self, vals):
        if not vals.get("name", False) or vals["name"] == "New":
            vals["name"] = self.env["ir.sequence"].next_by_code("vit.capaian_kinerja_unit_kerja") or "Error Number!!!"
        return super(capaian_kinerja_unit_kerja, self).create(vals)

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
        return super(capaian_kinerja_unit_kerja, self).unlink()
