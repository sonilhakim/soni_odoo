#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class skp_kkn_pkn_pkl(models.Model):
    _name = "vit.skp_kkn_pkn_pkl"
    _inherit = "vit.skp_kkn_pkn_pkl"

    # ak = fields.Integer( string="Ak", compute="compute_kkn", help="")

    # @api.multi
    # def compute_kkn(self):
    #     for kkn in self:
    #         kkn.jumlah = kkn.semester_genap + kkn.semester_ganjil
    #         kkn.ak = kkn.jumlah
