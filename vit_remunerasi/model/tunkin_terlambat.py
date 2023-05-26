#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft','Rancangan'),('open','Proses'),('done','Valid')]
from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class tunkin_terlambat(models.Model):

    _name = "vit.tunkin_terlambat"
    _description = "vit.tunkin_terlambat"
    name = fields.Char( required=True, default="New", readonly=True,  string="Name",  help="")
    description = fields.Char( string="Description",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    state = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",  help="")


    tunkin_terlambat_ids = fields.One2many(comodel_name="vit.tunkin_terlambat_detail",  inverse_name="tunkin_terlambat_id",  string="Tunkin terlambat",  readonly=True, states={"draft" : [("readonly",False)]},  help="")

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
        return super(tunkin_terlambat, self).unlink()

    @api.multi
    def action_reload(self, ):
        sql = "delete from vit_tunkin_terlambat_detail where tunkin_terlambat_id = %s"
        self.env.cr.execute(sql, (self.id,))
        sql = """
                insert into vit_tunkin_terlambat_detail (karyawan_id, tunkin_terlambat_id)
                select id, %s
                from hr_employee
                """
        self.env.cr.execute(sql, (self.id,))
