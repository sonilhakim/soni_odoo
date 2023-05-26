# -*- coding: utf-8 -*-
from odoo import models, api, _
from odoo.exceptions import UserError
from odoo import models, fields, api, _


class AddStyleWizard(models.TransientModel):

    _name = "vit.product.style.wizard"
    _description = "Confirm style"

    pengukuran_id = fields.Many2one('vit.pengukuran', string="Project")
    pengukuran_header_id = fields.Many2one('vit.pengukuran.header', string="SPK")
    style_ids = fields.Many2many('vit.data_pengukuran', string="Style's")
    

    @api.multi
    def add_style(self):
        context = dict(self._context or {})
        active_ids = context.get('active_ids', []) or []

        for record in self.env['vit.pengukuran_karyawan'].browse(active_ids).filtered(lambda emp:emp.pengukuran_id.id == self.pengukuran_id.id):
            if record.data_ids:
                raise UserError(_("karyawan dengan nik %s sudah di add style sebelumnya")%(record.nik))
            for style in self.style_ids :
                #if style.divisi_id.id == record.divisi_id.id and style.jabatan_id.id == record.jabatan_id.id and style.lokasi_id.id == record.lokasi_id.id and style.gender == record.gender : 
                style.copy({'karyawan_id': record.id, 'pengukuran_id' :self.pengukuran_id.id})
        return {'type': 'ir.actions.act_window_close'}

AddStyleWizard()