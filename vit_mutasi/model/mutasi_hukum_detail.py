#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class mutasi_hukum_detail(models.Model):

    _name = "vit.mutasi_hukum_detail"
    _description = "vit.mutasi_hukum_detail"
    name = fields.Char( required=False, string="Name",  help="")
    hukum_awal = fields.Char( string="Hukum awal",  help="")
    hukum_tujuan = fields.Char( string="Hukum baru",  help="")


    mutasi_hukum_id = fields.Many2one(comodel_name="vit.mutasi_hukum",  string="Mutasi hukum",  help="")
    employee_id = fields.Many2one(comodel_name="hr.employee",  string="Employee",  help="")
