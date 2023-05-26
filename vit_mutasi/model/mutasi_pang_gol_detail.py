#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class mutasi_pang_gol_detail(models.Model):

    _name = "vit.mutasi_pang_gol_detail"
    _description = "vit.mutasi_pang_gol_detail"
    name = fields.Char( required=False, string="Name",  help="")


    mutasi_pang_gol_id = fields.Many2one(comodel_name="vit.mutasi_pangkat_golongan",  string="Mutasi pang gol",  help="")
    employee_id = fields.Many2one(comodel_name="hr.employee",  string="Employee",  help="")
    pangkat_awal = fields.Many2one(comodel_name="vit.pangkat",  string="Pangkat awal",  help="")
    pangkat_tujuan = fields.Many2one(comodel_name="vit.pangkat",  string="Pangkat baru",  help="")
    golongan_awal = fields.Many2one(comodel_name="vit.golongan",  string="Golongan awal",  help="")
    golongan_tujuan = fields.Many2one(comodel_name="vit.golongan",  string="Golongan baru",  help="")
