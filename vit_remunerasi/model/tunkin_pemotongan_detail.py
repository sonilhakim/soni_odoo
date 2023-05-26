#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class tunkin_pemotongan_detail(models.Model):

    _name = "vit.tunkin_pemotongan_detail"
    _description = "vit.tunkin_pemotongan_detail"
    pemotongan = fields.Float( string="Pemotongan",  help="")


    karyawan_id = fields.Many2one(comodel_name="hr.employee",  string="Karyawan",  help="")
    tunkin_pemotongan_id = fields.Many2one(comodel_name="vit.tunkin_pemotongan",  string="Tunkin pemotongan",  help="")
