#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
import time
from odoo.exceptions import UserError, Warning

class asal_dana(models.Model):

    _name = "vit.asal_dana"
    _description = "vit.asal_dana"
    name = fields.Char( required=True, string="Dana",  help="")
    detail_ids = fields.One2many('vit.asal_dana_detail', 'dana_id')

class asal_dana_detail(models.Model):

    _name = "vit.asal_dana_detail"
    _description = "vit.asal_dana_detail"
    name = fields.Char( required=True, string="Asal Dana",  help="")
    tanggal = fields.Date( string="Tanggal", default=lambda self:time.strftime("%Y-%m-%d"), help="")
    nilai = fields.Float( string="Nilai Dana")
    dana_id = fields.Many2one('vit.asal_dana', 'Dana')


