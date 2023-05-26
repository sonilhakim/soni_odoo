#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
STATES=[('draft', 'Draft'), ('confirmed','Confirmed'), ('done','Done')]

class pengukuran_karyawan(models.Model):
    _name = "vit.pengukuran_karyawan"
    _inherit = ['mail.thread']
    _description = "Pengukuran Karyawan"
    _rec_name   = "nik"
    _order = 'pengukuran_header_id desc, nik asc'


    @api.multi
    def name_get(self):
        result = []
        for rec in self:
            name = '('+rec.nik+') '+rec.karyawan
            result.append((rec.id, name))
        return result


    name            = fields.Char( required=False, string="Name",  help="")
    date =  fields.Date("Schedule Date",
        required=True,
        readonly=True,
        default=fields.Date.context_today,
        states={'draft':[('readonly',False)]},
        track_visibility='onchange'
    )
    state           = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State", track_visibility='onchange')
    karyawan        = fields.Char( string="Employee Name", required=False, track_visibility='onchange')
    nik             = fields.Char( string="NIK", required=True, track_visibility='onchange')    
    lot             = fields.Integer( string="LOT", track_visibility='onchange')    
    divisi_id       = fields.Many2one( comodel_name="vit.divisi_karyawan",  string="Divisi", required=False, track_visibility='onchange')
    lokasi_id       = fields.Many2one( comodel_name='vit.lokasi_karyawan',string="Lokasi1", required=False, track_visibility='onchange')
    lokasi2_id       = fields.Many2one( comodel_name='vit.lokasi_karyawan',string="Lokasi2", required=False, track_visibility='onchange')
    lokasi3_id       = fields.Many2one( comodel_name='vit.lokasi_karyawan',string="Lokasi3", required=False, track_visibility='onchange')
    jabatan_id      = fields.Many2one("vit.jabatan_karyawan", "Jabatan" , track_visibility='onchange')
    gender          = fields.Selection( selection=[('male','Male'), ('female','Female')], string="Gender", required=False, index=True, track_visibility='onchange')
    pengukuran_id   = fields.Many2one( comodel_name="vit.pengukuran",  string="Project")
    pengukuran_state   = fields.Selection(related='pengukuran_header_id.state',  string="Project State", store=True)
    pengukuran_header_id   = fields.Many2one(comodel_name="vit.pengukuran.header",  string="Intruksi Pengukuran",)
    partner_id      = fields.Many2one( comodel_name="res.partner", string="Customer")
    desc            = fields.Text( string="Description", track_visibility='onchange')
    spk_id            = fields.Many2one( comodel_name="vit.spk_pengukuran",string="SPK", ondelete='cascade')
    data_ids        = fields.One2many(comodel_name="vit.data_pengukuran",  inverse_name="karyawan_id",  string="Data Pengukuran",  help="" )

    _sql_constraints = [
        ('cek_unik_nik', 'UNIQUE(nik,pengukuran_header_id)',
            'NIK per project harus uniq')
    ]

    # @api.constrains('nik')
    # def unik_nik(self):
    #     # import pdb;pdb.set_trace()
    #     for k in self:
    #         pengukuran = k.env['vit.pengukuran'].search([('id','!=',k.pengukuran_id.id),('project','=',k.pengukuran_id.project)])
    #         for uk in pengukuran:                
    #             for kuk in uk.karyawan_ids:
    #                 if k.nik in [kuk.nik] :
    #                     raise ValidationError(_('NIK tidak boleh sama dalam satu project'))

    # @api.onchange('divisi_id')
    # def size_onchange(self):
    #     if not self.divisi_id:
    #         return        
    #     item_data = []
    #     for record in self:
    #         record.update({"data_ids": False})
    #         for s in record.divisi_id.style_ids:
    #             item_data = [(0, 0, {
    #                 'style_id'   : s.style_id.id,
    #                 })]
    #             record.update({"data_ids": item_data})

    @api.multi 
    def action_draft(self):
        self.state = STATES[0][0]

    @api.multi 
    def action_confirm(self):
        self.state = STATES[1][0]

    @api.multi 
    def action_done(self):
        self.state = STATES[2][0]
        # self.create_variant()
        # self.create_lot()

    @api.multi
    def unlink(self):
        for data in self:
            if data.state != 'draft':
                raise UserError(_('Data yang bisa dihapus hanya yang berstatus draft !'))
        return super(pengukuran_karyawan, self).unlink()

    def create_variant(self):
        # import pdb;pdb.set_trace()
        for pk in self:
            for pro in pk.data_ids:
                product_tmpl = pro.style_id
                attribute = product_tmpl.attribute_line_ids.filtered(lambda x : x.attribute_id == pro.variant_id)
                if not attribute:
                    data = (0, 0, {'attribute_id' : pro.variant_id.id,'value_ids' : [(6, 0, pro.size_id.ids)] })
                    product_tmpl.write({'attribute_line_ids' : [data]})
                else:
                    if pro.size_id not in attribute.value_ids:
                        for att in attribute:
                            att.write({'value_ids' : [(4, pro.size_id.id)]})
                        product_tmpl.update({'attribute_line_ids' : att})
                for pp in product_tmpl.product_variant_ids:
                    if pp.attribute_value_ids:
                        for attribute_ids in pp.attribute_value_ids:
                            pp.default_code = product_tmpl.default_code_c +'-'+ attribute_ids.name
            return True

    def create_lot(self):
        # import pdb;pdb.set_trace()        
        lot = self.env['stock.production.lot']
        for pk in self:
            for dp in pk.data_ids:
                project = dp.pengukuran_header_id.spk_id.po_id.sph_id.proposal_id.inquery_id.name
                if dp.style_id.product_variant_ids:
                    for pro in dp.style_id.product_variant_ids:
                        for val in pro.attribute_value_ids:
                            if val.id == dp.size_id.id:
                                lot.create({
                                        'name'          : project + pk.nik,
                                        'product_id'    : pro.id,
                                        'pengukuran_karyawan' : pk.id,
                                    })

pengukuran_karyawan()