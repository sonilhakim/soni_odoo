#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class gaji_pnbp_detail(models.Model):

    _name = "vit.gaji_pnbp_detail"
    _description = "vit.gaji_pnbp_detail"
    gaji = fields.Float( string="Gaji",  help="")


    karyawan_id = fields.Many2one(comodel_name="hr.employee",  string="Karyawan",  help="")
    gaji_id = fields.Many2one(comodel_name="vit.gaji_pnbp",  string="Gaji",  help="")
