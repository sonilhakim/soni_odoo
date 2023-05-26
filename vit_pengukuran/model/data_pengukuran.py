#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
import math
from odoo.exceptions import UserError, ValidationError

STATES=[('draft', 'Draft'), ('submit', 'Submitted')]

class data_pengukuran(models.Model):
    _name = "vit.data_pengukuran"
    _inherit = ['mail.thread']
    _description = "Data Pengukuran (Style)"
    _rec_name = "style_id"
    _order = "spk_id desc"
    
    @api.multi
    @api.depends('style_id', 'pengukuran_id','karyawan_id')
    def name_get(self):
        result = []
        for res in self:
            name = res.style_id.name
            if res.pengukuran_id:
                name = name + ' ('+res.pengukuran_id.name+')'
            elif res.karyawan_id and res.karyawan_id.karyawan:
                name = name + ' ('+ res.karyawan_id.karyawan+')'
            result.append((res.id, name))
        return result

    @api.multi
    def unlink(self):
        for data in self:
            if data.state != 'draft':
                raise UserError(_('Data yang bisa dihapus hanya yang berstatus draft !'))
        return super(data_pengukuran, self).unlink()

    #name        = fields.Many2one( comodel_name="product.template", required=True, string="Style Name",domain=[('sale_ok','=',True)])
    spec_type		= fields.Selection([('Normal','Normal'),('SP','SP')],string="Spec Type", required=True, default='Normal',readonly=True, states={"draft" : [("readonly",False)]})    
    variant_id      = fields.Many2one( "product.attribute",string="Variant", required=False,readonly=True, states={"draft" : [("readonly",False)]})
    size_id 		= fields.Many2one( "product.attribute.value",string="Size", required=False,readonly=True, states={"draft" : [("readonly",False)]})
    size_ids        = fields.Many2many( "product.attribute.value",string="Size(s)", required=False,readonly=True, states={"draft" : [("readonly",False)]})
    qty 			= fields.Integer( string="Qty", required=True, default=1,readonly=True, states={"draft" : [("readonly",False)]})
    karyawan_id 	= fields.Many2one( comodel_name="vit.pengukuran_karyawan",string="Karyawan",readonly=True, states={"draft" : [("readonly",False)]})
    template_id     = fields.Many2one( comodel_name="vit.template_pengukuran", required=False, string="Template Pengukuran",readonly=True, states={"draft" : [("readonly",False)]})
    style_id        = fields.Many2one( comodel_name="product.template", required=True, string="Style",domain=[('sale_ok','=',True)],readonly=True, states={"draft" : [("readonly",False)]})
    item_ids    	= fields.One2many(comodel_name="vit.data_pengukuran_item",  inverse_name="data_id",  string="Item Pengukuran",  copy=True,readonly=True, states={"draft" : [("readonly",False)]} )
    pengukuran_id   = fields.Many2one( comodel_name="vit.pengukuran",  string="Project",readonly=True, states={"draft" : [("readonly",False)]})
    pengukuran_header_id  = fields.Many2one( comodel_name="vit.pengukuran.header",  string="Project",readonly=True, states={"draft" : [("readonly",False)]})
    spk_id            = fields.Many2one( comodel_name="vit.spk_pengukuran",string="SPK",readonly=True, states={"draft" : [("readonly",False)]})
    divisi_id       = fields.Many2one( comodel_name="vit.divisi_karyawan",  string="Divisi", required=False, track_visibility='onchange')
    lokasi_id       = fields.Many2one( comodel_name='vit.lokasi_karyawan',string="Lokasi", required=False, track_visibility='onchange')
    jabatan_id      = fields.Many2one("vit.jabatan_karyawan", "Jabatan" , track_visibility='onchange')
    gender          = fields.Selection( selection=[('male','Male'), ('female','Female')], string="Gender", required=False, index=True, track_visibility='onchange')
    state        = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",  track_visibility='onchange')

    @api.onchange('variant_id')
    def onchange_variant_id(self):
        if self.variant_id :
            self.size_ids = False
            self.size_id = False

    @api.onchange('size_ids')
    def onchange_size_ids(self):
        if self.size_ids :
            self.size_id = self.size_ids[0].id

    @api.multi
    def insert_template(self):
        if self.template_id :
            if self.item_ids and self.template_id.line_ids:
                raise UserError(_('Data item pengukuran harus dihapus dulu !'))
            item_pengukuran= self.env['vit.data_pengukuran_item']
            for desc in self.template_id.line_ids:
                line = item_pengukuran.create({'data_id' : self.id,
                                                'name' : desc.name, 
                                                'size' : desc.size,
                                                'min_value' : desc.min_value,
                                                'max_value' : desc.max_value})
                line.name_onchange()

    @api.multi 
    def action_submit(self):
        for data in self :
            if data.pengukuran_id :
                if data.spk_id.karyawan_ids.filtered(lambda st:st.state == 'draft' ):
                    raise UserError(_('Di SPK (%s) masih ada data pengukuran karyawan yang berstatus draft !')% (data.spk_id.name))
                data.state = STATES[1][0] 
                data.pengukuran_id.action_done()              

data_pengukuran()


class data_pengukuran_item(models.Model):
    _name = "vit.data_pengukuran_item"
    _description = "Data Pengukuran (Items)"

    @api.onchange('size')
    def size_onchange(self):
        if self.size :
            message = False 
            if self.size < self.min_value :
                message =  _("Size yang di input (%s) kurang dari size standar pengukuran '%s' (%s), yakin data sudah benar?") % (str(round(self.size,2)),self.name,str(round(self.min_value,2)))
            elif self.size > self.max_value :
                message =  _("Size yang di input (%s) lebih dari size standar pengukuran '%s' (%s), yakin data sudah benar?") % (str(round(self.size,2)),self.name,str(round(self.max_value,2)))
            if message :
                warning_mess = {
                    'title': _('Info !'),
                    'message' : message
                }
                return {'warning': warning_mess}
        return {}  

    @api.onchange('name')
    def name_onchange(self):
        if self.name :
            item_data = []
            for record in self:
                if record.data_id.size_ids :
                    record.update({"size_spec_detail_ids": False})
                    for spec in record.data_id.size_ids:
                        item_data = [(0, 0, {
                            'size_id'   : spec.id,
                            })]
                        record.update({"size_spec_detail_ids": item_data})

    name    = fields.Char( required=True, string="Item Pengukuran",  help="")
    max_value = fields.Float('Max Value', default=100, required=True)
    min_value = fields.Float('Min Value', default=1, required=True)
    size    = fields.Float( string="Default Size", required=True, help="")
    data_id = fields.Many2one("vit.data_pengukuran", "Data Pengukuran", ondelete='cascade')
    variant_id = fields.Many2one( "product.attribute", related="data_id.variant_id",string="Variant", store=True)
    size_spec_detail_ids   = fields.One2many("vit.size_spec_details", "data_pengukuran_item_id",string="Size Spec")
 
    # def cek_duplicate_size_id(self):
    #     # cek jika ada duplicate size
    #     list_var = []
    #     for cek in self.size_spec_detail_ids :
    #         if cek.size_id.id in list_var:
    #             cek.unlink()
    #             continue
    #         list_var.append(cek.size_id.id)

    # @api.model
    # def create(self, vals):
    #     res = super(data_pengukuran_item, self).create(vals)
    #     res.cek_duplicate_size_id()
    #     return res


data_pengukuran_item()


class size_spec_details(models.Model):
    _name = "vit.size_spec_details"
    _description = "Data Pengukuran (Size Spec)"
    _rec_name = "size_id"

    @api.multi
    @api.depends('size_spec_id', 'size','size_id')
    def name_get(self):
        result = []
        for res in self:
            name = res.size_id.name
            if res.size > 0.0:
                val = math.modf(res.size)
                if val[0] == 0.0 :
                    name = name + ': '+str(int(res.size))
                else:
                    name = name + ': '+str(round(res.size,2))
            result.append((res.id, name))
        return result


    size_id = fields.Many2one( "product.attribute.value",string="Size", required=True)
    data_pengukuran_item_id = fields.Many2one( "vit.data_pengukuran_item", string="Pengukuran Item", ondelete='cascade')
    size = fields.Float("Value")


size_spec_details()
