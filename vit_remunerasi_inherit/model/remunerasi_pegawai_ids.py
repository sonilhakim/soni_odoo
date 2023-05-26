#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class remunerasi_pegawai_ids(models.Model):
    _name = "vit.remunerasi_pegawai_ids"
    _inherit = "vit.remunerasi_pegawai_ids"

    golongan_id = fields.Many2one(comodel_name="vit.golongan",  string="Golongan",  help="")
    pangkat_id = fields.Many2one(comodel_name="vit.pangkat",  string="Pangkat",  help="")
    wage = fields.Float('Gaji', digits=(16, 2))
    currency_id = fields.Many2one(string="Currency", related='karyawan_id.user_id.company_id.currency_id', readonly=True)
