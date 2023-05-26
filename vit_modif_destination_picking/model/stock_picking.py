from odoo import tools
from odoo import fields,models,api
from odoo.tools.translate import _
from odoo.exceptions import UserError

class StockPickingM(models.Model):
    _inherit = "stock.picking"

    location_dest_id = fields.Many2one(
        'stock.location', "Destination Location",
        default=lambda self: self.env['stock.picking.type'].browse(self._context.get('default_picking_type_id')).default_location_dest_id,
        readonly=True, required=True,
        states={'draft': [('readonly', False)], 'confirmed': [('readonly', False)]})