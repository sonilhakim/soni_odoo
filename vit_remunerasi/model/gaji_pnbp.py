#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft','Rancangan'),('open','Proses'),('done','Valid')]
from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class gaji_pnbp(models.Model):

    _name = "vit.gaji_pnbp"
    _description = "vit.gaji_pnbp"
    name = fields.Char( required=True, default="New", readonly=True,  string="Name",  help="")
    description = fields.Char( string="Description",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    state = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",  help="")


    gaji_pnbp_ids = fields.One2many(comodel_name="vit.gaji_pnbp_detail",  inverse_name="gaji_id",  string="Gaji pnbp",  readonly=True, states={"draft" : [("readonly",False)]},  help="")

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
        return super(gaji_pnbp, self).unlink()

    @api.multi
    def action_reload(self, ):
        sql = "delete from vit_gaji_pnbp_detail where gaji_id = %s"
        self.env.cr.execute(sql, (self.id,))
        sql = """
                insert into vit_gaji_pnbp_detail (karyawan_id, gaji_id)
                select id, %s
                from hr_employee
                """
        self.env.cr.execute(sql, (self.id,))
