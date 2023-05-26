# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import Warning, UserError
import time
from datetime import datetime
import logging
_logger = logging.getLogger(__name__)
STATES = [('draft','Draft'),('confirm','Confirm'),('done','Done')]

class VitMasterDataJPP(models.Model):
    _name = 'vit.masterdata.jpp'
    _description = 'Master Data JPP'
    _order = 'sequence, id'

    name        = fields.Char(string='Name', default="New", readonly=True)
    description = fields.Char(string='Description', required=True)
    # type        = fields.Selection(string='Type', selection=[('md', 'MD'), ('ppic', 'PPIC'),], required=True)
    sequence    = fields.Integer(
                string='Sequence', required=True, default="1")

class VitPelaksanaanProduksi(models.Model):
    _name = 'vit.pelaksanaan_produksi'
    _description = 'Pelaksanaan Produksi'
    _inherit = 'mail.thread'

    name        = fields.Char(string='Name', default="New", readonly=True)
    user_id     = fields.Many2one(comodel_name='res.users', string='User', default=lambda self: self.env.uid, readonly=True)
    company_id  = fields.Many2one(comodel_name='res.company', string='Company',required=True,readonly=True,
                default=lambda self: self.env.user.company_id, track_visibility='onchange')
    date        = fields.Date( string="Date", required=False, default=lambda self: time.strftime("%Y-%m-%d"), readonly=True, states={"draft" : [("readonly",False)]}, help="")
    state       = fields.Selection(selection=STATES,  
                readonly=True, default=STATES[0][0], 
                string="State", track_visibility='onchange')
    partner_id  = fields.Many2one('res.partner','Buyer', readonly=True, states={"draft" : [("readonly",False)]})
    sph_id      = fields.Many2one('vit.marketing_sph_garmen','SPH',track_visibility='onchange', readonly=True, states={"draft" : [("readonly",False)]})
    project     = fields.Text('Project',related='sph_id.project')
    line_ids    = fields.One2many(comodel_name='vit.pelaksanaan_produksi.line', inverse_name='produksi_line_id', string='Master Data', )
    notes       = fields.Text('Notes',track_visibility='onchange')
    desc_style  = fields.Char(string='Syle', readonly=True, states={"draft" : [("readonly",False)]})

    @api.model
    def create(self, vals):
        if not vals.get("name", False) or vals["name"] == "New":
            vals["name"] = self.env["ir.sequence"].next_by_code("vit.pelaksanaan_produksi") or "Error Number!!!"
        return super(VitPelaksanaanProduksi, self).create(vals)

    @api.onchange('company_id')
    def _onchange_company_id(self):
        data_master = self.env['vit.masterdata.jpp'].sudo().search([])
        final_line = []
        line = []
        for record in data_master:
            line = [0, 0, {
                "sequence": record.sequence,
                "name": record.description,
                # "type": record.type,
            }]
            final_line.append(line)
        self.line_ids = final_line

    @api.multi
    def action_draft(self):
        self.state = STATES[0][0]

    @api.multi
    def action_confirm(self):
        # for rec in self:
        #     if rec.line_ids.filtered(lambda x:x.date_end < x.date_start):
        #         raise UserError('Tanggal selesai tidak bisa kurang dari Tanggal Mulai')
        #     if rec.line_ids.filtered(lambda x:x.type == 'md' and x.date_start == False and x.date_end == False):
        #         raise UserError('Tidak bisa confirm, jika ada data yg masih kosong')
        #     rec.line_ids.filtered(lambda x:x.type == 'md').update({'is_confirm': True})
        self.state = STATES[1][0]

    @api.multi
    def action_done(self):
        # for rec in self:
        #     if rec.line_ids.filtered(lambda x:x.date_end < x.date_start):
        #         raise UserError('Tanggal selesai tidak bisa kurang dari Tanggal Mulai')
        #     if rec.line_ids.filtered(lambda x:x.type == 'ppic' and x.date_start == False and x.date_end == False):
        #         raise UserError('Tidak bisa done, jika ada data yg masih kosong')
        #     rec.line_ids.filtered(lambda x:x.type == 'ppic').update({'is_confirm': True})
        self.state = STATES[2][0]

    @api.multi
    def unlink(self):
        for me_id in self :
            if me_id.state != STATES[0][0]:
                raise UserError("Cannot delete non draft record!")
        return super(VitPelaksanaanOrder, self).unlink()

class VitPelaksanaanProduksiLine(models.Model):
    _name = 'vit.pelaksanaan_produksi.line'
    _description = 'Pelaksanaan Produksi Line'

    name              = fields.Char(string='Name', default="New", readonly=True)
    plan              = fields.Datetime(string='Plan')
    actual            = fields.Datetime(string='Actual')
    sequence          = fields.Integer(string='Sequence', required=True, default="1")
    # type            = fields.Selection(string='Type', selection=[('md', 'MD'), ('ppic', 'PPIC'),])
    is_confirm        = fields.Boolean(string='Is a Confirm')
    produksi_line_id  = fields.Many2one(comodel_name='vit.pelaksanaan_produksi', string='Pelaksanaan produksi')
    partner_id        = fields.Many2one('res.partner','Buyer', related='produksi_line_id.partner_id')
    