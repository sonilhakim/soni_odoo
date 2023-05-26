# -*- coding: utf-8 -*-
# Part of Kiran Infosoft. See LICENSE file for full copyright and licensing details.

from odoo import api, models
from odoo.exceptions import ValidationError, RedirectWarning, UserError


class ListStickerPolybag(models.AbstractModel):
    _name = 'report.vit_sticker_polybag.list_sticker_polybag_report_tmpl'

    @api.model
    def _compute_list_polybag(self, data):
        lot_ids = tuple(data['lot_ids'])
        sql = """
            SELECT ph.id
            FROM stock_production_lot lot
            LEFT JOIN vit_pengukuran_header ph ON lot.project_id = ph.id
            WHERE lot.is_comp is True AND lot.id IN %s
            GROUP BY ph.id
            """
        self.env.cr.execute(sql, (lot_ids,))
        result = self.env.cr.fetchall()
        ph_ids = [r[0] for r in result]
        polybags = self.env['list.sticker.polybag'].sudo().search([('pengukuran_header_id','in',ph_ids)])
        return polybags

    @api.model
    def _get_report_values(self, docids, data=None):
        # import pdb;pdb.set_trace()
        self.model = 'list.sticker.polybag'
        wiz_rec = self.env[self._context.get('active_model', False)].browse(self._context.get('active_ids', False))
        result = self._compute_list_polybag(data)
        lot_ids = [r[0] for r in result]
        docs = self.env[self.model].browse(lot_ids)

        docargs = {
            'doc_ids': wiz_rec.ids,
            'doc_model': 'list.sticker.polybag.wizard',
            'data': data,
            'docs': wiz_rec,
            'data_dict': result,
        }
        return docargs
