#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class riwayat_dosen_mengajar_diluar(models.Model):

    _name = "vit.riwayat_dosen_mengajar_diluar"
    _description = "vit.riwayat_dosen_mengajar_diluar"
    name = fields.Char( required=True, string="Name",  help="")
    date_start = fields.Date( string="Date start",  help="")
    date_end = fields.Date( string="Date end",  help="")
    mata_kuliah = fields.Char( string="Mata kuliah",  help="")


    employee_id = fields.Many2one(comodel_name="hr.employee",  string="Employee",  help="")
    institusi_id = fields.Many2one(comodel_name="res.partner",  string="Institusi",  help="")
