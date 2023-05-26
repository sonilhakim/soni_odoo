#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft','Draft'),('open','Confirm'),('done','Done')]
from odoo import models, fields, api, _
import time
from odoo.exceptions import UserError, Warning

class kenaikan_gaji_berkala(models.Model):

    _name = "vit.kenaikan_gaji_berkala"
    _description = "vit.kenaikan_gaji_berkala"
    _rec_name   = "employee_id"

    name = fields.Char( required=False, default="New", readonly=True,  string="Name",  help="")
    state = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",  help="")


    employee_id = fields.Many2one(comodel_name="hr.employee",  string="Employee",  help="")
    gaji_detail_ids = fields.One2many(comodel_name="vit.kenaikan_gaji_detail",  inverse_name="naik_gaji_id",  string="Naik gaji detail",  readonly=True, states={"draft" : [("readonly",False)]},  help="")

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
        return super(kenaikan_gaji_berkala, self).unlink()


class kenaikan_gaji_detail(models.Model):

    _name = "vit.kenaikan_gaji_detail"
    _description = "vit.kenaikan_gaji_detail"
    name = fields.Char( required=False, string="Name",  help="")
    date = fields.Date( string="Tanggal",  help="")
    gaji_awal = fields.Float( string="Gaji awal",  help="")
    gaji_sekarang = fields.Float( string="Gaji sekarang",  help="")


    naik_gaji_id = fields.Many2one(comodel_name="vit.kenaikan_gaji_berkala",  string="Kenaikan Gaji Berkala",  help="")
