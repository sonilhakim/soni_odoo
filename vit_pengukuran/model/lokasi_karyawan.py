#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class lokasi_karyawan(models.Model):
    _name = "vit.lokasi_karyawan"
    _description = "Lokasi Karyawan"
    
    name         = fields.Char( required=True, string="Name",  track_visibility='onchange')
    spk_id   = fields.Many2one("vit.spk_pengukuran", "SPK", track_visibility='onchange')
    user_id      = fields.Many2one("res.users", "User", default=lambda self: self.env.uid, track_visibility='onchange')
    pengukuran_id   = fields.Many2one("vit.pengukuran", "Project", track_visibility='onchange')

    _sql_constraints = [
        ('cek_unik_lokasi_nik', 'UNIQUE(name)',
            'Nama lokasi harus uniq')
    ]

    @api.multi
    def copy_data(self, default=None):
        if default is None:
            default = {}
        default['name'] = self.name + _(' (copy)')
        return super(lokasi_karyawan, self).copy_data(default)

lokasi_karyawan()