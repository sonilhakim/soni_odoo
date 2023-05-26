#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft','Draft'),('open','Confirm'),('done','Done')]
from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class kenaikan_pangkat(models.Model):
    _name = "vit.kenaikan_pangkat"
    _inherit = "vit.kenaikan_pangkat"

    @api.model
    def create(self, vals):
        if not vals.get("name", False) or vals["name"] == "New":
            vals["name"] = self.env["ir.sequence"].next_by_code("vit.kenaikan_pangkat") or "Error Number!!!"
        return super(kenaikan_pangkat, self).create(vals)

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
        return super(kenaikan_pangkat, self).unlink()

    def action_reload(self, ):
        sql = "delete from vit_details_naik_pangkat where kenaikan_pangkat_id = %s"
        self.env.cr.execute(sql, (self.id,))
        sql = """
                insert into vit_details_naik_pangkat (name, nip, pangkat_awal, kenaikan_pangkat_id)
                select emp.name, emp.nip, pkt.name, %s
                from hr_employee emp
                left join vit_pangkat pkt on emp.pangkat_id = pkt.id
                where 1=1
                """
        if self.matra_id:
            sql += ' and emp.matra_id = %s ' %self.matra_id.id
            
        self.env.cr.execute(sql, (self.id,))

