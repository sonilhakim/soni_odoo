# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import time
from datetime import date
from datetime import datetime
from datetime import timedelta
from dateutil import relativedelta
import calendar
import pytz
import pdb
from odoo import models, fields, api, exceptions, _


class AttendanceLateOver(models.Model):
    _inherit = "hr.attendance"    


    late_hours      = fields.Float(string='Late', compute='_get_late_hours', store=True)
    overtime_hours  = fields.Float(string='Overtime', compute='_get_overtime_hours', store=True)
    late            = fields.Char(string='Late', compute='_get_hours', store=True)
    overt           = fields.Char(string='Overtime', compute='_get_hours', store=True)
    hari            = fields.Char(string="Hari", compute='_get_day', store=True)
    tgl             = fields.Date(string="Tanggal", compute='_get_day', store=True)

    @api.depends('check_in')
    def _get_day(self):
        for att in self:
            user    = att.env['res.users'].browse(att.env.uid)
            tz      = pytz.timezone(user.tz) or pytz.utc
            if att.check_in:
                # DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
                # date_field1 = datetime.strptime(str(att.check_in), DATETIME_FORMAT)
                # date_new = date_field1 + timedelta(hours=-7)
                # att.tgl_lmbt = str(date_new)
                date_new    = pytz.utc.localize(att.check_in).astimezone(tz)
                att.tgl     = str(date_new)
                # att.tgl = datetime.strftime(att.check_in, '%Y:%m:%d')
                # selected = fields.Datetime.from_string(date_new)
                att.hari    = calendar.day_name[date_new.weekday()]
            return {}   


    @api.depends('check_in')
    def _get_late_hours(self):

        for att in self:
            user        = att.env['res.users'].browse(att.env.uid)
            # converting time to users timezone
            # if user.tz:
            #     tz = pytz.timezone(user.tz) or pytz.utc
            #     check_in = pytz.utc.localize(self.check_in).astimezone(tz)
            # else:
            #     check_in = self.check_in
            # for attendance in self:
            
            tz          = pytz.timezone(user.tz) or pytz.utc
            check_in    = pytz.utc.localize(att.check_in).astimezone(tz)
            hour_in     = check_in.hour+check_in.minute/60.0
            hour_from   = hour_in
                    
            cda_obj     = att.env['hr.contract'].search([('employee_id', '=', att.employee_id.id),('active', '=', True),('state', '=', 'open')], limit=1)
            if cda_obj:
                # pdb.set_trace()
                wd_mon = att.env['resource.calendar.attendance'].search([('calendar_id', '=', cda_obj.resource_calendar_id.id),('dayofweek', '=', '0')])
                wd_tue = att.env['resource.calendar.attendance'].search([('calendar_id', '=', cda_obj.resource_calendar_id.id),('dayofweek', '=', '1')])
                wd_wed = att.env['resource.calendar.attendance'].search([('calendar_id', '=', cda_obj.resource_calendar_id.id),('dayofweek', '=', '2')])
                wd_thu = att.env['resource.calendar.attendance'].search([('calendar_id', '=', cda_obj.resource_calendar_id.id),('dayofweek', '=', '3')])
                wd_fri = att.env['resource.calendar.attendance'].search([('calendar_id', '=', cda_obj.resource_calendar_id.id),('dayofweek', '=', '4')])
                wd_sat = att.env['resource.calendar.attendance'].search([('calendar_id', '=', cda_obj.resource_calendar_id.id),('dayofweek', '=', '5')])
                wd_sun = att.env['resource.calendar.attendance'].search([('calendar_id', '=', cda_obj.resource_calendar_id.id),('dayofweek', '=', '6')])
                if ((att.hari == 'Monday' or att.hari == 'Senin') and wd_mon):
                    for wd in wd_mon[0]:
                        hour_from = wd.hour_from
                
                elif ((att.hari == 'Tuesday' or att.hari == 'Selasa') and wd_tue):
                    for wd in wd_tue[0]:
                        hour_from = wd.hour_from
                
                elif ((att.hari == 'Wednesday' or att.hari == 'Rabu') and wd_wed):
                    for wd in wd_wed[0]:
                        hour_from = wd.hour_from
                
                elif ((att.hari == 'Kamis' or att.hari == 'Thursday') and wd_thu):
                    for wd in wd_thu[0]:
                        hour_from = wd.hour_from
                
                elif ((att.hari == 'Friday' or att.hari == 'Jumat') and wd_fri):
                    for wd in wd_fri[0]:
                        hour_from = wd.hour_from
                
                elif ((att.hari == 'Saturday' or att.hari == 'Sabtu') and wd_sat):
                    for wd in wd_sat[0]:
                        hour_from = wd.hour_from
                
                elif ((att.hari == 'Sunday' or att.hari == 'Minggu') and wd_sun):
                    for wd in wd_sun[0]:
                        hour_from = wd.hour_from

                else:
                    overtime    = att.env['hr.overtime'].search([('tgl', '=', att.tgl), ('state', '=', 'validate')])
                    for overts in overtime:
                        over    = att.env['hr.overtime.employee'].search([('employee_id', '=', att.employee_id.id),('overtime_id', '=', overts.id)])
                        for ov in over:                
                            date_from = pytz.utc.localize(ov.overtime_id.date_from).astimezone(tz)                
                            over_hour = date_from.hour+date_from.minute/60.0
                            if over:
                                hour_from = over_hour

                delta           = hour_in - hour_from  
                att.late_hours  = delta*60

    @api.depends('check_out')
    def _get_overtime_hours(self):
        for att in self:
            user    = att.env['res.users'].browse(att.env.uid)
            tz      = pytz.timezone(user.tz) or pytz.utc
            if att.check_out != False:
                cr = self.env.cr
                check_in    = pytz.utc.localize(att.check_in).astimezone(tz)
                check_out   = pytz.utc.localize(att.check_out).astimezone(tz) #disesuaikan dengan timezone user
                hour_out    = check_out.hour+check_out.minute/60.0 #convert ke float
                new_in      = check_in + timedelta(days=+1)
                date_in     = datetime.strftime(new_in, '%Y:%m:%d')
                date_out    = datetime.strftime(check_out, '%Y:%m:%d')  
                hour_to     = hour_out              
                
                cda_obj     = att.env['hr.contract'].search([('employee_id', '=', att.employee_id.id),('active', '=', True),('state', '=', 'open')], limit=1)
                if cda_obj:
                    wd_mon = att.env['resource.calendar.attendance'].search([('calendar_id', '=', cda_obj.resource_calendar_id.id),('dayofweek', '=', '0')])
                    wd_tue = att.env['resource.calendar.attendance'].search([('calendar_id', '=', cda_obj.resource_calendar_id.id),('dayofweek', '=', '1')])
                    wd_wed = att.env['resource.calendar.attendance'].search([('calendar_id', '=', cda_obj.resource_calendar_id.id),('dayofweek', '=', '2')])
                    wd_thu = att.env['resource.calendar.attendance'].search([('calendar_id', '=', cda_obj.resource_calendar_id.id),('dayofweek', '=', '3')])
                    wd_fri = att.env['resource.calendar.attendance'].search([('calendar_id', '=', cda_obj.resource_calendar_id.id),('dayofweek', '=', '4')])
                    wd_sat = att.env['resource.calendar.attendance'].search([('calendar_id', '=', cda_obj.resource_calendar_id.id),('dayofweek', '=', '5')])
                    wd_sun = att.env['resource.calendar.attendance'].search([('calendar_id', '=', cda_obj.resource_calendar_id.id),('dayofweek', '=', '6')])
                    if ((att.hari == 'Monday' or att.hari == 'Senin') and wd_mon):
                        for wd in wd_mon:
                            hour_to = wd.hour_to
                                             
                    elif ((att.hari == 'Tuesday' or att.hari == 'Selasa') and wd_tue):
                        for wd in wd_tue:
                            hour_to = wd.hour_to
                    
                    elif ((att.hari == 'Wednesday' or att.hari == 'Rabu') and wd_wed):
                        for wd in wd_wed:                
                            hour_to = wd.hour_to
                    
                    elif ((att.hari == 'Kamis' or att.hari == 'Thursday') and wd_thu):
                        for wd in wd_thu:                
                            hour_to = wd.hour_to
                    
                    elif ((att.hari == 'Friday' or att.hari == 'Jumat') and wd_fri):
                        for wd in wd_fri:                
                            hour_to = wd.hour_to
                    
                    elif ((att.hari == 'Saturday' or att.hari == 'Sabtu') and wd_sat):
                        for wd in wd_sat:                
                            hour_to = wd.hour_to
                    
                    elif ((att.hari == 'Sunday' or att.hari == 'Minggu') and wd_sun):
                        for wd in wd_sun:                
                            hour_to = wd.hour_to
                    else:
                        overtime    = att.env['hr.overtime'].search([('tgl', '=', att.tgl), ('state', '=', 'validate')])
                        for overts in overtime:
                            over    = att.env['hr.overtime.employee'].search([('employee_id', '=', att.employee_id.id),('overtime_id', '=', overts.id)])
                            for ov in over:                
                                date_from = pytz.utc.localize(ov.overtime_id.date_from).astimezone(tz)                
                                over_hour = date_from.hour+date_from.minute/60.0
                        
                                if over:
                                    hour_to = over_hour

                    delta = hour_out - hour_to
                    if date_out == date_in:
                        att.overtime_hours = delta + 24.0
                    else:
                        att.overtime_hours = delta

                    # if not att.env['resource.calendar.attendance'].search([('calendar_id', '=', cda_obj.resource_calendar_id.id)]):
                    #     if over:
                    #         for ov in over:                
                    #             date_from = ov.overtime_id.date_from
                    #             delta = att.check_out - date_from  
                    #             att.overtime_hours= delta.total_seconds() / 3600.0
                
                    overtimes = att.env['hr.overtime'].search([('tgl', '=', att.tgl), ('state', '=', 'validate')])
                    for ovt in overtimes:
                        ovem = att.env['hr.overtime.employee'].search([('employee_id', '=', att.employee_id.id),('overtime_id', '=', ovt.id)])
                        if ovem:                    
                        #     for ov in over:             
                        #         date_from = ov.overtime_id.date_from
                        #         delta = att.check_out - date_from  
                        #         att.overtime_hours= delta.total_seconds() / 3600.0
                        # pdb.set_trace()
                            cr.execute("update hr_overtime_employee set ovt_hour=%s where employee_id = %s and overtime_id=%s",
                     ( att.overtime_hours, att.employee_id.id, ovem.id  ))


    @api.depends('late_hours', 'overtime_hours')
    def _get_hours(self):
        for att in self:
            att.late    = str(round(att.late_hours, 2)) + ' menit'
            att.overt   = str(round(att.overtime_hours, 2)) + ' jam'

