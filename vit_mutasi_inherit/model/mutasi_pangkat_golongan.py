#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft','Draft'),('open','Confirm'),('done','Done'),('reject','Ditolak')]
from odoo import models, fields, api, _
import time
import datetime
from odoo.exceptions import UserError, Warning

class mutasi_pangkat_golongan(models.Model):
    _name = "vit.mutasi_pangkat_golongan"
    _inherit = "vit.mutasi_pangkat_golongan"

    date = fields.Date( string="Tanggal Mutasi",  readonly=True, states={"draft" : [("readonly",False)]}, default=lambda self:time.strftime("%Y-%m-%d"), help="")
    state = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",  help="")

    @api.model
    def create(self, vals):
        if not vals.get("name", False) or vals["name"] == "New":
            vals["name"] = self.env["ir.sequence"].next_by_code("vit.mutasi_pangkat_golongan") or "Error Number!!!"
        return super(mutasi_pangkat_golongan, self).create(vals)

    def action_confirm(self):
        self.state = STATES[1][0]

    def action_done(self):
        for d in self.mutasi_pang_gol_ids:
            self.env.cr.execute("update hr_employee set pangkat_id=%s, golongan_id=%s where id = %s",( d.pangkat_tujuan.id, d.golongan_tujuan.id, d.employee_id.id ))

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
        return super(mutasi_pangkat_golongan, self).unlink()
