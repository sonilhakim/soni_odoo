from odoo import api, fields, models, _

class product(models.Model):
    _inherit = 'product.product'

    conv_reference 	= fields.Many2one('product.product', 'Konversi Reference', ondelete="cascade")
    conv_value 		= fields.Float("Nilai Konversi")