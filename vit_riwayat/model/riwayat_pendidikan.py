#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class riwayat_pendidikan(models.Model):

    _name = "vit.riwayat_pendidikan"
    _description = "vit.riwayat_pendidikan"
    name = fields.Char( required=True, string="Name",  help="")
    date_from = fields.Date( string="Date from",  help="")
    date_end = fields.Date( string="Date end",  help="")
    major = fields.Char( string="Major",  help="")


    employee_id = fields.Many2one(comodel_name="hr.employee",  string="Employee",  help="")
    institusi_id = fields.Many2one(comodel_name="res.partner",  string="Institusi",  help="")
    strata_id = fields.Many2one(comodel_name="vit.strata",  string="Strata",  help="")
