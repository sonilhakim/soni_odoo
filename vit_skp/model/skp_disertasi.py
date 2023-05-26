#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class skp_disertasi(models.Model):

    _name = "vit.skp_disertasi"
    _description = "vit.skp_disertasi"
    name = fields.Char( required=True, string="Name",  help="")
    jumlah_lulusan_pembimbing_utama = fields.Integer( string="Jumlah lulusan pembimbing utama",  help="")
    jumlah_lulusan_pembimbing_pembantu = fields.Integer( string="Jumlah lulusan pembimbing pembantu",  help="")
    ak_pembimbing_utama = fields.Integer( string="Ak pembimbing utama",  help="")
    ak_pembimbing_pembantu = fields.Integer( string="Ak pembimbing pembantu",  help="")
    ak_total = fields.Integer( string="Ak total",  help="")


    skp_id = fields.Many2one(comodel_name="vit.skp",  string="Skp",  help="")
    jenis_disertasi_id = fields.Many2one(comodel_name="vit.jenis_disertasi",  string="Jenis disertasi",  help="")
    semester_id = fields.Many2one(comodel_name="vit.semester",  string="Semester",  help="")
