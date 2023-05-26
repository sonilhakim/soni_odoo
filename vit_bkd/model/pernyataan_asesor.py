#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft','Draft'),('open','Proses'),('done','Selesai')]
from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class pernyataan_asesor(models.Model):

    _name = "vit.pernyataan_asesor"
    _description = "vit.pernyataan_asesor"
    name = fields.Char( required=True, default="New", readonly=True,  string="Name",  help="")
    date = fields.Date( string="Date",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    state = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",  help="")


    bkd_id = fields.Many2one(comodel_name="vit.bkd",  string="Bkd",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    asesor1_id = fields.Many2one(comodel_name="hr.employee",  string="Asesor1",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    asesor2_id = fields.Many2one(comodel_name="hr.employee",  string="Asesor2",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
