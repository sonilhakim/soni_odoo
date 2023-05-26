#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class kpi_gsp(models.Model):
    _name = "vit.kpi_gsp"
    _description = "vit.kpi_gsp"
    _order = 'id desc'
    _inherit = ['mail.thread']

    name        = fields.Char( readonly=True, required=True, default='New', string="Name", copy=False)
    start_date  = fields.Date( string="Start date", required=True,  help="")
    end_date    = fields.Date( string="End date", required=True,  help="")
    preference  = fields.Char( string="Preference",  help="")
    total_bobot = fields.Float( string="Total Bobot", compute='compute_total', store=True, help="")
    total_score = fields.Float( string="Total Score", compute='compute_total', store=True, help="")


    company_id    = fields.Many2one( comodel_name="res.company",  string="Company", required=True, index=True, default=lambda self: self.env.user.company_id.id)
    kpi_lines_ids = fields.One2many(comodel_name="vit.kpi_lines",  inverse_name="kpi_id",  string="KPI Lines",  help="")


    @api.model
    def create(self, vals):
        company_id = vals.get('company_id', self.default_get(['company_id'])['company_id'])
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].with_context(force_company=company_id).next_by_code('vit.kpi_gsp') or '/'
        return super(kpi_gsp, self.with_context(company_id=company_id)).create(vals)


    @api.depends('kpi_lines_ids')
    def compute_total(self):
        for kpi in self:
            if kpi.kpi_lines_ids:
                kpi.total_bobot = sum(line.bobot for line in kpi.kpi_lines_ids.filtered(lambda i:i.aspek_id.not_include == False))
                kpi.total_score = sum(line.score for line in kpi.kpi_lines_ids.filtered(lambda i:i.aspek_id.not_include == False))