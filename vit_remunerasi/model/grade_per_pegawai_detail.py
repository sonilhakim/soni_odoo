#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class grade_per_pegawai_detail(models.Model):

    _name = "vit.grade_per_pegawai_detail"
    _description = "vit.grade_per_pegawai_detail"
    grade = fields.Float( string="Grade",  help="")


    karyawan_id = fields.Many2one(comodel_name="hr.employee",  string="Karyawan",  help="")
    grade_id = fields.Many2one(comodel_name="vit.grade_per_pegawai",  string="Grade",  help="")
