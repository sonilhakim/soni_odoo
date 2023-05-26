from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class PurchaseOrderCust(models.Model):
    _inherit = "purchase.order"

    no_pr       = fields.Char( 'No. PR', related='requisition_id.origin', store=True)
    customer_id = fields.Many2one( comodel_name="res.partner", string="Customer", compute='_get_customer',)

    def _get_customer(self):
        for rec in self:
            pr = self.env['vit.product.request'].search([('name','=', rec.no_pr)], limit=1)
            if pr:
                rec.customer_id = pr.partner_id.id

    @api.multi
    def button_confirm(self):
        res = super(PurchaseOrderCust, self).button_confirm()
        for order in self:
            if order.requisition_id:
                for line in order.order_line:
                    sql = "update purchase_requisition_line set product_qty = (product_qty - %s) where product_id = %s and requisition_id = %s" % (line.product_qty, line.product_id.id, order.requisition_id.id)
                    self.env.cr.execute(sql)
        return res




class po_line_custom(models.Model):
    _inherit = 'purchase.order.line'

    note = fields.Char( 'Note' )