#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class kode_nikah(models.Model):

    _name = "vit.kode_nikah"
    _description = "vit.kode_nikah"
    name = fields.Char( required=True, string="Kode",  help="")

class status_nikah(models.Model):

    _name = "vit.status_nikah"
    _description = "vit.status_nikah"
    name = fields.Char( required=True, string="Status Nikah",  help="")
    kode_id = fields.Many2one('vit.kode_nikah', 'Kode')


