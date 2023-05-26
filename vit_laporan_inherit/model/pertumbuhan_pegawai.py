#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft','Draft'),('open','Confirm'),('done','Done')]
from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class pertumbuhan_pegawai(models.Model):

    _name = "vit.pertumbuhan_pegawai"
    _description = "vit.pertumbuhan_pegawai"
    name = fields.Char( required=True, default="New", readonly=True,  string="Name",  help="")
    state = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",  help="")

    matra_id = fields.Many2one(comodel_name="vit.matra",  string="Matra",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    fakultas_id = fields.Many2one(comodel_name="vit.fakultas",  string="Fakultas",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    detail_pertumbuhan_ids = fields.One2many(comodel_name="vit.detail_pertumbuhan_pegawai",  inverse_name="pertumbuhan_pegawai_id",  string="Detail Pertumbuhan",  readonly=True, states={"draft" : [("readonly",False)]},  help="")

    @api.model
    def create(self, vals):
        if not vals.get("name", False) or vals["name"] == "New":
            vals["name"] = self.env["ir.sequence"].next_by_code("vit.pertumbuhan_pegawai") or "Error Number!!!"
        return super(pertumbuhan_pegawai, self).create(vals)

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
        return super(pertumbuhan_pegawai, self).unlink()

    def action_reload(self, ):
        sql = "delete from vit_detail_pertumbuhan_pegawai where pertumbuhan_pegawai_id = %s"
        self.env.cr.execute(sql, (self.id,))
        sql = """
                insert into vit_detail_pertumbuhan_pegawai (name, nip, pertumbuhan_pegawai_id)
                select emp.name, emp.nip, %s
                from hr_employee emp
                where 1=1
                """
        if self.matra_id:
            sql += ' and emp.matra_id = %s ' %self.matra_id.id
        if self.fakultas_id:
            sql += ' and emp.fakultas_id = %s ' %self.fakultas_id.id
            
        self.env.cr.execute(sql, (self.id,))

class detail_pertumbuhan_pegawai(models.Model):

    _name = "vit.detail_pertumbuhan_pegawai"
    _description = "vit.detail_pertumbuhan_pegawai"
    name = fields.Char( required=True, string="Name",  help="")
    nip = fields.Char( string="Nip",  help="")
    nilai_asal = fields.Float( string="Pertumbuhan Tahun Lalu (%)",  help="")
    nilai_ini = fields.Float( string="Pertumbuhan Tahun Ini (%)",  help="")


    pertumbuhan_pegawai_id = fields.Many2one(comodel_name="vit.pertumbuhan_pegawai",  string="Pertumbuhan Pegawai",  help="")

