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


class MD_PR_Wizard(models.TransientModel):
    _name = "md.pr.wizard"
    
    date = fields.Date('Date Required')

    @api.multi
    def product_request_md(self):
        po_id = self._context.get('active_id', False)
        cr = self.env.cr
        if po_id:
            po_obj = self.env["vit.purchase_order_garmen"]
            pr = self.env["vit.product.request"]
            emp_obj = self.env['hr.employee']
            po = po_obj.browse(po_id)
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
            sql = """SELECT pp.id, sum(ml.qty), pt.name, u.id, sum(ml.total)
                    FROM vit_or_material_list ml
                    LEFT JOIN vit_boq_po_garmen_line bl ON ml.boq_id = bl.id
                    LEFT JOIN vit_purchase_order_garmen po ON bl.po_id = po.id
                    LEFT JOIN product_product pp ON ml.material = pp.id
                    LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
                    LEFT JOIN uom_uom u ON ml.uom = u.id
                    WHERE po.id = %s
                    GROUP BY pp.id, pt.id, u.id
                    """
            cr.execute(sql, (po.id,))
            result = cr.fetchall()
            line_ids = []
            for res in result:
                # import pdb;pdb.set_trace()
                line_ids.append((0,0,{
                        'product_id'    : res[0],
                        'quantity'      : res[4],
                        'product_qty'   : res[4],
                        'name'          : res[2],
                        'product_uom_id': res[3],
                        'unit_price'    : 0.0,
                    }))

            data = {
                'user_id'       : self._uid,
                'date_required' : self.date,
                'reference'     : po.name,
                'po_id'         : po.id,
                'department_id' : department.id,
                'category_id'   : category.id,
                'warehouse_id'  : warehouse.id or False,
                'merchandise_pr': True,
                'product_request_line_ids' : line_ids,
            }
            pr_id = pr.create(data)
            po.update({'product_request_id':pr_id.id})
        return {'type': 'ir.actions.act_window_close'}

MD_PR_Wizard()


class Material_PR_Wizard(models.TransientModel):
    _name = "material.pr.wizard"
    
    date = fields.Date('Date Required')

    @api.multi
    def material_request_md(self):
        mat_ids = self._context.get('active_ids', False)
        cr = self.env.cr
        if mat_ids:
            mat_obj = self.env["vit.or_material_list"]
            pr = self.env["vit.product.request"]
            emp_obj = self.env['hr.employee']
            mls = mat_obj.browse(mat_ids)
            for ml in mls:
                if ml.pr == True:
                    raise UserError(_('Material sudah di PR-kan'))
            po_ids = [mat.boq_id.po_id for mat in mls if mat.boq_id.po_id.id]
            po_ids = list(set(po_ids))
            if len(po_ids) != 1:
                raise UserError(_("Semua material harus dari Job Order yang sama"))
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
            for po in po_ids:
                # mat_obj = self.env["vit.or_material_list"]
                # pr = self.env["vit.product.request"]
                # emp_obj = self.env['hr.employee']
                # ml = mat_obj.browse(mat.id)
                
                sql = """SELECT pp.id, sum(ml.qty), pt.name, u.id, sum(ml.total)
                    FROM vit_or_material_list ml
                    LEFT JOIN vit_boq_po_garmen_line bl ON ml.boq_id = bl.id
                    LEFT JOIN vit_purchase_order_garmen po ON bl.po_id = po.id
                    LEFT JOIN product_product pp ON ml.material = pp.id
                    LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
                    LEFT JOIN uom_uom u ON ml.uom = u.id
                    WHERE po.id = %s AND ml.id IN %s
                    GROUP BY pp.id, pt.id, u.id
                    """
                cr.execute(sql, (po.id,tuple(mat_ids)))
                result = cr.fetchall()
                line_ids = []
                for res in result:
                    # import pdb;pdb.set_trace()
                    line_ids.append((0,0,{
                            'product_id'    : res[0],
                            'product_qty'   : res[4],
                            'quantity'      : res[4],
                            'name'          : res[2],
                            'product_uom_id': res[3],
                            'unit_price'    : 0.0,
                        }))

                data = {
                    'user_id'       : self._uid,
                    'date_required' : self.date,
                    'reference'     : po.name_jo,
                    'department_id' : department.id,
                    'category_id'   : category.id,
                    'warehouse_id'  : warehouse.id or False,
                    'partner_id'    : po.partner_id.id,
                    'project_description'    : po.project,
                    'merchandise_pr': True,                    
                    'product_request_line_ids' : line_ids,
                }
                pr_id = pr.create(data)
                po.update({'product_request_id':pr_id.id})
                for ml in mls:
                    sql1 = "update vit_or_material_list set pr = '%s' where id = %s" % (True, ml.id)
                    cr.execute(sql1)
            return {'type': 'ir.actions.act_window_close'}

Material_PR_Wizard()