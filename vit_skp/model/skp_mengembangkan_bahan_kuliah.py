#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class skp_mengembangkan_bahan_kuliah(models.Model):

    _name = "vit.skp_mengembangkan_bahan_kuliah"
    _description = "vit.skp_mengembangkan_bahan_kuliah"
    name = fields.Char( required=True, string="Name",  help="")
    jumlah = fields.Integer( string="Jumlah",  help="")
    ak_per_bahan_kuliah = fields.Integer( string="Ak per bahan kuliah",  help="")
    ak_jumlah = fields.Integer( string="Ak jumlah",  help="")


    skp_id = fields.Many2one(comodel_name="vit.skp",  string="Skp",  help="")
    semester_id = fields.Many2one(comodel_name="vit.semester",  string="Semester",  help="")
