#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class riwayat_izin_belajar(models.Model):

    _name = "vit.riwayat_izin_belajar"
    _description = "vit.riwayat_izin_belajar"
    name = fields.Char( required=True, string="Name",  help="")
    date = fields.Date( string="Date",  help="")


    employee_id = fields.Many2one(comodel_name="hr.employee",  string="Employee",  help="")
