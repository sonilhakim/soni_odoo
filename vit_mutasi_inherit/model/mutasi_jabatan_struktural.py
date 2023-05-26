#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft','Draft'),('open','Confirm'),('done','Done'),('reject','Ditolak')]
from odoo import models, fields, api, _
import time
import datetime
from odoo.exceptions import UserError, Warning

class mutasi_jabatan_struktural(models.Model):

    _name = "vit.mutasi_jabatan_struktural"
    _description = "vit.mutasi_jabatan"
    name = fields.Char( required=True, default="New", readonly=True,  string="Name",  help="")
    state = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",  help="")


    matra_id = fields.Many2one(comodel_name="vit.matra",  string="Matra",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    fakultas_id = fields.Many2one(comodel_name="vit.fakultas",  string="SUBSATKER",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    mutasi_jabatan_struktural_ids = fields.One2many(comodel_name="vit.mutasi_jabatan_struktural_detail",  inverse_name="mutasi_jabatan_struktural_id",  string="Mutasi jabatan", help="")

    date = fields.Date( string="Tanggal Mutasi",  readonly=True, states={"draft" : [("readonly",False)]}, default=lambda self:time.strftime("%Y-%m-%d"), help="")

    @api.model
    def create(self, vals):
        if not vals.get("name", False) or vals["name"] == "New":
            vals["name"] = self.env["ir.sequence"].next_by_code("vit.mutasi_jabatan_struktural") or "Error Number!!!"
        return super(mutasi_jabatan_struktural, self).create(vals)

    @api.multi
    def action_confirm(self):
        self.state = STATES[1][0]

    @api.multi
    def action_done(self):
        # import pdb; pdb.set_trace()
        for d in self.mutasi_jabatan_struktural_ids:
            self.env.cr.execute("update hr_employee set jabatan_id=%s where id = %s",( d.jabatan_tujuan.id, d.employee_id.id ))
        self.state = STATES[2][0]

    def action_reject(self):
        self.state = STATES[3][0]

    @api.multi
    def action_draft(self):
        self.state = STATES[0][0]

    @api.multi
    def unlink(self):
        for me_id in self :
            if me_id.state != STATES[0][0]:
                raise UserError("Cannot delete non draft record!")
        return super(mutasi_jabatan_struktural, self).unlink()