#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class status_pegawai(models.Model):

    _name = "hr.employee.category"
    _description = "hr.employee.category"

    _inherit = "hr.employee.category"


