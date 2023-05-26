#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class mutasi_ak_detail(models.Model):
    _name = "vit.mutasi_ak_detail"
    _inherit = "vit.mutasi_ak_detail"

    matra_id = fields.Many2one(comodel_name="vit.matra",  string="Matra",  help="")
    fakultas_id = fields.Many2one(comodel_name="vit.fakultas",  string="SUBSATKER",  help="")

    @api.onchange('matra_id','fakultas_id')
    def onchange_mf(self):
        for rec in self:
            rec.matra_id = rec.mutasi_ak_id.matra_id.id
            rec.fakultas_id = rec.mutasi_ak_id.fakultas_id.id
