#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft','Draft'),('open','Confirm'),('done','Done')]
from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class laporan_statistik_pegawai(models.Model):
    _name = "vit.laporan_statistik_pegawai"
    _inherit = "vit.laporan_statistik_pegawai"

    @api.model
    def create(self, vals):
        if not vals.get("name", False) or vals["name"] == "New":
            vals["name"] = self.env["ir.sequence"].next_by_code("vit.laporan_statistik_pegawai") or "Error Number!!!"
        return super(laporan_statistik_pegawai, self).create(vals)

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
        return super(laporan_statistik_pegawai, self).unlink()

    def action_reload(self, ):
        sql = "delete from vit_lap_statistik_detail where statistik_id = %s"
        self.env.cr.execute(sql, (self.id,))
        sql = """
                insert into vit_lap_statistik_detail (name, nip, golongan, jabatan, statistik_id)
                select emp.name, emp.nip, gol.name, jab.name, %s
                from hr_employee emp
                left join vit_golongan gol on emp.golongan_id = gol.id
                left join vit_jabatan jab on emp.jabatan_id = jab.id
                where 1=1
                """
        if self.matra_id:
            sql += ' and emp.matra_id = %s ' %self.matra_id.id
        if self.fakultas_id:
            sql += ' and emp.fakultas_id = %s ' %self.fakultas_id.id
        if self.golongan_id:
            sql += ' and emp.golongan_id = %s ' %self.golongan_id.id
            
        self.env.cr.execute(sql, (self.id,))

