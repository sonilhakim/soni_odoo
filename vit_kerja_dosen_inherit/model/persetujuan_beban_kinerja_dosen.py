#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft','Rancangan'),('open','Proses'),('done','Valid'),('reject','Ditolak')]
from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class persetujuan_beban_kinerja_dosen(models.Model):
    _name = "vit.persetujuan_beban_kinerja_dosen"
    _inherit = "vit.persetujuan_beban_kinerja_dosen"

    state = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",  help="")
    employee_id = fields.Many2one(comodel_name="hr.employee",  string="Dosen",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    beban_kinerja = fields.Many2one( comodel_name="vit.bkd", string="Beban kinerja",  readonly=True, states={"draft" : [("readonly",False)]},  help="")

    @api.model
    def create(self, vals):
        if not vals.get("name", False) or vals["name"] == "New":
            vals["name"] = self.env["ir.sequence"].next_by_code("vit.persetujuan_beban_kinerja_dosen") or "Error Number!!!"
        return super(persetujuan_beban_kinerja_dosen, self).create(vals)

    def action_confirm(self):
        self.state = STATES[1][0]

    def action_done(self):
        self.state = STATES[2][0]

    def action_reject(self):
        self.state = STATES[3][0]

    def action_draft(self):
        self.state = STATES[0][0]

    @api.multi
    def unlink(self):
        for me_id in self :
            if me_id.state != STATES[0][0]:
                raise UserError("Cannot delete non draft record!")
        return super(persetujuan_beban_kinerja_dosen, self).unlink()
