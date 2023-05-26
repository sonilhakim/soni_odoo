# -*- coding: utf-8 -*-

import time
from datetime import datetime, timedelta
import dateutil.parser
from dateutil import relativedelta
import pytz
from odoo import api, models, fields, _


class ReportRekapStockAccWizard(models.TransientModel):
    _name = "rekap.stock.acc"

    @api.model
    def _get_default_year(self):
        now = datetime.now()
        year = int(datetime.strftime(now, '%Y'))
        return year
   
    date_from = fields.Date(string='Start Date', compute='get_date_start_end', store=True)
    date_to = fields.Date( string='End Date', compute='get_date_start_end', store=True)
    periode = fields.Selection([
        (1, 'JANUARI'),
        (2, 'FEBRUARI'),
        (3, 'MARET'),
        (4, 'APRIL'),
        (5, 'MEI'),
        (6, 'JUNI'),
        (7, 'JULI'),
        (8, 'AGUSTUS'),
        (9, 'SEPTEMBER'),
        (10, 'OKTOBER'),
        (11, 'NOVEMBER'),
        (12, 'DESEMBER')
        ], string='Periode', default=1,)
    year = fields.Selection([
        (2015, '2015'),
        (2016, '2016'),
        (2017, '2017'),
        (2018, '2018'),
        (2019, '2019'),
        (2020, '2020'),
        (2021, '2021'),
        (2022, '2022'),
        (2023, '2023'),
        (2024, '2024'),
        (2025, '2025'),
        (2026, '2026'),
        (2027, '2027'),
        (2028, '2028'),
        (2029, '2029'),
        (2030, '2030'),
        (2031, '2031'),
        (2032, '2032'),
        (2033, '2033'),
        (2034, '2034'),
        (2035, '2035'),
        (2036, '2036'),
        (2037, '2037'),
        (2038, '2038'),
        (2039, '2039'),
        (2040, '2040'),
        ], string='Year', default=_get_default_year,)

    @api.depends('periode')
    def get_date_start_end(self):
        for ra in self:
            now = datetime.now()
            # thn = datetime.strftime(now, '%Y')
            thn = str(ra.year)
            if ra.periode == 1:
                ra.date_from = datetime.strftime(now, thn +'-01-01')
                ra.date_to = datetime.strftime(now, thn +'-01-31')
            if ra.periode == 2:
                ra.date_from = datetime.strftime(now, thn +'-02-01')
                if int(thn) / 4 == 1:
                    ra.date_to = datetime.strftime(now, thn +'-02-29')
                else:
                    ra.date_to = datetime.strftime(now, thn +'-02-28')
            if ra.periode == 3:
                ra.date_from = datetime.strftime(now, thn +'-03-01')
                ra.date_to = datetime.strftime(now, thn +'-03-31')
            if ra.periode == 4:
                ra.date_from = datetime.strftime(now, thn +'-04-01')
                ra.date_to = datetime.strftime(now, thn +'-04-30')
            if ra.periode == 5:
                ra.date_from = datetime.strftime(now, thn +'-05-01')
                ra.date_to = datetime.strftime(now, thn +'-05-31')
            if ra.periode == 6:
                ra.date_from = datetime.strftime(now, thn +'-06-01')
                ra.date_to = datetime.strftime(now, thn +'-06-30')
            if ra.periode == 7:
                ra.date_from = datetime.strftime(now, thn +'-07-01')
                ra.date_to = datetime.strftime(now, thn +'-07-31')
            if ra.periode == 8:
                ra.date_from = datetime.strftime(now, thn +'-08-01')
                ra.date_to = datetime.strftime(now, thn +'-08-31')
            if ra.periode == 9:
                ra.date_from = datetime.strftime(now, thn +'-09-01')
                ra.date_to = datetime.strftime(now, thn +'-09-30')
            if ra.periode == 10:
                ra.date_from = datetime.strftime(now, thn +'-10-01')
                ra.date_to = datetime.strftime(now, thn +'-10-31')
            if ra.periode == 11:
                ra.date_from = datetime.strftime(now, thn +'-11-01')
                ra.date_to = datetime.strftime(now, thn +'-11-30')
            if ra.periode == 12:
                ra.date_from = datetime.strftime(now, thn +'-12-01')
                ra.date_to = datetime.strftime(now, thn +'-12-31')
        

    @api.multi
    def get_current_date(self):
        date = ''
        for ra in self:
            now = datetime.now()
            user = ra.env['res.users'].browse(ra.env.uid)
            tz   = pytz.timezone(user.tz) or pytz.utc
            date_new = pytz.utc.localize(now).astimezone(tz)
            tgl    = datetime.strftime(date_new, '%d')
            bln    = datetime.strftime(date_new, '%m')
            thn    = datetime.strftime(date_new, '%Y')
            b = ''
            if bln == '01':
                b = 'Januari'
            if bln == '02':
                b = 'Februari'
            if bln == '03':
                b = 'Maret'
            if bln == '04':
                b = 'April'
            if bln == '05':
                b = 'Mei'
            if bln == '06':
                b = 'Juni'
            if bln == '07':
                b = 'Juli'
            if bln == '08':
                b = 'Agustus'
            if bln == '09':
                b = 'September'
            if bln == '10':
                b = 'Oktober'
            if bln == '11':
                b = 'November'
            if bln == '12':
                b = 'Desember'
            date = str(tgl) +" "+ b +" "+ str(thn)
        return date

    @api.multi
    def action_print_report(self):
        data = {
            'date_from': self.date_from,
            'date_to': self.date_to,
        }
        report_action = self.env.ref(
            'vit_report_rekap_inventory.action_rekap_stock_acc'
        ).report_action(self, data=data)
        report_action['close_on_report_download']=True

        return report_action



