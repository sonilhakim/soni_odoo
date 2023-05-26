#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft', 'Draft'),('open','Confirm'),('done','Done')]
from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class laporan_daftar_pegawai_status(models.Model):

    _name = "vit.laporan_daftar_pegawai_status"
    _description = "vit.laporan_daftar_pegawai_status"
    name = fields.Char( required=True, default="New", readonly=True,  string="Name",  help="")
    state = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",  help="")

    status_id = fields.Many2one(comodel_name="hr.employee.category",  string="Status",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    lap_status_detail_ids = fields.One2many(comodel_name="vit.laporan_status_detail",  inverse_name="lap_daftar_pegawai_status_id",  string="Lap status detail",  readonly=True, states={"draft" : [("readonly",False)]},  help="")

    @api.model
    def create(self, vals):
        if not vals.get("name", False) or vals["name"] == "New":
            vals["name"] = self.env["ir.sequence"].next_by_code("vit.laporan_daftar_pegawai_status") or "Error Number!!!"
        return super(laporan_daftar_pegawai_status, self).create(vals)

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
        return super(laporan_daftar_pegawai_status, self).unlink()

    def action_reload(self, ):
        sql = "delete from vit_laporan_status_detail where lap_daftar_pegawai_status_id = %s"
        self.env.cr.execute(sql, (self.id,))
        sql = """
                insert into vit_laporan_status_detail (name, nip, golongan, jabatan, lap_daftar_pegawai_status_id)
                select emp.name, emp.nip, gol.name, jab.name, %s
                from hr_employee emp
                left join vit_golongan gol on emp.golongan_id = gol.id
                left join vit_jabatan jab on emp.jabatan_id = jab.id
                where 1=1
                """
        if self.status_id:
            sql += ' and emp.status_pegawai = %s ' %self.status_id.id
            
        self.env.cr.execute(sql, (self.id,))

class laporan_status_detail(models.Model):

    _name = "vit.laporan_status_detail"
    _description = "vit.laporan_status_detail"
    name = fields.Char( required=True, string="Name",  help="")
    nip = fields.Char( string="Nip",  help="")
    golongan = fields.Char( string="Golongan",  help="")
    jabatan = fields.Char( string="Jabatan",  help="")


    lap_daftar_pegawai_status_id = fields.Many2one(comodel_name="vit.laporan_daftar_pegawai_status",  string="Lap daftar pegawai status",  help="")

