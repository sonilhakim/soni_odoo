# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
import datetime

class StockPickingTypeKS(models.Model):
    _inherit = 'stock.picking.type'

    code = fields.Selection(selection_add=[('kasir_store', 'Kasir/Store')])
    count_ks_todo = fields.Integer(string="Number of Kasir/Store to Process",
        compute='_get_ks_count')
    count_ks_waiting = fields.Integer(string="Number of Kasir/Store Waiting",
        compute='_get_ks_count')
    count_lot_store_pass   = fields.Integer(string='Sudah melewati Store', compute='_get_lots_store')
    count_lot_store_wait   = fields.Integer(string='Belum melewati Store', compute='_get_lots_store')

    def _get_lots_store(self):
        for spt in self:
            lot_ids = self.env["stock.production.lot"].search([('location_id','child_of',spt.default_location_dest_id.id),('project_id','!=',False),('store','=',True)])
            lot_ids_wait = self.env["stock.production.lot"].search([('location_id','child_of',spt.default_location_dest_id.id),('project_id','!=',False),('store','=',False)])
            spt.count_lot_store_pass = len(set(lot_ids.ids))
            spt.count_lot_store_wait = len(set(lot_ids_wait.ids))

    def get_action_packing_list_store(self):
        for spt in self:
            lot_ids = self.env["stock.production.lot"].search([('location_id','child_of',spt.default_location_dest_id.id)])
            action = self._get_action('vit_kasir_store.action_packing_list_store')
            if lot_ids:
                action['domain'] = [('id', 'in', lot_ids.ids)]
            else:
                action = {'type': 'ir.actions.act_window_close'}
            return action

    def get_action_packing_list_store_pass(self):
        for spt in self:
            lot_ids = self.env["stock.production.lot"].search([('location_id','child_of',spt.default_location_dest_id.id),('store','=',True)])
            action = self._get_action('vit_kasir_store.action_packing_list_store')
            if lot_ids:
                action['domain'] = [('id', 'in', lot_ids.ids)]
            else:
                action = {'type': 'ir.actions.act_window_close'}
            return action

    def get_action_packing_list_store_wait(self):
        for spt in self:
            lot_ids = self.env["stock.production.lot"].search([('location_id','child_of',spt.default_location_dest_id.id),('store','=',False)])
            action = self._get_action('vit_kasir_store.action_packing_list_store')
            if lot_ids:
                action['domain'] = [('id', 'in', lot_ids.ids)]
            else:
                action = {'type': 'ir.actions.act_window_close'}
            return action

    def _get_ks_count(self):
        ks_picking_types = self.filtered(lambda picking: picking.code == 'kasir_store')
        if not ks_picking_types:
            return
        domains = {
            'count_ks_waiting': [('state', '=', 'draft')],
            'count_ks_todo': [('state', 'in', ['draft','confirm'])],
        }
        for field in domains:
            data = self.env['vit.kasir_store'].read_group(domains[field] +
                [('state', 'not in', ('done', 'cancel')), ('picking_type_id', 'in', self.ids)],
                ['picking_type_id'], ['picking_type_id'])
            count = {x['picking_type_id'] and x['picking_type_id'][0]: x['picking_type_id_count'] for x in data}
            for record in ks_picking_types:
                record[field] = count.get(record.id, 0)


    def get_ks_stock_picking_action_picking_type(self):
        return self._get_action('vit_kasir_store.kasir_store_action_picking_dashboard')
    
class StockPicking(models.Model):
    _inherit = 'stock.picking'

    # @api.multi
    # def write(self, vals):
    #     res = super(StockPicking, self).write(vals)
    #     for move_line in self.move_line_ids:
    #         if self.picking_type_id.is_setting:
    #             move_line.filtered(lambda ol: not ol.lot_id).unlink()
    #     return res

    @api.onchange('barcode')
    def add_polybag_product(self):
        if self.picking_type_id.is_setting and self.barcode:
            if self and self.state in ["done"]:
                selections = self.fields_get()["state"]["selection"]
                value = next((v[1] for v in selections if v[0] == self.state), self.state)
                self.warning = "Tidak bisa scan item dalam status " + value
                self.barcode = False
                return

            elif self:
                polybag = self.env['stock.production.lot'].search([('polybag', '=', self.barcode)])
                lots = self.env['stock.production.lot'].search([('name', '=', self.barcode)])
                if not polybag and not lots:
                    self.warning = "QR Code " + self.barcode + " tidak ditemukan!"
                    self.barcode = False
                    return

                elif polybag and not lots:
                    polybag_store = self.env['vit.summary_polybag_store'].search([('polybag_name', '=', self.barcode), ('store_id.state', '=', 'done')])
                    # import pdb;pdb.set_trace()
                    if not polybag_store:
                        self.warning = "Polybag belum melalui store!"
                        self.barcode = False
                        return
                    if polybag_store:
                        polybag_lots = self.env['stock.production.lot'].search([('polybag', '=', self.barcode),('store', '=', True),('location_id','!=',self.location_dest_id.id),('location_id.usage','!=','customer')])
                        for lot in polybag_lots:
                            search_stock_move = self.move_ids_without_package.filtered(lambda ol: ol.product_id == lot.product_id)

                            if self.lokasi_id:
                                if lot.lokasi_id.id != self.lokasi_id.id:
                                    self.warning = "Barcode tidak sesuai dengan lokasi yang dipilih!"
                                    self.barcode = False
                                    return

                            if self.po_id:
                                if lot.po_id.id != self.po_id.id:
                                    self.warning = "Barcode tidak sesuai dengan No. OR yang dipilih!"
                                    self.barcode = False
                                    return

                            if search_stock_move:
                                search_stock_move_lines = self.env['stock.move.line'].search([('lot_id', '=', lot.id), ('move_id.picking_id.picking_type_id.is_setting', '=', True)])
                                search_stock_move_line = self.move_line_ids.filtered(lambda ol: ol.lot_id.id == lot.id)

                                # warning apabila polybag pernah di scan di dokumen lain
                                if search_stock_move_lines:
                                    for ssml in search_stock_move_lines:
                                        self.warning = "Polybag sudah terdaftar di " + ssml.move_id.picking_id.name + ". Harap pindai barcode yang berbeda.!"
                                        self.barcode = False
                                        return

                                # Isi qty done jika ditemukan lot
                                if search_stock_move_line:
                                    for ssml in search_stock_move_line:
                                        search_polybag_move = self.env['stock.production.lot'].search([('polybag','=',ssml.lot_id.polybag)])
                                        for spm in search_polybag_move:
                                            if lot.polybag == spm.polybag:
                                                # import pdb;pdb.set_trace()
                                                self.warning = "Polybag " + self.barcode + " sudah pernah discan."
                                                self.barcode = False
                                                return
                                            try:
                                                ssml.qty_done = ssml.product_uom_qty
                                            except:
                                                pass

                                # insert stock.move.line jika tidak ditemukan lot
                                else:
                                    # validasi untuk check double lot di stock.move.line status done
                                    if self.backorder_id:
                                        cr = self.env.cr
                                        sql = """
                                        select sml.id from stock_move_line sml
                                        left join stock_picking sp on sp.id = sml.picking_id
                                        left join stock_production_lot spl on spl.id = sml.lot_id
                                        left join stock_location sl on sl.id = sp.location_id
                                        where sml.lot_id=%(lot_id)s and sml.picking_id=%(backorder_id)s and spl.product_id=%(product_id)s and sml.state='done' and sl.usage='production' limit 1
                                        """
                                        cr.execute(sql, {'lot_id': lot.id, 'backorder_id':self.backorder_id.id, 'product_id': lot.product_id.id})
                                        sml = cr.dictfetchall()

                                        if sml:
                                            self.warning = "Already Existing Barcode  " + self.backorder_id.name
                                            self.barcode = False
                                            return


                                    for move in self.move_ids_without_package:
                                        if lot.product_id.id == move.product_id.id:
                                            move.quantity_done = move.quantity_done + 1
                                            move.reserved_availability = move.reserved_availability + 1
                                            move.product_uom_qty = move.product_uom_qty + 1
                                            # Check picking type untuk barang jadi
                                            # picking_type_receipt_production = self.env.ref('vit_mrp_cost.picking_type_receipt_production', raise_if_not_found=True)
                                            # if picking_type_receipt_production.id != self.picking_type_id.id:
                                            #     move.product_uom_qty = move.product_uom_qty + 1

                                    stock_move_line_val = {
                                        'date'              : datetime.datetime.now(),
                                        'reference'         : self.name,
                                        'product_id'        : lot.product_id.id, 
                                        'location_id'       : self.location_id.id,
                                        'location_dest_id'  : self.location_dest_id.id,
                                        'qty_done'          : 1,
                                        # 'product_uom_qty' : 1,
                                        'product_uom_id'    : lot.product_id.uom_id,
                                        'state'             : self.state,
                                        'lot_id'            : lot.id,
                                    }
                                    new_stock_move_line = self.move_line_ids.new(stock_move_line_val)
                                    self.move_line_ids += new_stock_move_line

                            else:
                                # insert stock.move dan stock.move.line ============================
                                stock_move_val = {
                                    'name'                  : lot.product_id.name,
                                    'product_id'            : lot.product_id.id,
                                    'product_uom_qty'       : 1,
                                    'quantity_done'         : 1,
                                    'reserved_availability' : 1,
                                    'state'                 : 'draft',
                                    'product_uom'           : lot.product_id.uom_id,
                                    'picking_type_id'       : self.picking_type_id.id,
                                    'date_expected'         : datetime.datetime.now(),
                                    'location_id'           : self.location_id.id,
                                    'location_dest_id'      : self.location_dest_id.id,
                                }
                                new_stock_move = self.move_ids_without_package.new(stock_move_val)
                                self.move_ids_without_package += new_stock_move

                                stock_move_line_val = {
                                    'date'              : datetime.datetime.now(),
                                    'reference'         : self.name,
                                    'product_id'        : lot.product_id.id, 
                                    'location_id'       : self.location_id.id,
                                    'location_dest_id'  : self.location_dest_id.id,
                                    'qty_done'          : 1,
                                    # 'product_uom_qty' : 1,
                                    'product_uom_id'    : lot.product_id.uom_id,
                                    'state'             : self.state,
                                    'lot_id'            : lot.id,
                                }
                                new_stock_move_line = self.move_line_ids.new(stock_move_line_val)
                                self.move_line_ids += new_stock_move_line

                            self.warning = False
                            self.barcode = False


                elif lots and not polybag:
                    if not lots.store:
                        self.warning = "Barang belum melalui store!"
                        self.barcode = False
                        return

                    search_stock_move = self.move_ids_without_package.filtered(lambda ol: ol.product_id == lots.product_id)
                    search_stock_moves_set = self.env['stock.move'].search([('product_id', '=', lots.product_id.id),('picking_id.picking_type_id.is_setting','!=',False)])
                    
                    if self.lokasi_id:
                        if lots.lokasi_id.id != self.lokasi_id.id:
                            self.warning = "QRCode tidak sesuai dengan lokasi yang dipilih!"
                            self.barcode = False
                            return

                    if self.po_id:
                        if lots.po_id.id != self.po_id.id:
                            self.warning = "QRCode tidak sesuai dengan No. OR yang dipilih!"
                            self.barcode = False
                            return
                    
                    if search_stock_move:
                        search_stock_move_line = self.move_line_ids.filtered(lambda ol: ol.lot_id.name == self.barcode)

                        # Warning jika lot sudah terdaftar
                        if search_stock_move_line and search_stock_move.picking_id.auto_picking_id.picking_type_id.auto_picking_type_id and not search_stock_move_line.qty_done:
                            try:
                                search_stock_move_line.qty_done = search_stock_move_line.product_uom_qty
                            except:
                                pass
                        elif search_stock_move_line and search_stock_move.picking_id.picking_type_id.is_setting and search_stock_move_line.qty_done: 
                            self.warning = "Barcode sudah terdaftar. Harap pindai barcode yang berbeda."
                            self.barcode = False
                            return
                        
                        # update stock.move.line jika ditemukan lot
                        else:
                            # validasi untuk check double lot di stock.move.line status done
                            if self.backorder_id:
                                cr = self.env.cr
                                sql = """
                                select sml.id from stock_move_line sml
                                left join stock_picking sp on sp.id = sml.picking_id
                                left join stock_production_lot spl on spl.id = sml.lot_id
                                left join stock_location sl on sl.id = sp.location_id
                                where sml.lot_id=%(lot_id)s and sml.picking_id=%(backorder_id)s and spl.product_id=%(product_id)s and sml.state='done' and sl.usage='production' limit 1
                                """
                                cr.execute(sql, {'lot_id': lots.id, 'backorder_id':self.backorder_id.id, 'product_id': lots.product_id.id})
                                sml = cr.dictfetchall()

                                if sml:
                                    self.warning = "Already Existing Barcode  " + self.backorder_id.name
                                    self.barcode = False
                                    return
                            
                            for move in self.move_ids_without_package:
                                if not move.picking_id.picking_type_id.is_production and lots.product_id.id == move.product_id.id:
                                    move.quantity_done = move.quantity_done + 1
                                    move.reserved_availability = move.reserved_availability + 1
                                    move.product_uom_qty = move.product_uom_qty + 1
                                elif move.picking_id.picking_type_id.is_production and lots.product_id.id == move.product_id.id and move.reserved_availability != move.product_uom_qty:
                                    move.quantity_done = move.quantity_done + 1
                                    move.reserved_availability = move.reserved_availability + 1
                                elif move.picking_id.picking_type_id.is_production and lots.product_id.id == move.product_id.id and move.reserved_availability == move.product_uom_qty:
                                    move.quantity_done = move.quantity_done + 1

                            stock_move_line_val = {
                            'date'              : datetime.datetime.now(),
                            'reference'         : self.name,
                            'product_id'        : lots.product_id.id, 
                            'location_id'       : self.location_id.id,
                            'location_dest_id'  : self.location_dest_id.id,
                            'qty_done'          : 1,
                            # 'product_uom_qty' : 1,
                            'product_uom_id'    : lots.product_id.uom_id,
                            'state'             : self.state,
                            'lot_id'            : lots.id,
                            }
                            new_stock_move_line = self.move_line_ids.new(stock_move_line_val)
                            self.move_line_ids += new_stock_move_line
                    else:
                        # insert stock.move dan stock.move.line ============================
                        stock_move_val = {
                            'name'                  : lots.product_id.name,
                            'product_id'            : lots.product_id.id,
                            'product_uom_qty'       : 1,
                            'quantity_done'         : 1,
                            'reserved_availability' : 1,
                            'state'                 : 'draft',
                            'product_uom'           : lots.product_id.uom_id,
                            'picking_type_id'       : self.picking_type_id.id,
                            'date_expected'         : datetime.datetime.now(),
                            'location_id'           : self.location_id.id,
                            'location_dest_id'      : self.location_dest_id.id,
                        }
                        new_stock_move = self.move_ids_without_package.new(stock_move_val)
                        self.move_ids_without_package += new_stock_move

                        stock_move_line_val = {
                            'date'              : datetime.datetime.now(),
                            'reference'         : self.name,
                            'product_id'        : lots.product_id.id, 
                            'location_id'       : self.location_id.id,
                            'location_dest_id'  : self.location_dest_id.id,
                            'qty_done'          : 1,
                            # 'product_uom_qty' : 1,
                            'product_uom_id'    : lots.product_id.uom_id,
                            'state'             : self.state,
                            'lot_id'            : lots.id,
                        }
                        new_stock_move_line = self.move_line_ids.new(stock_move_line_val)
                        self.move_line_ids += new_stock_move_line
                    self.barcode = False
                    self.warning = False

                else:
                    pass