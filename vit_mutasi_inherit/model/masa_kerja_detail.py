#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class masa_kerja_detail(models.Model):
    _name = "vit.masa_kerja_detail"
    _inherit = "vit.masa_kerja_detail"

    mk_thn_awal = fields.Char(related="employee_id.mk_thn", string="MK thn awal",  help="")
    mk_bln_awal = fields.Char(related="employee_id.mk_bln", string="MK bln awal",  help="")
    mk_thn_tujuan = fields.Char( string="MK thn baru", help="")
    mk_bln_tujuan = fields.Char( string="MK thn baru", help="")
    matra_id = fields.Many2one(comodel_name="vit.matra",  string="Matra",  help="")
    fakultas_id = fields.Many2one(comodel_name="vit.fakultas",  string="SUBSATKER",  help="")

    @api.onchange('matra_id','fakultas_id')
    def onchange_mf(self):
        for rec in self:
            rec.matra_id = rec.mutasi_mk_id.matra_id.id
            rec.fakultas_id = rec.mutasi_mk_id.fakultas_id.id