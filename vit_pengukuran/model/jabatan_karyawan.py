#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class jabatan_karyawan(models.Model):
    _name = "vit.jabatan_karyawan"
    _description = "Jabatan Karyawan"
    
    name         = fields.Char( required=True, string="Name",  track_visibility='onchange')
    pengukuran_id   = fields.Many2one("vit.pengukuran", "Project", track_visibility='onchange')
    spk_id   = fields.Many2one("vit.spk_pengukuran", "SPK", track_visibility='onchange')
    user_id      = fields.Many2one("res.users", "User", default=lambda self: self.env.uid, track_visibility='onchange')

    _sql_constraints = [
        ('cek_unik_jabatan_name', 'UNIQUE(name,spk_id)',
            'Nama jabatan per SPK harus uniq')
    ]

jabatan_karyawan()