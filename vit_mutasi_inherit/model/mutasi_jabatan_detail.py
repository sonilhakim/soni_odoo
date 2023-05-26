#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class mutasi_jabatan_detail(models.Model):
    _name = "vit.mutasi_jabatan_detail"
    _inherit = "vit.mutasi_jabatan_detail"

    employee_id = fields.Many2one(comodel_name="hr.employee",  string="Employee", domain=[('jabatan_id.fungsional','=',True)], help="")
    jabatan_awal = fields.Many2one(comodel_name="vit.jabatan", related="employee_id.jabatanf_id", string="Jabatan awal",  help="")

    matra_id = fields.Many2one(comodel_name="vit.matra",  string="Matra",  help="")
    fakultas_id = fields.Many2one(comodel_name="vit.fakultas",  string="SUBSATKER",  help="")

    @api.onchange('matra_id','fakultas_id')
    def onchange_mf(self):
        for rec in self:
            rec.matra_id = rec.mutasi_jabatan_id.matra_id.id
            rec.fakultas_id = rec.mutasi_jabatan_id.fakultas_id.id
