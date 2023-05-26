#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft', 'Draft'),('open','Confirm'),('done','Done')]
from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class buku_inventaris(models.Model):

    _name = "vit.buku_inventaris"
    _description = "vit.buku_inventaris"
    name = fields.Char( required=True, default="New", readonly=True,  string="Name",  help="")
    state = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",  help="")
    date = fields.Date( string="Date",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    status = fields.Selection(selection=[('draft', 'Draft'),('open','Confirm'),('done','Done')],  string="Status",  readonly=True, states={"draft" : [("readonly",False)]},  help="")


    def action_reload(self, ):
        pass


    lokasi_id = fields.Many2one(comodel_name="vit.location",  string="Lokasi",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    detail_ids = fields.One2many(comodel_name="vit.buku_inventaris_detail",  inverse_name="buku_inventaris_id",  string="Detail",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    kategori_id = fields.Many2one(comodel_name="account.asset.category",  string="Kategori",  readonly=True, states={"draft" : [("readonly",False)]},  help="")

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
        return super(buku_inventaris, self).unlink()
