# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

class MrpWorkorderQP(models.Model):
    _inherit = 'mrp.workorder'

    
    @api.multi
    def record_production(self):

        if self.qty_produced != sum(self.summary_produce_ids.mapped('quantity_done')):
            self.qty_produced = sum(self.summary_produce_ids.mapped('quantity_done'))

        res = super(MrpWorkorderQP, self).record_production()

        if self.next_work_order_id:
            qty_produced = sum(self.summary_produce_ids.mapped('quantity_done'))
            if self.qty_produced != qty_produced:            
                sql = "UPDATE mrp_workorder set qty_produced=%(qty)s WHERE id=%(id)s"
                self.env.cr.execute(sql, {'qty':qty_produced, 'id':self.id})

        return res
