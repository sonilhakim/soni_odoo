#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class riwayat_organisasi_pegawai(models.Model):

    _name = "vit.riwayat_organisasi_pegawai"
    _description = "vit.riwayat_organisasi_pegawai"
    name = fields.Char( required=True, string="Name",  help="")
    date = fields.Date( string="Date",  help="")
    description = fields.Text( string="Description",  help="")


    employee_id = fields.Many2one(comodel_name="hr.employee",  string="Employee",  help="")
