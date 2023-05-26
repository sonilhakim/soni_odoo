#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class kpi_lines(models.Model):
    _name = "vit.kpi_lines"
    _description = "vit.kpi_lines"
    _order = "kpi_id,sequence,id"
    _rec_name = "aspek_id"

    name       = fields.Text(string='Description')
    satuan     = fields.Char( string="Satuan",  help="")
    bobot      = fields.Float( string="Bobot",  help="")
    target     = fields.Float( string="Target",  help="")
    realisasi  = fields.Float( string="Realisasi",  help="")
    nilai      = fields.Float( string="Nilai",  help="")
    score      = fields.Float( string="Score",  help="")
    start_date = fields.Date( string="Start date", related="kpi_id.start_date", store=True, help="")
    end_date   = fields.Date( string="End date", related="kpi_id.end_date",store=True, help="")
    display_type = fields.Selection([('line_section', "Section"), ('line_note', "Note")], default=False, help="")
    sequence   = fields.Integer(default=10, help="")
    

    kpi_id     = fields.Many2one(comodel_name="vit.kpi_gsp",  string="Kpi", ondelete='cascade', help="")
    company_id = fields.Many2one(comodel_name="res.company", related="kpi_id.company_id", string="Company", store=True, help="")
    aspek_id   = fields.Many2one(comodel_name="vit.kpi_aspek",  string="Aspek",  help="")
    parent_aspek_id = fields.Many2one(comodel_name="vit.kpi_aspek",  string="Parent Aspek", related="aspek_id.parent_aspek_id", store=True, help="")
