#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class skp_perkuliahan(models.Model):

    _name = "vit.skp_perkuliahan"
    _description = "vit.skp_perkuliahan"
    name = fields.Char( required=True, string="Name",  help="")
    sks = fields.Integer( string="Sks",  help="")
    jumlah_kelas = fields.Integer( string="Jumlah kelas",  help="")
    jumlah_dosen_pengampu = fields.Integer( string="Jumlah dosen pengampu",  help="")
    totak_sks_per_smt = fields.Float( string="Totak sks per smt",  help="")


    skp_id = fields.Many2one(comodel_name="vit.skp",  string="Skp",  help="")
    semester_id = fields.Many2one(comodel_name="vit.semester",  string="Semester",  help="")
