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


class SA_PR_Wizard(models.TransientModel):
    _name = "sa.pr.wizard"

    @api.model
    def _get_default_date(self):
        if self._context.get('active_id'):
            sa_obj = self.env["vit.sample_approval"]
            sa = sa_obj.browse(self._context.get('active_id'))
            date = sa.due_date         
            return date
    
    date = fields.Date('Date Required',default=_get_default_date)

    @api.multi
    def sa_request_rawmate(self):
        sa_id = self._context.get('active_id', False)
        cr = self.env.cr
        if sa_id:
            sa_obj = self.env["vit.sample_approval"]
            pr = self.env["vit.product.request"]
            emp_obj = self.env['hr.employee']
            sa = sa_obj.browse(sa_id)
            employee = emp_obj.sudo().search([('user_id','=',self._uid)])
            if not employee :
                raise UserError(_('User ini tidak di-link-an ke master pegawai (employee) !'))
            department = employee.department_id
            if not department :
                raise UserError(_('Employee ini tidak punya department !'))            
            department = self.env['hr.department'].sudo().search([('name','=',employee.department_id.name)],limit=1)
            warehouse = department.warehouse_id
            # department = self.env['hr.department'].search([('name','=','Marketing')])
            category = self.env['product.category'].search([('name','=','All')])
            sql = """SELECT pp.id, sum(ml.qty), pt.name, u.id
                    FROM vit_approval_material_list ml
                    LEFT JOIN vit_sample_approval_line al ON ml.approval_line_id = al.id
                    LEFT JOIN vit_sample_approval sa ON al.sample_approval_id = sa.id
                    LEFT JOIN product_product pp ON ml.material = pp.id
                    LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
                    LEFT JOIN uom_uom u ON ml.uom = u.id
                    WHERE sa.id = %s
                    GROUP BY pp.id, pt.id, u.id
                    """
            cr.execute(sql, (sa.id,))
            result = cr.fetchall()
            line_ids = []
            for res in result:
                # import pdb;pdb.set_trace()
                line_ids.append((0,0,{
                        'product_id'    : res[0],
                        'product_qty'   : res[1],
                        'quantity'      : res[1],
                        'name'          : res[2],
                        'product_uom_id': res[3],
                        'unit_price'    : 0.0,
                    }))

            data = {
                'user_id'       : self._uid,
                'date_required' : self.date,
                'reference'     : sa.name,
                'sample_id'     : sa.id,
                'department_id' : department.id,
                'category_id'   : category.id,
                'warehouse_id'  : warehouse.id or False,
                'product_request_line_ids' : line_ids,
            }
            pr_id = pr.create(data)
            sa.update({'product_request_id':pr_id.id})
        return {'type': 'ir.actions.act_window_close'}

SA_PR_Wizard()