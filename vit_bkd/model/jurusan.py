#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class jurusan(models.Model):

    _name = "vit.jurusan"
    _description = "vit.jurusan"

    _inherit = "vit.jurusan"


    fakultas_id = fields.Many2one(comodel_name="vit.fakultas",  string="Fakultas",  help="")
