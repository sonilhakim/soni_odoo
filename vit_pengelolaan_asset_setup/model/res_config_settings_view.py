# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    aset_location = fields.Boolean(string='Lokasi Aset')
    aset_category = fields.Boolean(string="Jenis Aset")
    aset_kelompok = fields.Boolean("Kelompok Aset")
    aset_satuan   = fields.Boolean("Satuan Aset")
    aset_pengadaan = fields.Boolean("Pengadaan Aset")