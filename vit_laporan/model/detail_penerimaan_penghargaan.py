#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class detail_penerimaan_penghargaan(models.Model):

    _name = "vit.detail_penerimaan_penghargaan"
    _description = "vit.detail_penerimaan_penghargaan"
    name = fields.Char( required=True, string="Name",  help="")
    nip = fields.Char( string="Nip",  help="")
    jenis_penghargaan = fields.Char( string="Jenis penghargaan",  help="")
    tgl_penerimaan = fields.Date( string="Tgl penerimaan",  help="")


    penerimaan_penghargaan_id = fields.Many2one(comodel_name="vit.penerimaan_penghargaan",  string="Penerimaan penghargaan",  help="")
