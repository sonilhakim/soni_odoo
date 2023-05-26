#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class asetPemakaian(models.Model):
    _name = "account.asset.asset"
    _inherit = "account.asset.asset"

    pemakai_id = fields.Many2one(comodel_name="hr.employee", string="Karyawan Pemakai Aset")
    unit_kerja_pemakai_id = fields.Many2one(comodel_name="vit.unit_kerja",  string="SUBSATKER Pemakai Aset",  track_visibility='onchange')
    used = fields.Selection( [('belum', 'Belum dipakai'), ('sudah', 'Sudah dipakai')], string='Status Pemakaian', default='belum')
