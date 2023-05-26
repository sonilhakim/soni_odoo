#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class riwayat_kepakaran_dosen(models.Model):

    _name = "vit.riwayat_kepakaran_dosen"
    _description = "vit.riwayat_kepakaran_dosen"
    name = fields.Char( required=True, string="Name",  help="")
    description = fields.Text( string="Description",  help="")


    employee_id = fields.Many2one(comodel_name="hr.employee",  string="Employee",  help="")
