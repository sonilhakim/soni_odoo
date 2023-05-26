#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class daftar_buruh(models.Model):

    _name = "vit.daftar_buruh"
    _description = "vit.daftar_buruh"
    uang_makan = fields.Float( string="Uang makan",  help="", )
    potongan = fields.Float( string="Potongan",  help="", )
    note = fields.Char( string="Keterangan",  help="", )


    data_buruh_id = fields.Many2one(comodel_name="vit.data_buruh",  string="Data buruh",  help="", ondelete="cascade")
    buruh_id = fields.Many2one(comodel_name="res.partner",  string="Buruh",  help="", )
