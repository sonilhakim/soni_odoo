from odoo import tools
from odoo import fields,models,api
import time
import logging
from odoo.tools.translate import _
class ProductRequestFOB(models.Model):
    _inherit = "vit.product.request"

    boq_po_line_id = fields.Many2one("vit.boq_po_garmen_line", "Style List")
    