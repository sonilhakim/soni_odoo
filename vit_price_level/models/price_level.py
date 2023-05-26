from odoo import models, fields, api, _
from odoo.addons import decimal_precision as dp

class PriceLevel(models.Model):
    _name = 'vit.price.level'
    _description = 'vit.price.level'

    product_id          = fields.Many2one( "product.product","Product UOM",)
    name                = fields.Char( string="Name", required=True, help="")
    # cust_categ          = fields.Many2one("res.partner.category", "Kategory Customer")
    # cust_categ 			= fields.Selection([('retail', 'RETAIL'), ('grosir', 'GROSIR')], string='Kategory Customer', default='retail')
    # price               = fields.Float(string='Harga', digits=dp.get_precision('Product Price'))

    # product_template_id = fields.Many2one("product.template", "Product Template")

    list_ids  			= fields.One2many("vit.price.list", "level_id", "Daftar Harga")

    _sql_constraints = [
        ('product_id_uniq', 'unique (product_id)', 'Product tidak boleh memiliki lebih dari 1 Daftar harga!')
    ]

    @api.onchange('product_id')
    def _get_default_name(self):
        if self.product_id:
            self.name = self.product_id.display_name



class PriceList(models.Model):
    _name = 'vit.price.list'
    _description = 'vit.price.list'

    name     = fields.Integer( string="No.", required=True, help="")
    price    = fields.Float(string='Harga', digits=dp.get_precision('Product Price'))
    level_id  = fields.Many2one("vit.price.level", "Level Harga")
    product_id = fields.Many2one( "product.product","Product", related="level_id.product_id", store=True)