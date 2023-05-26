#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class employee(models.Model):
    _name = "hr.employee"
    _inherit = "hr.employee"

    status_pegawai = fields.Many2one(comodel_name="hr.employee.category",  string="Status Pegawai",  help="")
    # masa_kerja = fields.Char( string="Masa kerja",  help="")
    hukuman = fields.Char( string="Hukuman",  help="")