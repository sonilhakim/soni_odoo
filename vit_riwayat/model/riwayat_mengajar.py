#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class riwayat_mengajar(models.Model):

    _name = "vit.riwayat_mengajar"
    _description = "vit.riwayat_mengajar"
    name = fields.Char( required=True, string="Name",  help="")
    date_from = fields.Date( string="Date from",  help="")
    date_end = fields.Date( string="Date end",  help="")
    matakuliah = fields.Char( string="Matakuliah",  help="")


    employee_id = fields.Many2one(comodel_name="hr.employee",  string="Employee",  help="")
    institusi_id = fields.Many2one(comodel_name="res.partner",  string="Institusi",  help="")
