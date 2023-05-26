# -*- coding: utf-8 -*-

from odoo import models, fields

class RespUsers(models.Model):
    
    _inherit = 'res.users'

    unit_ids = fields.Many2many('vit.unit_kerja', string='Subsatker')