from odoo import api, fields, models, _
import time
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)


class StockPickingInv(models.Model):
    _name = "stock.picking"
    _inherit = "stock.picking"

    bill_number = fields.Many2one('account.invoice', 'Bill')