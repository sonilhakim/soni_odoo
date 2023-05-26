#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
import time
from odoo.exceptions import UserError, ValidationError
import base64
from xlrd import open_workbook

STATES=[('draft', 'Draft'), ('confirmed', 'Confirmed'), ('done','Done')]

class PengukuranHeader(models.Model):
    _name = "vit.pengukuran.header"
    _inherit = ['mail.thread']
    _description = "SPK Pengukuran"
    _order = 'name desc'
  
    @api.multi
    @api.depends('name', 'partner_id','karyawan_ids')
    def name_get(self):
        result = []
        for res in self:
            name = ''
            if res.name:
                name = res.name
            if res.partner_id :
                name = name + ' - '+ res.partner_id.name
            if res.project :
                name = name + ' - '+ res.project
            result.append((res.id, name))
        return result

    name         = fields.Char( readonly=True, required=True, default='New', string="Name",  track_visibility='onchange')
    state        = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",  track_visibility='onchange')
    user_id      = fields.Many2one("res.users", "User", default=lambda self: self.env.uid, track_visibility='onchange', readonly=True)
    company_id   = fields.Many2one( comodel_name="res.company",  string="Company", related='user_id.company_id', readonly=True,  track_visibility='onchange')
    date         = fields.Date( string="Date", required=True, default=lambda self: time.strftime("%Y-%m-%d"), readonly=True, states={"draft" : [("readonly",False)]}, track_visibility='onchange')
    project      = fields.Char( string="Project",  help="", readonly=True, states={"draft" : [("readonly",False)]} ,track_visibility='onchange')
    notes        = fields.Text( string="Notes",  help="", readonly=True, states={"draft" : [("readonly",False)]} ,track_visibility='onchange')    
    partner_id   = fields.Many2one( required=True, comodel_name="res.partner",  string="Customer", readonly=True, states={"draft" : [("readonly",False)]},  track_visibility='onchange')
    karyawan_ids = fields.One2many(comodel_name="vit.pengukuran_karyawan",  inverse_name="pengukuran_header_id",  string="Karyawan",  help="", readonly=True, states={"draft" : [("readonly",False)]} )
    pengukuran_ids = fields.One2many(comodel_name="vit.pengukuran",  inverse_name="pengukuran_header_id",  string="Karyawan",  help="", readonly=True, states={"draft" : [("readonly",False)]} )
    spk_id       = fields.Many2one( comodel_name="vit.spk_pengukuran",string="SPK")
    import_count = fields.Integer(string='Hitung Import', compute='_get_import')

    _sql_constraints = [
        ('cek_uniq_name', 'UNIQUE(name)', 'Nama Pengukuran Project harus uniq'),
    ]

    @api.model
    def create(self, vals):
        if not vals.get('name', False) or vals['name'] == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('vit.pengukuran.header') or 'Error Number!!!'
        return super(PengukuranHeader, self).create(vals)

    @api.multi
    def unlink(self):
        for data in self:
            if data.state != 'draft':
                raise UserError(_('Data yang bisa dihapus hanya yang berstatus draft !'))
        return super(PengukuranHeader, self).unlink()
    
    @api.multi 
    def action_draft(self):
        self.state = STATES[0][0]
        for line in self.pengukuran_ids :
            line.action_draft()

    @api.multi 
    def action_confirm(self):
        self.state = STATES[1][0]
        for line in self.pengukuran_ids :
            line.action_confirm()

    @api.multi 
    def action_done(self):
        self.state = STATES[2][0]
        for line in self.pengukuran_ids.filtered(lambda ukuran:ukuran.state != 'done') :
            line.action_done()

    @api.multi 
    def create_import_pengukuran(self):
        self.ensure_one()
        imports = self.env["vit.import.pengukuran.karyawan"]
        cr = self.env.cr
        for ph in self:
            import_id = imports.create({'project_id' : ph.id})

    def _get_import(self):
        for ph in self:
            import_ids = self.env["vit.import.pengukuran.karyawan"].search([('project_id','=',ph.id)])
            ph.import_count = len(set(import_ids.ids))

    @api.multi
    def action_view_import(self):
        for ph in self:
            import_ids = self.env["vit.import.pengukuran.karyawan"].search([('project_id','=',ph.id)])
            action = self.env.ref('vit_import_pengukuran.action_vit_import_pengukuran_karyawan').read()[0]
            if len(import_ids) > 1:
                action['domain'] = [('id', 'in', import_ids.ids)]
            elif len(import_ids) == 1:
                form_view = [(self.env.ref('vit_import_pengukuran.view_vit_import_pengukuran_karyawan_form').id, 'form')]
                if 'views' in action:
                    action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
                else:
                    action['views'] = form_view
                action['res_id'] = import_ids.ids[0]
            else:
                action = {'type': 'ir.actions.act_window_close'}
            return action

