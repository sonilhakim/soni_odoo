# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2019  Odoo SA  (http://www.vitraining.com)
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

from odoo import api, fields, models, exceptions, _
import datetime
from odoo.exceptions import UserError, AccessError, ValidationError

class uudp(models.Model):
    _inherit = 'uudp'

    @api.multi
    def write(self, vals):
        _super = super(uudp, self).write(vals)
        if self.budget and self.max_budget > 0.0 :
            if self.total_ajuan > self.max_budget :
                raise UserError(_('Max revisi total Ajuan Rp. %s  \n Total nilai Ajuan saat ini Rp. %s') % (str(self.max_budget),str(self.total_ajuan)))
        return _super

    budget= fields.Boolean('Budget Available', copy=False, default=False)
    max_budget = fields.Float('Budget Value', copy=False)
    budget_position_id = fields.Many2one('account.budget.post','Budget', readonly=True, states={'draft': [('readonly', False)]})

    @api.multi
    def action_check_budget(self):
        for u in self :
            # if u.type == 'penyelesaian' :
                # continue
            # cek jika ada harga product yg masih nol
            if u.total_ajuan <= 0.0 :
                raise UserError(_('Nilai total ajuan tidak boleh nol !'))
            if not u.department_id.analytic_account_id :
                raise UserError(_('Analytic Account belum di set di master department !'))

            self.env.cr.execute("""
                    SELECT cbl.id
                    FROM crossovered_budget_lines cbl
                    LEFT JOIN crossovered_budget cb ON cbl.crossovered_budget_id = cb.id
                    WHERE cb.state = 'validate'
                        AND cbl.analytic_account_id = %s
                        AND cb.company_id = %s
                        AND (cb.date_from <= %s AND cb.date_to >= %s)
                        AND cbl.general_budget_id = %s """,
            (u.department_id.analytic_account_id.id, u.company_id.id, u.date, u.date, u.budget_position_id.id,))
            budget_exist = self.env.cr.fetchone() or False
            if not budget_exist :
                raise UserError(_('Budget belum di set / belum divalidasi ! \n \n Analytic Account : %s \n Company : %s \n Type : %s \n Ajuan (Budgetary Position) : %s \n Range Date : %s') % (str(u.department_id.analytic_account_id.name),str(u.company_id.name),'Operational UUDP',u.budget_position_id.name,str(u.date)))
            else :
                budget_line = self.env['crossovered.budget.lines']
                budget = budget_line.sudo().browse(budget_exist[0])
                total_request = budget.practical_amount_operational_expense
                total_budget = budget.planned_amount
                sisa_budget = total_budget - total_request
                if u.total_ajuan > sisa_budget :
                    rupiah = "{:,}".format(sisa_budget)
                    raise UserError(_('Sisa Budget Rp. %s silahkan sesuaikan kembali pengajuan dana/biaya anda (%s) !') % (str(rupiah),budget.crossovered_budget_id.name))
            u.write({'budget':True, 'max_budget': u.total_ajuan})
        return True

    @api.multi
    def button_cancel(self):
        for uu in self :
            uu.write({'budget':False, 'max_budget': 0.0})
        return super(uudp, self).button_cancel()

    @api.multi
    def button_set_to_draft(self):
        for uu in self :
            uu.write({'budget':False, 'max_budget': 0.0})
        return super(uudp, self).button_set_to_draft()

    @api.multi
    def button_refuse_finance(self):
        for uu in self :
            uu.write({'budget':False, 'max_budget': 0.0})
        return super(uudp, self).button_refuse_finance()

uudp() 