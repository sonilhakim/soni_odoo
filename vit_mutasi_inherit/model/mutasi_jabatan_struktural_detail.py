#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class mutasi_jabatan_struktural_detail(models.Model):

    _name = "vit.mutasi_jabatan_struktural_detail"
    _description = "vit.mutasi_jabatan_struktural_detail"
    name = fields.Char( required=False, string="Name",  help="")


    mutasi_jabatan_struktural_id = fields.Many2one(comodel_name="vit.mutasi_jabatan_struktural",  string="Mutasi jabatan",  help="")
    employee_id = fields.Many2one(comodel_name="hr.employee",  string="Employee", domain=[('jabatan_id.struktural','=',True)], help="")
    jabatan_awal = fields.Many2one(comodel_name="vit.jabatan",  string="Jabatan awal",  related="employee_id.jabatan_id", help="")
    jabatan_tujuan = fields.Many2one(comodel_name="vit.jabatan",  string="Jabatan baru",  help="")

    matra_id = fields.Many2one(comodel_name="vit.matra",  string="Matra",  help="")
    fakultas_id = fields.Many2one(comodel_name="vit.fakultas",  string="SUBSATKER",  help="")

    @api.onchange('matra_id','fakultas_id')
    def onchange_mf(self):
        for rec in self:
            rec.matra_id = rec.mutasi_jabatan_struktural_id.matra_id.id
            rec.fakultas_id = rec.mutasi_jabatan_struktural_id.fakultas_id.id

