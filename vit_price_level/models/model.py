from odoo import models, fields, api, _
from odoo.exceptions import Warning, UserError

# class ProductTemplatePL(models.Model):
#     _name = 'product.template'
#     _inherit = 'product.template'

#     price_level_ids = fields.One2many(comodel_name="vit.price.level",  inverse_name="product_template_id",  string="Level Harga",  help="")
    

# ProductTemplatePL()


# class PartnerPL(models.Model):
#     _name = 'res.partner'
#     _inherit = 'res.partner'

#     cust_categ = fields.Selection([('retail', 'RETAIL'), ('grosir', 'GROSIR')], string='Kategory Customer', default='retail')
#     # cust_categ = fields.Many2one("res.partner.category", "Kategory Customer")

# PartnerPL()

class ProductVariantPL(models.Model):
    _name = 'product.product'
    _inherit = 'product.product'

    
    price_level_id = fields.Many2one(comodel_name="vit.price.level",  string="Harga Jual", domain="[('product_id','=',id)]", help="")

    @api.multi
    def write(self, values):
        res = super(ProductVariantPL, self).write(values)
        if 'standard_price' in values:
            # import pdb; pdb.set_trace()
            self._compute_harga_beli()
            self._compute_profit()
            price_list = self.env['vit.price.list'].search([('product_id','=',self.id), ('level_id','=',self.price_level_id.id), ('name','=',1)])
            if price_list:
                price_list.price = self.standard_price + self.nilai_profit
        
        return res
    

ProductVariantPL()


class SaleOrderLinePL(models.Model):
    _name = 'sale.order.line'
    _inherit = 'sale.order.line'

    price_list_id = fields.Many2one(comodel_name="vit.price.list",  string="Harga Jual", domain="[('product_id','=',product_id)]", required=True, help="")

    # @api.onchange('product_id')
    # def _get_default_price_list(self):        
    #     if self.product_id:
    #         sql = " SELECT id FROM vit_price_list WHERE product_id = %s and name = 1"
    #         self.env.cr.execute(sql,(self.product_id.id,))
    #         result = self.env.cr.fetchone()
            
    #         self.price_list_id = result

    @api.onchange('product_uom', 'product_uom_qty', 'price_list_id')
    def product_uom_change(self):
        result = super(SaleOrderLinePL, self).product_uom_change()

        if self.price_list_id:
            self.price_unit = self.price_list_id.price

        return result

    # @api.onchange('product_uom', 'product_uom_qty')
    # def product_uom_change(self):
    #     result = super(SaleOrderLinePL, self).product_uom_change()
    #     if not self.order_id.partner_id:
    #         raise UserError(_('Kolom Customer tidak boleh kosong!'))

    #     if self.product_id and self.order_id.partner_id.cust_categ:
    #         sql = """
    #                 select pl.price
    #                 from vit_price_level pl
    #                 left join res_partner pc on pl.cust_categ = pc.cust_categ
    #                 left join product_product pp on pl.product_id = pp.id
    #                 where pc.id = %s and pp.id = %s
    #             """
    #         self.env.cr.execute(sql, (self.order_id.partner_id.id,self.product_id.id,))
    #         price = self.env.cr.fetchone()
    #         if price:
    #             # import pdb; pdb.set_trace()
    #             self.price_unit = float(price[0])

    #     return result


SaleOrderLinePL()