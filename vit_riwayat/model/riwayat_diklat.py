#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class riwayat_diklat(models.Model):

    _name = "vit.riwayat_diklat"
    _description = "vit.riwayat_diklat"
    name = fields.Char( required=True, string="Name",  help="")
    date_start = fields.Date( string="Date start",  help="")
    date_end = fields.Date( string="Date end",  help="")
    description = fields.Text( string="Description",  help="")
    certificate = fields.Binary( string="Certificate",  help="")


    employee_id = fields.Many2one(comodel_name="hr.employee",  string="Employee",  help="")
    institusi_id = fields.Many2one(comodel_name="res.partner",  string="Institusi",  help="")
