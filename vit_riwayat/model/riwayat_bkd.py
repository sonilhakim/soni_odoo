#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class riwayat_bkd(models.Model):

    _name = "vit.riwayat_bkd"
    _description = "vit.riwayat_bkd"
    name = fields.Char( required=True, string="Name",  help="")
    date_start = fields.Date( string="Date start",  help="")
    date_from = fields.Date( string="Date from",  help="")
    description = fields.Text( string="Description",  help="")


    employee_id = fields.Many2one(comodel_name="hr.employee",  string="Employee",  help="")
