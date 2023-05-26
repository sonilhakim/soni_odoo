#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class jenis_kegiatan_kewajiban_khusus(models.Model):
    _name = "vit.jenis_kegiatan_kewajiban_khusus"
    _inherit = "vit.jenis_kegiatan_kewajiban_khusus"
