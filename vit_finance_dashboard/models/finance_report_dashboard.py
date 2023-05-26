# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import Warning, UserError
import time
from datetime import date, datetime
import logging
_logger = logging.getLogger(__name__)

class FinanceReportDashType(models.Model):
    _name = 'vit.finance_report_dashboard_type'
    _description = 'Financial Report Dashboard Type'

    name = fields.Char( required=True)
    types = fields.Selection([('ltbs', 'Laba/Rugi Bersih'), ('pm', 'Pendapatan Murni'), ('tbu', 'Total Beban Usaha'), ('ba', 'Saldo Kas dan Setara Kas'), ('rec', 'Saldo Piutang'), ('cl4', 'Saldo Pinjaman'), ('ta', 'Total Aset'), ('netto', 'Total Aktiva Tetap')], default='ltbs', required=True)

class FinanceReportDash(models.Model):
    _name = 'vit.finance_report_dashboard'
    _description = 'Financial Report Dashboard'
    _inherit = ['mail.thread']

    name        = fields.Char( required=True)
    start_date  = fields.Date( string="Start date", required=True, track_visibility='onchange', help="")
    end_date    = fields.Date( string="End date", required=True, track_visibility='onchange', help="")
    
    company_id   = fields.Many2one( comodel_name="res.company",  string="Company", index=True, default=lambda self: self.env.user.company_id.id)
    frd_line_ids = fields.One2many(comodel_name="vit.finance_report_dashboard_line",  inverse_name="frd_id",  string="FRD Lines",  help="")

    @api.multi
    def load_dash_line(self, ):
        for frd in self:
            date_start = frd.start_date
            date_end = frd.end_date
            company = frd.company_id.id

            xfrd = self.env['vit.finance_report_dashboard'].search([('company_id','=',company),('start_date','=',date_start),('end_date','=',date_end),('id','!=',frd.id)])
            if xfrd:
                raise Warning(_('Financial Report Dashboard company %s dengan periode %s - %s sudah ada!') % (frd.company_id.name,date_start,date_end))

            self.env.cr.execute("""DELETE FROM vit_finance_report_dashboard_line WHERE frd_id = %s""" % (self.id,))
            
            # select jurnal items
            cr = self.env.cr            
            sql = """select 
                (select abs(sum(aml1.balance))
                    from account_move_line aml1
                    left join account_move am1 on aml1.move_id = am1.id
                    left join account_account aa1 on aml1.account_id = aa1.id
                    left join res_company rc on aml1.company_id = rc.id
                    where aml1.date >= %s and aml1.date <= %s and rc.id = %s and am1.state = 'posted' and aa1.code between %s and %s) as pu,
                (select abs(sum(aml2.balance))
                    from account_move_line aml2
                    left join account_move am2 on aml2.move_id = am2.id
                    left join account_account aa2 on aml2.account_id = aa2.id
                    left join res_company rc on aml2.company_id = rc.id
                    where aml2.date >= %s and aml2.date <= %s and rc.id = %s and am2.state = 'posted' and aa2.code between %s and %s) as bpp,
                (select abs(sum(aml3.balance))
                    from account_move_line aml3
                    left join account_move am3 on aml3.move_id = am3.id
                    left join account_account aa3 on aml3.account_id = aa3.id
                    left join res_company rc on aml3.company_id = rc.id
                    where aml3.date >= %s and aml3.date <= %s and rc.id = %s and am3.state = 'posted' and aa3.code between %s and %s) as bkp,
                (select abs(sum(aml4.balance))
                    from account_move_line aml4
                    left join account_move am4 on aml4.move_id = am4.id
                    left join account_account aa4 on aml4.account_id = aa4.id
                    left join res_company rc on aml4.company_id = rc.id
                    where aml4.date >= %s and aml4.date <= %s and rc.id = %s and am4.state = 'posted' and aa4.code between %s and %s) as bpl,
                (select abs(sum(aml5.balance))
                    from account_move_line aml5
                    left join account_move am5 on aml5.move_id = am5.id
                    left join account_account aa5 on aml5.account_id = aa5.id
                    left join res_company rc on aml5.company_id = rc.id
                    where aml5.date >= %s and aml5.date <= %s and rc.id = %s and am5.state = 'posted' and aa5.code between %s and %s) as pda,
                (select abs(sum(aml6.balance))
                    from account_move_line aml6
                    left join account_move am6 on aml6.move_id = am6.id
                    left join account_account aa6 on aml6.account_id = aa6.id
                    left join res_company rc on aml6.company_id = rc.id
                    where aml6.date >= %s and aml6.date <= %s and rc.id = %s and am6.state = 'posted' and aa6.code between %s and %s) as uma,
                (select abs(sum(aml7c.credit))
                    from account_move_line aml7c
                    left join account_move am7c on aml7c.move_id = am7c.id
                    left join account_account aa7c on aml7c.account_id = aa7c.id
                    left join res_company rc on aml7c.company_id = rc.id
                    where aml7c.date >= %s and aml7c.date <= %s and rc.id = %s and am7c.state = 'posted' and aa7c.code between %s and %s) as pbl1c,
                (select abs(sum(aml7d.debit))
                    from account_move_line aml7d
                    left join account_move am7d on aml7d.move_id = am7d.id
                    left join account_account aa7d on aml7d.account_id = aa7d.id
                    left join res_company rc on aml7d.company_id = rc.id
                    where aml7d.date >= %s and aml7d.date <= %s and rc.id = %s and am7d.state = 'posted' and aa7d.code between %s and %s) as pbl1d,
                (select abs(sum(aml8.balance))
                    from account_move_line aml8
                    left join account_move am8 on aml8.move_id = am8.id
                    left join account_account aa8 on aml8.account_id = aa8.id
                    left join res_company rc on aml8.company_id = rc.id
                    where aml8.date >= %s and aml8.date <= %s and rc.id = %s and am8.state = 'posted' and aa8.code between %s and %s) as pbl2,
                (select abs(sum(aml9.balance))
                    from account_move_line aml9
                    left join account_move am9 on aml9.move_id = am9.id
                    left join account_account aa9 on aml9.account_id = aa9.id
                    left join res_company rc on aml9.company_id = rc.id
                    where aml9.date >= %s and aml9.date <= %s and rc.id = %s and am9.state = 'posted' and aa9.code between %s and %s) as pbl3,
                (select abs(sum(aml10.balance))
                    from account_move_line aml10
                    left join account_move am10 on aml10.move_id = am10.id
                    left join account_account aa10 on aml10.account_id = aa10.id
                    left join res_company rc on aml10.company_id = rc.id
                    where aml10.date >= %s and aml10.date <= %s and rc.id = %s and am10.state = 'posted' and aa10.code between %s and %s) as bpj1,
                (select abs(sum(aml11.balance))
                    from account_move_line aml11
                    left join account_move am11 on aml11.move_id = am11.id
                    left join account_account aa11 on aml11.account_id = aa11.id
                    left join res_company rc on aml11.company_id = rc.id
                    where aml11.date >= %s and aml11.date <= %s and rc.id = %s and am11.state = 'posted' and aa11.code between %s and %s) as bpj2,
                (select abs(sum(aml12.balance))
                    from account_move_line aml12
                    left join account_move am12 on aml12.move_id = am12.id
                    left join account_account aa12 on aml12.account_id = aa12.id
                    left join res_company rc on aml12.company_id = rc.id
                    where aml12.date >= %s and aml12.date <= %s and rc.id = %s and am12.state = 'posted' and aa12.code between %s and %s) as kas,
                (select abs(sum(aml13.balance))
                    from account_move_line aml13
                    left join account_move am13 on aml13.move_id = am13.id
                    left join account_account aa13 on aml13.account_id = aa13.id
                    left join res_company rc on aml13.company_id = rc.id
                    where aml13.date >= %s and aml13.date <= %s and rc.id = %s and am13.state = 'posted' and aa13.code between %s and %s) as bank,
                (select abs(sum(aml14.balance))
                    from account_move_line aml14
                    left join account_move am14 on aml14.move_id = am14.id
                    left join account_account aa14 on aml14.account_id = aa14.id
                    left join res_company rc on aml14.company_id = rc.id
                    where aml14.date >= %s and aml14.date <= %s and rc.id = %s and am14.state = 'posted' and aa14.code between %s and %s) as de,
                (select abs(sum(aml15.balance))
                    from account_move_line aml15
                    left join account_move am15 on aml15.move_id = am15.id
                    left join account_account aa15 on aml15.account_id = aa15.id
                    left join res_company rc on aml15.company_id = rc.id
                    where aml15.date >= %s and aml15.date <= %s and rc.id = %s and am15.state = 'posted' and aa15.code between %s and %s) as ga,
                (select abs(sum(aml16.balance))
                    from account_move_line aml16
                    left join account_move am16 on aml16.move_id = am16.id
                    left join account_account aa16 on aml16.account_id = aa16.id
                    left join res_company rc on aml16.company_id = rc.id
                    where aml16.date >= %s and aml16.date <= %s and rc.id = %s and am16.state = 'posted' and aa16.code between %s and %s) as inv,
                (select abs(sum(aml17.balance))
                    from account_move_line aml17
                    left join account_move am17 on aml17.move_id = am17.id
                    left join account_account aa17 on aml17.account_id = aa17.id
                    left join res_company rc on aml17.company_id = rc.id
                    where aml17.date >= %s and aml17.date <= %s and rc.id = %s and am17.state = 'posted' and aa17.code between %s and %s) as ip,
                (select abs(sum(aml18.balance))
                    from account_move_line aml18
                    left join account_move am18 on aml18.move_id = am18.id
                    left join account_account aa18 on aml18.account_id = aa18.id
                    left join res_company rc on aml18.company_id = rc.id
                    where aml18.date >= %s and aml18.date <= %s and rc.id = %s and am18.state = 'posted' and aa18.code between %s and %s) as rec,
                (select abs(sum(aml19.balance))
                    from account_move_line aml19
                    left join account_move am19 on aml19.move_id = am19.id
                    left join account_account aa19 on aml19.account_id = aa19.id
                    left join res_company rc on aml19.company_id = rc.id
                    where aml19.date >= %s and aml19.date <= %s and rc.id = %s and am19.state = 'posted' and aa19.code between %s and %s) as pui,
                (select abs(sum(aml20.balance))
                    from account_move_line aml20
                    left join account_move am20 on aml20.move_id = am20.id
                    left join account_account aa20 on aml20.account_id = aa20.id
                    left join res_company rc on aml20.company_id = rc.id
                    where aml20.date >= %s and aml20.date <= %s and rc.id = %s and am20.state = 'posted' and aa20.code between %s and %s) as pl,
                (select abs(sum(aml21.balance))
                    from account_move_line aml21
                    left join account_move am21 on aml21.move_id = am21.id
                    left join account_account aa21 on aml21.account_id = aa21.id
                    left join res_company rc on aml21.company_id = rc.id
                    where aml21.date >= %s and aml21.date <= %s and rc.id = %s and am21.state = 'posted' and aa21.code between %s and %s) as neto,
                (select abs(sum(aml22.balance))
                    from account_move_line aml22
                    left join account_move am22 on aml22.move_id = am22.id
                    left join account_account aa22 on aml22.account_id = aa22.id
                    left join res_company rc on aml22.company_id = rc.id
                    where aml22.date >= %s and aml22.date <= %s and rc.id = %s and am22.state = 'posted' and aa22.code between %s and %s) as nebo,
                (select abs(sum(aml23.balance))
                    from account_move_line aml23
                    left join account_move am23 on aml23.move_id = am23.id
                    left join account_account aa23 on aml23.account_id = aa23.id
                    left join res_company rc on aml23.company_id = rc.id
                    where aml23.date >= %s and aml23.date <= %s and rc.id = %s and am23.state = 'posted' and aa23.code between %s and %s) as ahgn0,
                (select abs(sum(aml24.balance))
                    from account_move_line aml24
                    left join account_move am24 on aml24.move_id = am24.id
                    left join account_account aa24 on aml24.account_id = aa24.id
                    left join res_company rc on aml24.company_id = rc.id
                    where aml24.date >= %s and aml24.date <= %s and rc.id = %s and am24.state = 'posted' and aa24.code between %s and %s) as ahgn1,
                (select abs(sum(aml25.balance))
                    from account_move_line aml25
                    left join account_move am25 on aml25.move_id = am25.id
                    left join account_account aa25 on aml25.account_id = aa25.id
                    left join res_company rc on aml25.company_id = rc.id
                    where aml25.date >= %s and aml25.date <= %s and rc.id = %s and am25.state = 'posted' and aa25.code between %s and %s) as pig0,
                (select abs(sum(aml26.balance))
                    from account_move_line aml26
                    left join account_move am26 on aml26.move_id = am26.id
                    left join account_account aa26 on aml26.account_id = aa26.id
                    left join res_company rc on aml26.company_id = rc.id
                    where aml26.date >= %s and aml26.date <= %s and rc.id = %s and am26.state = 'posted' and aa26.code between %s and %s) as pig1,
                (select abs(sum(aml27.balance))
                    from account_move_line aml27
                    left join account_move am27 on aml27.move_id = am27.id
                    left join account_account aa27 on aml27.account_id = aa27.id
                    left join res_company rc on aml27.company_id = rc.id
                    where aml27.date >= %s and aml27.date <= %s and rc.id = %s and am27.state = 'posted' and aa27.code between %s and %s) as attb0,
                (select abs(sum(aml28.balance))
                    from account_move_line aml28
                    left join account_move am28 on aml28.move_id = am28.id
                    left join account_account aa28 on aml28.account_id = aa28.id
                    left join res_company rc on aml28.company_id = rc.id
                    where aml28.date >= %s and aml28.date <= %s and rc.id = %s and am28.state = 'posted' and aa28.code between %s and %s) as attb1,
                (select abs(sum(aml29.balance))
                    from account_move_line aml29
                    left join account_move am29 on aml29.move_id = am29.id
                    left join account_account aa29 on aml29.account_id = aa29.id
                    left join res_company rc on aml29.company_id = rc.id
                    where aml29.date >= %s and aml29.date <= %s and rc.id = %s and am29.state = 'posted' and aa29.code between %s and %s) as atbd,
                (select abs(sum(aml30.balance))
                    from account_move_line aml30
                    left join account_move am30 on aml30.move_id = am30.id
                    left join account_account aa30 on aml30.account_id = aa30.id
                    left join res_company rc on aml30.company_id = rc.id
                    where aml30.date >= %s and aml30.date <= %s and rc.id = %s and am30.state = 'posted' and aa30.code between %s and %s) as pdpn,
                (select abs(sum(aml31.balance))
                    from account_move_line aml31
                    left join account_move am31 on aml31.move_id = am31.id
                    left join account_account aa31 on aml31.account_id = aa31.id
                    left join res_company rc on aml31.company_id = rc.id
                    where aml31.date >= %s and aml31.date <= %s and rc.id = %s and am31.state = 'posted' and aa31.code between %s and %s) as prs,
                (select abs(sum(aml32.balance))
                    from account_move_line aml32
                    left join account_move am32 on aml32.move_id = am32.id
                    left join account_account aa32 on aml32.account_id = aa32.id
                    left join res_company rc on aml32.company_id = rc.id
                    where aml32.date >= %s and aml32.date <= %s and rc.id = %s and am32.state = 'posted' and aa32.code between %s and %s) as pdp,
                (select abs(sum(aml33.balance))
                    from account_move_line aml33
                    left join account_move am33 on aml33.move_id = am33.id
                    left join account_account aa33 on aml33.account_id = aa33.id
                    left join res_company rc on aml33.company_id = rc.id
                    where aml33.date >= %s and aml33.date <= %s and rc.id = %s and am33.state = 'posted' and aa33.code between %s and %s) as pdpj,
                (select abs(sum(aml34.balance))
                    from account_move_line aml34
                    left join account_move am34 on aml34.move_id = am34.id
                    left join account_account aa34 on aml34.account_id = aa34.id
                    left join res_company rc on aml34.company_id = rc.id
                    where aml34.date >= %s and aml34.date <= %s and rc.id = %s and am34.state = 'posted' and aa34.code between %s and %s) as pya,
                (select abs(sum(aml35.balance))
                    from account_move_line aml35
                    left join account_move am35 on aml35.move_id = am35.id
                    left join account_account aa35 on aml35.account_id = aa35.id
                    left join res_company rc on aml35.company_id = rc.id
                    where aml35.date >= %s and aml35.date <= %s and rc.id = %s and am35.state = 'posted' and aa35.code between %s and %s) as aln,
                (select abs(sum(aml36.balance))
                    from account_move_line aml36
                    left join account_move am36 on aml36.move_id = am36.id
                    left join account_account aa36 on aml36.account_id = aa36.id
                    left join res_company rc on aml36.company_id = rc.id
                    where aml36.date >= %s and aml36.date <= %s and rc.id = %s and am36.state = 'posted' and aa36.code between %s and %s) as pdpjp,
                (select abs(sum(aml37.balance))
                    from account_move_line aml37
                    left join account_move am37 on aml37.move_id = am37.id
                    left join account_account aa37 on aml37.account_id = aa37.id
                    left join res_company rc on aml37.company_id = rc.id
                    where aml37.date >= %s and aml37.date <= %s and rc.id = %s and am37.state = 'posted' and aa37.code between %s and %s) as atpjp,
                (select abs(sum(aml38.balance))
                    from account_move_line aml38
                    left join account_move am38 on aml38.move_id = am38.id
                    left join account_account aa38 on aml38.account_id = aa38.id
                    left join res_company rc on aml38.company_id = rc.id
                    where aml38.date >= %s and aml38.date <= %s and rc.id = %s and am38.state = 'posted' and aa38.code between %s and %s) as apt,
                (select abs(sum(aml39.balance))
                    from account_move_line aml39
                    left join account_move am39 on aml39.move_id = am39.id
                    left join account_account aa39 on aml39.account_id = aa39.id
                    left join res_company rc on aml39.company_id = rc.id
                    where aml39.date >= %s and aml39.date <= %s and rc.id = %s and am39.state = 'posted' and aa39.code between %s and %s) as atll,
                (select abs(sum(aml40.balance))
                    from account_move_line aml40
                    left join account_move am40 on aml40.move_id = am40.id
                    left join account_account aa40 on aml40.account_id = aa40.id
                    left join res_company rc on aml40.company_id = rc.id
                    where aml40.date >= %s and aml40.date <= %s and rc.id = %s and am40.state = 'posted' and aa40.code between %s and %s) as cl4
                """
            cr.execute(sql, (date_start,date_end,company,'4001001001','4001001099',date_start,date_end,company,'5001001001','5001001099',date_start,date_end,company,'6001001001','6001001009',
                date_start,date_end,company,'6001002001','6001002099',date_start,date_end,company,'6001003001','6001003009',date_start,date_end,company,'6001004001','6001004099',date_start,date_end,company,'7001001001','7001001099',
                date_start,date_end,company,'7001001001','7001001099',date_start,date_end,company,'7001002001','7001002099',date_start,date_end,company,'7002001001','7002001099',
                date_start,date_end,company,'8001001001','8001001099',date_start,date_end,company,'8001002001','8001002099',date_start,date_end,company,'1201101101','1201101109',
                date_start,date_end,company,'1201201200','1201201299',date_start,date_end,company,'1201202001','1201202009',date_start,date_end,company,'1201203001','1201203009',
                date_start,date_end,company,'1202001000','1202001099',date_start,date_end,company,'1203001001','1203001009',date_start,date_end,company,'1204001000','1204001999',
                date_start,date_end,company,'1204101000','1204101999',date_start,date_end,company,'1205001000','1205001999',date_start,date_end,company,'1301001100','1301001199',
                date_start,date_end,company,'1301001200','1301001299',date_start,date_end,company,'1302001101','1302001109',date_start,date_end,company,'1302001200','1302001299',
                date_start,date_end,company,'1303001101','1303001109',date_start,date_end,company,'1303001201','1303001209',date_start,date_end,company,'1304001101','1304001109',
                date_start,date_end,company,'1304001201','1304001209',date_start,date_end,company,'1305001000','1305001099',date_start,date_end,company,'1401001000','1401001099',
                date_start,date_end,company,'1206001000','1206001099',date_start,date_end,company,'1207001000','1207001099',date_start,date_end,company,'1208001000','1208001099',
                date_start,date_end,company,'1209001000','1209001099',date_start,date_end,company,'1210001000','1210001099',date_start,date_end,company,'1501001000','1501001099',
                date_start,date_end,company,'1224001000','1224001999',date_start,date_end,company,'1601001000','1601001099',date_start,date_end,company,'1701001000','1701001099',
                date_start,date_end,company,'2101002000','2101002099',))

            result = cr.fetchall()
            for res in result:
                # import pdb;pdb.set_trace()
                if res[0] == None:
                    pu = 0.0
                else:
                    pu = res[0]
                if res[1] == None:
                    bpp = 0.0
                else:
                    bpp = res[1]
                if res[2] == None:
                    bkp = 0.0
                else:
                    bkp = res[2]
                if res[3] == None:
                    bpl = 0.0
                else:
                    bpl = res[3]

                if res[4] == None:
                    pda = 0.0
                else:
                    pda = res[4]
                if res[5] == None:
                    uma = 0.0
                else:
                    uma = res[5]
                if res[6] == None:
                    pbl1c = 0.0
                else:
                    pbl1c = res[6]
                if res[7] == None:
                    pbl1d = 0.0
                else:
                    pbl1d = res[7]
                if res[8] == None:
                    pbl2 = 0.0
                else:
                    pbl2 = res[8]
                if res[9] == None:
                    pbl3 = 0.0
                else:
                    pbl3 = res[9]
                if res[10] == None:
                    bpj1 = 0.0
                else:
                    bpj1 = res[10]
                if res[11] == None:
                    bpj2 = 0.0
                else:
                    bpj2 = res[11]
                if res[12] == None:
                    kas = 0.0
                else:
                    kas = res[12]
                if res[13] == None:
                    bank = 0.0
                else:
                    bank = res[13]
                if res[14] == None:
                    de = 0.0
                else:
                    de = res[14]
                if res[15] == None:
                    ga = 0.0
                else:
                    ga = res[15]
                if res[16] == None:
                    inv = 0.0
                else:
                    inv = res[16]
                if res[17] == None:
                    ip = 0.0
                else:
                    ip = res[17]
                if res[18] == None:
                    rec = 0.0
                else:
                    rec = res[18]
                if res[19] == None:
                    pui = 0.0
                else:
                    pui = res[19]
                if res[20] == None:
                    pl = 0.0
                else:
                    pl = res[20]
                if res[21] == None:
                    neto = 0.0
                else:
                    neto = res[21]
                if res[22] == None:
                    nebo = 0.0
                else:
                    nebo = res[22]
                if res[23] == None:
                    ahgn0 = 0.0
                else:
                    ahgn0 = res[23]
                if res[24] == None:
                    ahgn1 = 0.0
                else:
                    ahgn1 = res[24]
                if res[25] == None:
                    pig0 = 0.0
                else:
                    pig0 = res[25]
                if res[26] == None:
                    pig1 = 0.0
                else:
                    pig1 = res[26]
                if res[27] == None:
                    attb0 = 0.0
                else:
                    attb0 = res[27]
                if res[28] == None:
                    attb1 = 0.0
                else:
                    attb1 = res[28]
                if res[29] == None:
                    atbd = 0.0
                else:
                    atbd = res[29]
                if res[30] == None:
                    pdpn = 0.0
                else:
                    pdpn = res[30]
                if res[31] == None:
                    prs = 0.0
                else:
                    prs = res[31]
                if res[32] == None:
                    pdp = 0.0
                else:
                    pdp = res[32]
                if res[33] == None:
                    pdpj = 0.0
                else:
                    pdpj = res[33]
                if res[34] == None:
                    pya = 0.0
                else:
                    pya = res[34]
                if res[35] == None:
                    aln = 0.0
                else:
                    aln = res[35]
                if res[36] == None:
                    pdpjp = 0.0
                else:
                    pdpjp = res[36]
                if res[37] == None:
                    atpjp = 0.0
                else:
                    atpjp = res[37]
                if res[38] == None:
                    apt = 0.0
                else:
                    apt = res[38]
                if res[39] == None:
                    atll = 0.0
                else:
                    atll = res[39]
                if res[40] == None:
                    cl4 = 0.0
                else:
                    cl4 = res[40]


                inc = pu - bpp
                lex = bkp + bpl + pda + uma
                nep = inc - lex
                pbl1 = pbl1c - pbl1d
                pbl = pbl1 + pbl2 - pbl3
                lsp = nep + pbl
                bpj = bpj1 + bpj2
                ltbs = lsp - bpj
                pm = pu + pbl1 + pbl2
                tbu = bpp + lex + pbl3
                ba = kas + bank + de + ga
                ca = ba + inv + ip + rec + pui + pl + prs + pdp + pdpj + pya + aln
                netto = neto - nebo
                ahgn = ahgn0 - ahgn1
                pig = pig0 - pig1
                attb = attb0 - attb1
                atlr = netto + ahgn + pig + attb + atbd + pdpn + pdpjp + atpjp + apt + atll
                ta = ca + atlr

                t1 = self.env['vit.finance_report_dashboard_type'].search([('types', '=', 'ltbs')])
                t2 = self.env['vit.finance_report_dashboard_type'].search([('types', '=', 'pm')])
                t3 = self.env['vit.finance_report_dashboard_type'].search([('types', '=', 'tbu')])
                t4 = self.env['vit.finance_report_dashboard_type'].search([('types', '=', 'ba')])
                t5 = self.env['vit.finance_report_dashboard_type'].search([('types', '=', 'rec')])
                t6 = self.env['vit.finance_report_dashboard_type'].search([('types', '=', 'cl4')])
                t7 = self.env['vit.finance_report_dashboard_type'].search([('types', '=', 'ta')])
                t8 = self.env['vit.finance_report_dashboard_type'].search([('types', '=', 'netto')])

                # insert Laba Rugi
                self.env.cr.execute("""
                    INSERT INTO vit_finance_report_dashboard_line (name, amount, start_date, end_date, company_id, frd_id)
                    VALUES (%s, %s, '%s', '%s', %s, %s)
                    """ % (t1.id, ltbs, date_start, date_end, company, frd.id,))
                # insert Pendapatan Murni
                self.env.cr.execute("""
                    INSERT INTO vit_finance_report_dashboard_line (name, amount, start_date, end_date, company_id, frd_id)
                    VALUES (%s, %s, '%s', '%s', %s, %s)
                    """ % (t2.id, pm, date_start, date_end, company, frd.id,))
                # insert Total Beban Usaha
                self.env.cr.execute("""
                    INSERT INTO vit_finance_report_dashboard_line (name, amount, start_date, end_date, company_id, frd_id)
                    VALUES (%s, %s, '%s', '%s', %s, %s)
                    """ % (t3.id, tbu, date_start, date_end, company, frd.id,))
                # insert Saldo Kas dan Setara Kas
                self.env.cr.execute("""
                    INSERT INTO vit_finance_report_dashboard_line (name, amount, start_date, end_date, company_id, frd_id)
                    VALUES (%s, %s, '%s', '%s', %s, %s)
                    """ % (t4.id, ba, date_start, date_end, company, frd.id,))
                # insert Saldo Piutang
                self.env.cr.execute("""
                    INSERT INTO vit_finance_report_dashboard_line (name, amount, start_date, end_date, company_id, frd_id)
                    VALUES (%s, %s, '%s', '%s', %s, %s)
                    """ % (t5.id, rec, date_start, date_end, company, frd.id,))
                # insert Saldo Pinjaman
                self.env.cr.execute("""
                    INSERT INTO vit_finance_report_dashboard_line (name, amount, start_date, end_date, company_id, frd_id)
                    VALUES (%s, %s, '%s', '%s', %s, %s)
                    """ % (t6.id, cl4, date_start, date_end, company, frd.id,))
                # insert Total Aset
                self.env.cr.execute("""
                    INSERT INTO vit_finance_report_dashboard_line (name, amount, start_date, end_date, company_id, frd_id)
                    VALUES (%s, %s, '%s', '%s', %s, %s)
                    """ % (t7.id, ta, date_start, date_end, company, frd.id,))
                # insert Total Aktiva Tetap
                self.env.cr.execute("""
                    INSERT INTO vit_finance_report_dashboard_line (name, amount, start_date, end_date, company_id, frd_id)
                    VALUES (%s, %s, '%s', '%s', %s, %s)
                    """ % (t8.id, netto, date_start, date_end, company, frd.id,))
                
                
class FinanceReportDashLine(models.Model):
    _name = 'vit.finance_report_dashboard_line'
    _description = 'Financial Report Dashboard Item'

    start_date  = fields.Date( string="Start date", related="frd_id.start_date", store=True, help="")
    end_date    = fields.Date( string="End date", help="")
    amount      = fields.Float( string="Amount")
    
    frd_id      = fields.Many2one( comodel_name="vit.finance_report_dashboard", string="Report Dashboard", ondelete='cascade', help="")
    company_id  = fields.Many2one(comodel_name="res.company", string="Company", help="")
    name        = fields.Many2one(comodel_name="vit.finance_report_dashboard_type", string="Name", help="")
    