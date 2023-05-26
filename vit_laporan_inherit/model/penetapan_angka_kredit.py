#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft', 'Draft'),('open','Confirm'),('done','Done')]
from odoo import models, fields, api, _
import time
from odoo.exceptions import UserError, Warning

class penetapan_angka_kredit(models.Model):

    _name = "vit.penetapan_angka_kredit"
    _description = "vit.penetapan_angka_kredit"
    name = fields.Char( required=True, default="New", readonly=True,  string="Name",  help="")
    kegiatan = fields.Char( string="Kegiatan",required=True, readonly=True, states={"draft" : [("readonly",False)]})
    date = fields.Date( string="Tanggal", default=lambda self:time.strftime("%Y-%m-%d"), help="")
    state = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",  help="")

    penetapan_detail_ids = fields.One2many(comodel_name="vit.penetapan_angka_kredit_detail",  inverse_name="penetapan_id",  string="Penetapan AK detail",  readonly=True, states={"draft" : [("readonly",False)]},  help="")

    @api.model
    def create(self, vals):
        if not vals.get("name", False) or vals["name"] == "New":
            vals["name"] = self.env["ir.sequence"].next_by_code("vit.penetapan_angka_kredit") or "Error Number!!!"
        return super(penetapan_angka_kredit, self).create(vals)

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
        return super(penetapan_angka_kredit, self).unlink()

class penetapan_angka_kredit_detail(models.Model):

    _name = "vit.penetapan_angka_kredit_detail"
    _description = "vit.penetapan_angka_kredit_detail"
    _rec_name = "employee_id"
    name = fields.Char( required=False, default="New", string="Name",  help="")
    date_penetapan = fields.Date( string="Tanggal Penetapan", help="")
    employee_id = fields.Many2one(comodel_name="hr.employee",  string="Yang Menetapkan",  help="")
    angka_kredit = fields.Float( string="Angka Kredit",  help="")


    penetapan_id = fields.Many2one(comodel_name="vit.penetapan_angka_kredit",  string="Penetapan AK",  help="")

