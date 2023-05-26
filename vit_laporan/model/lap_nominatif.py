#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft','Draft'),('open','Confirm'),('done','Done')]
from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class lap_nominatif(models.Model):

    _name = "vit.lap_nominatif"
    _description = "vit.lap_nominatif"
    name = fields.Char( required=True, default="New", readonly=True,  string="Name",  help="")
    state = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",  help="")


    def action_reload(self, ):
        pass


    nom_detail_ids = fields.One2many(comodel_name="vit.nom_detail",  inverse_name="nominatif_id",  string="Nom detail",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    matra_id = fields.Many2one(comodel_name="vit.matra",  string="Matra",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    fakultas = fields.Many2one(comodel_name="vit.fakultas",  string="Fakultas",  readonly=True, states={"draft" : [("readonly",False)]},  help="")

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
        return super(lap_nominatif, self).unlink()
