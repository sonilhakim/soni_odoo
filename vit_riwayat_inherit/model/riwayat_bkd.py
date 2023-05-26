#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class riwayat_bkd(models.Model):
    _name = "vit.riwayat_bkd"
    _inherit = "vit.riwayat_bkd"

    name = fields.Many2one(comodel_name="vit.bkd", required=True, string="Name",  help="")
    date_start = fields.Date( related="name.date", string="Date start",  help="")
    employee_id = fields.Many2one(comodel_name="hr.employee", related="name.employee_id", string="Employee",  help="")
