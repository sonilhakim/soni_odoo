from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import float_compare, float_round
from odoo.addons import decimal_precision as dp

class StockMoveLineFinishMove(models.Model):
    _name = "stock.move.line"
    _inherit = "stock.move.line"

    is_worksheet = fields.Boolean('Is WS')


class MrpWorkorderFinishMove(models.Model):
    _name = 'mrp.workorder'
    _inherit = 'mrp.workorder'

    product_tmpl_id = fields.Many2one(
        'product.template', 'Style',
        related='production_id.product_tmpl_id', readonly=True,
        help='Technical: used in views only.', store=True)

    # complete = fields.Boolean('Complete', compute='_set_complete', store=True)
    qty_sisa = fields.Float(string='Qty Sisa', compute='_compute_sisa',)
    qty_uncomplete = fields.Float(string='Qty Uncomplete', compute='_compute_noncomplete')
    qty_cek_qa = fields.Float(string='Qty Cek QA', compute='_compute_cek_qa', store=True,)
    sample = fields.Boolean( related="production_id.sample", string="Sample", store=True,)


    def _compute_sisa(self):
        for summ in self:
            summ.qty_sisa = summ.qty_production - summ.qty_produced


    def _compute_noncomplete(self):
        for summ in self:
            lots = summ.lot_ids.filtered(lambda x: x.status_complete == 'onprogress')
            summ.qty_uncomplete = len(lots)

    @api.depends('lot_ids.is_scan_qa')
    def _compute_cek_qa(self):
        for rec in self:
            total = 0
            for line in rec.lot_ids:
                if rec.workcenter_id.done_by == 'scan_qa':
                    if line.is_scan_qa:
                        total += 1
                        if not rec.final_lot_id and rec.product_id.id == line.product_id.id:
                            rec.final_lot_id = line.id
            rec.qty_cek_qa = total

    @api.multi
    def record_production(self):
        new_produce = self.qty_producing
        # create history
        sql = """select lot.id, pp.id, pk.id
            from stock_production_lot lot
            left join mrp_workorder wo on lot.workorder_id = wo.id
            left join product_product pp on lot.product_id = pp.id
            left join vit_pengukuran_karyawan pk on lot.pengukuran_karyawan = pk.id
            WHERE wo.id = %s
            """
        if self.workcenter_id.done_by == 'numbering':
            sql += " and lot.is_numbering = True "
        if self.workcenter_id.done_by == 'scan':
            sql += ' and lot.is_scan = True '
        if self.workcenter_id.done_by == 'print':
            sql += ' and lot.is_print = True '
        self.env.cr.execute(sql, (self.id,))
        result = self.env.cr.fetchall()
        item_ids = []
        for res in result:
            item_ids.append((0,0,{
                    'lot_id'                : res[0],
                    'product_id'            : res[1],
                    'pengukuran_karyawan'   : res[2],                    
                }))
        self.env['mrp.workorder.history'].create({'name':new_produce,'workorder_id':self.id,'item_ids':item_ids})
        res = super(MrpWorkorderFinishMove, self).record_production()
        return res



    # @api.depends('production_id.product_qty','lot_ids')
    # def _set_complete(self):        
    #     for wo in self:
    #         qty_produce = wo.production_id.product_qty
    #         qty_lots = len(wo.lot_ids)
    #         if qty_produce == qty_lots:qty_production
    #             wo.complete = True

    @api.multi
    def button_complete(self):
        self.ensure_one()
        if not self.next_work_order_id :
            if self.qty_uncomplete < 1 and not self.sample:
                raise UserError(_('Tidak ada barang yang perlu diproses.'))
            # if self.complete == False:
            #     self.write({'qty_produced': len(self.lot_ids)})
            # else:
            #     self.write({'qty_produced': len(self.lot_ids),'state': 'done', 'date_finished': fields.Datetime.now()})

            # production_move = self.production_id.move_finished_ids.filtered(
            #                 lambda x:(x.state not in ('done', 'cancel')))
            # for pm in production_move:
            #     pm._action_confirm()

            # sql = """
            #         update stock_production_lot set status_complete=%(status_complete)s where workorder_id=%(id)s;
            # """
            # self.env.cr.execute(sql, {'status_complete':'finished','id':self.id,})
        
            if self.workcenter_id.done_by == 'scan_qa':
                self.qty_produced = len(self.lot_ids)
                new_produce = self.qty_uncomplete
                # create history
                sql = """select lot.id, pp.id, pk.id
                    from stock_production_lot lot
                    left join mrp_workorder wo on lot.workorder_id = wo.id
                    left join product_product pp on lot.product_id = pp.id
                    left join vit_pengukuran_karyawan pk on lot.pengukuran_karyawan = pk.id
                    WHERE wo.id = %s and lot.status_complete = %s
                    """
                self.env.cr.execute(sql, (self.id,'onprogress'))
                result = self.env.cr.fetchall()
                item_ids = []
                for res in result:
                    item_ids.append((0,0,{
                            'lot_id'                : res[0],
                            'product_id'            : res[1],
                            'pengukuran_karyawan'   : res[2],                    
                        }))
                self.env['mrp.workorder.history'].create({'name':new_produce,'workorder_id':self.id,'item_ids':item_ids})
        
                # create workorder history lot ===================
                for lot in self.lot_ids.filtered(lambda x: x.status_complete == 'onprogress'):
                    self.env.cr.execute("""
                        INSERT INTO workorder_history_lot (id, user_id, wo_from, lot_id, qty, date)
                        VALUES (nextval('workorder_history_lot_id_seq'), %s, %s, %s, %s, (now() at time zone 'UTC'))
                        """ % (self.env.user.id, self.id, lot.id, new_produce))

                sql = """
                    update stock_production_lot set status_complete=%(status_complete)s, is_return = False where workorder_id=%(id)s and status_complete=%(status)s;
                """
                self.env.cr.execute(sql, {'status_complete':'finished','id':self.id,'status':'onprogress',})
                for summary in self.summary_produce_ids:
                    lots = self.lot_ids.filtered(lambda x: x.product_id.id == summary.product_id.id)
                    t_qty = len(lots)
                    if t_qty > summary.product_uom_qty:
                        raise UserError(_("Qty done (%s) product (%s) lebih besar dari qty demand (%s)") %(str(int(t_qty)),summary.product_id.display_name,str(int(summary.product_uom_qty))))
                    summary.quantity_done = t_qty
            elif self.workcenter_id.done_by == 'numbering':
                self.qty_produced += self.qty_producing
                new_produce = self.qty_producing
                # create history
                sql = """select lot.id, pp.id, pk.id
                    from stock_production_lot lot
                    left join mrp_workorder wo on lot.workorder_id = wo.id
                    left join product_product pp on lot.product_id = pp.id
                    left join vit_pengukuran_karyawan pk on lot.pengukuran_karyawan = pk.id
                    WHERE wo.id = %s and lot.is_numbering = True and lot.status_complete = %s
                    """
                self.env.cr.execute(sql, (self.id,'onprogress'))
                result = self.env.cr.fetchall()
                item_ids = []
                for res in result:
                    item_ids.append((0,0,{
                            'lot_id'                : res[0],
                            'product_id'            : res[1],
                            'pengukuran_karyawan'   : res[2],                    
                        }))
                self.env['mrp.workorder.history'].create({'name':new_produce,'workorder_id':self.id,'item_ids':item_ids})
                for lot in self.lot_ids:
                    if lot.is_numbering:
                        summary = self.summary_produce_ids.filtered(lambda x: x.product_id.id == lot.product_id.id)                       
                        summary.quantity_done = summary.quantity_done + 1
                        sql = """
                            update stock_production_lot set status_complete=%(status_complete)s, is_return = False where workorder_id=%(wo_id)s and id=%(id)s and status_complete=%(status)s;
                        """
                        self.env.cr.execute(sql, {'status_complete':'finished','wo_id':self.id,'id':lot.id,'status':'onprogress',})

                        # create workorder history lot ===================
                        self.env.cr.execute("""
                            INSERT INTO workorder_history_lot (id, user_id, wo_from, lot_id, qty, date)
                            VALUES (nextval('workorder_history_lot_id_seq'), %s, %s, %s, %s, (now() at time zone 'UTC'))
                            """ % (self.env.user.id, self.id, lot.id, self.qty_producing))

            elif self.workcenter_id.done_by == 'print':
                self.qty_produced += self.qty_producing
                new_produce = self.qty_producing
                # create history
                sql = """select lot.id, pp.id, pk.id
                    from stock_production_lot lot
                    left join mrp_workorder wo on lot.workorder_id = wo.id
                    left join product_product pp on lot.product_id = pp.id
                    left join vit_pengukuran_karyawan pk on lot.pengukuran_karyawan = pk.id
                    WHERE wo.id = %s and lot.is_print = True and lot.status_complete = %s
                    """
                self.env.cr.execute(sql, (self.id,'onprogress'))
                result = self.env.cr.fetchall()
                item_ids = []
                for res in result:
                    item_ids.append((0,0,{
                            'lot_id'                : res[0],
                            'product_id'            : res[1],
                            'pengukuran_karyawan'   : res[2],                    
                        }))
                self.env['mrp.workorder.history'].create({'name':new_produce,'workorder_id':self.id,'item_ids':item_ids})
                for lot in self.lot_ids:
                    if lot.is_print:
                        summary = self.summary_produce_ids.filtered(lambda x: x.product_id.id == lot.product_id.id)                       
                        summary.quantity_done = summary.quantity_done + 1
                        sql = """
                            update stock_production_lot set status_complete=%(status_complete)s, is_return = False where workorder_id=%(wo_id)s and id=%(id)s and status_complete=%(status)s;
                        """
                        self.env.cr.execute(sql, {'status_complete':'finished','wo_id':self.id,'id':lot.id,'status':'onprogress',})

                        # create workorder history lot ===================
                        self.env.cr.execute("""
                            INSERT INTO workorder_history_lot (id, user_id, wo_from, lot_id, qty, date)
                            VALUES (nextval('workorder_history_lot_id_seq'), %s, %s, %s, %s, (now() at time zone 'UTC'))
                            """ % (self.env.user.id, self.id, lot.id, self.qty_producing))

            elif self.workcenter_id.done_by == 'scan':
                self.qty_produced += self.qty_producing
                new_produce = self.qty_producing
                # create history
                sql = """select lot.id, pp.id, pk.id
                    from stock_production_lot lot
                    left join mrp_workorder wo on lot.workorder_id = wo.id
                    left join product_product pp on lot.product_id = pp.id
                    left join vit_pengukuran_karyawan pk on lot.pengukuran_karyawan = pk.id
                    WHERE wo.id = %s and and lot.is_scan = True and lot.status_complete = %s
                    """
                self.env.cr.execute(sql, (self.id,'onprogress'))
                result = self.env.cr.fetchall()
                item_ids = []
                for res in result:
                    item_ids.append((0,0,{
                            'lot_id'                : res[0],
                            'product_id'            : res[1],
                            'pengukuran_karyawan'   : res[2],                    
                        }))
                self.env['mrp.workorder.history'].create({'name':new_produce,'workorder_id':self.id,'item_ids':item_ids})
                for lot in self.lot_ids:
                    if lot.is_scan:
                        summary = self.summary_produce_ids.filtered(lambda x: x.product_id.id == lot.product_id.id)                       
                        summary.quantity_done = summary.quantity_done + 1
                        sql = """
                            update stock_production_lot set status_complete=%(status_complete)s, is_return = False where workorder_id=%(wo_id)s and id=%(id)s and status_complete=%(status)s;
                        """
                        self.env.cr.execute(sql, {'status_complete':'finished','wo_id':self.id,'id':lot.id,'status':'onprogress',})

                        # create workorder history lot ===================
                        self.env.cr.execute("""
                            INSERT INTO workorder_history_lot (id, user_id, wo_from, lot_id, qty, date)
                            VALUES (nextval('workorder_history_lot_id_seq'), %s, %s, %s, %s, (now() at time zone 'UTC'))
                            """ % (self.env.user.id, self.id, lot.id, self.qty_producing))

            elif not self.workcenter_id.done_by:
                self.qty_produced = len(self.lot_ids)
                new_produce = len(self.lot_ids)
                # create history
                sql = """select lot.id, pp.id, pk.id
                    from stock_production_lot lot
                    left join mrp_workorder wo on lot.workorder_id = wo.id
                    left join product_product pp on lot.product_id = pp.id
                    left join vit_pengukuran_karyawan pk on lot.pengukuran_karyawan = pk.id
                    WHERE wo.id = %s and lot.status_complete = %s
                    """
                self.env.cr.execute(sql, (self.id,'onprogress'))
                result = self.env.cr.fetchall()
                item_ids = []
                for res in result:
                    item_ids.append((0,0,{
                            'lot_id'                : res[0],
                            'product_id'            : res[1],
                            'pengukuran_karyawan'   : res[2],                    
                        }))
                self.env['mrp.workorder.history'].create({'name':new_produce,'workorder_id':self.id,'item_ids':item_ids})
                for summary in self.summary_produce_ids:
                    lots = self.lot_ids.filtered(lambda x: x.product_id.id == summary.product_id.id)
                    if lots:
                        summary.quantity_done = len(lots)
                    else:
                        summary.quantity_done = 1
                # create workorder history lot ===================
                for lot in self.lot_ids.filtered(lambda x: x.status_complete == 'onprogress'):
                    self.env.cr.execute("""
                        INSERT INTO workorder_history_lot (id, user_id, wo_from, lot_id, qty, date)
                        VALUES (nextval('workorder_history_lot_id_seq'), %s, %s, %s, %s, (now() at time zone 'UTC'))
                        """ % (self.env.user.id, self.id, lot.id, self.qty_producing))

                sql = """
                    update stock_production_lot set status_complete=%(status_complete)s, is_return = False where workorder_id=%(id)s and status_complete=%(status)s;
                """
                self.env.cr.execute(sql, {'status_complete':'finished','id':self.id,'status':'onprogress',})              

            if self.qty_produced != sum(self.summary_produce_ids.mapped('quantity_done')):
                self.qty_produced = sum(self.summary_produce_ids.mapped('quantity_done'))

            if self.qty_produced == self.qty_production:
                self.button_finish()

        return True




    # @api.multi
    # def record_production(self):
    #     res = super(MrpWorkorderFinishMove, self).record_production()
    #     production_move = self.production_id.move_finished_ids.filtered(
    #                     lambda x: (x.state not in ('done', 'cancel')))
    #     for pm in production_move:
    #         pm.write({'state': 'draft'})

    #     move_line_lot = self.env['stock.move.line']
    #     cr = self.env.cr
    #     if self.production_id.boq_po_line_id and not self.next_work_order_id :
    #         sqld = "delete from stock_move_line where workorder_id = %s and is_worksheet is null"
    #         self.env.cr.execute(sqld, (self.id,))
    #         sql = """SELECT lot.id, pp.id
    #             FROM stock_production_lot lot
    #             LEFT JOIN mrp_workorder wo ON lot.workorder_id = wo.id
    #             LEFT JOIN mrp_production mrp ON lot.mo_id = mrp.id
    #             LEFT JOIN product_product pp ON lot.product_id = pp.id
    #             WHERE wo.id = %s
    #             """
    #         if self.workcenter_id.done_by == 'scan':
    #             sql += " AND mrp.id = %s AND lot.is_scan is true " %self.production_id.id
    #         if self.workcenter_id.done_by == 'scan_qa':
    #             sql += " AND mrp.id = %s " %self.production_id.id
    #         if self.workcenter_id.done_by == 'print':
    #             sql += " AND mrp.id = %s AND lot.is_print is true " %self.production_id.id
    #         cr.execute(sql, (self.id,))
    #         lot_g = cr.fetchall()
    #         for lg in lot_g:
                # import pdb;pdb.set_trace()
                # production_move = self.production_id.move_finished_ids.filtered(
                #         lambda x: (x.product_id.id == lg[1]) and (x.state not in ('done', 'cancel')))
                # move_line_lot.create({'move_id': production_move.id,
                #          'product_id': production_move.product_id.id,
                #          'lot_id': lg[0],
                #          'product_uom_qty': 1,
                #          'product_uom_id': production_move.product_uom.id,
                #          'qty_done': 1,
                #          'workorder_id': self.id,
                #          'location_id': production_move.location_id.id,
                #          'location_dest_id': production_move.location_dest_id.id,
                #          'picking_id': production_move.picking_id.id,
                #          'is_worksheet': True,
                # })
                ###### write stock move state
                # production_move.write({'state': 'assigned'})
                ###### update stock_production_lot
        #         sqlt ="""update stock_production_lot set workorder_id = null where id=%s """
        #         cr.execute(sqlt, (lg[0], ))

        # return res


class MrpWorkorderHistoryFM(models.Model):
    _inherit = 'mrp.workorder.history'

    item_ids = fields.One2many('mrp.workorder.history.item', 'workorder_history_id')


class MrpWorkorderHistoryItem(models.Model):
    _name = 'mrp.workorder.history.item'
    _description = 'mrp.workorder.history.item'

    workorder_history_id = fields.Many2one('mrp.workorder.history', string='Workorder History')
    lot_id               = fields.Many2one('stock.production.lot', string='Lots/Serial Numbers')
    product_id           = fields.Many2one('product.product', 'Product')
    pengukuran_karyawan = fields.Many2one('vit.pengukuran_karyawan', 'Pengukuran')
