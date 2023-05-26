#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class capaian_kinerja_unit_kerja_detail(models.Model):

    _name = "vit.capaian_kinerja_unit_kerja_detail"
    _description = "vit.capaian_kinerja_unit_kerja_detail"
    capaian = fields.Float( string="Capaian",  help="")


    unit_id = fields.Many2one(comodel_name="vit.unit_kerja",  string="Unit",  help="")
    capaian_unit_id = fields.Many2one(comodel_name="vit.capaian_kinerja_unit_kerja",  string="Capaian unit",  help="")
