#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class riwayat_study_lanjutan(models.Model):

    _name = "vit.riwayat_study_lanjutan"
    _description = "vit.riwayat_study_lanjutan"
    name = fields.Char( required=True, string="Name",  help="")
    major = fields.Char( string="Major",  help="")
    date_start = fields.Date( string="Date start",  help="")
    date_end = fields.Date( string="Date end",  help="")


    employee_id = fields.Many2one(comodel_name="hr.employee",  string="Employee",  help="")
    country_id = fields.Many2one(comodel_name="res.country",  string="Country",  help="")
