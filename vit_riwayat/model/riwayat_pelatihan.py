#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class riwayat_pelatihan(models.Model):

    _name = "vit.riwayat_pelatihan"
    _description = "vit.riwayat_pelatihan"
    name = fields.Char( required=True, string="Name",  help="")
    date_start = fields.Date( string="Date start",  help="")
    date_end = fields.Date( string="Date end",  help="")
    description = fields.Text( string="Description",  help="")
    certificate = fields.Binary( string="Certificate",  help="")


    employee_id = fields.Many2one(comodel_name="hr.employee",  string="Employee",  help="")
    country_id = fields.Many2one(comodel_name="res.country",  string="Country",  help="")
