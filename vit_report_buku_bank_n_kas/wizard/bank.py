from odoo import api, fields, models, _
import time
from datetime import date, datetime
import csv
from odoo.modules import get_module_path
from odoo.exceptions import UserError
import copy
import logging
from io import StringIO
import base64
from io import BytesIO
import xlsxwriter
_logger = logging.getLogger(__name__)

class export_buku_bank_wizard(models.TransientModel):
    _name = 'vit.export_buku_bank'

    current_date  = date.today()

    def _get_years(self):
        this_year = datetime.today().year
        results = sorted([(str(x), str(x)) for x in range(this_year - 5, this_year + 2)],reverse = True)
        return results

    @api.model
    def _get_default_year(self):
        year = self.current_date.strftime('%Y')
        return year
    
    export_file = fields.Binary(string="Export File",  )
    export_filename = fields.Char(string="Export File",  )

    date_start  = fields.Date(string='Start Date', compute='get_date_start_end', store=True)
    date_end    = fields.Date(string='End Date', compute='get_date_start_end', store=True)

    journal_id  = fields.Many2one('account.journal', string='Jurnal')
    html        = fields.Html('HTML')
    
    year   = fields.Selection(_get_years,string="Tahun", default = _get_default_year,)
    month = fields.Selection([
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
        (12, 'DESEMBER'),
        ], string='Bulan', default=1,)

    @api.depends('month','year')
    def get_date_start_end(self):
        for ra in self:
            if ra.year:
                thn = ra.year
                if ra.month == 1:
                    ra.date_start = self.current_date.strftime(thn +'-01-01')
                    ra.date_end = self.current_date.strftime(thn +'-01-31')
                if ra.month == 2:
                    ra.date_start = self.current_date.strftime(thn +'-02-01')
                    if float(thn) % 4 == 0 :
                        ra.date_end = self.current_date.strftime(thn +'-02-29')
                    else:
                        ra.date_end = self.current_date.strftime(thn +'-02-28')
                if ra.month == 3:
                    ra.date_start = self.current_date.strftime(thn +'-03-01')
                    ra.date_end = self.current_date.strftime(thn +'-03-31')
                if ra.month == 4:
                    ra.date_start = self.current_date.strftime(thn +'-04-01')
                    ra.date_end = self.current_date.strftime(thn +'-04-30')
                if ra.month == 5:
                    ra.date_start = self.current_date.strftime(thn +'-05-01')
                    ra.date_end = self.current_date.strftime(thn +'-05-31')
                if ra.month == 6:
                    ra.date_start = self.current_date.strftime(thn +'-06-01')
                    ra.date_end = self.current_date.strftime(thn +'-06-30')
                if ra.month == 7:
                    ra.date_start = self.current_date.strftime(thn +'-07-01')
                    ra.date_end = self.current_date.strftime(thn +'-07-31')
                if ra.month == 8:
                    ra.date_start = self.current_date.strftime(thn +'-08-01')
                    ra.date_end = self.current_date.strftime(thn +'-08-31')
                if ra.month == 9:
                    ra.date_start = self.current_date.strftime(thn +'-09-01')
                    ra.date_end = self.current_date.strftime(thn +'-09-30')
                if ra.month == 10:
                    ra.date_start = self.current_date.strftime(thn +'-10-01')
                    ra.date_end = self.current_date.strftime(thn +'-10-31')
                if ra.month == 11:
                    ra.date_start = self.current_date.strftime(thn +'-11-01')
                    ra.date_end = self.current_date.strftime(thn +'-11-30')
                if ra.month == 12:
                    ra.date_start = self.current_date.strftime(thn +'-12-01')
                    ra.date_end = self.current_date.strftime(thn +'-12-31')

    def cell_format(self, workbook):
        cell_format = {}
        cell_format['header'] = workbook.add_format({
            'font_size': 12,
            'font_color': '#000000',
            'align': 'center',
            'bg_color': '#d3d3d3',
            'border': True,
        })
        cell_format['content'] = workbook.add_format({
            'font_size': 11,
            'border': True,
            'align': 'center',
        })
        cell_format['contentf'] = workbook.add_format({
            'font_size': 11,
            'border': True,
            'align': 'right',
        })
        cell_format['info'] = workbook.add_format({
            'font_size': 16,
        })
        return cell_format, workbook

    @api.multi
    def get_datas(self):
        # import pdb;pdb.set_trace()
        res = {}
        cra = self.env.cr
        cr = self.env.cr
        crx = self.env.cr
        headers = [
            "Tanggal",
            "No. Jurnal",
            "Deskripsi",
            "Label",
            "Kode Akun",
            "Debit",
            "Kredit",
            "Balance",
        ]

        sqla = """SELECT sum(sa.balance) as saldo_awal
                FROM account_move_line sa
                LEFT JOIN account_account saa ON sa.account_id = saa.id
                LEFT JOIN account_move ams ON sa.move_id = ams.id
                LEFT JOIN account_journal ajs ON ajs.default_debit_account_id = saa.id
                WHERE sa.date < %s AND ams.state = 'posted'
                """
        if self.journal_id:
            sqla += " AND ajs.id = %s  " % self.journal_id.id
        else:
            sqla += " AND ajs.type = 'bank' "

        cra.execute(sqla, (self.date_start,))
        recorda = cra.dictfetchall()
        initial = []
        values = []
        final = []
        sal = 0.0
        for reca in recorda:            
            if reca['saldo_awal'] == None:
                sal = 0.0
            else:
                sal = reca['saldo_awal']
            initial.append({
                "Tanggal"   : '',
                "No. Jurnal": '',
                "Deskripsi" : 'Saldo Awal',
                "Label"     : '',
                "Kode Akun" : '',
                "Debit"     : '',
                "Kredit"    : '',
                "Balance"   : "{:,.2f}".format(sal),
            })

        sql = """SELECT aml.id as id, aml.date as tgl, am.name as jnl, aml.ref as desk, aml.name as lbl, aa.code as acc, aml.credit as debit, aml.debit as credit, aml.balance as balance
                FROM account_move_line aml
                LEFT JOIN account_account aa ON aml.account_id = aa.id
                LEFT JOIN account_move am ON aml.move_id = am.id
                LEFT JOIN account_move_line amj ON amj.move_id = am.id
                LEFT JOIN account_account aaj ON amj.account_id = aaj.id
                LEFT JOIN account_journal aj ON aj.default_debit_account_id = aaj.id
                WHERE aml.date >= %s AND aml.date <= %s AND am.state = 'posted' AND aa.id != aaj.id
                """
        if self.journal_id:
            sql += " AND aj.id = %s GROUP BY aml.id, am.name, aa.id ORDER BY aml.date " % self.journal_id.id
        else:
            sql += " AND aj.type = 'bank' GROUP BY aml.id, am.name, aa.id ORDER BY aml.date "

        cr.execute(sql, (self.date_start,self.date_end,))
        record = cr.dictfetchall()
        for rec in record:
            sqlx = """SELECT sum(amlx.balance) as balance
                FROM account_move_line amlx
                LEFT JOIN account_account aax ON amlx.account_id = aax.id
                LEFT JOIN account_move amx ON amlx.move_id = amx.id
                LEFT JOIN account_move_line amjx ON amjx.move_id = amx.id
                LEFT JOIN account_account aajx ON amjx.account_id = aajx.id
                LEFT JOIN account_journal ajx ON ajx.default_debit_account_id = aajx.id
                WHERE amlx.id <= %s AND amx.state = 'posted' AND aax.id != aajx.id
                """
            if self.journal_id:
                sqlx += " AND ajx.id = %s " % self.journal_id.id
            else:
                sqlx += " AND ajx.type = 'bank' "

            crx.execute(sqlx, (rec['id'],))
            recordx = crx.dictfetchall()
            for recx in recordx:
                values.append({
                    "Tanggal"   : datetime.strftime(rec['tgl'], '%d-%m-%Y'),
                    "No. Jurnal": rec['jnl'],
                    "Deskripsi" : rec['desk'],
                    "Label"     : rec['lbl'],
                    "Kode Akun" : rec['acc'],
                    "Debit"     : "{:,.2f}".format(rec['debit']),
                    "Kredit"    : "{:,.2f}".format(rec['credit']),
                    "Balance"   : "{:,.2f}".format(recx['balance'] * -1),
                })

                final.append({
                    "Tanggal"   : '',
                    "No. Jurnal": '',
                    "Deskripsi" : 'Saldo Akhir',
                    "Label"     : '',
                    "Kode Akun" : '',
                    "Debit"     : "{:,.2f}".format(sum(rec['debit'] for rec in record)),
                    "Kredit"    : "{:,.2f}".format(sum(rec['credit'] for rec in record)),
                    "Balance"   : "{:,.2f}".format(sal - sum(rec['balance'] for rec in record)),
                })

        res['Report Buku Bank'] = [headers, initial, values, final]        
        return res

    @api.multi
    def confirm_button(self):
        self.ensure_one()
        self.get_preview()
        datas = self.get_datas()
        if not datas :
            raise Warning("Data tidak ditemukan.")
        fp = BytesIO()
        workbook = xlsxwriter.Workbook(fp)
        cell_format, workbook = self.cell_format(workbook)
        for sheet, header_content in datas.items():
            headers, initial, contents, final = header_content
            worksheet = workbook.add_worksheet(sheet)
            worksheet.set_column('A:A', 12)
            worksheet.set_column('B:B', 20)
            worksheet.set_column('C:C', 40)
            worksheet.set_column('D:D', 40)
            worksheet.set_column('E:E', 15)
            worksheet.set_column('F:F', 15)
            worksheet.set_column('G:G', 15)
            worksheet.set_column('H:H', 15)
            column_length = len(headers)

            if self.month == 1:
                bulan = 'JANUARI'
            elif self.month == 2:
                bulan = 'FEBRUARI'
            elif self.month == 3:
                bulan = 'MARET'
            elif self.month == 4:
                bulan = 'APRIL'
            elif self.month == 5:
                bulan = 'MEI'
            elif self.month == 6:
                bulan = 'JUNI'
            elif self.month == 7:
                bulan = 'JULI'
            elif self.month == 8:
                bulan = 'AGUSTUS'
            elif self.month == 9:
                bulan = 'SEPTEMBER'
            elif self.month == 10:
                bulan = 'OKTOBER'
            elif self.month == 11:
                bulan = 'NOVEMBER'
            elif self.month == 12:
                bulan = 'DESEMBER'

            column = 0
            row = 0
            if self.journal_id:
                worksheet.write(row, column, 'Buku Bank '+self.journal_id.name, cell_format['info'])
            else:
                worksheet.write(row, column, 'Buku Bank', cell_format['info'])
            row = 1
            worksheet.write(row, column, bulan + ' ' + self.year)
            
            column = 0
            row = 3
            for col in headers :
                worksheet.write(row, column, col, cell_format['header'])
                column += 1
            row = 4
            for ini in initial :
                # column = 0
                # for key, value in ini.items():
                #     worksheet.write(row, column, value, cell_format['content'])
                #     column += 1
                worksheet.write(row, 0, ini['Tanggal'], cell_format['content'])
                worksheet.write(row, 1, ini['No. Jurnal'], cell_format['content'])
                worksheet.write(row, 2, ini['Deskripsi'], cell_format['content'])
                worksheet.write(row, 3, ini['Label'], cell_format['content'])
                worksheet.write(row, 4, ini['Kode Akun'], cell_format['content'])
                worksheet.write(row, 5, ini['Debit'], cell_format['contentf'])
                worksheet.write(row, 6, ini['Kredit'], cell_format['contentf'])
                worksheet.write(row, 7, ini['Balance'], cell_format['contentf'])
            i = 0
            row = 5
            rowc = 5
            for data in contents :
                # column = 0
                # for key, value in data.items():
                #     worksheet.write(row, column, value, cell_format['content'])
                #     column += 1
                worksheet.write(row, 0, data['Tanggal'], cell_format['content'])
                worksheet.write(row, 1, data['No. Jurnal'], cell_format['content'])
                worksheet.write(row, 2, data['Deskripsi'], cell_format['content'])
                worksheet.write(row, 3, data['Label'], cell_format['content'])
                worksheet.write(row, 4, data['Kode Akun'], cell_format['content'])
                worksheet.write(row, 5, data['Debit'], cell_format['contentf'])
                worksheet.write(row, 6, data['Kredit'], cell_format['contentf'])
                worksheet.write(row, 7, data['Balance'], cell_format['contentf'])
                row += 1
                rowc += 1
                i += 1
            row = rowc
            for fin in final :
                # column = 0
                # for key, value in fin.items():
                #     worksheet.write(row, column, value, cell_format['content'])
                #     column += 1
                worksheet.write(row, 0, fin['Tanggal'], cell_format['content'])
                worksheet.write(row, 1, fin['No. Jurnal'], cell_format['content'])
                worksheet.write(row, 2, fin['Deskripsi'], cell_format['content'])
                worksheet.write(row, 3, fin['Label'], cell_format['content'])
                worksheet.write(row, 4, fin['Kode Akun'], cell_format['content'])
                worksheet.write(row, 5, fin['Debit'], cell_format['contentf'])
                worksheet.write(row, 6, fin['Kredit'], cell_format['contentf'])
                worksheet.write(row, 7, fin['Balance'], cell_format['contentf'])

        workbook.close()
        result = base64.encodestring(fp.getvalue())
        if self.journal_id:
            filename = 'Report Buku Bank ' + self.journal_id.name + ' ' + bulan + ' ' + self.year + '.xlsx'
        else:
            filename = 'Report Buku Bank ' + ' ' + self.year + '.xlsx'
        self.write({'export_file':result, 'export_filename':filename})
        return {
            'name': "Export Complete, total %s records" % i,
            'type': 'ir.actions.act_window',
            'res_model': 'vit.export_buku_bank',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'views': [(False, 'form')],
            'target': 'new',
        }


    def get_preview(self):
        cra = self.env.cr
        cr = self.env.cr
        crx = self.env.cr

        header = "<table style='font-size:12px;width:100%'><tr style='background-color:#d3d3d3'><th style='border:1px solid #000000;padding-left:5px;text-align:center;width:8%;color:#000000'>Tanggal</th><th style='border:1px solid #000000;text-align:center;width:12%;color:#000000'>No. Jurnal</th><th style='border:1px solid #000000;text-align:center;width:20%;color:#000000'>Deskripsi</th><th style='border:1px solid #000000;text-align:center;width:20%;color:#000000'>Label</th><th style='border:1px solid #000000;text-align:center;width:10%;color:#000000'>Kode Akun</th><th style='border:1px solid #000000;text-align:center;width:10%;color:#000000'>Debit</th><th style='border:1px solid #000000;text-align:center;width:10%;color:#000000'>Kredit</th><th style='border:1px solid #000000;text-align:center;width:10%;color:#000000'>Balance</th></tr>"
        footer = "</table>"

        sqla = """SELECT sum(sa.balance) as saldo_awal
                FROM account_move_line sa
                LEFT JOIN account_account saa ON sa.account_id = saa.id
                LEFT JOIN account_move ams ON sa.move_id = ams.id
                LEFT JOIN account_journal ajs ON ajs.default_debit_account_id = saa.id
                WHERE sa.date < %s AND ams.state = 'posted'
                """
        if self.journal_id:
            sqla += " AND ajs.id = %s " % self.journal_id.id
        else:
            sqla += " AND ajs.type = 'bank' "

        cra.execute(sqla, (self.date_start,))
        recorda = cra.dictfetchall()
        saldo_awal = ""
        # transaksi  = ""
        saldo_akhir = ""
        sal = 0.0
        for reca in recorda:            
            if reca['saldo_awal'] == None:
                sal = 0.0
            else:
                sal = reca['saldo_awal']
            
            saldo_awal = "<tr><th style='border:1px solid #000000'></th><th style='border:1px solid #000000'></th><th style='border:1px solid #000000;text-align:center'>Saldo Awal</th><th style='border:1px solid #000000'></th><th style='border:1px solid #000000'></th><th style='border:1px solid #000000'></th><th style='border:1px solid #000000'></th><th style='border:1px solid #000000;text-align:right'>%s</th></tr>" % ("{:,.2f}".format(sal),)

        sql = """SELECT aml.id as id, aml.date as tgl, am.name as jnl, aml.ref as desk, aml.name as lbl, aa.code as acc, aml.credit as debit, aml.debit as credit, aml.balance as balance
                FROM account_move_line aml
                LEFT JOIN account_account aa ON aml.account_id = aa.id
                LEFT JOIN account_move am ON aml.move_id = am.id
                LEFT JOIN account_move_line amj ON amj.move_id = am.id
                LEFT JOIN account_account aaj ON amj.account_id = aaj.id
                LEFT JOIN account_journal aj ON aj.default_debit_account_id = aaj.id
                WHERE aml.date >= %s AND aml.date <= %s AND am.state = 'posted' AND aa.id != aaj.id
            """
        if self.journal_id:
            sql += " AND aj.id = %s GROUP BY aml.id, am.name, aa.id ORDER BY aml.date " % self.journal_id.id
        else:
            sql += " AND aj.type = 'bank' GROUP BY aml.id, am.name, aa.id ORDER BY aml.date "

        cr.execute(sql, (self.date_start,self.date_end,))
        record = cr.dictfetchall()
        transaksis = []
        for rec in record:                
            sqlx = """SELECT sum(amlx.balance) as balance
                    FROM account_move_line amlx
                    LEFT JOIN account_account aax ON amlx.account_id = aax.id
                    LEFT JOIN account_move amx ON amlx.move_id = amx.id
                    LEFT JOIN account_move_line amjx ON amjx.move_id = amx.id
                    LEFT JOIN account_account aajx ON amjx.account_id = aajx.id
                    LEFT JOIN account_journal ajx ON ajx.default_debit_account_id = aajx.id
                    WHERE amlx.id <= %s AND amx.state = 'posted' AND aax.id != aajx.id
                    """
            if self.journal_id:
                sqlx += " AND ajx.id = %s " % self.journal_id.id
            else:
                sqlx += " AND ajx.type = 'bank' "

            crx.execute(sqlx, (rec['id'],))
            recordx = crx.dictfetchall()
            balancex = 0.0
            for recx in recordx:
                balancex = (recx['balance'] * -1)
                saldo_akhir = "<tr><th style='border:1px solid #000000'></th><th style='border:1px solid #000000'></th><th style='border:1px solid #000000;text-align:center'>Saldo Akhir</th><th style='border:1px solid #000000'></th><th style='border:1px solid #000000'></th><th style='border:1px solid #000000;text-align:right'>%s</th><th style='border:1px solid #000000;text-align:right'>%s</th><th style='border:1px solid #000000;text-align:right'>%s</th></tr>" % ("{:,.2f}".format(sum(rec['debit'] for rec in record)),"{:,.2f}".format(sum(rec['credit'] for rec in record)),"{:,.2f}".format(sal - sum(rec['balance'] for rec in record)))
            transaksis.append("<tr><th style='border:1px solid #000000;text-align:center'>%s</th><th style='border:1px solid #000000;text-align:center'>%s</th><th style='border:1px solid #000000;text-align:center'>%s</th><th style='border:1px solid #000000;text-align:center'>%s</th><th style='border:1px solid #000000;text-align:center'>%s</th><th style='border:1px solid #000000;text-align:right'>%s</th><th style='border:1px solid #000000;text-align:right'>%s</th><th style='border:1px solid #000000;text-align:right'>%s</th></tr>" % (datetime.strftime(rec['tgl'], '%d-%m-%Y'),rec['jnl'],rec['desk'],rec['lbl'],rec['acc'],"{:,.2f}".format(rec['debit']),"{:,.2f}".format(rec['credit']),"{:,.2f}".format(balancex)))
        transaksi = "".join(transaksis)
            # import pdb;pdb.set_trace()
        self.html = header + saldo_awal + transaksi + saldo_akhir + footer
