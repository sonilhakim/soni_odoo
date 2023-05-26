#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class riwayat_verifikasi(models.Model):

    _name = "vit.riwayat_verifikasi"
    _description = "vit.riwayat_verifikasi"
    name = fields.Char( required=True, string="Name",  help="")
    kegiatan = fields.Char( string="Kegiatan",  help="")
    date_start = fields.Date( string="Date start",  help="")
    date_end = fields.Date( string="Date end",  help="")


    employee_id = fields.Many2one(comodel_name="hr.employee",  string="Penanggung Jawab",  help="")
    status_verifikasi = fields.Many2one(comodel_name="vit.status_verifikasi",  string="Status Verifikasi",  help="")
