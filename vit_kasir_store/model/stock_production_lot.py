from odoo import models, fields, api, _
from odoo.exceptions import UserError
import datetime
import sys
import logging
_logger = logging.getLogger(__name__)

class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    swap_history_ids = fields.One2many('swap.history.barcode', 'lot_id')
    store = fields.Boolean('Store', default=False,)
    date_done_store = fields.Datetime(string='Store Done')


class SwapHistoryBarcode(models.Model):
    _name = 'swap.history.barcode'

    date        = fields.Datetime(string='Date')
    karyawan    = fields.Char( string="Nama")
    nik         = fields.Char( string="NIK")
    swap_lot_id = fields.Many2one('stock.production.lot', string='Lot/Serial Number')
    store_doc   = fields.Many2one('vit.kasir_store', string='No. Dokumen')
    lot_id      = fields.Many2one('stock.production.lot', string='Lot')
