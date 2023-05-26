#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class riwayat_membimbing(models.Model):

    _name = "vit.riwayat_membimbing"
    _description = "vit.riwayat_membimbing"
    name = fields.Char( required=True, string="Name",  help="")
    date_start = fields.Date( string="Date start",  help="")
    date_end = fields.Date( string="Date end",  help="")
    mahasiswa = fields.Char( string="Mahasiswa",  help="")
    jurusan = fields.Char( string="Jurusan",  help="")
    judul_thesis = fields.Char( string="Judul thesis",  help="")


    employee_id = fields.Many2one(comodel_name="hr.employee",  string="Employee",  help="")
