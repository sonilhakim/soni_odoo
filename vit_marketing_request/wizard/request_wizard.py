# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2017  Odoo SA  (http://www.vitraining.com)
#    All Rights Reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import datetime
from odoo.exceptions import ValidationError, RedirectWarning, UserError
from odoo import api, fields, models, SUPERUSER_ID, _


class ReqWizard(models.TransientModel):
    _name = "marketing.request.wizard"

    @api.model
    def _get_default_picking_type(self):
        if self._context.get('active_id'):
            req_obj = self.env['vit.request_detail']
            req_det = req_obj.browse(self._context.get('active_id'))
            company_id = req_det.request_line_id.request_id.company_id        
            return self.env['stock.picking.type'].search([
                ('code', '=', 'mrp_operation'),
                ('warehouse_id.company_id', '=', company_id.id)],
                limit=1).id

    @api.model
    def _get_default_location_src_id(self):
        if self._context.get('active_id'):
            req_obj = self.env['vit.request_detail']
            loc_obj = self.env['stock.location']
            req_det = req_obj.browse(self._context.get('active_id'))
            company_id = req_det.request_line_id.request_id.company_id
            loc_src_id = loc_obj.search([('name','ilike','Raw Materials'),('usage','=','internal'),('company_id', '=', company_id.id)],limit=1)
            if not loc_src_id:
                loc_src_id = self.env['stock.picking.type'].search([
                    ('name', '=', 'Consume'),
                    ('warehouse_id.company_id', '=', company_id.id)],
                    limit=1).default_location_src_id
            return loc_src_id.id


    @api.model
    def _get_default_location_dest_id(self):
        if self._context.get('active_id'):
            req_obj = self.env['vit.request_detail']
            loc_obj = self.env['stock.location']
            req_det = req_obj.browse(self._context.get('active_id'))
            company_id = req_det.request_line_id.request_id.company_id
            loc_dest_id = loc_obj.search([('name','ilike','Sample MO'),('usage','=','internal'),('company_id', '=', company_id.id)],limit=1) 
            if not loc_dest_id :
                loc_dest_id = self.env['stock.picking.type'].search([
                    ('code', '=', 'mrp_operation'),
                    ('warehouse_id.company_id', '=', company_id.id)],limit=1).default_location_dest_id
            return loc_dest_id

            
    # quantity = fields.Float("Quantity MO Sample", default=1, required=True)
    sample_room  = fields.Selection([('tebet', 'Tebet'),('cibinong', 'Cibinong')], string="Sample Room", default='tebet')
    date_planned = fields.Datetime('Plan Date', default=fields.Datetime.now, required=True)
    picking_type_id = fields.Many2one(
        'stock.picking.type', 'Picking Type',
        default=_get_default_picking_type, required=True)
    company_id = fields.Many2one('res.company','Company',default=lambda self: self.env.user.company_id)
    location_src_id = fields.Many2one(
        'stock.location', 'Raw Materials Location',
        default=_get_default_location_src_id, required=True,
        help="Location where the system will look for components.")
    location_dest_id = fields.Many2one(
        'stock.location', 'Finished Products Location',
        default=_get_default_location_dest_id, required=True,
        help="Location where the system will stock the finished products.")


    @api.multi
    def create_mo_sample(self):
        #import pdb;pdb.set_trace()
        req_detail_id = self._context.get('active_id', False)
        if req_detail_id:
            req_obj = self.env['vit.request_detail']
            req = req_obj.browse(req_detail_id)            
            product_tmpl_id = req.product_id
            prod_id = self.env['product.product'].sudo().search([('product_tmpl_id','=',product_tmpl_id.id)], limit=1)
            
            qty = 1
            if req.qty > 1 :
                qty = req.qty
            mrp_tmp = self.env['mrp.production']
            datas = {
                'product_tmpl_id'           : product_tmpl_id.id,
                'product_id'                : prod_id.id,
                'product_uom_id'            : product_tmpl_id.uom_id.id,
                'bom_id'                    : req.bom_id.id,
                'origin'                    : req.request_line_id.request_id.name,
                'sample'                    : True,
                'sample_room'               : self.sample_room,
                'request_detail_id'         : req.id,
                'product_qty'               : qty,
                'picking_type_id'           : self.picking_type_id.id,
                'location_src_id'           : self.location_src_id.id,
                'location_dest_id'          : self.location_dest_id.id,
                'date_planned_start'        : self.date_planned,
                'company_id'                : req.request_line_id.request_id.company_id.id,
                'partner_id'                : req.request_line_id.request_id.partner_id.id
            }
            mo_sample = mrp_tmp.create(datas)

            req.write({'state': 'mo'})
        return {'type': 'ir.actions.act_window_close'}