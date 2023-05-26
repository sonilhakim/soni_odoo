#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class capaian_kinerja_unit_kerja_detail(models.Model):
    _name = "vit.capaian_kinerja_unit_kerja_detail"
    _inherit = "vit.capaian_kinerja_unit_kerja_detail"

    target_capaian = fields.Float( string="Target Capaian",  help="")
    penilaian = fields.Char( string="Penilaian",  help="")

    @api.onchange('capaian','target_capaian')
    def onchange_penilaian(self):
    	for rec in self:
    		if rec.capaian >= rec.target_capaian:
    			rec.penilaian = "Tercapai"
    		else:
    			rec.penilaian = "Belum Tercapai"
