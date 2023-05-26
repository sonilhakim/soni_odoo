#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
import math

class data_pengukuran(models.Model):
    _name = "vit.template_pengukuran"
    _description = "Template Pengukuran"

    name        = fields.Char(required=True, string="Template Name")
    line_ids    = fields.One2many(comodel_name="vit.template_pengukuran_details",  inverse_name="template_pengukuran_id",  string="Deskripsi Pengukuran",  copy=True )

data_pengukuran()


class data_pengukuran_details(models.Model):
    _name = "vit.template_pengukuran_details"
    _description = "Template Pengukuran Details"

    name        = fields.Char(required=True, string="Description")
    max_value = fields.Float('Max Value', default=100, required=False)
    min_value = fields.Float('Min Value', default=1, required=False)
    size    = fields.Float( string="Default Size", required=False)
    template_pengukuran_id      = fields.Many2one( "vit.template_pengukuran",string="Template", ondelete='cascade')

data_pengukuran_details()