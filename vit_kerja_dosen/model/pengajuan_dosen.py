#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft','Draft'),('open','Confirm'),('done','Done')]
from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class pengajuan_dosen(models.Model):

    _name = "vit.pengajuan_dosen"
    _description = "vit.pengajuan_dosen"
    name = fields.Char( required=True, default="New", readonly=True,  string="Name",  help="")
    state = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",  help="")
    nama_dosen = fields.Char( string="Nama dosen",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    nip = fields.Char( string="Nip",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    jabatan = fields.Char( string="Jabatan",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    golongan = fields.Char( string="Golongan",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    fakultas = fields.Char( string="Fakultas",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    jurusan = fields.Char( string="Jurusan",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    bidang_studi = fields.Char( string="Bidang studi",  readonly=True, states={"draft" : [("readonly",False)]},  help="")


    employee_id = fields.Many2one(comodel_name="hr.employee",  string="Employee",  readonly=True, states={"draft" : [("readonly",False)]},  help="")

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
        return super(pengajuan_dosen, self).unlink()
