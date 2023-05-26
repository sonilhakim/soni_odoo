#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class riwayat_seminar(models.Model):

    _name = "vit.riwayat_seminar"
    _description = "vit.riwayat_seminar"
    name = fields.Char( required=True, string="Name",  help="")
    date_start = fields.Date( string="Date start",  help="")
    date_end = fields.Date( string="Date end",  help="")
    description = fields.Text( string="Description",  help="")


    employee_id = fields.Many2one(comodel_name="hr.employee",  string="Employee",  help="")
    penyelenggara_id = fields.Many2one(comodel_name="res.partner",  string="Penyelenggara",  help="")
