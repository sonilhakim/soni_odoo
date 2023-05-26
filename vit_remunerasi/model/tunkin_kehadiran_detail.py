#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class tunkin_kehadiran_detail(models.Model):

    _name = "vit.tunkin_kehadiran_detail"
    _description = "vit.tunkin_kehadiran_detail"
    kehadiran = fields.Float( string="Kehadiran",  help="")


    karyawan_id = fields.Many2one(comodel_name="hr.employee",  string="Karyawan",  help="")
    tunkin_kehadiran_id = fields.Many2one(comodel_name="vit.tunkin_kehadiran",  string="Tunkin kehadiran",  help="")
