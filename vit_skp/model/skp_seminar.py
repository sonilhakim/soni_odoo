#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class skp_seminar(models.Model):

    _name = "vit.skp_seminar"
    _description = "vit.skp_seminar"
    name = fields.Char( required=True, string="Name",  help="")
    pelaksanaan = fields.Integer( string="Pelaksanaan",  help="")
    ak = fields.Integer( string="Ak",  help="")


    skp_id = fields.Many2one(comodel_name="vit.skp",  string="Skp",  help="")
    semester_id = fields.Many2one(comodel_name="vit.semester",  string="Semester",  help="")
