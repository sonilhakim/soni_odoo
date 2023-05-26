from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class ProductTemplatePOtag(models.Model):
    _name = "product.template"
    _inherit = "product.template"

    analytic_tag_id = fields.Many2one('account.analytic.tag', string='Analytic Tag')

ProductTemplatePOtag()

class ProductProductPOtag(models.Model):
    _name = "product.product"
    _inherit = "product.product"

    analytic_tag_id = fields.Many2one('account.analytic.tag', string='Analytic Tag', related="product_tmpl_id.analytic_tag_id", store=True)

ProductProductPOtag()

class purchase_order_garmen_atag(models.Model):
    _name = "vit.purchase_order_garmen"
    _inherit = "vit.purchase_order_garmen"

    def create_product_jadi(self):
        res = super(purchase_order_garmen_atag, self).create_product_jadi()
        for po in self:
            # import pdb;pdb.set_trace()
            product_template = self.env['product.template'].search([('inquery_id','=',po.sph_id.proposal_id.inquery_id.id)])
            for pt in product_template:
                if pt.inquery_id.analytic_tag_id:
                    pt.analytic_tag_id = pt.inquery_id.analytic_tag_id.id
            return res

purchase_order_garmen_atag()
