#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft','Draft'),('open','Proses'),('done','Selesai')]
from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class kesimpulan_kinerja_dosen(models.Model):

    _name = "vit.kesimpulan_kinerja_dosen"
    _description = "vit.kesimpulan_kinerja_dosen"
    name = fields.Char( required=True, default="New", readonly=True,  string="Name",  help="")
    nip = fields.Char( string="Nip",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    state = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",  help="")


    dosen_id = fields.Many2one(comodel_name="hr.employee",  string="Dosen",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    status_dosen_id = fields.Many2one(comodel_name="vit.status_dosen",  string="Status dosen",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    tahun_akademik_id = fields.Many2one(comodel_name="vit.tahun_akademik",  string="Tahun akademik",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    line_ids = fields.One2many(comodel_name="vit.kesimpulan_kinerja_dosen_line",  inverse_name="kesimpulan_id",  string="Line",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
