#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft','Draft'),('open','Confirmed'),('done','Done'),('cancel','Cancel')]
from odoo import models, fields, api, _
import time
from datetime import datetime
from odoo.exceptions import UserError, Warning

class data_buruh(models.Model):

    _name = "vit.data_buruh"
    _description = "vit.data_buruh"
    _inherit = ['mail.thread']

    name = fields.Char( required=True, default="New", readonly=True,  string="Name",  help="", )
    tanggal = fields.Date( string="Tanggal", required=True, default=lambda self:time.strftime("%Y-%m-%d"), readonly=True, states={"draft" : [("readonly",False)]},  help="", )
    state = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",  help="", )
    note = fields.Text( string="Keterangan",  readonly=True, states={"draft" : [("readonly",False)]},  help="", )

    _sql_constraints = [
        ('tgl_uniq', 'unique (tanggal)', 'Data Buruh tanggal ini sudah ada di dokumen lain!')
    ]

    @api.model
    def create(self, vals):
        if not vals.get("name", False) or vals["name"] == "New":
            tanggal = datetime.strptime(vals["tanggal"], '%Y-%m-%d')
            # vals["name"] = self.env["ir.sequence"].next_by_code("vit.data_buruh") or "Error Number!!!"
            vals["name"] = "DB" + "/" + tanggal.strftime('%d-%m-%Y') or "Error Number!!!"
        return super(data_buruh, self).create(vals)

    def action_confirm(self):
        self.state = STATES[1][0]

    def action_done(self):
        self.state = STATES[2][0]

    def action_cancel(self):
        sqld = "delete from vit_daftar_buruh where data_buruh_id = %s"
        self.env.cr.execute(sqld, (self.id,))
        self.state = STATES[3][0]

    def action_draft(self):
        self.state = STATES[0][0]

    @api.multi
    def unlink(self):
        for me_id in self :
            if me_id.state != STATES[0][0]:
                raise UserError("Cannot delete non draft record!")
        return super(data_buruh, self).unlink()

    daftar_ids = fields.One2many(comodel_name="vit.daftar_buruh",  inverse_name="data_buruh_id",  string="Daftar",  readonly=True, states={"draft" : [("readonly",False)],"open" : [("readonly",False)]},  help="", )
    user_id = fields.Many2one(comodel_name="res.users", string="User", required=True, default=lambda self: self.env.uid, readonly=True, states={"draft" : [("readonly",False)]},  help="", )
