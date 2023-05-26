#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class skp_detasering(models.Model):

    _name = "vit.skp_detasering"
    _description = "vit.skp_detasering"
    name = fields.Char( required=True, string="Name",  help="")
    semester_genap = fields.Integer( string="Semester genap",  help="")
    semester_ganjil = fields.Integer( string="Semester ganjil",  help="")
    jumlah = fields.Integer( string="Jumlah",  help="")
    ak = fields.Integer( string="Ak",  help="")


    skp_id = fields.Many2one(comodel_name="vit.skp",  string="Skp",  help="")
