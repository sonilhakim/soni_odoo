#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft','Draft'),('open','Confirm'),('done','Done')]
from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class lap_nominatif(models.Model):
    _name = "vit.lap_nominatif"
    _inherit = "vit.lap_nominatif"

    @api.model
    def create(self, vals):
        if not vals.get("name", False) or vals["name"] == "New":
            vals["name"] = self.env["ir.sequence"].next_by_code("vit.lap_nominatif") or "Error Number!!!"
        return super(lap_nominatif, self).create(vals)

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
        return super(lap_nominatif, self).unlink()

    def action_reload(self, ):
        sql = "delete from vit_nom_detail where nominatif_id = %s"
        self.env.cr.execute(sql, (self.id,))
        sql = """
                insert into vit_nom_detail (name, nip, pangkat_gol_ruang, jabatan, tmt_jabatan, nominatif_id)
                select emp.name, emp.nip, emp.pangkat_gol_ruang, jab.name, emp.tmt_jabatan, %s
                from hr_employee emp
                left join vit_jabatan jab on emp.jabatan_id = jab.id
                where 1=1
                """
        if self.matra_id:
            sql += ' and emp.matra_id = %s ' %self.matra_id.id
        if self.fakultas:
            sql += ' and emp.fakultas_id = %s ' %self.fakultas.id
            
        self.env.cr.execute(sql, (self.id,))

