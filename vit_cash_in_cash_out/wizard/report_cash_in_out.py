# -*- coding: utf-8 -*-

import time
from datetime import datetime, timedelta
import dateutil.parser
from dateutil import relativedelta
import pytz
from odoo import api, models, fields, _


class CashInOutWizard(models.TransientModel):
    _name = "cash.in.out.wizard"

    company_id = fields.Many2one('res.company', string='Company', help='')
    name = fields.Char( string="Nama Report")
    start_date  = fields.Date( string="Start date", required=True, default=lambda self:time.strftime("%Y-%m-%d"), help="")
    end_date    = fields.Date( string="End date", required=True, default=lambda self:time.strftime("%Y-%m-%d"), help="")
    grand_total = fields.Float( string="Grand Total",  help="", )
    
    transaksi_ids = fields.One2many(comodel_name="transaksi.cash_in_out.wizard",  inverse_name="cio_wizard_id",  string="Transaksi",  readonly=True, )
    report_ids = fields.One2many(comodel_name="report.cash_in_out.wizard",  inverse_name="cio_wizard_id",  string="Transaksi",  readonly=True, )
    
    @api.multi
    def _get_cash_in(self):
        cr = self.env.cr
        sql = """
            SELECT tc.tanggal, aa.id, tc.name, tc.no_voucher, tc.keterangan, tc.jumlah
            FROM vit_transaksi_cash tc
            LEFT JOIN account_account aa ON tc.kode_transaksi = aa.id
            WHERE tc.tanggal BETWEEN %s AND %s AND tc.jumlah > 0.0
            """
        cr.execute(sql, (self.start_date, self.end_date,))
        result = cr.fetchall()
        trans_ids = []
        for res in result:
            # import pdb;pdb.set_trace()
            trans_ids.append((0,0,{
                    'tanggal' : res[0],
                    'kode_transaksi' : res[1],
                    'name' : res[2],
                    'no_voucher': res[3],
                    'keterangan' : res[4],
                    'jumlah' : res[5],
                    }))

        data = {
            'name'       : "LAPORAN CASH IN",
            'company_id' : self.env.user.company_id.id,
            'grand_total': sum(res[5] for res in result),
            'transaksi_ids' : trans_ids,
        }
        self.write(data)

    @api.multi
    def _get_cash_out(self):
        cr = self.env.cr
        sql = """
            SELECT tc.tanggal, aa.id, tc.name, tc.no_voucher, tc.keterangan, tc.jumlah
            FROM vit_transaksi_cash tc
            LEFT JOIN account_account aa ON tc.kode_transaksi = aa.id
            WHERE tc.tanggal BETWEEN %s AND %s AND tc.jumlah < 0.0
            """
        cr.execute(sql, (self.start_date, self.end_date,))
        result = cr.fetchall()
        trans_ids = []
        for res in result:
            # import pdb;pdb.set_trace()
            trans_ids.append((0,0,{
                    'tanggal' : res[0],
                    'kode_transaksi' : res[1],
                    'name' : res[2],
                    'no_voucher': res[3],
                    'keterangan' : res[4],
                    'jumlah' : (res[5] * -1),
                    }))

        data = {
            'name'       : "LAPORAN CASH OUT",
            'company_id' : self.env.user.company_id.id,
            'grand_total': (sum(res[5] for res in result) * -1),
            'transaksi_ids' : trans_ids,
        }
        self.write(data)


    @api.multi
    def _get_cash_in_out(self):
        # import pdb;pdb.set_trace()
        cr = self.env.cr
        sql = """
            SELECT cio.tanggal, cio.keterangan,
            (SELECT sum(tci.jumlah)
            FROM vit_transaksi_cash tci
            WHERE tci.cash_in_out_id = cio.id AND tci.jumlah > 0.0),
            (SELECT sum(tco.jumlah)
            FROM vit_transaksi_cash tco
            WHERE tco.cash_in_out_id = cio.id AND tco.jumlah < 0.0),
            (SELECT sum(tci.jumlah)
            FROM vit_transaksi_cash tci
            WHERE tci.cash_in_out_id = cio.id AND tci.jumlah > 0.0)
            +
            (SELECT sum(tco.jumlah)
            FROM vit_transaksi_cash tco
            WHERE tco.cash_in_out_id = cio.id AND tco.jumlah < 0.0)
            FROM vit_cash_in_out cio
            WHERE cio.tanggal BETWEEN %s AND %s
            GROUP BY cio.id
            """
        cr.execute(sql, (self.start_date, self.end_date,))
        result = cr.fetchall()
        report_ids = []
        for res in result:
            cash_in = 0.0
            cash_out = 0.0
            if res[2]:
                cash_in = res[2]
            if res[3]:
                cash_out = res[3] * -1
            if res[4]:
                total = res[4]
            report_ids.append((0,0,{
                    'tanggal' : res[0],
                    'cash_in' : cash_in,
                    'ket_cash_in' : res[1],
                    'cash_out': cash_out,
                    'ket_cash_out' : res[1],
                    'total' : cash_in - cash_out,
                    }))

        data = {
            'name'       : "LAPORAN CASH IN / CASH OUT",
            'company_id' : self.env.user.company_id.id,
            'report_ids' : report_ids,
        }
        self.write(data)

    @api.multi
    def action_print_report_cash_in(self):
        self._get_cash_in()
        report_action = self.env.ref(
            'vit_cash_in_cash_out.report_vit_transaksi_cash'
        ).report_action(self)

        report_action['close_on_report_download']=True

        return report_action

    @api.multi
    def action_print_report_cash_out(self):
        self._get_cash_out()
        report_action = self.env.ref(
            'vit_cash_in_cash_out.report_vit_transaksi_cash'
        ).report_action(self)

        report_action['close_on_report_download']=True

        return report_action

    @api.multi
    def action_print_report_cash_in_out(self):
        self._get_cash_in_out()
        report_action = self.env.ref(
            'vit_cash_in_cash_out.report_vit_cash_in_out'
        ).report_action(self)

        report_action['close_on_report_download']=True

        return report_action

CashInOutWizard()

class TransaksiCIOWizard(models.TransientModel):
    _name = "transaksi.cash_in_out.wizard"
    _description = "transaksi.cash_in_out.wizard"

    name = fields.Char( string="Nama Transaksi",  help="", )
    tanggal = fields.Date( string="Tanggal",  help="", )
    jumlah = fields.Float( string="Jumlah",  help="", )
    keterangan = fields.Char( string="Keterangan",  help="", )
    no_voucher = fields.Char( string="No voucher",  help="", )

    cio_wizard_id = fields.Many2one(comodel_name="cash.in.out.wizard",  string="Cash in out",  help="", )
    kode_transaksi = fields.Many2one(comodel_name="account.account",  string="Kode transaksi",  help="", )
    
TransaksiCIOWizard()


class ReportCIOWizard(models.TransientModel):
    _name = "report.cash_in_out.wizard"
    _description = "report.cash_in_out.wizard"

    tanggal = fields.Date( string="Tanggal",  help="", )
    cash_in = fields.Float( string="Cash In",  help="", )
    ket_cash_in = fields.Char( string="Keterangan Cash In",  help="", )
    cash_out = fields.Float( string="Cash Out",  help="", )
    ket_cash_out = fields.Char( string="Keterangan Cash Out",  help="", )
    total = fields.Float( string="Total",  help="", )

    cio_wizard_id = fields.Many2one(comodel_name="cash.in.out.wizard",  string="Cash in out",  help="", )
    
ReportCIOWizard()