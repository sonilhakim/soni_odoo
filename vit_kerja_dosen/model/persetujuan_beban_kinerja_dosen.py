#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft','Draft'),('open','Confirm'),('done','Done')]
from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class persetujuan_beban_kinerja_dosen(models.Model):

    _name = "vit.persetujuan_beban_kinerja_dosen"
    _description = "vit.persetujuan_beban_kinerja_dosen"
    name = fields.Char( required=True, default="New", readonly=True,  string="Name",  help="")
    state = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",  help="")
    beban_kinerja = fields.Char( string="Beban kinerja",  readonly=True, states={"draft" : [("readonly",False)]},  help="")


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
        return super(persetujuan_beban_kinerja_dosen, self).unlink()
