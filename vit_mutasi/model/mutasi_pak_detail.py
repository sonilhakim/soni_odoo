#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class mutasi_pak_detail(models.Model):

    _name = "vit.mutasi_pak_detail"
    _description = "vit.mutasi_pak_detail"
    name = fields.Char( required=False, string="Name",  help="")
    pak_awal = fields.Char( string="PAK awal",  help="")
    pak_tujuan = fields.Char( string="PAK baru",  help="")


    mutasi_pak_id = fields.Many2one(comodel_name="vit.mutasi_penetapan_angka_kredit",  string="Mutasi pak",  help="")
    employee_id = fields.Many2one(comodel_name="hr.employee",  string="Employee",  help="")
