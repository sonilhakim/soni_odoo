#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class skp_rekapitulasi_perkuliahan(models.Model):

    _name = "vit.skp_rekapitulasi_perkuliahan"
    _description = "vit.skp_rekapitulasi_perkuliahan"
    name = fields.Char( required=True, string="Name",  help="")
    sks = fields.Integer( string="Sks",  help="")
    sks_riil = fields.Integer( string="Sks riil",  help="")
    ak_10_sks_pertama = fields.Integer( string="Ak 10 sks pertama",  help="")
    ak_sks_berikutnya = fields.Integer( string="Ak sks berikutnya",  help="")
    ak_jumlah = fields.Integer( string="Ak jumlah",  help="")


    skp_id = fields.Many2one(comodel_name="vit.skp",  string="Skp",  help="")
    semester_id = fields.Many2one(comodel_name="vit.semester",  string="Semester",  help="")
