#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class riwayat_pengabdian_masyarakat(models.Model):

    _name = "vit.riwayat_pengabdian_masyarakat"
    _description = "vit.riwayat_pengabdian_masyarakat"
    name = fields.Char( required=True, string="Name",  help="")
    date_start = fields.Date( string="Date start",  help="")
    date_end = fields.Date( string="Date end",  help="")
    description = fields.Text( string="Description",  help="")


    employee_id = fields.Many2one(comodel_name="hr.employee",  string="Employee",  help="")
