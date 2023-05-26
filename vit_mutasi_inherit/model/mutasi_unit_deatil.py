#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class mutasi_unit_deatil(models.Model):
    _name = "vit.mutasi_unit_deatil"
    _inherit = "vit.mutasi_unit_deatil"

    unit_awal = fields.Many2one(comodel_name="vit.unit_kerja",  related="employee_id.unit_kerja_id", string="Unit awal",  help="")
    matra_id = fields.Many2one(comodel_name="vit.matra",  string="Matra",  help="")
    fakultas_id = fields.Many2one(comodel_name="vit.fakultas",  string="SUBSATKER",  help="")

    @api.onchange('matra_id','fakultas_id')
    def onchange_mf(self):
        for rec in self:
            rec.matra_id = rec.mutasi_unit_id.matra_id.id
            rec.fakultas_id = rec.mutasi_unit_id.fakultas_id.id