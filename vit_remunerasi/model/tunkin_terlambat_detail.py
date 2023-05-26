#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class tunkin_terlambat_detail(models.Model):

    _name = "vit.tunkin_terlambat_detail"
    _description = "vit.tunkin_terlambat_detail"
    terlambat = fields.Float( string="Terlambat",  help="")


    karyawan_id = fields.Many2one(comodel_name="hr.employee",  string="Karyawan",  help="")
    tunkin_terlambat_id = fields.Many2one(comodel_name="vit.tunkin_terlambat",  string="Tunkin terlambat",  help="")
