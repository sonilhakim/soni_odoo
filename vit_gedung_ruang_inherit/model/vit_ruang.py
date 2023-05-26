#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class vit_ruang(models.Model):
    _name = "vit.vit_ruang"
    _inherit = "vit.vit_ruang"

    satuan = fields.Many2one('uom.uom', 'Satuan')
