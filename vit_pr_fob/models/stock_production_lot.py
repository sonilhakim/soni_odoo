# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
import datetime
import logging
_logger = logging.getLogger(__name__)

class StockProductionLotFOB(models.Model):
	_inherit = 'stock.production.lot'

	product_request_id = fields.Many2one( comodel_name="vit.product.request", string="Product Request", help="")