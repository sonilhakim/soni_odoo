from odoo import api, fields, models, _
import time
from datetime import datetime, timedelta
import dateutil.parser
import pytz
from odoo.exceptions import UserError, ValidationError

class hr_overtime(models.Model):
	_inherit = "hr.overtime"

	tgl = fields.Date(string="Tanggal", compute='_get_day', store=True)
	

	@api.depends('date_from')
	def _get_day(self):
		for ovt in self:
			user 	= ovt.env['res.users'].browse(ovt.env.uid)
			tz 		= pytz.timezone(user.tz) or pytz.utc
			if ovt.date_from:
				date_new 	= pytz.utc.localize(ovt.date_from).astimezone(tz)
				ovt.tgl 	= str(date_new)
			return {} 
	

class hr_overtime_attendance(models.Model):
	_inherit = "hr.overtime.employee"

	ovt_hour = fields.Float("Real Overtime Hours", compute='_get_ovt_hour', store=True)
	
	@api.depends('employee_id')
	def _get_ovt_hour(self):
		for over in self:
			attendance = over.env['hr.attendance'].search([('employee_id', '=', over.employee_id.id),('tgl', '=', over.overtime_id.tgl)])
			for att in attendance:
				over.ovt_hour = att.overtime_hours

class overtime_hour_detail(models.Model):
	_inherit = "hr.overtime.hour.detail"


	from_hour 	= fields.Selection([("1","Jam 1"),("1.5","Jam 1:30"),("2","Jam 2"),("2.5","Jam 2:30"),("3","Jam 3"),("3.5","Jam 3:30"),("4","Jam 4"),("4.5","Jam 4:30"),("5","Jam 5"),("5.5","Jam 5:30"),("6","Jam 6"),("6.5","Jam 6:30"),("7","Jam 7"),("7.5","Jam 7:30"),
			("8","Jam 8"),("8.5","Jam 8:30"),("9","Jam 9"),("9.5","Jam 9:30"),("10","Jam 10"),("10.5","Jam 10:30"),("11","Jam 11"),("11.5","Jam 11:30"),("12","Jam 12"),("12.5","Jam 12:30"),("13","Jam 13"),("13.5","Jam 13:30"),("14","Jam 14"),("14.5","Jam 14:30"),("15","Jam 15"),("15.5","Jam 15:30"),
			("16","Jam 16"),("16.5","Jam 16:30"),("17","Jam 17"),("17.5","Jam 17:30"),("18","Jam 18"),("18.5","Jam 18:30"),("19","Jam 19"),("19.5","Jam 19:30"),("20","Jam 20"),("20.5","Jam 20:30"),("21","Jam 21"),("21.5","Jam 21:30"),("22","Jam 22"),("22.5","Jam 22:30"),("23","Jam 23"),("23.5","Jam 23:30"),("24","Jam 24")], string="Hour Start", required=True)
	to_hour 	= fields.Selection([("1","Jam 1"),("1.5","Jam 1:30"),("2","Jam 2"),("2.5","Jam 2:30"),("3","Jam 3"),("3.5","Jam 3:30"),("4","Jam 4"),("4.5","Jam 4:30"),("5","Jam 5"),("5.5","Jam 5:30"),("6","Jam 6"),("6.5","Jam 6:30"),("7","Jam 7"),("7.5","Jam 7:30"),
			("8","Jam 8"),("8.5","Jam 8:30"),("9","Jam 9"),("9.5","Jam 9:30"),("10","Jam 10"),("10.5","Jam 10:30"),("11","Jam 11"),("11.5","Jam 11:30"),("12","Jam 12"),("12.5","Jam 12:30"),("13","Jam 13"),("13.5","Jam 13:30"),("14","Jam 14"),("14.5","Jam 14:30"),("15","Jam 15"),("15.5","Jam 15:30"),
			("16","Jam 16"),("16.5","Jam 16:30"),("17","Jam 17"),("17.5","Jam 17:30"),("18","Jam 18"),("18.5","Jam 18:30"),("19","Jam 19"),("19.5","Jam 19:30"),("20","Jam 20"),("20.5","Jam 20:30"),("21","Jam 21"),("21.5","Jam 21:30"),("22","Jam 22"),("22.5","Jam 22:30"),("23","Jam 23"),("23.5","Jam 23:30"),("24","Jam 24")], string="Hour End", required=True)
	
overtime_hour_detail()