import logging

from datetime import datetime, time
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.addons import decimal_precision as dp
from odoo.addons.resource.models.resource import HOURS_PER_DAY
from odoo.exceptions import AccessError, UserError
from odoo.tools.translate import _
from odoo.tools.float_utils import float_round

_logger = logging.getLogger(__name__)


class HolidaysAllocationBO(models.Model):
    _name = "hr.leave.allocation"
    _inherit = "hr.leave.allocation"

    number_of_days_display = fields.Float(
        'Duration (days)', compute='_compute_number_of_days_display',
        states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]}, digits=dp.get_precision('Cuti'),
        help="UX field allowing to see and modify the allocation duration, computed in days.")

    @api.onchange('date_from', 'date_to', 'employee_id')
    def _onchange_leave_dates(self):
        if self.date_from and self.date_to:
            self.number_of_days = self._get_number_of_days(self.date_from, self.date_to, self.employee_id.id)
        else:
            self.number_of_days = 0


    def _get_number_of_days(self, date_from, date_to, employee_id):
        """ Returns a float equals to the timedelta between two dates given as string."""
        if employee_id:
            employee = self.env['hr.employee'].browse(employee_id)
            return employee.get_work_days_data(date_from, date_to)['days']

        today_hours = self.env.user.company_id.resource_calendar_id.get_work_hours_count(
            datetime.combine(date_from.date(), time.min),
            datetime.combine(date_from.date(), time.max),
            False)

        return self.env.user.company_id.resource_calendar_id.get_work_hours_count(date_from, date_to) / (today_hours or HOURS_PER_DAY)

HolidaysAllocationBO()


class HolidaysRequestBO(models.Model):
    _name = "hr.leave"
    _inherit = "hr.leave"

    number_of_days_display = fields.Float(
        'Duration in days', compute='_compute_number_of_days_display', copy=False, readonly=True,
        digits=dp.get_precision('Cuti'), help='Number of days of the leave request. Used for interface.')