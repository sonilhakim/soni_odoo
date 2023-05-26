#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class gb_detail(models.Model):

    _name = "vit.gb_detail"
    _description = "vit.gb_detail"
    name = fields.Char( required=True, string="Name",  help="")
    nip = fields.Char( string="Nip",  help="")
    jabatan = fields.Char( string="Jabatan",  help="")
    golongan = fields.Char( string="Golongan",  help="")


    gb_id = fields.Many2one(comodel_name="vit.daftar_guru_besar",  string="Gb",  help="")
