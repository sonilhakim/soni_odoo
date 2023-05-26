#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class riwayat_penelitian_karya_imliah(models.Model):

    _name = "vit.riwayat_penelitian_karya_imliah"
    _description = "vit.riwayat_penelitian_karya_imliah"
    name = fields.Char( required=True, string="Name",  help="")
    description = fields.Text( string="Description",  help="")
    date = fields.Date( string="Date",  help="")


    employee_id = fields.Many2one(comodel_name="hr.employee",  string="Employee",  help="")
