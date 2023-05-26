from odoo import tools
from odoo import fields,models,api
import time
import logging
from odoo.tools.translate import _
class ProductRequestMD(models.Model):
    _name    = "vit.product.request"
    _inherit = "vit.product.request"

    merchandise_pr = fields.Boolean(string="PR MD", default=False)
    po_id = fields.Many2one(comodel_name="vit.purchase_order_garmen", string="No. OR", readonly=True)
    