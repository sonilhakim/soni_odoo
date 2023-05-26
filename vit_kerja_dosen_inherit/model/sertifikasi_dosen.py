#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft','Rancangan'),('open','Konfirmasi'),('done','Valid')]
from odoo import models, fields, api, _
import time
from odoo.exceptions import UserError, Warning

class SertifikasiDosen(models.Model):
    _name = "vit.sertifikasi_dosen"
    _description = "vit.sertifikasi_dosen"

    name = fields.Char(string="No. Sertifikasi", required=True,  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    employee_id = fields.Many2one(comodel_name="hr.employee",  string="Dosen",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    date = fields.Date( string="Tanggal Disahkan",  readonly=True, default=lambda self: time.strftime("%Y-%m-%d"), states={"draft" : [("readonly",False)]},  help="")
    state = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",  help="")

    # @api.model
    # def create(self, vals):
    #     if not vals.get("name", False) or vals["name"] == "New":
    #         vals["name"] = self.env["ir.sequence"].next_by_code("vit.sertifikasi_dosen") or "Error Number!!!"
    #     return super(SertifikasiDosen, self).create(vals)

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
        return super(usulan_sertifikasi, self).unlink()
