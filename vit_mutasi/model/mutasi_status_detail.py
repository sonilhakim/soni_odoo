#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class mutasi_status_detail(models.Model):

    _name = "vit.mutasi_status_detail"
    _description = "vit.mutasi_status_detail"
    name = fields.Char( required=False, string="Name",  help="")


    mutasi_status_id = fields.Many2one(comodel_name="vit.mutasi_status_pegawai",  string="Mutasi status",  help="")
    employee_id = fields.Many2one(comodel_name="hr.employee",  string="Employee",  help="")
    status_awal = fields.Many2one(comodel_name="hr.employee.category",  string="Status awal",  help="")
    status_tujuan = fields.Many2one(comodel_name="hr.employee.category",  string="Status baru",  help="")
