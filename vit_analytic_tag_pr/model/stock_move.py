from odoo import api, fields, models, _
from odoo.exceptions import UserError

class StockMoveAT(models.Model):
    _name = "stock.move"
    _inherit = "stock.move"

    analytic_tag_id = fields.Many2one('account.analytic.tag', string='Analytic Tag')


    @api.model
    def create(self, values):
        res = super(StockMoveAT, self).create(values)
        # import pdb;pdb.set_trace()
        if res.picking_id.origin:
            purchase = self.env['purchase.order'].search([('name','=',res.picking_id.origin)])
            if purchase:
                for po_line in purchase.order_line:
                    for tag in po_line.analytic_tag_ids:
                        res.analytic_tag_id = tag.id
        return res

StockMoveAT()

class MrpProductionAT(models.Model):
    _inherit = 'mrp.production'

    @api.multi
    def assign_picking(self):
        res = super(MrpProductionAT, self).assign_picking()
        # import pdb;pdb.set_trace()
        for production in self:
            if production.product_tmpl_id.analytic_tag_id:
                picking = self.env['stock.picking'].search([('origin','=',production.name)])
                for pick in picking:
                    sql ="""update stock_move set analytic_tag_id = %s where picking_id=%s """
                    self.env.cr.execute(sql, (production.product_tmpl_id.analytic_tag_id.id,pick.id, ))
            return res