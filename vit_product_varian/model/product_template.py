from odoo import api, fields, models, _

class product_template(models.Model):
    _inherit = 'product.template'

    nick_name = fields.Char('Nick Name', index=True, translate=True)
    ongkos_kirim = fields.Char('Ongkos Kirim')