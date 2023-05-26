# -*- coding: utf-8 -*-

import time
from datetime import datetime, timedelta
import dateutil.parser
from dateutil import relativedelta
import pytz
from odoo import api, models, fields, _


class ReportRekapBKBWizard(models.TransientModel):
    _name = "rekap.bkb.wizard"
   
    date_from = fields.Date(string='Start Date',)
    date_to = fields.Date( string='End Date',)
    option = fields.Selection([(0, 'All'),(1, 'Date Range')], string='Option', default=0,)

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
        # return self.env.ref(
        #     'vit_report_rekap_inventory.action_rekap_bkb_report'
        # ).report_action(self, data=data)
        report_action = self.env.ref(
            'vit_report_rekap_inventory.action_rekap_bkb_report'
        ).report_action(self, data=data)
        report_action['close_on_report_download']=True

        return report_action



