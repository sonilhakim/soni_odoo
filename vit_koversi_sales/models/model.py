from odoo import models, fields, api, _
from odoo.exceptions import UserError
import time
from datetime import datetime
import sys
import math
from odoo.tools import float_utils, float_compare
from odoo.addons import decimal_precision as dp
import logging
_logger = logging.getLogger(__name__)

class SaleOrderKonv(models.Model):
    _inherit = "sale.order"

    sale_id         = fields.Many2one(comodel_name="sale.order",  string="Sale Order",  help="",)
    need_konversi   = fields.Boolean('Need Konversi')
    konv_count      = fields.Integer(string='Hitung Konversi', compute='_get_konv')

    @api.onchange('order_line')
    def stock_konv_onchange(self):
        for line in self.order_line:
            product_uom = self.env['product.product'].search([('product_tmpl_id','=',line.product_id.product_tmpl_id.id),('stock_quant_ids','!=', False)])
            
            if line.product_qty_on_hand <= 0.0 and product_uom:
                self.need_konversi = True    

    @api.multi
    def action_confirm(self):
        res = super(SaleOrderKonv, self).action_confirm()
        for so in self:
            if so.need_konversi:
                so.create_konversi()

            # picking = self.env['stock.picking'].sudo().search([('origin', '=', so.name)])
            # for line in so.order_line:
            #     if line.product_uom_qty > line.product_qty_on_hand:
            #         line.action_konversi()

            #     if line.location_id:
            #         move = self.env['stock.move'].sudo().search([('picking_id', '=', picking.id),('sale_line_id', '=', line.id)])
            #         if move:
            #             move.update({ 'location_id': line.location_id,})
        return res

    # def action_approve_manager(self):
    #     res = super(SaleOrderKonv, self).action_approve_manager()
    #     for so in self:
    #         if so.need_konversi:
    #             so.create_konversi()
    #     return res

    # def action_approve_admin(self):
    #     res = super(SaleOrderKonv, self).action_approve_admin()
    #     for so in self:
    #         if so.need_konversi:
    #             so.create_konversi()
    #     return res

    # def action_approve_minimal_price(self):
    #     res = super(SaleOrderKonv, self).action_approve_minimal_price()
    #     for so in self:
    #         if so.need_konversi:
    #             so.create_konversi()
    #     return res

    # def action_approve_sale_price(self):
    #     res = super(SaleOrderKonv, self).action_approve_sale_price()
    #     for so in self:
    #         if so.need_konversi:
    #             so.create_konversi()
    #     return res


    @api.multi
    def create_konversi(self):
        konversi = self.env['product.konversi']
        # product_line = self.env['sale.order.line'].search([('order_id','=', self.id),('product_qty_on_hand','<=', 0.0)])
        lokasi = self.env['stock.location'].search([('is_etalase', '=', True)], limit=1)
        sql = """SELECT pp.id, pt.id, sol.product_uom_qty, pp.conv_value
                FROM sale_order_line sol
                LEFT JOIN sale_order so ON sol.order_id = so.id
                LEFT JOIN product_product pp ON sol.product_id = pp.id
                LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
                WHERE so.id = %s AND sol.product_qty_on_hand <= 0.0
                """
        self.env.cr.execute(sql, (self.id,))
        result = self.env.cr.fetchall()
        line_ids = []
        for line in result:
            
            # product_asal = self.env['product.product'].search([('product_tmpl_id','=',line[1]),('stock_quant_ids','!=', False)], limit=1)
            # lokasi_asal = self.env['product.product'].search([('product_tmpl_id','=',line[1]),('stock_quant_ids','!=', False)], limit=1)
            # crp = self.env.cr
            # sql = """SELECT pp.id, lok.id
            #     FROM stock_quant sq
            #     LEFT JOIN product_product pp ON sq.product_id = pp.id
            #     LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
            #     LEFT JOIN stock_location lok ON sq.location_id = lok.id
            #     WHERE pt.id = %s AND sq.quantity >= 0.0
            #     LIMIT 1
            #     """
            # crp.execute(sql, (line[1],))
            # record = crp.fetchall()
            # product_asal_id = 0
            # lokasi_asal_id = 0
            product_id = self.env['product.product'].browse(line[0])
            product_conv1 = self.env['product.product'].search([('product_tmpl_id','=',line[1]),('stock_quant_ids','!=', False),('sequence','=',(product_id.sequence) - 1)])
            product_conv2 = self.env['product.product'].search([('product_tmpl_id','=',line[1]),('stock_quant_ids','!=', False),('sequence','=',(product_id.sequence) - 2)])
            product_conv3 = self.env['product.product'].search([('product_tmpl_id','=',line[1]),('stock_quant_ids','!=', False),('sequence','=',(product_id.sequence) - 3)])
            product_asal_id = self.env['product.product']
            quant = self.env['stock.quant']
            if product_conv1:
                product_asal_id = product_conv1
                quant = quant.search([('product_id','=',product_conv1.id),('quantity','>=',0.0)],limit=1)
            elif not product_conv1 and product_conv2:
                product_asal_id = product_conv2
                quant = quant.search([('product_id','=',product_conv2.id),('quantity','>=',0.0)],limit=1)
            elif not product_conv1 and not product_conv2 and product_conv3:
                product_asal_id = product_conv3
                quant = quant.search([('product_id','=',product_conv3.id),('quantity','>=',0.0)],limit=1)
            else:
                pass
            # import pdb; pdb.set_trace()
            # qty = sol.product_uom_qty - sol.product_qty_on_hand
            # qty_a = 0.0
            # if sol.product_id.conv_value:
            #     qty_a = math.ceil((product_conv.conv_value / sol.product_id.conv_value) * qty)
            # qty_b = 0.0
            # if product_conv.conv_value:
            #     qty_b = (sol.product_id.conv_value / product_conv.conv_value) * qty_a
            # for rec in record:
            #     product_asal_id = rec[0]
            #     lokasi_asal_id = rec[1]
            # import pdb;pdb.set_trace()            
            qty = int(math.ceil(line[2] / line[3]))
            line_ids.append((0,0,{
                    'product_asal_id'   : product_asal_id.id,
                    'product_tujuan_id' : product_id.id,
                    'location_id'       : quant.location_id.id,
                    'location_dest_id'  : lokasi.id,
                    'qty_asal'          : qty,
                }))

        data = {
            'conv_date'  : datetime.now(),
            'sale_id'    : self.id,
            'detail_ids' : line_ids,
        }
        konv_id = konversi.create(data)
        konv_id.action_confirm()
        self.need_konversi = False

        # return self.action_view_konv()


    def _get_konv(self):
        for so in self:
            konv_ids = self.env["product.konversi"].search([('sale_id','=',so.id)])
            if konv_ids:
                so.konv_count = len(set(konv_ids.ids))

    @api.multi
    def action_view_konv(self):
        for so in self:
            konv_ids = self.env["product.konversi"].search([('sale_id','=',so.id)])
            action = self.env.ref('vit_product_konversi.action_koversi_list').read()[0]
            if len(konv_ids) > 1:
                action['domain'] = [('id', 'in', konv_ids.ids)]
            elif len(konv_ids) == 1:
                form_view = [(self.env.ref('vit_product_konversi.view_product_konversi_form').id, 'form')]
                if 'views' in action:
                    action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
                else:
                    action['views'] = form_view
                action['res_id'] = konv_ids.ids[0]
            else:
                action = {'type': 'ir.actions.act_window_close'}
            return action

    

SaleOrderKonv()


# class SaleOrderLineKonv(models.Model):
#     _inherit = 'sale.order.line'

#     location_id = fields.Many2one('stock.location', 'Location',)
#     parent_location = fields.Many2one('stock.location', string='Parent Location', related= 'order_id.warehouse_id.view_location_id', store=True)

    # @api.multi
    # def _prepare_procurement_values(self, group_id=False):
    #     values = super(SaleOrderLineKonv, self)._prepare_procurement_values(group_id)
    #     if self.location_id:
    #         values.update({
    #             'location_id': self.location_id,
    #         })
    #     return values

    # @api.multi
    # def action_konversi(self):
    #     product_conv = self.env['product.product']
    #     conv_details = []
    #     for sol in self:
    #         product_conv1 = product_conv.search([('product_tmpl_id','=',sol.product_id.product_tmpl_id.id),('stock_quant_ids','!=', False),('sequence','=',(sol.product_id.sequence) - 1)])
    #         product_conv2 = product_conv.search([('product_tmpl_id','=',sol.product_id.product_tmpl_id.id),('stock_quant_ids','!=', False),('sequence','=',(sol.product_id.sequence) - 2)])
    #         product_conv3 = product_conv.search([('product_tmpl_id','=',sol.product_id.product_tmpl_id.id),('stock_quant_ids','!=', False),('sequence','=',(sol.product_id.sequence) - 3)])
    #         quant = self.env['stock.quant']
    #         adjust = self.env['stock.inventory']
    #         if product_conv1:
    #             product_conv = product_conv1
    #             quant = quant.search([('product_id','=',product_conv1.id)],limit=1)
    #         elif not product_conv1 and product_conv2:
    #             product_conv = product_conv2
    #             quant = quant.search([('product_id','=',product_conv1.id)],limit=1)
    #         elif not product_conv1 and not product_conv2 and product_conv3:
    #             product_conv = product_conv3
    #             quant = quant.search([('product_id','=',product_conv1.id)],limit=1)
    #         else:
    #             pass
    #         # import pdb; pdb.set_trace()
    #         qty = sol.product_uom_qty - sol.product_qty_on_hand
    #         qty_a = 0.0
    #         if sol.product_id.conv_value:
    #             qty_a = math.ceil((product_conv.conv_value / sol.product_id.conv_value) * qty)
    #         qty_b = 0.0
    #         if product_conv.conv_value:
    #             qty_b = (sol.product_id.conv_value / product_conv.conv_value) * qty_a
    #         conv_details.append((0,0,{
    #             'product_id'        : product_conv.id,
    #             'location_id'       : quant.location_id.id,
    #             # 'prod_lot_id'       : quant.lot_id.id,
    #             'product_qty'       : quant.quantity - qty_a,
    #             }))
                        
    #         conv_details.append((0,0,{
    #         'product_id'        : sol.product_id.id,
    #         'location_id'       : sol.location_id.id,
    #         # 'prod_lot_id'       : 0,
    #         'product_qty'       : sol.product_qty_on_hand + qty_b,
    #         }))

    #         adjust_id = adjust.create({
    #                 'name': sol.order_id.name,
    #                 'date': sol.order_id.date_order,
    #                 'line_ids': conv_details,
    #                 })
    #         s_adjust = adjust.browse(adjust_id.id)
    #         s_adjust.action_start()
    #         s_adjust.action_validate()
    #         inventory_lines = s_adjust.line_ids.filtered(lambda l: l.product_id.tracking in ['lot', 'serial'] and not l.prod_lot_id and l.theoretical_qty != l.product_qty)
    #         lines = s_adjust.line_ids.filtered(lambda l: float_compare(l.product_qty, 1, precision_rounding=l.product_uom_id.rounding) > 0 and l.product_id.tracking == 'serial' and l.prod_lot_id)
    #         if inventory_lines and not lines:
    #             wiz_lines = [(0, 0, {'product_id': product.id, 'tracking': product.tracking}) for product in inventory_lines.mapped('product_id')]
    #             wiz = s_adjust.env['stock.track.confirmation'].create({'inventory_id': s_adjust.id, 'tracking_line_ids': wiz_lines})
    #             wiz.action_confirm()

    #     return True

# SaleOrderLineKonv()

class ProductKonversiSales(models.Model):
    _inherit = "product.konversi"

    sale_id = fields.Many2one(comodel_name="sale.order",  string="Sale Order",  help="",)

ProductKonversiSales()