#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
import time
import base64

class document_po_garmen_line(models.Model):
    _name = "vit.document_po_garmen_line"
    _description = "vit.document_po_garmen_line"

    @api.model
    def _get_default_po_id(self):
        if self._context.get('active_id'):
            po_obj = self.env['vit.purchase_order_garmen']
            po_id = po_obj.browse(self._context.get('active_id'))
            return po_id

    name = fields.Char( required=False, string="Description",  help="")
    date = fields.Date( string="Date", required=False, default=lambda self: time.strftime("%Y-%m-%d"),  help="")
    doc = fields.Binary( string="Document",  help="")
    doc_name = fields.Char( string="Document Name",)

    po_id = fields.Many2one(comodel_name="vit.purchase_order_garmen",  string="Po", default=_get_default_po_id, help="")
