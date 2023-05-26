#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class tunkin_pulang_detail(models.Model):

    _name = "vit.tunkin_pulang_detail"
    _description = "vit.tunkin_pulang_detail"
    pulang = fields.Float( string="Pulang",  help="")


    karyawan_id = fields.Many2one(comodel_name="hr.employee",  string="Karyawan",  help="")
    tunkin_pulang_id = fields.Many2one(comodel_name="vit.tunkin_pulang",  string="Tunkin pulang",  help="")
