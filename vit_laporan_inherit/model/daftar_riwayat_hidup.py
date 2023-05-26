#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft','Draft'),('open','Confirm'),('done','Done')]
from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class daftar_riwayat_hidup(models.Model):
    _name = "vit.daftar_riwayat_hidup"
    _inherit = "vit.daftar_riwayat_hidup"

    @api.model
    def create(self, vals):
        if not vals.get("name", False) or vals["name"] == "New":
            vals["name"] = self.env["ir.sequence"].next_by_code("vit.daftar_riwayat_hidup") or "Error Number!!!"
        return super(daftar_riwayat_hidup, self).create(vals)

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
        return super(daftar_riwayat_hidup, self).unlink()

    def action_reload(self, ):
        sql = "delete from vit_daftar_detail where riwayat_hidup_id = %s"
        self.env.cr.execute(sql, (self.id,))
        sql = """
                insert into vit_daftar_detail (name, nip, tgl_lahir, tmp_lahir, riwayat_hidup_id)
                select emp.name, emp.nip, emp.birthday, emp.place_of_birth, %s
                from hr_employee emp
                where 1=1
                """
        if self.jabatn_id:
            sql += ' and emp.jabatan_id = %s ' %self.jabatn_id.id
        if self.matra_id:
            sql += ' and emp.matra_id = %s ' %self.matra_id.id
        if self.fakultas_id:
            sql += ' and emp.fakultas_id = %s ' %self.fakultas_id.id
        if self.golongan_id:
            sql += ' and emp.golongan_id = %s ' %self.golongan_id.id
            
        self.env.cr.execute(sql, (self.id,))

