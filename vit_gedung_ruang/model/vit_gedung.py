#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft','Draft'),('open','Confirmed'),('done','Done')]
from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class vit_gedung(models.Model):

    _name = "vit.vit_gedung"
    _description = "vit.vit_gedung"
    name = fields.Char( required=True, default="New", readonly=True,  string="Name",  help="")
    kode_gedung = fields.Char( string="Kode gedung",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    alamat = fields.Char( string="Alamat",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    state = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",  help="")


    asset_id = fields.Many2one(comodel_name="account.asset.asset",  string="Asset",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    penanggung_jawab_id = fields.Many2one(comodel_name="res.users",  string="Penanggung jawab",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    ruang_ids = fields.One2many(comodel_name="vit.vit_ruang",  inverse_name="gedung_id",  string="Ruang",  readonly=True, states={"draft" : [("readonly",False)]},  help="")

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
        return super(vit_gedung, self).unlink()
