#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class skp_seminar(models.Model):
    _name = "vit.skp_seminar"
    _inherit = "vit.skp_seminar"

    # @api.multi
    # def compute_seminar(self):
    #     for sem in self:
    #         sem.ak = sem.pelaksanaan
