from odoo import models, fields, api, exceptions, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.float_utils import float_is_zero, float_compare
from odoo.exceptions import ValidationError, RedirectWarning, UserError


class MrpProductionFinishMove(models.Model):
    _name = "mrp.production"
    _inherit = "mrp.production"

    def _generate_finished_moves(self):
        res = super(MrpProductionFinishMove, self)._generate_finished_moves()
        cr = self.env.cr
        move = self.env['stock.move']
        if self.boq_po_line_id :
            sql = "delete from stock_move where production_id = %s"
            self.env.cr.execute(sql, (self.id,))
            # import pdb;pdb.set_trace()
            sql = """SELECT pp.id, u.id, count(lot.id)
                FROM stock_production_lot lot
                LEFT JOIN vit_boq_po_garmen_line bl ON lot.style_id = bl.id
                LEFT JOIN product_product pp ON lot.product_id = pp.id
                LEFT JOIN product_template pl ON pp.product_tmpl_id = pl.id
                LEFT JOIN uom_uom u ON pl.uom_id = u.id
                WHERE bl.id = %s AND lot.id IN %s AND lot.mo_id Is Null
                GROUP BY pp.id, u.id
                """
            cr.execute(sql, (self.boq_po_line_id.id,eval(self.boq_po_line_id.lot_selected)))
            result = cr.fetchall()
            for rec in result:
                move.create({
                    'name': self.name,
                    'date': self.date_planned_start,
                    'date_expected': self.date_planned_start,
                    'picking_type_id': self.picking_type_id.id,
                    'product_id': rec[0],
                    'product_uom': rec[1],
                    'product_uom_qty': rec[2],
                    'location_id': self.product_tmpl_id.property_stock_production.id,
                    'location_dest_id': self.location_dest_id.id,
                    'company_id': self.company_id.id,
                    'production_id': self.id,
                    'warehouse_id': self.location_dest_id.get_warehouse().id,
                    'origin': self.name,
                    'group_id': self.procurement_group_id.id,
                    'propagate': self.propagate,
                    'move_dest_ids': [(4, x.id) for x in self.move_dest_ids],
                })

        
        move._action_confirm()
        return res