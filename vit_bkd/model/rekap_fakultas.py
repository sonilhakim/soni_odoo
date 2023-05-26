#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft','Draft'),('open','Proses'),('done','Selesai')]
from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class rekap_fakultas(models.Model):

    _name = "vit.rekap_fakultas"
    _description = "vit.rekap_fakultas"
    name = fields.Char( required=True, default="New", readonly=True,  string="Name",  help="")
    date = fields.Date( string="Date",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    nip_dekan = fields.Char( string="Nip dekan",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    state = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",  help="")


    institusi_id = fields.Many2one(comodel_name="res.company",  string="Institusi",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    fakultas_id = fields.Many2one(comodel_name="vit.fakultas",  string="Fakultas",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    dekan_id = fields.Many2one(comodel_name="hr.employee",  string="Dekan",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    line_ids = fields.One2many(comodel_name="vit.rekap_fakultas_line",  inverse_name="rekap_fakultas_id",  string="Line",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
