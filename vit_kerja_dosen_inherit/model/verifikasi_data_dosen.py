#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft','Rancangan'),('open','Proses'),('done','Valid'),('reject','Ditolak')]
from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class verifikasi_data_dosen(models.Model):
    _name = "vit.verifikasi_data_dosen"
    _inherit = "vit.verifikasi_data_dosen"

    employee_id = fields.Many2one(comodel_name="hr.employee",  string="Karyawan",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    nip = fields.Char( string="Nip", related="employee_id.nip", readonly=True, states={"draft" : [("readonly",True)]},  help="")
    jabatan = fields.Many2one(comodel_name="vit.jabatan", related="employee_id.jabatanf_id", string="Jabatan",  readonly=True,  help="")
    golongan = fields.Many2one(comodel_name="vit.golongan", related="employee_id.golongan_id", string="Golongan",  readonly=True,   help="")
    fakultas = fields.Many2one(comodel_name="vit.fakultas", related="employee_id.fakultas_id", string="Fakultas",  readonly=True,   help="")
    jurusan = fields.Many2one(comodel_name="vit.jurusan", related="employee_id.jurusan_id", string="Jurusan",  readonly=True,   help="")
    program_studi = fields.Many2one(comodel_name="vit.program_studi", related="employee_id.program_studi_id", string="Program studi",  help="")
    status_dosen = fields.Many2one(comodel_name="vit.status_dosen", related="employee_id.status_dosen_id", string="Status dosen", readonly=True,  help="")
    bidang_studi = fields.Char( string="Bidang studi", related="employee_id.bidang_ilmu", readonly=True,   help="")

    state = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",  help="")

    @api.model
    def create(self, vals):
        if not vals.get("name", False) or vals["name"] == "New":
            vals["name"] = self.env["ir.sequence"].next_by_code("vit.verifikasi_data_dosen") or "Error Number!!!"
        return super(verifikasi_data_dosen, self).create(vals)

    def action_confirm(self):
        self.state = STATES[1][0]

    def action_done(self):
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
        return super(verifikasi_data_dosen, self).unlink()
