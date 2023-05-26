#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class ref_pendidikan(models.Model):

    _name = "vit.ref_pendidikan"
    _description = "vit.ref_pendidikan"
    name = fields.Char( required=True, string="Name",  help="")
    jenis_id = fields.Many2one('vit.jenis_pendidikan', 'Jenis Pendidikan')


