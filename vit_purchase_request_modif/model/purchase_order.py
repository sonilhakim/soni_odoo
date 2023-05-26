#!/usr/bin/python
#-*- coding: utf-8 -*-
from odoo import models, fields, api, _

class PurchaseOrderModif(models.Model):
    _name = "purchase.order"
    _inherit = "purchase.order"

    READONLY_STATES = {
        'purchase': [('readonly', True)],
        'done': [('readonly', True)],
        'cancel': [('readonly', True)],
    }

    
    @api.model
    def _get_nomor_or(self):
        requisition = self.env['purchase.requisition'].sudo().browse(self._context.get('active_id'))
        rec = self.env['vit.purchase_order_garmen']
        if requisition.product_request_id.sample_id:
            rec = requisition.product_request_id.sample_id.or_id.id
        elif requisition.product_request_id.po_id:
            rec = requisition.product_request_id.po_id.id
        else:
            rec = False
        return rec


    due_date = fields.Date('Due Date', states=READONLY_STATES, index=True, copy=False)
    po_id = fields.Many2one(comodel_name="vit.purchase_order_garmen", string="No. OR", default=_get_nomor_or)
    inquery_id = fields.Many2one(comodel_name="vit.marketing_inquery_garmen", string="No Inquery")
    
    # @api.onchange('requisition_id')
    # def _onchange_account_ids(self):
    #     for rec in self:
    #         rec.po_id = rec.requisition_id.product_request_id.sample_id.or_id.id

