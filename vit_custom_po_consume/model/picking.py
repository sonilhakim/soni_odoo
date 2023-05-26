from odoo import models, fields, api, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)


class StockPickingCust(models.Model):
    _inherit = 'stock.picking'

    qty_to_produce = fields.Float('Quantity To Produce', compute='_compute_qty_produce',)
    customer_id    = fields.Many2one( comodel_name="res.partner", string="Customer", related='po_id.partner_id', store=True,)

    def _compute_qty_produce(self):
        for rec in self:
            mo = self.env['mrp.production'].search([('name','=', rec.origin)], limit=1)
            if mo:
                rec.qty_to_produce = mo.product_qty
    