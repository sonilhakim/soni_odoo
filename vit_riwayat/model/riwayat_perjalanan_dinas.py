#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class riwayat_perjalanan_dinas(models.Model):

    _name = "vit.riwayat_perjalanan_dinas"
    _description = "vit.riwayat_perjalanan_dinas"
    name = fields.Char( required=True, string="Name",  help="")
    date_start = fields.Date( string="Date start",  help="")
    date_end = fields.Date( string="Date end",  help="")
    description = fields.Text( string="Description",  help="")


    country_id = fields.Many2one(comodel_name="res.country",  string="Country",  help="")
    employee_id = fields.Many2one(comodel_name="hr.employee",  string="Employee",  help="")
