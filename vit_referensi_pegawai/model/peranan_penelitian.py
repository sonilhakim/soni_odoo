#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class peranan_penelitian(models.Model):

    _name = "vit.peranan_penelitian"
    _description = "vit.peranan_penelitian"
    name = fields.Char( required=True, string="Peranan",  help="")
    jenis_id = fields.Many2one('vit.jenis_penelitian', 'Jenis Penelitian')
