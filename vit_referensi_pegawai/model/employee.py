#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class employee(models.Model):
    _name = "hr.employee"
    _inherit = "hr.employee"

    status_nikah = fields.Many2one( "vit.status_nikah","Status Pernikahan",  help="")
    unit_wilayah = fields.Many2one( "vit.unit_wilayah","Unit Wilayah",  help="")
    gol_darah = fields.Many2one( "vit.golongan_darah","Golongan Darah",  help="")
    jenis_pegawai = fields.Many2one( "vit.jenis_pegawai","Jenis Pegawai",  help="")
    asal_dana = fields.Many2one( "vit.asal_dana","Asal Dana",  help="")
    tunjangan_kesehatan = fields.Many2one( "vit.tunjangan_kesehatan","Tunjangan Kesehatan",  help="")
    ref_level = fields.Many2one( "vit.ref_level","Level",  help="")
    agama = fields.Many2one( "vit.agama","Agama",  help="")
    bidang_ilmu_id = fields.Many2one( "vit.bidang_ilmu","Bidang Ilmu",  help="")

    subsatker_id = fields.Many2one(comodel_name='vit.unit_kerja', string='SUBSATKER')
    eselon = fields.Char('Eselon')
    jenis_jabatan_id = fields.Many2one(comodel_name="vit.jenis.jabatan",  string="Jenis Jabatan",  help="")
    jenis_jabatan_code = fields.Char(string="Kode Jabatan", related="jenis_jabatan_id.code",  help="")

