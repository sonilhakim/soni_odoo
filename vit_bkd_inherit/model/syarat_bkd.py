#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class syarat_bkd(models.Model):

    _name = "vit.syarat_bkd"
    _description = "vit.syarat_bkd"

    name = fields.Char( required=True, string="Name",  help="")
    status_dosen_id = fields.Many2one(comodel_name="vit.status_dosen", string="Status dosen",  help="")
    # status_dosen_ids = fields.Many2many('vit.status_dosen',relation='vit_status_dosen_vit_syarat_bkd_rel', column1='vit_syarat_bkd_id',column2='vit_status_dosen_id', string="Status Dosen")
    min_sks = fields.Float( string="Min sks", default= 0, help="")
    max_sks = fields.Float( string="Max sks", default= 0, help="")
    pendidikan = fields.Boolean( string="Pendidikan")
    penelitian = fields.Boolean( string="Penelitian")
    pengabdian = fields.Boolean( string="Pengabdian")
    pendidikan_penelitian = fields.Boolean( string="Pendidikan + Penelitian")
    pengabdian_penunjang = fields.Boolean( string="Pengabdian + Penunjang")
    total_kinerja = fields.Boolean( string="Total Kinerja")
