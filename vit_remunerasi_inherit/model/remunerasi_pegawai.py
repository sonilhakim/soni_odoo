#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft','Rancangan'),('open','Proses'),('done','Valid')]
from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class remunerasi_pegawai(models.Model):
    _name = "vit.remunerasi_pegawai"
    _inherit = "vit.remunerasi_pegawai"

    matra_id = fields.Many2one(comodel_name="vit.matra",  string="Matra",  help="")
    date_from = fields.Date(string='Date From')
    date_to = fields.Date(string='Date To')

    @api.model
    def create(self, vals):
        if not vals.get("name", False) or vals["name"] == "New":
            vals["name"] = self.env["ir.sequence"].next_by_code("vit.remunerasi_pegawai") or "Error Number!!!"
        return super(remunerasi_pegawai, self).create(vals)

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
        res = super(remunerasi_pegawai, self).action_reload()
        sql = "delete from vit_remunerasi_pegawai_ids where remunerasi_id = %s"
        self.env.cr.execute(sql, (self.id,))
        sql = """
                insert into vit_remunerasi_pegawai_ids (karyawan_id, golongan_id, pangkat_id, wage, remunerasi_id)
                select emp.id, emp.golongan_id, emp.pangkat_id, psl.total, %s
                from hr_employee emp
                left join hr_payslip ps on emp.id = ps.employee_id
                left join hr_payslip_line psl on ps.id = psl.slip_id
                left join hr_salary_rule_category src on psl.category_id = src.id
                where emp.matra_id = %s and ps.date_from = %s and ps.date_to = %s and src.code = 'NET'
                """
        self.env.cr.execute(sql, (self.id,self.matra_id.id,self.date_from,self.date_to))
        return res
