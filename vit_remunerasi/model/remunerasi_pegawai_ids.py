#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class remunerasi_pegawai_ids(models.Model):

    _name = "vit.remunerasi_pegawai_ids"
    _description = "vit.remunerasi_pegawai_ids"
    remunerasi = fields.Char( string="Remunerasi",  help="")


    karyawan_id = fields.Many2one(comodel_name="hr.employee",  string="Karyawan",  help="")
    remunerasi_id = fields.Many2one(comodel_name="vit.remunerasi_pegawai",  string="Remunerasi",  help="")
