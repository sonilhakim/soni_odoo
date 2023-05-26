#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
import time
from odoo.exceptions import UserError, ValidationError
import base64
from xlrd import open_workbook

class spk_pengukuran(models.Model):
    _inherit = "vit.spk_pengukuran"

    karyawan_ids = fields.One2many(comodel_name="vit.pengukuran_karyawan",  inverse_name="spk_id",  string="Karyawan", )
    file         = fields.Binary("File",copy=False)
    filename     = fields.Char(string='File Name',copy=False)
    pengukuran_header_id   = fields.Many2one(comodel_name="vit.pengukuran.header",  string="Pengukuran")


    @api.multi 
    def action_done(self):
        res = super(spk_pengukuran, self).action_done()
        for spk in self:
            # if not spk.karyawan_ids :
            #     raise UserError(_("Data karyawan belum dimasukan/import ! "))
            # cr = self.env.cr
            pengukuran_header = self.env['vit.pengukuran.header']
            pengukuran = self.env['vit.pengukuran']
            style = self.env['vit.data_pengukuran']
            pengukuran_header_id = pengukuran_header.create({'name': 'New',
                                                                'project' : spk.project,
                                                                'notes' : spk.notes or '',
                                                                'company_id':spk.company_id.id,
                                                                'partner_id': spk.partner_id.id,
                                                                'spk_id': spk.id,})
            
            for line in spk.spk_product_ids :
                pengukuran_id = pengukuran.create({'pengukuran_id' : line.id,
                                                'pengukuran_header_id': pengukuran_header_id.id,
                                                'partner_id' : spk.partner_id.id,
                                                'company_id' : spk.company_id.id,
                                                
                                                'spk_line_id' : line.id})
                style_id = style.create({'spec_type' : 'Normal',
                                            # 'variant_id' : line.variant_id.id,
                                            # 'size_id' : line.size_ids[0].id,
                                            # 'size_ids' : [ (6, 0, line.size_ids.ids )],
                                            'qty' : 1,
                                            'template_id' : line.template_id.id if line.template_id else False,
                                            'style_id' : line.product_id.id,
                                            'pengukuran_id' : pengukuran_id.id,
                                            'pengukuran_header_id': pengukuran_header_id.id,
                                            'spk_id': spk.id,
                                            })
                if style_id.template_id:
                    style_id.insert_template()
                line.write({'pengukuran_id': pengukuran_id.id})
            spk.write({'pengukuran_header_id': pengukuran_header_id.id})
            # cr.commit()
            #update data karyawan
            # sql = "update vit_pengukuran_karyawan set pengukuran_header_id=%s, partner_id=%s where spk_id=%s" % (pengukuran_header_id.id, spk.partner_id.id, spk.id)
            # cr.execute(sql)
        return res

    # @api.multi
    # def action_import(self):
    #     for spk in self :
    #         if not spk.filename.lower().endswith(('.xls', '.xlsx')):
    #             raise UserError(_("File yang akan diimport (%s) harus ber ekstension .xls atau .xlsx")%(spk.filename))
    #         wb = open_workbook(file_contents=base64.decodestring(spk.file))
    #         values = []
            
    #         for s in wb.sheets():
    #             for row in range(s.nrows):
    #                 col_value = []
    #                 for col in range(s.ncols):
    #                     value = (s.cell(row, col).value)
    #                     col_value.append(value)
    #                 values.append(col_value)
    #         products = {}
    #         header_found = False
    #         karyawan = self.env['vit.pengukuran_karyawan']
    #         spk_pengukuran = self.env['vit.spk_pengukuran']
    #         divisi = self.env['vit.divisi_karyawan']
    #         jabatan = self.env['vit.jabatan_karyawan']
    #         lokasi = self.env['vit.lokasi_karyawan']

    #         for value in values :
    #             if len(value) > 6 :
    #                 continue 
    #             if value[0] and value[0] not in ('NAMA','NIK','DIVISI','JABATAN','LOKASI','GENDER'):
    #                 if not karyawan.sudo().search([('nik','=',str(value[1])),('spk_id','=',spk.id)]) :
                        # if type(value[1]) is not str :
                        #     raise UserError(_('Kolom NIK (%s) harus bertype string')%(str(value[1])))
                        # data = {'karyawan': str(value[0]).upper(), 'nik': str(value[1]).upper(), 'spk_id': spk.id}
                        # DIVISI
                        # if type(value[2]) is float or type(value[2]) is int:
                        #     continue
                        # divisi_name = value[2].upper()
                        # if divisi_name :
                        #     div = divisi.sudo().search([('spk_id','=',spk.id),('name','=',divisi_name)],limit=1)
                        #     if not div :
                        #         div_name = divisi.create({'spk_id' : spk.id,'name' : divisi_name})
                        #         divisi_id = div_name.id
                        #     else:
                        #         divisi_id = div.id
                        #     data.update({'divisi_id': divisi_id})
                        # JABATAN
                        # if type(value[3]) is float or type(value[3]) is int:
                        #     continue
                        # jabatan_name = value[3].upper()
                        # if jabatan_name :
                        #     job = jabatan.sudo().search([('spk_id','=',spk.id),('name','=',jabatan_name)],limit=1)
                        #     if not job :
                        #         job_name = jabatan.create({'spk_id' : spk.id,'name' : jabatan_name})
                        #         jabatan_id = job_name.id
                        #     else:
                        #         jabatan_id = job.id
                        #     data.update({'jabatan_id': jabatan_id})
                        # LOKASI
                        # if type(value[4]) is float or type(value[4]) is int:
                        #     continue
                        # lokasi_name = value[4].upper()
                        # if lokasi_name :
                        #     lok = lokasi.sudo().search([('spk_id','=',spk.id),('name','=',lokasi_name)],limit=1)
                        #     if not lok :
                        #         lok_name = lokasi.create({'spk_id' : spk.id,'name' : lokasi_name})
                        #         lokasi_id = lok_name.id
                        #     else:
                        #         lokasi_id = lok.id
                        #     data.update({'lokasi_id': lokasi_id})
                        # GENDER
                        # gender_name = str(value[5])
                        # if gender_name :
                        #     gen = gender_name.lower()
                        #     if gen in ('male','female'):
                        #         gender = gen
                        #         data.update({'gender': gender})
                        #     else :
                        #         data.update({'gender': 'male'})
                        # karyawan.create(data)

spk_pengukuran()


class spk_product_pengukuran(models.Model):
    _inherit = "vit.spk_product_pengukuran"

    @api.multi
    @api.depends('spk_id', 'product_id')
    def name_get(self):
        result = []
        for res in self:
            name = ''
            if res.spk_id:
                name = res.spk_id.name
            if res.product_id :
                name = name + ' ('+ res.product_id.name+')'
            result.append((res.id, name))
        return result

    template_id     = fields.Many2one( comodel_name="vit.template_pengukuran", required=False, string="Template Pengukuran",)
    pengukuran_id = fields.Many2one("vit.pengukuran", "Pengukuran (Project)")

spk_product_pengukuran()

class spk_pengukuran_line_inherit(models.Model):

    _inherit = "vit.spk_pengukuran_line"

    method_id = fields.Many2one("vit.metode.pengukuran", "Metode")

spk_pengukuran_line_inherit()