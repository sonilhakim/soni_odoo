#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class pak_kegiatan(models.Model):

    _name = "vit.pak_kegiatan"
    _description = "vit.pak_kegiatan"
    name = fields.Char( required=True, string="Name",  help="")
    unsur_pak_id = fields.Many2one( 'vit.pak_unsur_kegiatan', 'PAK Unsur Kegiatan')


