#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class masa_kerja_detail(models.Model):

    _name = "vit.masa_kerja_detail"
    _description = "vit.masa_kerja_detail"
    name = fields.Char( required=False, string="Name",  help="")
    masa_kerja_awal = fields.Char( string="Masa kerja awal",  help="")
    masa_kerja_tujuan = fields.Char( string="Masa kerja baru",  help="")


    mutasi_mk_id = fields.Many2one(comodel_name="vit.mutasi_penyesuaian_masa_kerja",  string="Mutasi mk",  help="")
    employee_id = fields.Many2one(comodel_name="hr.employee",  string="Employee",  help="")
