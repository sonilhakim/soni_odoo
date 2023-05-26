#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft','Draft'),('open','Proses'),('done','Selesai')]
from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class rekap_perguruan_tinggi(models.Model):

    _name = "vit.rekap_perguruan_tinggi"
    _description = "vit.rekap_perguruan_tinggi"
    name = fields.Char( required=True, default="New", readonly=True,  string="Name",  help="")
    date = fields.Date( string="Date",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    nip_rektor = fields.Char( string="Nip rektor",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    alamat_perguruan_tinggi = fields.Char( string="Alamat perguruan tinggi",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    state = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",  help="")


    institusi_id = fields.Many2one(comodel_name="res.company",  string="Institusi",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    line_ids = fields.One2many(comodel_name="vit.rekap_perguruan_tinggi_line",  inverse_name="rekap_perguruan_tinggi_id",  string="Line",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
