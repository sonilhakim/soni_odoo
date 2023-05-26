#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft','Rancangan'),('open','Proses'),('done','Valid'),('reject','Ditolak')]
from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class usulan_sertifikasi(models.Model):
    _name = "vit.usulan_sertifikasi"
    _inherit = "vit.usulan_sertifikasi"

    employee_id = fields.Many2one(comodel_name="hr.employee",  string="Dosen",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    no_sertifikasi = fields.Char(string="No. Sertifikasi",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    state = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",  help="")

    @api.model
    def create(self, vals):
        if not vals.get("name", False) or vals["name"] == "New":
            vals["name"] = self.env["ir.sequence"].next_by_code("vit.usulan_sertifikasi") or "Error Number!!!"
        return super(usulan_sertifikasi, self).create(vals)

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
        return super(usulan_sertifikasi, self).unlink()
