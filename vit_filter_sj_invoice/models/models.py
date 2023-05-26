from odoo import models, fields, api, _
from odoo.exceptions import UserError
import datetime
import sys
import logging
_logger = logging.getLogger(__name__)
import pdb


class AccountInvoiceFilterSJ(models.Model):
    _name = 'account.invoice'
    _inherit = 'account.invoice'

    @api.onchange('partner_id')
    def _onchange_customer(self):
        partner_id = self.partner_id.id
        picking = self.env['stock.picking'].search([('partner_id','=',partner_id)]).ids

        domain = {'stock_picking_id': [('picking_type_code','=','outgoing'), ('state','=','done'), ('is_invoiced', '=', False)]}
        for rec in self:
            if rec.partner_id:
                domain = {'stock_picking_id': [('id','in',picking), ('picking_type_code','=','outgoing'), ('state','=','done'), ('is_invoiced', '=', False)]}
        return {'domain': domain}

    @api.multi
    def action_invoice_open(self):
        record = super(AccountInvoiceFilterSJ, self).action_invoice_open()
        for inv in self:
            if inv.surat_jalan:
                # import pdb; pdb.set_trace()
                surat_jalan = inv.surat_jalan.replace(' ', '').split(",")
                for sj in tuple(surat_jalan):
                    sql = """
                        update stock_picking set is_invoiced = true where name = %s;
                    """
                    self.env.cr.execute(sql, (sj,))

        return record

    
AccountInvoiceFilterSJ()


class StockPickingFilter(models.Model):
    _name = 'stock.picking'
    _inherit = 'stock.picking'

    is_invoiced = fields.Boolean('Invoiced',)


StockPickingFilter()
