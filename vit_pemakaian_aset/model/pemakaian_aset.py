#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft','Draft'),('open','Confirm'),('done','Done')]
from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class pemakaian_aset(models.Model):

    _name = "vit.pemakaian_aset"
    _description = "vit.pemakaian_aset"
    name = fields.Char( required=True, default="New", readonly=True,  string="Name",  help="")
    date = fields.Date( string="Date",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    state = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",  help="")


    penanggung_jawab_id = fields.Many2one(comodel_name="hr.employee",  string="Penanggung jawab",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    unit_kerja_id = fields.Many2one(comodel_name="vit.unit_kerja",  string="Unit kerja",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    jurusan_id = fields.Many2one(comodel_name="vit.jurusan",  string="Jurusan",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    fakultas_id = fields.Many2one(comodel_name="vit.fakultas",  string="Fakultas",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    aset_ids = fields.One2many(comodel_name="vit.aset_pemakaian",  inverse_name="pemakaian_id",  string="Aset",  readonly=True, states={"draft" : [("readonly",False)]},  help="")

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
        return super(pemakaian_aset, self).unlink()
