#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
import time
from odoo.exceptions import UserError, ValidationError
import base64
from xlrd import open_workbook

STATES=[('draft', 'Draft'), ('confirmed', 'Confirmed'), ('edp', 'EDP'), ('done','Done')]

class pengukuran(models.Model):
    _name = "vit.pengukuran"
    _inherit = ['mail.thread']
    _description = "Pengukuran"
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
                name = name + ' ('+ res.partner_id.name+')'
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
    karyawan_ids = fields.One2many(comodel_name="vit.pengukuran_karyawan",  inverse_name="pengukuran_id",  string="Karyawan",  help="", readonly=True, states={"draft" : [("readonly",False)]} )
    edp          = fields.Boolean("EDP",track_visibility='onchange')
    file         = fields.Binary("File",copy=False)
    filename     = fields.Char(string='File Name',copy=False)
    spk_line_id       = fields.Many2one(comodel_name="vit.spk_product_pengukuran", string="SPK Pengukuran Line")
    pengukuran_header_id   = fields.Many2one(comodel_name="vit.pengukuran.header",  string="Intruksi Pengukuran",)

    @api.multi
    def action_import(self):
        for project in self :
            if not project.filename.lower().endswith(('.xls', '.xlsx')):
                raise UserError(_("File yang akan diimport (%s) harus ber ekstension .xls atau .xlsx")%(project.filename))
            wb = open_workbook(file_contents=base64.decodestring(project.file))
            values = []
            
            for s in wb.sheets():
                for row in range(s.nrows):
                    col_value = []
                    for col in range(s.ncols):
                        value = (s.cell(row, col).value)
                        col_value.append(value)
                    values.append(col_value)
            products = {}
            header_found = False
            karyawan = self.env['vit.pengukuran_karyawan']
            divisi = self.env['vit.divisi_karyawan']
            jabatan = self.env['vit.jabatan_karyawan']
            lokasi = self.env['vit.lokasi_karyawan']
            for value in values :
                if len(value) > 6 :
                    continue 
                if value[0] and value[0] not in ('NAMA','NIK','DIVISI','JABATAN','LOKASI','GENDER'):
                    if not karyawan.sudo().search([('nik','=',str(value[1])),('pengukuran_id','=',project.id)]) :
                        data = {'pengukuran_id': project.id,'karyawan': str(value[0]).upper(), 'nik': str(value[1]).upper()}
                        # DIVISI
                        if type(value[2]) is float or type(value[2]) is int:
                            continue
                        divisi_name = value[2].upper()
                        if divisi_name :
                            div = divisi.sudo().search([('pengukuran_id','=',project.id),('name','=',divisi_name)],limit=1)
                            if not div :
                                div_name = divisi.create({'pengukuran_id' : project.id,'name' : divisi_name})
                                divisi_id = div_name.id
                            else:
                                divisi_id = div.id
                            data.update({'divisi_id': divisi_id})
                        # JABATAN
                        if type(value[3]) is float or type(value[3]) is int:
                            continue
                        jabatan_name = value[3].upper()
                        if jabatan_name :
                            job = jabatan.sudo().search([('pengukuran_id','=',project.id),('name','=',jabatan_name)],limit=1)
                            if not job :
                                job_name = jabatan.create({'pengukuran_id' : project.id,'name' : jabatan_name})
                                jabatan_id = job_name.id
                            else:
                                jabatan_id = job.id
                            data.update({'jabatan_id': jabatan_id})
                        # LOKASI
                        if type(value[4]) is float or type(value[4]) is int:
                            continue
                        lokasi_name = value[4].upper()
                        if lokasi_name :
                            lok = lokasi.sudo().search([('pengukuran_id','=',project.id),('name','=',lokasi_name)],limit=1)
                            if not lok :
                                lok_name = lokasi.create({'pengukuran_id' : project.id,'name' : lokasi_name})
                                lokasi_id = lok_name.id
                            else:
                                lokasi_id = lok.id
                            data.update({'lokasi_id': lokasi_id})
                        # GENDER
                        gender_name = str(value[5])
                        if gender_name :
                            gen = gender_name.lower()
                            if gen in ('male','female'):
                                gender = gen
                                data.update({'gender': gender})
                        karyawan.create(data)

    @api.model
    def create(self, vals):
        if not vals.get('name', False) or vals['name'] == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('vit.pengukuran') or 'Error Number!!!'
        return super(pengukuran, self).create(vals)

    @api.multi
    def unlink(self):
        for data in self:
            if data.state != 'draft':
                raise UserError(_('Data yang bisa dihapus hanya yang berstatus draft !'))
        return super(pengukuran, self).unlink()
    
    @api.multi 
    def action_draft(self):
        self.state = STATES[0][0]

    @api.multi 
    def action_confirm(self):
        self.state = STATES[1][0]

    @api.multi 
    def action_submit(self):
        self.state = STATES[2][0]

    @api.multi 
    def action_done(self):
        self.edp = False
        self.state = STATES[3][0]
        # product_tmpl = self.create_variant()


    # def create_variant(self):
        #import pdb;pdb.set_trace()
        # product_tmpl = self.env['product.template']
        # for ukur in self:
        #     styles = self.env['vit.data_pengukuran'].sudo().search([('pengukuran_id','=',ukur.id),('karyawan_id','=',False)])
        #     if not styles:
        #         raise UserError(_('Style dengan project %s tidak ditemukan di master style !')% (ukur.name))
        #     data = []
        #     for pro in styles.filtered(lambda var:var.variant_id and var.size_ids):
        #         data = (0, 0, {'attribute_id' : pro.variant_id.id,'value_ids' : [(6, 0, pro.size_ids.ids)] })
        #         pro.style_id.write({'attribute_line_ids' : [data]})
        #         product_tmpl |= pro.style_id
        # return product_tmpl

