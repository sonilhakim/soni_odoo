#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft','Draft'),('open','Proses'),('done','Selesai')]
from odoo import models, fields, api, _
import time
from odoo.exceptions import UserError, Warning

class pernyataan_asesor(models.Model):
    _name = "vit.pernyataan_asesor"
    _inherit = "vit.pernyataan_asesor"

    date = fields.Date( string="Tanggal",  readonly=True, default=lambda self: time.strftime("%Y-%m-%d"), states={"draft" : [("readonly",False)]},  help="")
    pernyataan = fields.Text('Pernyataan', readonly=True, states={"draft" : [("readonly",False)]} )

    @api.model
    def create(self, vals):
        if not vals.get("name", False) or vals["name"] == "New":
            vals["name"] = self.env["ir.sequence"].next_by_code("vit.pernyataan_asesor") or "Error Number!!!"
        return super(pernyataan_asesor, self).create(vals)

    def action_confirm(self):
        self.state = STATES[1][0]

    def action_done(self):
        if self.bkd_id:
            self.env.cr.execute("update vit_bkd set state=%s where id = %s",
                        ( 'done', self.bkd_id.id,))
        self.state = STATES[2][0]

    def action_draft(self):
        self.state = STATES[0][0]

    @api.multi
    def unlink(self):
        for me_id in self :
            if me_id.state != STATES[0][0]:
                raise UserError("Cannot delete non draft record!")
        return super(pernyataan_asesor, self).unlink()
