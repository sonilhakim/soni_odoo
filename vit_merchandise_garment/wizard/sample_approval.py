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
from odoo.addons import decimal_precision as dp
import time
import base64


class JO_sample_Wizard(models.TransientModel):
    _name = "jo.sample.wizard"

    @api.model
    def _get_default_line(self):
        if self._context.get('active_id', False):
            jo_obj = self.env['vit.purchase_order_garmen']
            jo = jo_obj.browse(self._context.get('active_id', False))
            # line_ids = []
            samlines = self.env['vit.boq_po_garmen_line'].search([('po_id','=',jo.id)])
            line_ids = []
            if samlines :
                line_ids = []
                # routing_id = 0
                for sam in samlines:
                    # import pdb;pdb.set_trace()
                    # cr = self.env.cr
                    # sql = """SELECT rt.id
                    #         FROM mrp_bom bm
                    #         LEFT JOIN mrp_routing rt ON bm.routing_id = rt.id
                    #         LEFT JOIN product_template pt ON bm.product_tmpl_id = pt.id
                    #         WHERE pt.id = %s
                    #         """
                    # cr.execute(sql, (sam.sample_id.id,))
                    # result = cr.fetchall()
                    # for res in result:
                    #     routing_id = res[0]
                    line_ids.append([0,0,{'name': sam.name,'kain':sam.kain,'qty':1.0,'uom':sam.uom_id.id,'desc':sam.product_name,'boq_jo_id':sam.id}])
            return line_ids

    requester           = fields.Char( string="Request", required=True, help="" )
    recipient           = fields.Char( string="Recipient", required=True, help="" )
    due_date            = fields.Date(string="Due Date", required=True, help="")
    josamline_ids       = fields.One2many(comodel_name="jo.sample.line.wizard",  inverse_name="jo_sample_wizard_id",  string="Detail", default=_get_default_line)
        

    @api.multi
    def create_sample_approval(self):
        #import pdb;pdb.set_trace()
        jo_id = self._context.get('active_id', False)
        if jo_id:
            jo_obj = self.env['vit.purchase_order_garmen']
            jo = jo_obj.browse(jo_id)            
            sample_approval = self.env["vit.sample_approval"]
            # samline = self.env['vit.boq_po_garmen_line'].search([('po_id','=',jo.id)])
            # for sam in samline:
                # cr = self.env.cr
                # sql = """SELECT pp.default_code, pp.id, pt.spec, pt.colour, bl.product_qty, um.id
                #         FROM mrp_bom_line bl
                #         LEFT JOIN product_product pp ON bl.product_id = pp.id
                #         LEFT JOIN mrp_bom bm ON bl.bom_id = bm.id
                #         LEFT JOIN product_template pt ON bm.product_tmpl_id = pt.id
                #         LEFT JOIN uom_uom um ON bl.product_uom_id = um.id
                #         WHERE pt.id = %s
                #         """
                # cr.execute(sql, (sam.sample_id.id,))
                # result = cr.fetchall()
                # materials = self.env['vit.or_material_list'].search([('boq_id','=',sam.id)])
                # mat_data = []
                # for mat in materials:
                #     # import pdb;pdb.set_trace()
                #     mat_data.append((0, 0, {
                #         "material" : mat.material.id,
                #         "spec"     : mat.material.product_tmpl_id.spec,
                #         "colour"   : mat.material.product_tmpl_id.colour,
                #         "qty"      : mat.qty,
                #         "uom"      : mat.uom.id,
                #         }))
                # document = self.env['vit.or_line_doc'].search([('boq_id','=',sam.id)])
                # doc_data = []
                # for doc in document:
                #     doc_data.append((0,0,{
                #         'doc_name'   : doc.doc_name,
                #         'doc'        : doc.doc,
                #         'date'       : doc.date,
                #         'name'       : doc.name,
                #         }))
            line_ids = []
            for wl in self.josamline_ids:
                materials = self.env['vit.or_material_list'].search([('boq_id','=',wl.boq_jo_id.id)])
                mat_data = []
                for mat in materials:
                    # import pdb;pdb.set_trace()
                    mat_data.append((0, 0, {
                        "material" : mat.material.id,
                        "spec"     : mat.material.product_tmpl_id.spec,
                        "colour"   : mat.material.product_tmpl_id.colour,
                        "qty"      : mat.qty,
                        "uom"      : mat.uom.id,
                        "cons"     : mat.cons,
                        }))
                document = self.env['vit.or_line_doc'].search([('boq_id','=',wl.boq_jo_id.id)])
                doc_data = []
                for doc in document:
                    doc_data.append((0,0,{
                        'doc_name'   : doc.doc_name,
                        'doc'        : doc.doc,
                        'date'       : doc.date,
                        'name'       : doc.name,
                        }))
                line_ids.append((0,0,{
                    "name"          : wl.name,
                    # "xsample_id"    : wl.xsample_id.id,
                    "kain"          : wl.kain,
                    "uom"           : wl.uom.id,
                    "size"          : wl.size.id,
                    "desc"          : wl.desc,
                    # "routing_id"    : wl.routing_id.id,
                    "boq_jo_id"     : wl.boq_jo_id.id,
                    "material_ids"  : mat_data,
                    "design_ids"    : doc_data,
                    }))
            data = {
                'jo_id'         : jo.name_jo,
                'or_id'         : jo.id,
                'partner_id'    : jo.partner_id.id ,
                'project'       : jo.project,
                'notes'         : jo.note,
                'requester'     : self.requester,
                'recipient'     : self.recipient,
                'due_date'      : self.due_date,
                'line_approval_ids' : line_ids,
            }
            sam_id = sample_approval.create(data)
            jo.write({'sample_approval_id' : sam_id.name})
        return {'type': 'ir.actions.act_window_close'}

JO_sample_Wizard()

class JO_sample_line_Wizard(models.TransientModel):

    _name = "jo.sample.line.wizard"

    name            = fields.Char( required=True, string="Style",  help="")
    qty             = fields.Float( string="Qty", digits=dp.get_precision('Product Unit of Measure'),  help="")
    kain            = fields.Char( string="Kain",  help="")
    uom             = fields.Many2one(comodel_name="uom.uom", string="Satuan")
    size            = fields.Many2one( "product.attribute.value",string="Size")
    desc            = fields.Char( string="Description",  help="")    
    # xsample_id      = fields.Many2one( comodel_name="product.template",  string="XSample",  help="")
    # routing_id      = fields.Many2one(comodel_name="mrp.routing", string="Routing")
    boq_jo_id       = fields.Many2one( comodel_name="vit.boq_po_garmen_line", string="BOQ", help="")
    jo_sample_wizard_id = fields.Many2one( comodel_name="jo.sample.wizard", string="BOQ", help="")

JO_sample_line_Wizard()