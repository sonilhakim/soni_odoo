from odoo import models, fields, api, _
from odoo.exceptions import UserError
import datetime
import sys
import logging
_logger = logging.getLogger(__name__)
import pdb


class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    status_complete = fields.Selection([('onprogress','Onprogress'),('finished','Finish Production'),('done','Done')], string='Status Item', required=True, default='onprogress')
    