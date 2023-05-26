#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class kehadiran_pegawai_detail(models.Model):

    _name = "vit.kehadiran_pegawai_detail"
    _description = "vit.kehadiran_pegawai_detail"
    kehadiran = fields.Float( string="Kehadiran",  help="")


    karyawan_id = fields.Many2one(comodel_name="hr.employee",  string="Karyawan",  help="")
    kehadiran_pegawai_id = fields.Many2one(comodel_name="vit.kehadiran_pegawai",  string="Kehadiran pegawai",  help="")
