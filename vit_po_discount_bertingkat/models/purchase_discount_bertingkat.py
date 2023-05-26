# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools.misc import format_date


class PurchaseDiscountBertingkat(models.Model):
    _name = "purchase.discount.bertingkat"

    name        = fields.Char("Name", required=True, )
    partner_id = fields.Many2one('res.partner', string='Vendor', required=False, change_default=True, track_visibility='always', help="You can find a vendor by its Name, TIN, Email or Internal Reference.")
    valid_from = fields.Date('Valid From', index=True, copy=False)
    valid_until = fields.Date('Valid Until', index=True, copy=False)
    line_ids = fields.One2many('purchase.discount.bertingkat.line', 'purchase_discount_bertingkat_id', string='Discount Detail', required=True)

class PurchaseDiscountBertingkatLine(models.Model):
    _name = "purchase.discount.bertingkat.line"
    _order = "sequence asc"

    purchase_discount_bertingkat_id = fields.Many2one('purchase.discount.bertingkat', string='Discount Detail', required=True, ondelete='cascade', index=True)
    sequence = fields.Integer(string="Sequence", required=True)
    discount = fields.Float(string="Discount", required=True)
    calculate = fields.Selection([('upper', 'Upper'),('base', 'Base Price')], 'calculate', default='base')