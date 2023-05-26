#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
import time
from odoo.exceptions import UserError, ValidationError


class boq_po_garmen_line_pr_fob(models.Model):
    _inherit = 'vit.boq_po_garmen_line'
    
    fob = fields.Boolean('FOB')
    pr_count = fields.Integer(string='Hitung Worksheet', compute='_get_pr')
    
    def _get_pr(self):
        for boq in self:
            pr_ids = self.env["vit.product.request"].search([('boq_po_line_id','=',boq.id)])
            boq.pr_count = len(set(pr_ids.ids))

    @api.multi
    def action_view_pr(self):
        for boq in self:
            pr_ids = self.env["vit.product.request"].search([('boq_po_line_id','=',boq.id)])
            action = self.env.ref('vit_product_request.action_product_request').read()[0]
            if len(pr_ids) > 1:
                action['domain'] = [('id', 'in', pr_ids.ids)]
            elif len(pr_ids) == 1:
                form_view = [(self.env.ref('vit_product_request.view_product_request_form').id, 'form')]
                if 'views' in action:
                    action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
                else:
                    action['views'] = form_view
                action['res_id'] = pr_ids.ids[0]
            else:
                action = {'type': 'ir.actions.act_window_close'}
            return action

    