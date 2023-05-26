# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools.misc import format_date
import time
from datetime import datetime
import math

class SaleOrderQ(models.Model):
    _inherit = "sale.order"

    need_int_trans  = fields.Boolean('Need Internal Transfer')
    need_do         = fields.Boolean('Need DO')

    # int_do_count    = fields.Integer(string='Hitung Internal DO', compute='_get_int_do')
    # surat_jalan     = fields.Boolean('Surat Jalan')

    @api.model
    def _default_warehouse_id(self):
        company = self.env.user.company_id.id
        warehouse_ids = self.env['stock.warehouse'].search([('company_id', '=', company), ('is_etalase', '=', True)], limit=1)
        return warehouse_ids

    warehouse_id = fields.Many2one(
        'stock.warehouse', string='Warehouse',
        required=True, readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
        default=_default_warehouse_id)

    @api.onchange('order_line')
    def stock_qty_onchange(self):
        for line in self.order_line:
            product_uom = self.env['product.product'].search([('product_tmpl_id','=',line.product_id.product_tmpl_id.id),('stock_quant_ids','!=', False)])
            gudang_toko = self.env['stock.quant'].search([('product_id', '=', line.product_id.id), ('location_id.usage', '=', 'internal'), ('location_id.is_toko', '=', True),])
            gudang_etalase = self.env['stock.quant'].search([('product_id', '=', line.product_id.id), ('location_id.usage', '=', 'internal'), ('location_id.is_etalase', '=', True),])
            gudang_utama = self.env['stock.quant'].search([('product_id', '=', line.product_id.id), ('location_id.usage', '=', 'internal'), ('location_id.is_utama', '=', True),])
            
            if line.product_qty_on_hand > 0.0 and gudang_etalase.quantity < line.product_uom_qty and gudang_toko.quantity > (line.product_uom_qty - gudang_etalase.quantity):
                self.need_int_trans = True

            if line.product_qty_on_hand > 0.0 and gudang_etalase.quantity <= 0.0 and gudang_toko.quantity <= 0.0 and gudang_utama.quantity > 0.0:
                self.need_do = True


    def action_confirm(self):
        for order in self:            
            if order.need_int_trans:
                raise UserError("Jumlah barang di etalase kurang, perlu internal transfer dari gudang toko, klik tombol Create Internal Transfer!")

            if order.need_do:
                raise UserError("Barang ada di gudang utama, klik tombol Create Internal DO untuk membuat transfer DO dari gudang utama!")

            result = super(SaleOrderQ, self).action_confirm()

            delivery_order = self.env['stock.picking'].search([('sale_id','=',order.id),('picking_type_code','=','outgoing'),('location_id.is_etalase','=',True)])
            if delivery_order and delivery_order.state not in ('done','cancel'):
                for line in delivery_order.move_ids_without_package:
                    line.quantity_done = line.product_uom_qty
                    # report_action = self.env.ref('stock.action_report_delivery').report_action(delivery_order)
                delivery_order.button_validate()
                # return report_action

            return result

    def action_approve_manager(self):
        res =  super(SaleOrderQ, self).action_approve_manager()
        delivery_order = self.env['stock.picking'].search([('sale_id','=',self.id),('picking_type_code','=','outgoing'),('location_id.is_etalase','=',True)])
        if delivery_order and delivery_order.state not in ('done','cancel'):
            for line in delivery_order.move_ids_without_package:
                line.quantity_done = line.product_uom_qty
            delivery_order.button_validate()

        return res

    def action_approve_admin(self):
        res =  super(SaleOrderQ, self).action_approve_admin()
        delivery_order = self.env['stock.picking'].search([('sale_id','=',self.id),('picking_type_code','=','outgoing'),('location_id.is_etalase','=',True)])
        if delivery_order and delivery_order.state not in ('done','cancel'):
            for line in delivery_order.move_ids_without_package:
                line.quantity_done = line.product_uom_qty
            delivery_order.button_validate()

        return res

    def action_approve_minimal_price(self):
        res = super(SaleOrderQ, self).action_approve_minimal_price()
        delivery_order = self.env['stock.picking'].search([('sale_id','=',self.id),('picking_type_code','=','outgoing'),('location_id.is_etalase','=',True)])
        if delivery_order and delivery_order.state not in ('done','cancel'):
            for line in delivery_order.move_ids_without_package:
                line.quantity_done = line.product_uom_qty
            delivery_order.button_validate()

        return res

    def action_approve_sale_price(self):
        res = super(SaleOrderQ, self).action_approve_sale_price()
        delivery_order = self.env['stock.picking'].search([('sale_id','=',self.id),('picking_type_code','=','outgoing'),('location_id.is_etalase','=',True)])
        if delivery_order and delivery_order.state not in ('done','cancel'):
            for line in delivery_order.move_ids_without_package:
                line.quantity_done = line.product_uom_qty
            delivery_order.button_validate()

        return res

    
    @api.multi
    def create_int_do(self):
        picking = self.env['stock.picking']
        lokasi_dest = self.env['stock.location'].search([('is_etalase', '=', True)], limit=1)
        picking_type = self.env['stock.picking.type'].search([('is_utama', '=', True), ('code', '=', 'internal')])
        sql = """SELECT pp.id, sol.product_uom_qty, sol.name, uom.id
                FROM sale_order_line sol
                LEFT JOIN sale_order so ON sol.order_id = so.id
                LEFT JOIN product_product pp ON sol.product_id = pp.id
                LEFT JOIN stock_quant sq ON sq.product_id = pp.id
                LEFT JOIN stock_location sl ON sq.location_id = sl.id
                LEFT JOIN uom_uom uom ON sol.product_uom = uom.id
                WHERE so.id = %s AND sol.product_qty_on_hand > 0.0 AND sl.is_utama is True
                """
        self.env.cr.execute(sql, (self.id,))
        result = self.env.cr.fetchall()
        line_ids = []
        for line in result:
            line_ids.append((0,0,{
                    'product_id'      : line[0],
                    'product_uom_qty' : line[1],
                    'name'            : line[2],
                    'product_uom'     : line[3],
                }))

        data = {
            'partner_id'                : self.partner_id.id,
            'location_id'               : picking_type.default_location_src_id.id,
            'location_dest_id'          : lokasi_dest.id,
            'picking_type_id'           : picking_type.id,
            'scheduled_date'            : datetime.now(),
            'origin'                    : self.name,
            'sale_id'                   : self.id,
            'is_do'                     : True,
            'move_ids_without_package'  : line_ids,
        }
        do_id = picking.create(data)
        do_id.action_assign()
        report_action = self.env.ref('stock.action_report_picking').report_action(do_id)
        self.need_do = False

        return report_action


    @api.multi
    def create_int_trans(self):
        picking = self.env['stock.picking']
        lokasi_dest = self.env['stock.location'].search([('is_etalase', '=', True)], limit=1)
        picking_type = self.env['stock.picking.type'].search([('is_toko', '=', True), ('code', '=', 'internal')])
        sql = """SELECT pp.id, sol.product_uom_qty, sol.name, uom.id
                FROM sale_order_line sol
                LEFT JOIN sale_order so ON sol.order_id = so.id
                LEFT JOIN product_product pp ON sol.product_id = pp.id
                LEFT JOIN stock_quant sq ON sq.product_id = pp.id
                LEFT JOIN stock_location sl ON sq.location_id = sl.id
                LEFT JOIN uom_uom uom ON sol.product_uom = uom.id
                WHERE so.id = %s AND sol.product_qty_on_hand > 0.0 AND sl.is_toko is True
                """
        self.env.cr.execute(sql, (self.id,))
        result = self.env.cr.fetchall()
        line_ids = []
        for line in result:
            line_ids.append((0,0,{
                    'product_id'      : line[0],
                    'product_uom_qty' : line[1],
                    'name'            : line[2],
                    'product_uom'     : line[3],
                }))

        data = {
            'partner_id'                : self.partner_id.id,
            'location_id'               : picking_type.default_location_src_id.id,
            'location_dest_id'          : lokasi_dest.id,
            'picking_type_id'           : picking_type.id,
            'scheduled_date'            : datetime.now(),
            'origin'                    : self.name,
            'sale_id'                   : self.id,
            'move_ids_without_package'  : line_ids,
        }
        int_id = picking.create(data)
        int_id.action_assign()
        self.need_int_trans = False

        return self.action_view_delivery()

