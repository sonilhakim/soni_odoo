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

from odoo import api, fields, models, _
from odoo.tools import ustr
from odoo.exceptions import UserError


class AccountBudgetPost(models.Model):
    _inherit = "account.budget.post"

    uudp = fields.Boolean(string='Show on UUDP',track_visibility='onchange')

AccountBudgetPost()


class CrossoveredBudgetLines(models.Model):
    _inherit = "crossovered.budget.lines"

    practical_amount_operational_expense = fields.Monetary(compute='_compute_practical_amount_operational_expense', string='Practical Operational Amount Expense', digits=0)

    @api.multi
    def _compute_practical_amount_operational_expense(self):
        for line in self:
            result = 0.0
            date_to = self.env.context.get('wizard_date_to') or line.date_to
            date_from = self.env.context.get('wizard_date_from') or line.date_from
            if line.analytic_account_id :
                self.env.cr.execute("""
                    SELECT SUM(u.total_ajuan)
                    FROM uudp u
                    LEFT JOIN hr_department hrd ON u.department_id = hrd.id
                    WHERE u.state not in ('cancel','refuse','draft')
                        AND hrd.analytic_account_id = %s
                        AND u.company_id = %s
                        AND u.budget_position_id = %s
                        AND (u.date between %s AND %s) """,
                (line.analytic_account_id.id, line.general_budget_id.company_id.id,line.general_budget_id.id, date_from, date_to,))
                result = self.env.cr.fetchone()[0] or 0.0
            line.practical_amount_operational_expense = result

CrossoveredBudgetLines()