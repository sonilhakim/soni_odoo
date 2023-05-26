from odoo import models, fields, api, _
from odoo.exceptions import UserError
import datetime
import sys
import logging
_logger = logging.getLogger(__name__)
import pdb

class production(models.Model):
    _inherit = 'stock.production.lot'

    is_comp = fields.Boolean( string="IS Complete", compute='_is_comp', store=True, help="")

    @api.depends('location_id')
    def _is_comp(self):
        for spl in self:
            if spl.location_id:
                data_ukur = self.env["vit.data_pengukuran"].search([('karyawan_id','=',spl.pengukuran_karyawan.id)])
                lot_ids = self.env["stock.production.lot"].search([('pengukuran_karyawan','=',spl.pengukuran_karyawan.id),('location_id','child_of',spl.location_id.id),('style_id','=',spl.style_id.id)])
                full_qty = sum(du.qty for du in data_ukur)
                count_packing = len(set(lot_ids.ids))
                if count_packing == full_qty:
                    spl.is_comp = True

production()
