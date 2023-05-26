# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import time
from datetime import datetime

class StockWarehouse(models.Model):
    _inherit = "stock.warehouse"

    is_utama = fields.Boolean('Utama')
    is_toko = fields.Boolean('Toko')
    is_etalase = fields.Boolean('Etalase')

class StockLocation(models.Model):
    _inherit = "stock.location"

    is_utama = fields.Boolean('Utama')
    is_toko = fields.Boolean('Toko')
    is_etalase = fields.Boolean('Etalase')

class StockPickingType(models.Model):
    _inherit = "stock.picking.type"

    is_utama = fields.Boolean('Utama')
    is_toko = fields.Boolean('Toko')
    is_etalase = fields.Boolean('Etalase')

class StockPicking(models.Model):
    _inherit = "stock.picking"

    is_do = fields.Boolean('DO')
