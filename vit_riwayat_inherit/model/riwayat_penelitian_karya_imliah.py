#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class riwayat_penelitian_karya_imliah(models.Model):
    _name = "vit.riwayat_penelitian_karya_imliah"
    _inherit = "vit.riwayat_penelitian_karya_imliah"

    ilmiah = fields.Many2one(comodel_name="vit.ilmiah",  string="Ilmiah",  help="")
    jenis_publikasi = fields.Many2one(comodel_name="vit.jenis_publikasi",  string="Jenis Publikasi",  help="")
    jenis_penelitian = fields.Many2one(comodel_name="vit.jenis_penelitian",  string="Jenis Penelitian",  help="")
    peranan_penelitian = fields.Many2one(comodel_name="vit.peranan_penelitian",  string="Peranan Dalam Penelitian",  help="")
