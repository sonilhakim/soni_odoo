#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft','Draft'),('open','Confirm'),('done','Done')]
from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class penerimaan_penghargaan(models.Model):
    _name = "vit.penerimaan_penghargaan"
    _inherit = "vit.penerimaan_penghargaan"

    @api.model
    def create(self, vals):
        if not vals.get("name", False) or vals["name"] == "New":
            vals["name"] = self.env["ir.sequence"].next_by_code("vit.penerimaan_penghargaan") or "Error Number!!!"
        return super(penerimaan_penghargaan, self).create(vals)

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
        return super(penerimaan_penghargaan, self).unlink()

    def action_reload(self, ):
        sql = "delete from vit_detail_penerimaan_penghargaan where penerimaan_penghargaan_id = %s"
        self.env.cr.execute(sql, (self.id,))
        sql = """
                insert into vit_detail_penerimaan_penghargaan (name, nip, penerimaan_penghargaan_id)
                select emp.name, emp.nip, %s
                from hr_employee emp
                where 1=1
                """
        if self.matra_id:
            sql += ' and emp.matra_id = %s ' %self.matra_id.id
        if self.fakultas_id:
            sql += ' and emp.fakultas_id = %s ' %self.fakultas_id.id
            
        self.env.cr.execute(sql, (self.id,))

