#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class mutasi_hukum_detail(models.Model):
    _name = "vit.mutasi_hukum_detail"
    _inherit = "vit.mutasi_hukum_detail"

    hukum_awal = fields.Char(related="employee_id.hukuman", string="Hukuman awal",  help="")

    matra_id = fields.Many2one(comodel_name="vit.matra",  string="Matra",  help="")
    fakultas_id = fields.Many2one(comodel_name="vit.fakultas",  string="SUBSATKER",  help="")

    @api.onchange('matra_id','fakultas_id')
    def onchange_mf(self):
        for rec in self:
            rec.matra_id = rec.mutasi_hukum_id.matra_id.id
            rec.fakultas_id = rec.mutasi_hukum_id.fakultas_id.id
