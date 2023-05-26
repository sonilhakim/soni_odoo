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
import pdb;


class WsWizard(models.TransientModel):
    _name = "md.ws.wizard"

    @api.model
    def _get_default_picking_type(self):
        if self._context.get('active_id'):
            st_obj = self.env['vit.boq_po_garmen_line']
            st_line = st_obj.browse(self._context.get('active_id'))
            company_id = st_line.po_id.company_id        
            return self.env['stock.picking.type'].search([
                ('code', '=', 'mrp_operation'),
                ('warehouse_id.company_id', '=', company_id.id)],
                limit=1).id

    @api.model
    def _get_default_location_src_id(self):
        if self._context.get('active_id'):
            st_obj = self.env['vit.boq_po_garmen_line']
            loc_obj = self.env['stock.location']
            st_line = st_obj.browse(self._context.get('active_id'))
            company_id = st_line.po_id.company_id
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
            st_obj = self.env['vit.boq_po_garmen_line']
            loc_obj = self.env['stock.location']
            st_line = st_obj.browse(self._context.get('active_id'))
            company_id = st_line.po_id.company_id
            loc_dest_id = loc_obj.search([('name','ilike','Sample MO'),('usage','=','internal'),('company_id', '=', company_id.id)],limit=1) 
            if not loc_dest_id :
                loc_dest_id = self.env['stock.picking.type'].search([
                    ('code', '=', 'mrp_operation'),
                    ('warehouse_id.company_id', '=', company_id.id)],limit=1).default_location_dest_id
            return loc_dest_id

            
    # quantity = fields.Float("Quantity MO Sample", default=1, required=True)
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
    start_number = fields.Integer(string='Start Number')
    end_number = fields.Integer(string='End Number')
    spec_type = fields.Selection([('Normal','Normal'), ('SP','SP')], string="Spec Type", default='Normal')
    generate_type = fields.Selection([('lot','LOT'), ('numbering','Numbering')], string="Generate Type", default='lot')
    lot = fields.Integer(string="LOT", default=1)


    @api.multi
    def create_worksheet(self):
        styles_id = self._context.get('active_id', False)
        if styles_id:
            st_obj = self.env['vit.boq_po_garmen_line']
            st = st_obj.browse(styles_id)            
            product_tmpl_id = st.product_id
            prod_id = self.env['product.product'].sudo().search([('product_tmpl_id','=',product_tmpl_id.id)], limit=1)
            
            if self.generate_type == 'numbering':
                select = [x for x in range(self.start_number, self.end_number + 1)]
                qty = len( st.lot_ids.filtered(lambda l: l.sequence in select).filtered(lambda x: not x.mo_id).filtered(lambda o: not o.is_print) )
                st.lot_selected = tuple(st.lot_ids.filtered(lambda l: l.sequence in select).filtered(lambda x: not x.mo_id).filtered(lambda o: not o.is_print).ids)
            elif self.generate_type == 'lot':
                qty = len( st.lot_ids.filtered(lambda l: l.lot == self.lot).filtered(lambda x: not x.mo_id).filtered(lambda o: not o.is_print) )
                st.lot_selected = tuple(st.lot_ids.filtered(lambda l: l.lot == self.lot).filtered(lambda x: not x.mo_id).filtered(lambda o: not o.is_print).ids)


            mrp_tmp = self.env['mrp.production']
            bom_tmp = self.env['mrp.bom']
            bom_line_ids = []
            for mt in st.material_ids:
                # import pdb;pdb.set_trace()
                bom_line_ids.append((0,0,{
                        'product_id'    : mt.material.id,
                        'product_qty'   : mt.cons,
                        'product_uom_id': mt.uom.id,
                    }))
            bom_datas = {
                'product_tmpl_id'           : product_tmpl_id.id,
                # 'product_id'                : prod_id.id,
                'product_qty'               : 1,
                'product_uom_id'            : st.uom_id.id,
                'routing_id'                : st.routing_id.id,
                'bom_line_ids'              : bom_line_ids,
            }
            bom = bom_tmp.create(bom_datas)
            datas = {
                'product_tmpl_id'           : product_tmpl_id.id,
                'product_id'                : prod_id.id,
                'product_uom_id'            : product_tmpl_id.uom_id.id,
                'bom_id'                    : bom.id,
                'routing_id'                : st.routing_id.id,
                'origin'                    : st.po_id.name,
                'worksheet'                 : True,
                'product_qty'               : qty,
                # 'state'                     : 'planned',
                'boq_po_line_id'            : st.id,
                'picking_type_id'           : self.picking_type_id.id,
                'location_src_id'           : self.location_src_id.id,
                'location_dest_id'          : self.location_dest_id.id,
                'date_planned_start'        : self.date_planned,
                'company_id'                : st.po_id.company_id.id,
                'partner_id'                : st.po_id.partner_id.id,
                'spec_type'                 : self.spec_type,
            }
            worksheet = mrp_tmp.create(datas)

            # st.write({'state': 'mo', 'mo_id' : mo_sample.id})
        return {'type': 'ir.actions.act_window_close', 'worksheet':worksheet.id, 'start_number':self.start_number, 'end_number':self.end_number, 'lot':self.lot, 'generate_type':self.generate_type}