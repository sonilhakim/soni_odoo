#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft','Rancangan'),('open','Proses'),('done','Valid'),('reject','Ditolak')]
from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class pengajuan_dosen(models.Model):
    _name = "vit.pengajuan_dosen"
    _inherit = "vit.pengajuan_dosen"

    employee_id = fields.Many2one(comodel_name="hr.employee",  string="Nama dosen",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    nip = fields.Char( string="Nip", related="employee_id.nip", readonly=True, states={"draft" : [("readonly",True)]},  help="")
    jabatan = fields.Many2one(comodel_name="vit.jabatan", related="employee_id.jabatanf_id", string="Jabatan",  readonly=True, states={"draft" : [("readonly",True)]},  help="")
    golongan = fields.Many2one(comodel_name="vit.golongan", related="employee_id.golongan_id", string="Golongan",  readonly=True, states={"draft" : [("readonly",True)]},  help="")
    fakultas = fields.Many2one(comodel_name="vit.fakultas", related="employee_id.fakultas_id", string="Fakultas",  readonly=True, states={"draft" : [("readonly",True)]},  help="")
    jurusan = fields.Many2one(comodel_name="vit.jurusan", related="employee_id.jurusan_id", string="Jurusan",  readonly=True, states={"draft" : [("readonly",True)]},  help="")
    program_studi = fields.Many2one(comodel_name="vit.program_studi", related="employee_id.program_studi_id", string="Program studi", readonly=True, states={"draft" : [("readonly",True)]}, help="")
    status_dosen = fields.Many2one(comodel_name="vit.status_dosen",  string="Status dosen", readonly=True, states={"draft" : [("readonly",False)]}, help="")

    state = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",  help="")
    
    @api.model
    def create(self, vals):
        if not vals.get("name", False) or vals["name"] == "New":
            vals["name"] = self.env["ir.sequence"].next_by_code("vit.pengajuan_dosen") or "Error Number!!!"
        return super(pengajuan_dosen, self).create(vals)

    def action_confirm(self):
        self.state = STATES[1][0]

    def action_done(self):
        if self.status_dosen:
            self.env.cr.execute("""update hr_employee
                                 set is_dosen=%s, status_dosen_id=%s, bidang_ilmu=%s 
                                 where id = %s""",
                                 ( True, self.status_dosen.id, self.bidang_studi, self.employee_id.id ))
        self.state = STATES[2][0]

    def action_reject(self):
        self.state = STATES[3][0]

    def action_draft(self):
        self.state = STATES[0][0]

    @api.multi
    def unlink(self):
        for me_id in self :
            if me_id.state != STATES[0][0]:
                raise UserError("Cannot delete non draft record!")
        return super(pengajuan_dosen, self).unlink()
