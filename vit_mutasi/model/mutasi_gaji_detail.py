#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class mutasi_gaji_detail(models.Model):

    _name = "vit.mutasi_gaji_detail"
    _description = "vit.mutasi_gaji_detail"
    name = fields.Char( required=False, string="Name",  help="")
    gaji_awal = fields.Float( string="Gaji awal",  help="")
    gaji_tujuan = fields.Float( string="Gaji baru",  help="")


    employee_id = fields.Many2one(comodel_name="hr.employee",  string="Employee",  help="")
    mutasi_gaji_id = fields.Many2one(comodel_name="vit.mutasi_kenaikan_gaji_berkala",  string="Mutasi gaji",  help="")
