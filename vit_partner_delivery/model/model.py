# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class PengukuranKaryawanPartnerDelivery(models.Model):
    _inherit = 'vit.pengukuran_karyawan'


    @api.multi
    def action_multi_confirm(self):
        res = super(PengukuranKaryawanPartnerDelivery, self).action_multi_confirm()
        self.create_partner_delivery()
        return res


    def create_partner_delivery(self):
        for kry in self:
            partner = self.env['res.partner'].search([('parent_id','=',kry.partner_id.id),('name','=',kry.lokasi_id.name)])
            # import pdb;pdb.set_trace()
            if not partner:
                sql = """
                        insert into res_partner (name, type, parent_id, company_id, customer, active, supplier, employee, display_name)
                        select rp.name ||' ('|| lk.name ||')', 'delivery', rp.id, rp.company_id, True, True, False, False, rp.name ||' ('|| lk.name ||')'
                        from vit_pengukuran_karyawan pk
                        left join vit_lokasi_karyawan lk on pk.lokasi_id = lk.id
                        left join res_partner rp on pk.partner_id = rp.id
                        where pk.id = %s
                        """
                self.env.cr.execute(sql, (kry.id,))