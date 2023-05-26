#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class mutasi_jabatan_detail(models.Model):

    _name = "vit.mutasi_jabatan_detail"
    _description = "vit.mutasi_jabatan_detail"
    name = fields.Char( required=False, string="Name",  help="")


    mutasi_jabatan_id = fields.Many2one(comodel_name="vit.mutasi_jabatan",  string="Mutasi jabatan",  help="")
    employee_id = fields.Many2one(comodel_name="hr.employee",  string="Employee",  help="")
    jabatan_awal = fields.Many2one(comodel_name="vit.jabatan",  string="Jabatan awal",  help="")
    jabatan_tujuan = fields.Many2one(comodel_name="vit.jabatan",  string="Jabatan baru",  help="")
