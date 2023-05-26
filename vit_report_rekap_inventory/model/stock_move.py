from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp


class stock_move_rekap(models.Model):
    _inherit = 'stock.move'

    quantity_done = fields.Float('Quantity Done', compute='_quantity_done_compute', digits=dp.get_precision('Product Unit of Measure'), inverse='_quantity_done_set', store=True)



class product_product_rekap(models.Model):
    _inherit = 'product.product'

    qty_available = fields.Float(
        'Quantity On Hand', compute='_compute_quantities', search='_search_qty_available',
        digits=dp.get_precision('Product Unit of Measure'), store=True,
        help="Current quantity of products.\n"
             "In a context with a single Stock Location, this includes "
             "goods stored at this Location, or any of its children.\n"
             "In a context with a single Warehouse, this includes "
             "goods stored in the Stock Location of this Warehouse, or any "
             "of its children.\n"
             "stored in the Stock Location of the Warehouse of this Shop, "
             "or any of its children.\n"
             "Otherwise, this includes goods stored in any Stock Location "
             "with 'internal' type.")
    