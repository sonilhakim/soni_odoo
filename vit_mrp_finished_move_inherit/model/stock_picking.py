from odoo import api, fields, models, _


class StockPickingWS(models.Model):
    _inherit = 'stock.picking'

    @api.multi
    def action_done(self):      
        res = super(StockPickingWS, self).action_done()
        for pick in self:
            new_picking = self.env['stock.picking'].search([('backorder_id', '=', pick.id)])
            new_move = self.env['stock.move'].search([('picking_id', '=', new_picking.id)])
            for move in new_move:
                if move.production_id:
                    sql = "delete from stock_move_line where move_id = %s"
                    self.env.cr.execute(sql, (move.id,))
                    move.write({'state': 'confirmed'})

        return res