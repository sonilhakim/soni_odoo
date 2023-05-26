#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft','Draft'),('open','Confirm'),('done','Done')]
from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class mutasi_kenaikan_gaji_berkala(models.Model):

    _name = "vit.mutasi_kenaikan_gaji_berkala"
    _description = "vit.mutasi_kenaikan_gaji_berkala"
    name = fields.Char( required=True, default="New", readonly=True,  string="Name",  help="")
    state = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",  help="")


    matra_id = fields.Many2one(comodel_name="vit.matra",  string="Matra",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    fakultas_id = fields.Many2one(comodel_name="vit.fakultas",  string="SUBSATKER",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    mutasi_gaji_detail_ids = fields.One2many(comodel_name="vit.mutasi_gaji_detail",  inverse_name="mutasi_gaji_id",  string="Mutasi gaji detail",  readonly=True, states={"draft" : [("readonly",False)]},  help="")

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
        return super(mutasi_kenaikan_gaji_berkala, self).unlink()
