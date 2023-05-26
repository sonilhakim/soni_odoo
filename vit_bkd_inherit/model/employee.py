#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class employee(models.Model):
    _name = "hr.employee"
    _inherit = "hr.employee"

    gelar_depan = fields.Char( string="Gelar Depan",  help="")
    gelar_belakang = fields.Char( string="Gelar Belakang",  help="")
