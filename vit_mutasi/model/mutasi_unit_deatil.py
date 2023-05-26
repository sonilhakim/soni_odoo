#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class mutasi_unit_deatil(models.Model):

    _name = "vit.mutasi_unit_deatil"
    _description = "vit.mutasi_unit_deatil"
    name = fields.Char( required=False, string="Name",  help="")


    mutasi_unit_id = fields.Many2one(comodel_name="vit.mutasi_unit_kerja",  string="Mutasi unit",  help="")
    employee_id = fields.Many2one(comodel_name="hr.employee",  string="Employee",  help="")
    unit_awal = fields.Many2one(comodel_name="vit.unit_kerja",  string="Unit awal",  help="")
    unit_tujuan = fields.Many2one(comodel_name="vit.unit_kerja",  string="Unit baru",  help="")
