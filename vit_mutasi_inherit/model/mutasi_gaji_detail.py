#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class mutasi_gaji_detail(models.Model):
    _name = "vit.mutasi_gaji_detail"
    _inherit = "vit.mutasi_gaji_detail"

    gaji_awal = fields.Monetary( string="Gaji awal", digits=(16, 2), required=True, track_visibility="onchange",  help="")
    gaji_tujuan = fields.Monetary( string="Gaji baru", digits=(16, 2), required=True, track_visibility="onchange",  help="")
    company_id = fields.Many2one('res.company', string='Company', required=True, index=True, default=lambda self: self.env.user.company_id)
    currency_id = fields.Many2one(string="Currency", related='company_id.currency_id', readonly=True)
    matra_id = fields.Many2one(comodel_name="vit.matra",  string="Matra",  help="")
    fakultas_id = fields.Many2one(comodel_name="vit.fakultas",  string="SUBSATKER",  help="")

    @api.onchange("employee_id")
    def onchange_gaji(self):
    	if self.employee_id:
	    	kontrak = self.env["hr.contract"].search([('employee_id', '=', self.employee_id.id)])
	    	for k in kontrak:
	    		self.gaji_awal = k.wage


    @api.onchange('matra_id','fakultas_id')
    def onchange_mf(self):
        for rec in self:
            rec.matra_id = rec.mutasi_gaji_id.matra_id.id
            rec.fakultas_id = rec.mutasi_gaji_id.fakultas_id.id
