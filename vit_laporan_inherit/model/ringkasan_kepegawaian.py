#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft', 'Draft'),('open','Confirm'),('done','Done')]
from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class ringkasan_kepegawaian(models.Model):

    _name = "vit.ringkasan_kepegawaian"
    _description = "vit.ringkasan_kepegawaian"
    name = fields.Char( required=True, default="New", readonly=True,  string="Name",  help="")
    state = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",  help="")

    fakultas_id = fields.Many2one(comodel_name="vit.fakultas",  string="Fakultas",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    matra_id = fields.Many2one(comodel_name="vit.matra",  string="Matra",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    golongan_id = fields.Many2one(comodel_name="vit.golongan",  string="Golongan",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    jabatan_id = fields.Many2one(comodel_name="vit.jabatan",  string="Jabatan",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    ringkasan_detail_ids = fields.One2many(comodel_name="vit.ringkasan_detail",  inverse_name="ringkasan_pegawai_id",  string="Ringkasan detail",  readonly=True, states={"draft" : [("readonly",False)]},  help="")

    @api.model
    def create(self, vals):
        if not vals.get("name", False) or vals["name"] == "New":
            vals["name"] = self.env["ir.sequence"].next_by_code("vit.ringkasan_kepegawaian") or "Error Number!!!"
        return super(ringkasan_kepegawaian, self).create(vals)

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
        return super(ringkasan_kepegawaian, self).unlink()

    def action_reload(self, ):
        sql = "delete from vit_ringkasan_detail where ringkasan_pegawai_id = %s"
        self.env.cr.execute(sql, (self.id,))
        sql = """
                insert into vit_ringkasan_detail (name, nip, status_pegawai, country_id, pendidikan, gaji, ringkasan_pegawai_id)
                select emp.name, emp.nip, st.name, co.name, str.name, kon.wage, %s
                from hr_employee emp
                left join hr_employee_category st on emp.status_pegawai = st.id
                left join res_country co on emp.country_id = co.id
                left join vit_strata str on emp.pendidikan_terakhir = str.id
                left join hr_contract kon on kon.employee_id = emp.id
                where 1=1
                """
        if self.jabatan_id:
            sql += ' and emp.jabatan_id = %s ' %self.jabatan_id.id
        if self.matra_id:
            sql += ' and emp.matra_id = %s ' %self.matra_id.id
        if self.fakultas_id:
            sql += ' and emp.fakultas_id = %s ' %self.fakultas_id.id
        if self.golongan_id:
            sql += ' and emp.golongan_id = %s ' %self.golongan_id.id
            
        self.env.cr.execute(sql, (self.id,))

class ringkasan_detail(models.Model):

    _name = "vit.ringkasan_detail"
    _description = "vit.ringkasan_detail"
    name = fields.Char( required=True, string="Name",  help="")
    nip = fields.Char( string="Nip",  help="")
    gaji = fields.Monetary("Gaji Pokok")
    status_pegawai = fields.Char( string="Status Pegawai",  help="")
    country_id = fields.Char( string="Kebangsaan",  help="")
    pendidikan = fields.Char( string="Pendidikan Terakhir",  help="")

    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id)
    currency_id = fields.Many2one(string="Currency", related='company_id.currency_id', readonly=True)
    ringkasan_pegawai_id = fields.Many2one(comodel_name="vit.ringkasan_kepegawaian",  string="Ringkasan Kepegawaian",  help="")

