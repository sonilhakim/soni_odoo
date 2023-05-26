#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft','Draft'),('open','Confirm'),('done','Done')]
from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class penerimaan_penghargaan(models.Model):

    _name = "vit.penerimaan_penghargaan"
    _description = "vit.penerimaan_penghargaan"
    name = fields.Char( required=True, default="New", readonly=True,  string="Name",  help="")
    state = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",  help="")


    def action_reload(self, ):
        pass


    matra_id = fields.Many2one(comodel_name="vit.matra",  string="Matra",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    fakultas_id = fields.Many2one(comodel_name="vit.fakultas",  string="Fakultas",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    detail_penghargaan_ids = fields.One2many(comodel_name="vit.detail_penerimaan_penghargaan",  inverse_name="penerimaan_penghargaan_id",  string="Detail penghargaan",  readonly=True, states={"draft" : [("readonly",False)]},  help="")

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
        return super(penerimaan_penghargaan, self).unlink()
