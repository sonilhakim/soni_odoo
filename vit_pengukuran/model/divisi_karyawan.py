#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class divisi_karyawan(models.Model):
    _name = "vit.divisi_karyawan"
    _description = "Divisi Karyawan"
    
    name         = fields.Char( required=True, string="Name",  help="")
    user_id      = fields.Many2one("res.users", "User", default=lambda self: self.env.uid, track_visibility='onchange')
    pengukuran_id   = fields.Many2one("vit.pengukuran", "Project", track_visibility='onchange')
    spk_id   = fields.Many2one("vit.spk_pengukuran", "SPK", track_visibility='onchange')

    _sql_constraints = [
        ('cek_unik_divisi_name', 'UNIQUE(name,spk_id)',
            'Nama divisi per SPK harus uniq')
    ]

class style_divisi(models.Model):
    _name = "vit.style_divisi"
    _description = "vit.style_divisi"
    _rec_name = "style_id"
    
    name         = fields.Char( required=False, string="Name",  help="")
    style_id     = fields.Many2one(comodel_name="vit.style_pengukuran",  string="Style", required=True, help="" )
    divisi_id    = fields.Many2one("vit.divisi_karyawan", "Divisi")
    