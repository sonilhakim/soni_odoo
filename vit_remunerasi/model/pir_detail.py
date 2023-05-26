#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class pir_detail(models.Model):

    _name = "vit.pir_detail"
    _description = "vit.pir_detail"
    pir = fields.Char( string="Pir",  help="")


    karyawan_id = fields.Many2one(comodel_name="hr.employee",  string="Karyawan",  help="")
    pir_id = fields.Many2one(comodel_name="vit.pir",  string="Pir",  help="")
