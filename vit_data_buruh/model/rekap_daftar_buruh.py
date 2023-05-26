#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class rekap_daftar_buruh(models.Model):

    _name = "vit.rekap_daftar_buruh"
    _description = "vit.rekap_daftar_buruh"
    upah = fields.Float( string="Upah",  help="", )
    potongan = fields.Float( string="Potongan",  help="", )
    total = fields.Float( string="Total",  help="", )
    note = fields.Char( string="Keterangan",  help="", )
    mandor = fields.Boolean( string="Mandor")
    hadir = fields.Integer( string="Kehadiran")


    rekap_data_id = fields.Many2one(comodel_name="vit.rekap_data_buruh",  string="Rekap data",  help="", ondelete="cascade" )
    buruh_id = fields.Many2one(comodel_name="res.partner",  string="Buruh",  help="", )
