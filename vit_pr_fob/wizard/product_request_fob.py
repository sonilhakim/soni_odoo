# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2018  Odoo SA  (http://www.vitraining.com)
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


class FOB_PR_Wizard(models.TransientModel):
    _name = "fob.pr.wizard"
    
    date = fields.Date('Date Required')
    start_number = fields.Integer(string='Start Number')
    end_number = fields.Integer(string='End Number')
    generate_type = fields.Selection([('all','All'), ('numbering','Numbering')], string="Generate Type", default='all')

    @api.multi
    def product_request_md(self):
        boq_id = self._context.get('active_id', False)
        cr = self.env.cr
        if boq_id:
            boq_obj = self.env["vit.boq_po_garmen_line"]
            pr = self.env["vit.product.request"]
            emp_obj = self.env['hr.employee']
            boq = boq_obj.browse(boq_id)
            employee = emp_obj.sudo().search([('user_id','=',self._uid)])
            if not employee :
                raise UserError(_('User ini tidak di-link-an ke master pegawai (employee) !'))
            department = employee.department_id
            if not department :
                raise UserError(_('Employee ini tidak punya department !'))            
            department = self.env['hr.department'].sudo().search([('name','=',employee.department_id.name)],limit=1)
            warehouse = department.warehouse_id
            
            sql = """SELECT pp.id, count(spl.id), pt.name, u.id
                    FROM stock_production_lot spl
                    LEFT JOIN vit_boq_po_garmen_line bl ON spl.style_id = bl.id
                    LEFT JOIN vit_purchase_order_garmen po ON bl.po_id = po.id
                    LEFT JOIN product_product pp ON spl.product_id = pp.id
                    LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
                    LEFT JOIN uom_uom u ON pt.uom_po_id = u.id
                    WHERE bl.id = %s AND spl.mo_id is Null AND spl.product_request_id is Null 
                    
                    """
            if self.generate_type == 'numbering':
                sql += ' AND spl.sequence BETWEEN %s AND %s GROUP BY pp.id, pt.id, u.id' %(self.start_number, self.end_number)
            else:
                sql += ' GROUP BY pp.id, pt.id, u.id'
            
            cr.execute(sql, (boq.id,))
            result = cr.fetchall()
            line_ids = []
            for res in result:
                # import pdb;pdb.set_trace()
                line_ids.append((0,0,{
                        'product_id'    : res[0],
                        'quantity'      : res[1],
                        'product_qty'   : res[1],
                        'name'          : res[2],
                        'product_uom_id': res[3],
                        'unit_price'    : 0.0,
                    }))
            data = {
                'user_id'       : self._uid,
                'date_required' : self.date,
                'reference'     : boq.po_id.name,
                'po_id'         : boq.po_id.id,
                'boq_po_line_id': boq.id,
                'department_id' : department.id,
                'category_id'   : boq.product_id.categ_id.id,
                'warehouse_id'  : warehouse.id or False,
                'product_request_line_ids' : line_ids,
            }
            pr_id = pr.create(data)
            sql1 = """UPDATE stock_production_lot SET product_request_id = %s
                    WHERE style_id = %s AND mo_id is Null AND product_request_id is Null      
                    """
            if self.generate_type == 'numbering':
                sql1 += ' AND sequence BETWEEN %s AND %s' %(self.start_number, self.end_number)            
            cr.execute(sql1, ( pr_id.id, boq.id,))
        return {'type': 'ir.actions.act_window_close'}

FOB_PR_Wizard()

