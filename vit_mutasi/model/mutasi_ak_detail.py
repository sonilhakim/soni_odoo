#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class mutasi_ak_detail(models.Model):

    _name = "vit.mutasi_ak_detail"
    _description = "vit.mutasi_ak_detail"
    name = fields.Char( required=False, string="Name",  help="")
    angka_kredit_awal = fields.Float( string="Angka kredit awal",  help="")
    angka_kredit_tujuan = fields.Float( string="Angka kredit baru",  help="")


    mutasi_ak_id = fields.Many2one(comodel_name="vit.mutasi_pengajuan_angka_kredit",  string="Mutasi ak",  help="")
    employee_id = fields.Many2one(comodel_name="hr.employee",  string="Employee",  help="")
