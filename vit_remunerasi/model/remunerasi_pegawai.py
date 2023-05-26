#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft','Rancangan'),('open','Proses'),('done','Valid')]
from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class remunerasi_pegawai(models.Model):

    _name = "vit.remunerasi_pegawai"
    _description = "vit.remunerasi_pegawai"
    name = fields.Char( required=True, default="New", readonly=True,  string="Name",  help="")
    description = fields.Char( string="Description",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    state = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",  help="")


    remunerasi_ids = fields.One2many(comodel_name="vit.remunerasi_pegawai_ids",  inverse_name="remunerasi_id",  string="Remunerasi",  readonly=True, states={"draft" : [("readonly",False)]},  help="")

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
        return super(remunerasi_pegawai, self).unlink()

    @api.multi
    def action_reload(self, ):
        sql = "delete from vit_remunerasi_pegawai_ids where remunerasi_id = %s"
        self.env.cr.execute(sql, (self.id,))
        sql = """
                insert into vit_remunerasi_pegawai_ids (karyawan_id, remunerasi_id)
                select id, %s
                from hr_employee
                """
        self.env.cr.execute(sql, (self.id,))
