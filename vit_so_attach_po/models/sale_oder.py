from odoo import models, fields, api


class SaleOrderattpo(models.Model):
    _name = 'sale.order'
    _inherit = 'sale.order'

    po_customer = fields.Binary( string="PO Customer",  help="")
    po_customer_name = fields.Char( string="PO Customer",)
