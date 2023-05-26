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

import time
import pytz
import babel
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, tools, _, SUPERUSER_ID
import pdb
import dateutil.parser

# class HRPayslip(models.Model):
#     _inherit = "hr.payslip"

#     journal_id = fields.Many2one('account.journal', 'Salary Journal', required=False)

class Hr_payslip_employee(models.TransientModel):
    _name = 'hr.payslip.employees'
    _inherit = "hr.payslip.employees"

    employee_ids = fields.Many2many('hr.employee', 'hr_employee_group_rel', 'payslip_id', 'employee_id', 'Employees')

    @api.multi
    def compute_sheet(self):
        def get_worked_day_lines(self, date_from, date_to):
            # pdb.set_trace()
            def get_weekend(day_from):
                weekday = day_from.weekday()

                attendances = self.env['resource.calendar.attendance']

                cda_obj = self.env['hr.contract'].search([('id', '=', self.contract_id.id)], order='date_start desc', limit=1)
                for attendance in cda_obj.resource_calendar_id.attendance_ids.filtered(
                    lambda att:
                        int(att.dayofweek) == weekday and
                        not (att.date_from and fields.Date.from_string(att.date_from) > day_from.date()) and
                        not (att.date_to and fields.Date.from_string(att.date_to) < day_from.date())):
                    attendances |= attendance
                test = ""
                test = ""
                return attendances


            res = []
            for contract in self.env['hr.contract'].search([('id', '=', self.contract_id.id)], order='date_start desc', limit=1).filtered(lambda contract: contract.resource_calendar_id):
                attendances = {
                     'name': _("Normal Working Days paid at 100%"),
                     'sequence': 1,
                     'code': 'Work100',
                     'number_of_days': 0.0,
                     'number_of_hours': 0.0,
                     'contract_id': contract.id,
                }
                presences = {
                     'name': _("Presences"),
                     'sequence': 2,
                     'code': 'Presences',
                     'number_of_days': 0.0,
                     'number_of_hours': 0.0,
                     'contract_id': contract.id,
                }

                alpha = {
                     'name': _("Tanpa Keterangan/Mangkir"),
                     'sequence': 3,
                     'code': 'Alpha',
                     'number_of_days': 0.0,
                     'number_of_hours': 0.0,
                     'contract_id': contract.id,            
                }

                sakit_o = {
                     'name': _("Sakit"),
                     'sequence': 4,
                     'code': 'Sakit',
                     'number_of_days': 0.0,
                     'number_of_hours': 0.0,
                     'contract_id': contract.id,            
                }

                ijin_o = {
                     'name': _("Ijin"),
                     'sequence': 5,
                     'code': 'Ijin',
                     'number_of_days': 0.0,
                     'number_of_hours': 0.0,
                     'contract_id': contract.id,            
                }

                cutilibur_o = {
                     'name': _("Cuti/Libur/Public holidays"),
                     'sequence': 6,
                     'code': 'Cutilibur',
                     'number_of_days': 0.0,
                     'number_of_hours': 0.0,
                     'contract_id': contract.id,            
                }

                overtime = {
                     'name': _("Lembur Biasa"),
                     'sequence': 7,
                     'code': 'Overtime',
                     'number_of_days': 0.0,
                     'number_of_hours': 0.0,
                     'contract_id': contract.id,
                }

                overtime2 = {
                     'name': _("Lembur Off in"),
                     'sequence': 8,
                     'code': 'Overtime2',
                     'number_of_days': 0.0,
                     'number_of_hours': 0.0,
                     'contract_id': contract.id,
                }

                overtime3 = {
                     'name': _("Lembur istimewa"),
                     'sequence': 9,
                     'code': 'Overtime3',
                     'number_of_days': 0.0,
                     'number_of_hours': 0.0,
                     'contract_id': contract.id,
                }

                overtime1h = {
                     'name': _("Lembur 1 Jam"),
                     'sequence': 10,
                     'code': 'Overtime1h',
                     'number_of_days': 0.0,
                     'number_of_hours': 0.0,
                     'contract_id': contract.id,
                }

                overtime1_5h = {
                     'name': _("Lembur 1.5 Jam"),
                     'sequence': 11,
                     'code': 'Overtime1_5h',
                     'number_of_days': 0.0,
                     'number_of_hours': 0.0,
                     'contract_id': contract.id,
                }

                overtime2h = {
                     'name': _("Lembur 2 Jam"),
                     'sequence': 12,
                     'code': 'Overtime2h',
                     'number_of_days': 0.0,
                     'number_of_hours': 0.0,
                     'contract_id': contract.id,
                }

                overtime2_5h = {
                     'name': _("Lembur 2.5 Jam"),
                     'sequence': 13,
                     'code': 'Overtime2_5h',
                     'number_of_days': 0.0,
                     'number_of_hours': 0.0,
                     'contract_id': contract.id,
                }

                overtime3h = {
                     'name': _("Lembur 3 Jam"),
                     'sequence': 14,
                     'code': 'Overtime3h',
                     'number_of_days': 0.0,
                     'number_of_hours': 0.0,
                     'contract_id': contract.id,
                }

                overtime3_5h = {
                     'name': _("Lembur 3.5 Jam"),
                     'sequence': 15,
                     'code': 'Overtime3_5h',
                     'number_of_days': 0.0,
                     'number_of_hours': 0.0,
                     'contract_id': contract.id,
                }

                overtime4h = {
                     'name': _("Lembur 4 Jam"),
                     'sequence': 16,
                     'code': 'Overtime4h',
                     'number_of_days': 0.0,
                     'number_of_hours': 0.0,
                     'contract_id': contract.id,
                }

                overtime4_5h = {
                     'name': _("Lembur 4.5 Jam"),
                     'sequence': 17,
                     'code': 'Overtime4_5h',
                     'number_of_days': 0.0,
                     'number_of_hours': 0.0,
                     'contract_id': contract.id,
                }

                overtime5_7h = {
                     'name': _("Lembur 5 - 7 Jam"),
                     'sequence': 18,
                     'code': 'Overtime5_7h',
                     'number_of_days': 0.0,
                     'number_of_hours': 0.0,
                     'contract_id': contract.id,
                }

                overtime2shift = {
                     'name': _("Lembur Double Shift"),
                     'sequence': 19,
                     'code': 'Overtime2shift',
                     'number_of_days': 0.0,
                     'number_of_hours': 0.0,
                     'contract_id': contract.id,
                }

                late = {
                     'name': _("Terlambat 5 Menit"),
                     'sequence': 20,
                     'code': 'Late',
                     'number_of_days': 0.0,
                     'number_of_hours': 0.0,
                     'contract_id': contract.id,
                }

                late2 = {
                     'name': _("Terlambat 10 Menit"),
                     'sequence': 21,
                     'code': 'Late2',
                     'number_of_days': 0.0,
                     'number_of_hours': 0.0,
                     'contract_id': contract.id,
                }

                late3 = {
                     'name': _("Terlambat 15 Menit"),
                     'sequence': 22,
                     'code': 'Late3',
                     'number_of_days': 0.0,
                     'number_of_hours': 0.0,
                     'contract_id': contract.id,
                }

                late4 = {
                     'name': _("Terlambat 20 Menit"),
                     'sequence': 23,
                     'code': 'Late4',
                     'number_of_days': 0.0,
                     'number_of_hours': 0.0,
                     'contract_id': contract.id,
                }


                # uom_hour = contract.employee_id.resource_id.calendar_id.uom_id or self.env.ref('product.product_uom_hour', raise_if_not_found=False)
                interval_data = []
                day_from = fields.Datetime.from_string(self.date_from)
                day_to = fields.Datetime.from_string(self.date_to)
                nb_of_days = (day_to - day_from).days + 1

                # Gather all intervals and holidays
                # working_intervals_on_day = contract.resource_calendar_id._work_intervals(start_dt=day_from + timedelta(days=day))
                # pdb.set_trace()

                for day in range(0, nb_of_days):
                    # working_intervals_on_day = contract.working_hours.get_working_intervals_of_day(start_dt=day_from + timedelta(days=day))
                    # work_data = contract.employee_id.get_work_days_data(day_from, day_to, calendar=contract.resource_calendar_id)
                    intervals = []
                    work_dt_o = day_from + timedelta(days=day)
                    work_dt = work_dt_o.replace(hour=0, minute=0, second=0, microsecond=0)

                    working_intervals = []
                    tz_info = fields.Datetime.context_timestamp(self, work_dt).tzinfo
                    
                    for calendar_working_day in get_weekend(work_dt_o):
                        dt_f = work_dt.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(seconds=(calendar_working_day.hour_from * 3600))
                        dt_t = work_dt.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(seconds=(calendar_working_day.hour_to * 3600))

                        # adapt tz
                        interval_data.append((dt_f.replace(tzinfo=tz_info).astimezone(pytz.UTC).replace(tzinfo=None), dt_t.replace(tzinfo=tz_info).astimezone(pytz.UTC).replace(tzinfo=None)))

                hours_new = 0
                days_new = 0
                hadir = 0
                ijin = 0
                sakit = 0
                cutilibur = 0
                # pdb.set_trace()
                ccc = []
                for cc in interval_data:
                    ccc.append(cc)

                for interval in interval_data:
                    hours = (interval[1] - interval[0]).total_seconds() / 3600.0
                    hours_new += hours
                    day_inter = interval[0].strftime("%Y-%m-%d")
                    day_inter_dari = day_inter + '  00:00:00'
                    day_inter_sampai = day_inter + '  23:59:59'
                    obj_attend = self.env['hr.attendance'].search([('check_in', '>=', day_inter_dari),('check_in', '<=', day_inter_sampai),('employee_id', '=', self.employee_id.id)], limit=1)
                    if obj_attend:
                        hadir += 1
                    obj_leave = self.env['hr.leave'].search([('state', '=', 'validate'),('date_from', '>=', day_inter_dari),('date_from', '<=', day_inter_sampai),('employee_id', '=', self.employee_id.id)], limit=1)
                    # pdb.set_trace()
                    if obj_leave.holiday_status_id.name:
                        if "IJIN" in obj_leave.holiday_status_id.name or "Ijin" in obj_leave.holiday_status_id.name or "ijin" in obj_leave.holiday_status_id.name:
                            ijin += obj_leave.number_of_days_display
                        elif "SAKIT" in obj_leave.holiday_status_id.name or "Sakit" in obj_leave.holiday_status_id.name or "sakit" in obj_leave.holiday_status_id.name:
                            sakit += obj_leave.number_of_days_display
                        elif "CUTI" in obj_leave.holiday_status_id.name or "Cuti" in obj_leave.holiday_status_id.name or "cuti" in obj_leave.holiday_status_id.name:
                            cutilibur += obj_leave.number_of_days_display
                        elif "LIBUR" in obj_leave.holiday_status_id.name or "Libur" in obj_leave.holiday_status_id.name or "libur" in obj_leave.holiday_status_id.name:
                            cutilibur += obj_leave.number_of_days_display
                        elif "Public Holidays" in obj_leave.holiday_status_id.name:
                            cutilibur += obj_leave.number_of_days_display

                work_schedule = self.env['resource.calendar'].search([('id', '=', self.contract_id.resource_calendar_id.id)])
                av_hours = work_schedule.hours_per_day
                days_new = hours_new / av_hours
                takadir = days_new - hadir - sakit - ijin - cutilibur
                alpha['number_of_days'] = round(takadir)
                presences['number_of_days'] = round(hadir)
                attendances['number_of_days'] = round(days_new)
                sakit_o['number_of_days'] = sakit
                ijin_o['number_of_days'] = ijin
                cutilibur_o['number_of_days'] = cutilibur
                
                # pdb.set_trace()
                for day1 in range(0, nb_of_days):
                    work_dt_o1 = day_from + timedelta(days=day1)
                    src_over = self.env['hr.overtime'].search([('tgl','=',work_dt_o1),('state','=','validate')])
                    for overt in src_over :
                        src_ovemp = self.env['hr.overtime.employee'].search([('overtime_id','=',overt.id),('employee_id','=',self.employee_id.id)],limit=1)
                        if src_ovemp :
                            jumlah = src_ovemp.total_jam
                            if overt.hari_libur:
                                overtime2['number_of_hours'] += jumlah
                                if jumlah >= 4.0 :
                                    overtime2['number_of_days'] += 1
                            elif overt.lembur_istimewa:
                                overtime3['number_of_hours'] += jumlah
                                if jumlah >= 4.0 :
                                    overtime3['number_of_days'] += 1
                            elif overt.lembur_biasa:
                                overtime['number_of_hours'] += jumlah
                                if jumlah >= 4.0 :
                                    overtime['number_of_days'] += 1

                            elif overt.type_id.name == 'Lembur 1 Jam':
                                overtime1h['number_of_hours'] += jumlah
                                if jumlah >= 1.0 :
                                    overtime1h['number_of_days'] += 1
                            elif overt.type_id.name == 'Lembur 1.5 Jam':
                                overtime1_5h['number_of_hours'] += jumlah
                                if jumlah >= 1.5 :
                                    overtime1_5h['number_of_days'] += 1
                            elif overt.type_id.name == 'Lembur 2 Jam':
                                overtime2h['number_of_hours'] += jumlah
                                if jumlah >= 2.0 :
                                    overtime2h['number_of_days'] += 1
                            elif overt.type_id.name == 'Lembur 2.5 Jam':
                                overtime2_5h['number_of_hours'] += jumlah
                                if jumlah >= 2.5 :
                                    overtime2_5h['number_of_days'] += 1
                            elif overt.type_id.name == 'Lembur 3 Jam':
                                overtime3h['number_of_hours'] += jumlah
                                if jumlah >= 3.0 :
                                    overtime3h['number_of_days'] += 1
                            elif overt.type_id.name == 'Lembur 3.5 Jam':
                                overtime3_5h['number_of_hours'] += jumlah
                                if jumlah >= 3.5 :
                                    overtime3_5h['number_of_days'] += 1
                            elif overt.type_id.name == 'Lembur 4 Jam':
                                overtime4h['number_of_hours'] += jumlah
                                if jumlah >= 4.0 :
                                    overtime4h['number_of_days'] += 1
                            elif overt.type_id.name == 'Lembur 4.5 Jam':
                                overtime4_5h['number_of_hours'] += jumlah
                                if jumlah >= 4.5 :
                                    overtime4_5h['number_of_days'] += 1
                            elif overt.type_id.name == 'Lembur 5 - 7 Jam':
                                overtime5_7h['number_of_hours'] += jumlah
                                if jumlah >= 5.0 :
                                    overtime5_7h['number_of_days'] += 1
                            elif overt.type_id.name == 'Lembur Double Shift':
                                overtime2shift['number_of_hours'] += jumlah
                                if jumlah >= 7.0 :
                                    overtime2shift['number_of_days'] += 1

                    src_late = self.env['hr.attendance'].search([('tgl','=',work_dt_o1),('employee_id','=',self.employee_id.id)])
                    for lmbt in src_late :
                        jumlah = lmbt.late_hours
                        if jumlah >= 5.0 and jumlah < 10.0:
                            late['number_of_hours'] += jumlah/60
                            late['number_of_days'] += 1
                        elif jumlah >= 10.0 and jumlah < 15.0:
                            late2['number_of_hours'] += jumlah/60
                            late2['number_of_days'] += 1
                        elif jumlah >= 15.0 and jumlah < 20.0:
                            late3['number_of_hours'] += jumlah/60
                            late3['number_of_days'] += 1
                        elif jumlah >= 20.0:
                            late4['number_of_hours'] += jumlah/60
                            late4['number_of_days'] += 1

                            
                            
                res += [attendances] + [presences] + [sakit_o] + [ijin_o] + [cutilibur_o] + [alpha] + [overtime] + [overtime2] + [overtime3] + [overtime1h] + [overtime1_5h] + [overtime2h] + [overtime2_5h] + [overtime3h] + [overtime3_5h]+ [overtime4h] + [overtime4_5h] + [overtime5_7h] + [overtime2shift] + [late] + [late2] + [late3] + [late4]
            return res
            
        # pdb.set_trace()
        payslips = self.env['hr.payslip']
        [data] = self.read()
        active_id = self.env.context.get('active_id')
        if active_id:
            [run_data] = self.env['hr.payslip.run'].browse(active_id).read(['date_start', 'date_end', 'credit_note','journal_id'])
        from_date = run_data.get('date_start')
        to_date = run_data.get('date_end')
        # pdb.set_trace()
        if not data['employee_ids']:
            raise UserError(_("You must select employee(s) to generate payslip(s)."))
        for employee in self.env['hr.employee'].browse(data['employee_ids']):

            #cek jika ada kontrak yg kedaluarsa, kalau ada di bypass
            check_contract = self.env['hr.contract'].search([('employee_id','=',employee.id)])
            for c in check_contract:
                if c.state == 'close':
                    continue

                slip_data = self.env['hr.payslip'].onchange_employee_id(from_date, to_date, employee.id, contract_id=False)
                res = {
                    'employee_id': employee.id,
                    'name': slip_data['value'].get('name'),
                    'struct_id': slip_data['value'].get('struct_id'),
                    'journal_id': run_data.get('journal_id')[0],
                    'contract_id': slip_data['value'].get('contract_id'),
                    'payslip_run_id': active_id,
                    'input_line_ids': [(0, 0, x) for x in slip_data['value'].get('input_line_ids')],
                    'worked_days_line_ids': [(0, 0, x) for x in slip_data['value'].get('worked_days_line_ids')],
                    'date_from': from_date,
                    'date_to': to_date,
                    'credit_note': run_data.get('credit_note'),
                }
                payslips += self.env['hr.payslip'].create(res)
        # pdb.set_trace()
        for self in payslips:
            slip_data_work = get_worked_day_lines(self, from_date, to_date)
            self.worked_days_line_ids = slip_data_work
            self.compute_sheet()
        return {'type': 'ir.actions.act_window_close'}