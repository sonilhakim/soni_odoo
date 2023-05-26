#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class fakultas(models.Model):

    _name = "vit.fakultas"
    _description = "vit.fakultas"

    _inherit = "vit.fakultas"


    institusi_id = fields.Many2one(comodel_name="res.company",  string="Institusi",  help="")
