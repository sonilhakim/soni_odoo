from concurrent.futures.process import _WorkItem
from concurrent.futures.thread import _worker
# from tkinter import W
from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.tools.float_utils import float_compare
import time
import pytz
import datetime 
from datetime import date
import csv
from odoo.modules import get_module_path
from odoo.exceptions import UserError
import copy
import logging
from io import StringIO
import base64
from PIL import Image
import xlwt
from urllib.request import urlopen
from io import BytesIO
import xlsxwriter
from xlsxwriter.utility import xl_rowcol_to_cell
# import xlwings as xw
# from xlwings import Range, constants
import openpyxl
from isoweek import Week
_logger = logging.getLogger(__name__)
import re

class BeliBayarSupWizard(models.TransientModel):
    _name    = 'vit.pembelian_pembayaran_sup'
    _inherit = 'report.report_xlsx.abstract'

    export_file     = fields.Binary(string="Export File",  )
    export_filename = fields.Char(string="Export File",  )

    current_date  = datetime.date.today()
    @api.model
    def _get_default_year(self):
        # current_date = datetime.date.today()
        year = int(self.current_date.strftime('%Y'))
        return year
    date_start      = fields.Date(string='Start Date', required=True)
    date_end        = fields.Date(string='End Date', required=True)

    str_periode = fields.Char(string='Periode Name', compute='get_date_start_end', store=True)
    periode = fields.Selection([
        (1, '1 (JAN-MAR)'),
        (2, '2 (APR-JUN)'),
        (3, '3 (JUL-SEP)'),
        (4, '4 (OKT-DES)'),
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
        ], string='Tahun', default=_get_default_year,)

    @api.depends('periode','year')
    def get_date_start_end(self):
        for ra in self:
            current_date  = datetime.date.today()
            thn = str(ra.year)
            if ra.periode == 1:
                ra.date_start = self.current_date.strftime(thn +'-01-01')
                ra.date_end = self.current_date.strftime(thn +'-03-31')
                ra.str_periode = '1 (JAN-MAR)'
            if ra.periode == 2:
                ra.date_start = self.current_date.strftime(thn +'-04-01')
                ra.date_end = self.current_date.strftime(thn +'-06-30')
                ra.str_periode = '2 (APR-JUN)'
            if ra.periode == 3:
                ra.date_start = self.current_date.strftime(thn +'-07-01')
                ra.date_end = self.current_date.strftime(thn +'-09-30')
                ra.str_periode = '3 (JUL-SEP)'
            if ra.periode == 4:
                ra.date_start = self.current_date.strftime(thn +'-10-01')
                ra.date_end = self.current_date.strftime(thn +'-12-31')
                ra.str_periode = '4 (OKT-DES)'

    # commercial_partner_id = fields.Many2one(comodel_name="res.partner", string="Vendor", default=lambda self: self.env.uid, track_visibility='onchange', readonly=True)

    def cell_format(self, workbook):
        cell_format = {}
        cell_format['header'] = workbook.add_format({
            'font_size': 11,
            'border': True,
            'align': 'center',
            'bg_color': '#D9D9D9',
            'valign': 'vcenter',
        })
        cell_format['header_1'] = workbook.add_format({
            'font_size': 11,
            'border': True,
            'align': 'center',
            'bg_color': '#90EE90',
            'valign': 'vcenter',
            'bold': True,
        })
        cell_format['header_2'] = workbook.add_format({
            'font_size': 11,
            'border': True,
            'align': 'center',
            'bg_color': '#add8e6',
            'valign': 'vcenter',
            'bold': True,
        })
        cell_format['header_3'] = workbook.add_format({
            'font_size': 11,
            'border': True,
            'align': 'center',
            'bg_color': '#f8ccad',
            'valign': 'vcenter',
            'bold': True,
        })
        cell_format['header_4'] = workbook.add_format({
            'font_size': 11,
            'border': True,
            'align': 'center',
            'bg_color': '#D8E4BC',
            'valign': 'vcenter',
            'bold': True,
        })
        cell_format['header_5'] = workbook.add_format({
            'font_size': 11,
            'border': True,
            'align': 'center',
            'bg_color': '#CC99FF',
            'valign': 'vcenter',
            'bold': True,
        })
        cell_format['content_def'] = workbook.add_format({
            'font_size': 11,
            'border': True,
            'align': 'center',
        })
        cell_format['content_left'] = workbook.add_format({
            'font_size': 11,
            'border': True,
            'align': 'left',
        })
        cell_format['content_left_nb'] = workbook.add_format({
            'font_size': 11,
            'border': False,
            'align': 'left',
        })
        cell_format['content_right'] = workbook.add_format({
            'font_size': 11,
            'border': True,
            'align': 'right',
        })
        cell_format['content_right_nb'] = workbook.add_format({
            'font_size': 11,
            'border': False,
            'align': 'right',
        })
        cell_format['content_right_bold'] = workbook.add_format({
            'font_size': 11,
            'border': True,
            'align': 'right',
            'bold': True,
        })
        cell_format['content_hide'] = workbook.add_format({
            'font_color': '#D9D9D9',
            'bg_color': '#D9D9D9',
            'border': True,
        })
        cell_format['info_1'] = workbook.add_format({
            'font_size': 36,
            'align': 'center',
            'bg_color': '#B3BBC8',
            'bold': True,
        })
        cell_format['info_2'] = workbook.add_format({
            'font_size': 13,
            'align': 'center',
            'bg_color': '#B3BBC8',
        })
        cell_format['footer'] = workbook.add_format({
            'font_size': 11,
            'align': 'center',
        })
        cell_format['space'] = workbook.add_format({
            'bg_color': '#B3BBC8',
        })
        cell_format['note'] = workbook.add_format({
            'font_size': 11,
            'border': False,
            'align': 'left',
            'bg_color': '#9966FF',
        })
        
        return cell_format, workbook

    @api.multi
    def get_datas(self):
        rec = {}
        contents = [{
                "1" :"NO",
                "2" :"SUPPLIER",
                "3" :"TGL.PO",
                "4" :"NO.PO",
                "5" :"DPP",
                "6" :"NOMINAL PO",
                "7" :"CUSTOMER",
                "8" :"NAMA PROYEK",
                "9" :"TGL.TAGIHAN",
                "10":"NOMINAL TAGIHAN",
                "11":"TGL.JATUH TEMPO",
                "12":"SUDAH DIBAYARKAN",
                "13":"WEEK",
                "14":"SELISIH",

        }]

        # values = []
        # purchase = self.env['purchase.order'].search([('date_order','>=',self.date_start), ('date_order','<=',self.date_end)])
        # if (self.periode == 1) :
        sql = """SELECT (rp.name) as supplier, (to_char(po.date_order :: DATE, 'DD Mon YYYY')) as tgl_po, (po.name) as no_po, (po.amount_untaxed) as dpp, (po.amount_total) as nominal_po, (rp2.name) as customer1, (aat.name) as nama_proyek, (to_char(ai.date_invoice :: DATE, 'DD Mon YYYY')) as tgl_tagihan, (ai.amount_total) as nominal_tagihan, (to_char(ai.date_due :: DATE, 'DD Mon YYYY')) as tgl_jatem, (sum(ai.amount_total)-sum(ai.residual)) as sdh_byr, DATE_PART('week', ai.date_due) AS date_due_week_num, (sum(po.amount_total)-(sum(ai.amount_total)-sum(ai.residual))) as nominal_plan_act, (rp3.name) as customer2
                FROM purchase_order po
                LEFT JOIN account_invoice ai ON po.name = ai.origin
                LEFT JOIN account_payment ap ON ap.communication = ai.number
                LEFT JOIN vit_marketing_inquery_garmen mig ON po.inquery_id = mig.id
                LEFT JOIN purchase_requisition te ON po.requisition_id = te.id
                LEFT JOIN vit_product_request pr ON pr.name = te.origin
                LEFT JOIN vit_purchase_order_garmen pog ON po.po_id = pog.id
                LEFT JOIN vit_marketing_sph_garmen msg ON pog.sph_id = msg.id
                LEFT JOIN vit_marketing_proposal mp ON msg.proposal_id = mp.id
                LEFT JOIN vit_marketing_inquery_garmen mig2 ON mp.inquery_id = mig2.id
                LEFT JOIN res_partner rp ON po.partner_id = rp.id
                LEFT JOIN res_partner rp2 ON mig.partner_id = rp2.id
                LEFT JOIN res_partner rp3 ON pog.partner_id = rp3.id
                LEFT JOIN account_analytic_tag aat ON pr.analytic_tag_id = aat.id
                WHERE pog.date >= %s AND pog.date <= %s
                OR mig.date >= %s AND mig.date <= %s
                GROUP BY aat.id, po.id, rp.id, ai.id, rp2.id, ap.id, rp3.id
                ORDER BY po.date_order
                """
        self.env.cr.execute(sql, (self.date_start,self.date_end,self.date_start,self.date_end))
        result = self.env.cr.dictfetchall()
        line_ids = []
        i = 1
        for res in result:

            contents.append({
                "1" : str(i),
                "2" : res['supplier'],
                "3" : res['tgl_po'],
                "4" : res['no_po'],
                "5" : res['dpp'],
                "6" : res['nominal_po'],
                "7" : res['customer1'] or res['customer2'],
                "8" : res['nama_proyek'],
                "9" : res['tgl_tagihan'],
                "10": res['nominal_tagihan'],
                "11": res['tgl_jatem'],
                "12": res['sdh_byr'],
                "13": res['date_due_week_num'],
                "14": res['nominal_plan_act'],

            })
            i += 1
        rec['PERIODE ' + str(self.periode)] = [contents]        
        return rec
        # result2 = self.env.cr.fetchall()
        # for res in result2:
        #     values.append({
        #         res[11]
        #     })
        #     i += 1
        # rec['PERIODE 2'] = [values]        
        # return rec

    @api.multi
    def confirm_button(self):
        self.ensure_one()
        datas = self.get_datas()
        if not datas :
            raise Warning("Data tidak ditemukan.")
        fp = BytesIO()
        workbook = xlsxwriter.Workbook(fp)
        cell_format, workbook = self.cell_format(workbook)
        for sheet, header_content in datas.items():
            contents = header_content
            worksheet = workbook.add_worksheet(sheet)
            worksheet.set_column('B:B', 5)
            worksheet.set_column('C:C', 55)
            worksheet.set_column('D:D', 12)
            worksheet.set_column('E:E', 12)
            worksheet.set_column('F:F', 25)
            worksheet.set_column('G:G', 25)
            worksheet.set_column('H:H', 38)
            worksheet.set_column('I:I', 70)
            worksheet.set_column('J:J', 12)
            worksheet.set_column('K:K', 18)
            worksheet.set_column('L:L', 16)
            worksheet.set_column('M:M', 18)
            worksheet.set_column('N:AG', 16)
            column_length = len(contents)
            # worksheet.set_row_pixels(16, 9)
            # worksheet.set_row_pixels(18, 6)


            current_uid = self._context.get('uid')
            user_obj = self.env['res.users'].browse(current_uid)

            column = 1
            row = 1
            logo=BytesIO(base64.b64decode(user_obj.company_id.logo))

            worksheet.insert_image(row, column,"logo.png", {'image_data': logo, 'x_scale': 1.0, 'y_scale': 0.9})
            worksheet.merge_range('B11:C11', user_obj.company_id.name)
            worksheet.merge_range('B12:C12', user_obj.company_id.street)
            worksheet.write('B13', user_obj.company_id.city)
            worksheet.write('B13', user_obj.company_id.zip)
            worksheet.merge_range('B14:C14', user_obj.company_id.state_id.name)
            worksheet.merge_range('B15:C15', user_obj.company_id.country_id.name)
            worksheet.merge_range('B17:AG17', ' ', cell_format['space'])
            worksheet.merge_range('B18:AG18', 'LAPORAN PEMBELIAN DAN PEMBAYARAN SUPPLIER', cell_format['info_1'])
            worksheet.merge_range('B19:AG19', ' ', cell_format['space'])
            worksheet.merge_range('B20:AG20', 'Periode' + ' ' + self.date_start.strftime('%d %b %Y') + ' s.d '+ self.date_end.strftime('%d %b %Y'), cell_format['info_2'])
            worksheet.merge_range('B21:AG21', ' ', cell_format['space'])

            column = 13
            row = 22
            k = 1
            for k in range(1,11) :
                if (column == 13 or column == 17 or column == 21 or column == 25 or column == 29) :
                    worksheet.merge_range(row, column, row, column + 1, 'PLAN', cell_format['header'])
                else : 
                    worksheet.merge_range(row, column, row, column + 1, 'ACT', cell_format['header'])
                column += 2

            column = 13
            row += 1
            m = 1
            for m in range(1,21) :
                if (column == 13 or column == 15 or column == 17 or column == 19 or column == 21 or column == 23 or column == 25 or column == 27 or column == 29 or column == 31) :
                    worksheet.write(row, column, 'MINGGU KE-', cell_format['header'])
                else : 
                    worksheet.write(row, column, 'NOMINAL', cell_format['header'])
                column += 1
            # start_dt = date(1, 1)
            # end_dt = date(3, 31)

            # for dt in daterange(start_dt, end_dt):
            #     print(dt.strftime("%m-%d"))

            column = 1
            row += 1
            n = 1
            for n in range(1,33) :
                worksheet.write(24, column, ' ', cell_format['content_hide'])
                column += 1

            i = 0
            j = 1
            dpp = 0
            nompo = 0
            nomta = 0
            suba = 0
            hut = 0
            palas = 0
            delas = 0
            dudu = 0
            dunam = 0
            tiluh = 0
            row = 21
            bul = 0
            column = 1
            # for j in range(1,4):
            # for col in headers :
            #     if (column == 13) :
            #         pass
            #     else :
            #         worksheet.merge_range(row, column, 23, column, col, cell_format['header'])
            #         column += 1

            for data in contents[0] :
                # import pdb;pdb.set_trace()
                if i == 0 :
                    worksheet.merge_range(row, 1, 23, 1, data['1'], cell_format['header'])
                    worksheet.merge_range(row, 2, 23, 2, data['2'], cell_format['header'])
                    worksheet.merge_range(row, 3, 23, 3, data['3'], cell_format['header'])
                    worksheet.merge_range(row, 4, 23, 4, data['4'], cell_format['header'])
                    worksheet.merge_range(row, 5, 23, 5, data['5'], cell_format['header'])
                    worksheet.merge_range(row, 6, 23, 6, data['6'], cell_format['header'])
                    worksheet.merge_range(row, 7, 23, 7, data['7'], cell_format['header'])
                    worksheet.merge_range(row, 8, 23, 8, data['8'], cell_format['header'])
                    worksheet.merge_range(row, 9, 23, 9, data['9'], cell_format['header'])
                    worksheet.merge_range(row, 10, 23, 10, data['10'], cell_format['header'])
                    worksheet.merge_range(row, 11, 23, 11, data['11'], cell_format['header'])
                    worksheet.merge_range(row, 12, 23, 12, data['12'], cell_format['header'])
                    
                    if (self.periode == 1) :
                        worksheet.merge_range(row, 13, row, 16, "FEBRUARI", cell_format['header_1'])
                        worksheet.merge_range(row, 17, row, 20, "MARET", cell_format['header_2'])
                        worksheet.merge_range(row, 21, row, 24, "APRIL", cell_format['header_3'])
                        worksheet.merge_range(row, 25, row, 28, "MEI", cell_format['header_4'])
                        worksheet.merge_range(row, 29, row, 32, "JUNI", cell_format['header_5'])

                    elif (self.periode == 2) :
                        worksheet.merge_range(row, 13, row, 16, "MEI", cell_format['header_1'])
                        worksheet.merge_range(row, 17, row, 20, "JUNI", cell_format['header_2'])
                        worksheet.merge_range(row, 21, row, 24, "JULI", cell_format['header_3'])
                        worksheet.merge_range(row, 25, row, 28, "AGUSTUS", cell_format['header_4'])
                        worksheet.merge_range(row, 29, row, 32, "SEPTEMBER", cell_format['header_5'])
            
                    elif (self.periode == 3) :
                        worksheet.merge_range(row, 13, row, 16, "AGUSTUS", cell_format['header_1'])
                        worksheet.merge_range(row, 17, row, 20, "SEPTEMBER", cell_format['header_2'])
                        worksheet.merge_range(row, 21, row, 24, "OKTOBER", cell_format['header_3'])
                        worksheet.merge_range(row, 25, row, 28, "NOVEMBER", cell_format['header_4'])
                        worksheet.merge_range(row, 29, row, 32, "DESEMBER", cell_format['header_5'])

                    else :
                        worksheet.merge_range(row, 13, row, 16, "NOVEMBER", cell_format['header_1'])
                        worksheet.merge_range(row, 17, row, 20, "DESEMBER", cell_format['header_2'])
                        worksheet.merge_range(row, 21, row, 24, "JANUARI", cell_format['header_3'])
                        worksheet.merge_range(row, 25, row, 28, "FEBRUARI", cell_format['header_4'])
                        worksheet.merge_range(row, 29, row, 32, "MARET", cell_format['header_5'])
                    row += 3

                else:
                    worksheet.write(row, 1, data['1'], cell_format['content_def'])
                    worksheet.write(row, 2, data['2'], cell_format['content_left'])
                    worksheet.write(row, 3, data['3'], cell_format['content_def'])
                    worksheet.write(row, 4, data['4'], cell_format['content_def'])
                    worksheet.write(row, 5, data['5'], cell_format['content_right'])
                    dpp += data['5']
                    worksheet.write(row, 6, data['6'], cell_format['content_right'])
                    nompo += data['6']
                    hut += data['6']
                    worksheet.write(row, 7, data['7'], cell_format['content_left'])
                    worksheet.write(row, 8, data['8'], cell_format['content_left'])
                    worksheet.write(row, 9, data['9'], cell_format['content_def'])
                    worksheet.write(row, 10, data['10'], cell_format['content_right'])
                    if (data['10'] == None) :
                        nomta = nomta
                    else :
                        nomta += data['10']
                    worksheet.write(row, 11, data['11'], cell_format['content_def'])
                    bul = data['11']
                    worksheet.write(row, 12, data['12'], cell_format['content_right'])
                    if (data['12'] == None) :
                        suba = suba
                    else :
                        suba += data['12']
                        hut -= data['12']
                    if (data['13'] == None) :
                            worksheet.write(row, 13, ' ', cell_format['content_def'])
                            worksheet.write(row, 14, ' ', cell_format['content_def'])
                            worksheet.write(row, 15, ' ', cell_format['content_def'])
                            worksheet.write(row, 16, ' ', cell_format['content_def'])
                            worksheet.write(row, 17, ' ', cell_format['content_def'])
                            worksheet.write(row, 18, ' ', cell_format['content_def'])
                            worksheet.write(row, 19, ' ', cell_format['content_def'])
                            worksheet.write(row, 20, ' ', cell_format['content_def'])
                            worksheet.write(row, 21, ' ', cell_format['content_def'])
                            worksheet.write(row, 22, ' ', cell_format['content_def'])
                            worksheet.write(row, 23, ' ', cell_format['content_def'])
                            worksheet.write(row, 24, ' ', cell_format['content_def'])
                            worksheet.write(row, 25, ' ', cell_format['content_def'])
                            worksheet.write(row, 26, ' ', cell_format['content_def'])
                            worksheet.write(row, 27, ' ', cell_format['content_def'])
                            worksheet.write(row, 28, ' ', cell_format['content_def'])
                            worksheet.write(row, 29, ' ', cell_format['content_def'])
                            worksheet.write(row, 30, ' ', cell_format['content_def'])
                            worksheet.write(row, 31, ' ', cell_format['content_def'])
                            worksheet.write(row, 32, ' ', cell_format['content_def'])

                    else :
                        if (self.periode == 1) :
                            if (int(data['13']) > 22) :
                                if (re.search("29", bul) or re.search("30", bul)) :
                                    worksheet.write(row, 13, ' ', cell_format['content_def'])
                                    worksheet.write(row, 15, ' ', cell_format['content_def'])
                                    worksheet.write(row, 17, ' ', cell_format['content_def'])
                                    worksheet.write(row, 19, ' ', cell_format['content_def'])
                                    worksheet.write(row, 21, ' ', cell_format['content_def'])
                                    worksheet.write(row, 23, ' ', cell_format['content_def'])
                                    worksheet.write(row, 25, ' ', cell_format['content_def'])
                                    worksheet.write(row, 27, ' ', cell_format['content_def'])
                                    worksheet.write(row, 29, int(data['13']) - 21, cell_format['content_def'])
                                    worksheet.write(row, 31, int(data['13']) - 21, cell_format['content_def'])
                                elif re.search("05 Jun", bul) or re.search("06 Jun", bul) or re.search("07 Jun", bul) or re.search("13 Jun", bul) or re.search("14 Jun", bul) or re.search("26 Jun", bul) or re.search("27 Jun", bul) or re.search("28 Jun", bul):
                                    worksheet.write(row, 13, ' ', cell_format['content_def'])
                                    worksheet.write(row, 15, ' ', cell_format['content_def'])
                                    worksheet.write(row, 17, ' ', cell_format['content_def'])
                                    worksheet.write(row, 19, ' ', cell_format['content_def'])
                                    worksheet.write(row, 21, ' ', cell_format['content_def'])
                                    worksheet.write(row, 23, ' ', cell_format['content_def'])
                                    worksheet.write(row, 25, ' ', cell_format['content_def'])
                                    worksheet.write(row, 27, ' ', cell_format['content_def'])
                                    worksheet.write(row, 29, int(data['13']) - 22, cell_format['content_def'])
                                    worksheet.write(row, 31, int(data['13']) - 22, cell_format['content_def'])

                                elif (int(data['13']) == 25) :
                                    if re.search("15 Jun", bul) or re.search("16 Jun", bul) or re.search("17 Jun", bul) or re.search("18 Jun", bul) or re.search("19 Jun", bul) or re.search("20 Jun", bul) or re.search("21 Jun", bul) :
                                        worksheet.write(row, 13, ' ', cell_format['content_def'])
                                        worksheet.write(row, 15, ' ', cell_format['content_def'])
                                        worksheet.write(row, 17, ' ', cell_format['content_def'])
                                        worksheet.write(row, 19, ' ', cell_format['content_def'])
                                        worksheet.write(row, 21, ' ', cell_format['content_def'])
                                        worksheet.write(row, 23, ' ', cell_format['content_def'])
                                        worksheet.write(row, 25, ' ', cell_format['content_def'])
                                        worksheet.write(row, 27, ' ', cell_format['content_def'])
                                        worksheet.write(row, 29, int(data['13']) - 22, cell_format['content_def'])
                                        worksheet.write(row, 31, int(data['13']) - 22, cell_format['content_def'])

                                    else :
                                        worksheet.write(row, 13, ' ', cell_format['content_def'])
                                        worksheet.write(row, 15, ' ', cell_format['content_def'])
                                        worksheet.write(row, 17, ' ', cell_format['content_def'])
                                        worksheet.write(row, 19, ' ', cell_format['content_def'])
                                        worksheet.write(row, 21, ' ', cell_format['content_def'])
                                        worksheet.write(row, 23, ' ', cell_format['content_def'])
                                        worksheet.write(row, 25, ' ', cell_format['content_def'])
                                        worksheet.write(row, 27, ' ', cell_format['content_def'])
                                        worksheet.write(row, 29, int(data['13']) - 21, cell_format['content_def'])
                                        worksheet.write(row, 31, int(data['13']) - 21, cell_format['content_def'])
                                else :
                                    worksheet.write(row, 13, ' ', cell_format['content_def'])
                                    worksheet.write(row, 15, ' ', cell_format['content_def'])
                                    worksheet.write(row, 17, ' ', cell_format['content_def'])
                                    worksheet.write(row, 19, ' ', cell_format['content_def'])
                                    worksheet.write(row, 21, ' ', cell_format['content_def'])
                                    worksheet.write(row, 23, ' ', cell_format['content_def'])
                                    worksheet.write(row, 25, ' ', cell_format['content_def'])
                                    worksheet.write(row, 27, ' ', cell_format['content_def'])
                                    worksheet.write(row, 29, int(data['13']) - 21, cell_format['content_def'])
                                    worksheet.write(row, 31, int(data['13']) - 21, cell_format['content_def'])

                            elif (int(data['13']) > 17 and int(data['13']) < 23) :
                                if ("May" in bul) :
                                    worksheet.write(row, 13, ' ', cell_format['content_def'])
                                    worksheet.write(row, 15, ' ', cell_format['content_def'])
                                    worksheet.write(row, 17, ' ', cell_format['content_def'])
                                    worksheet.write(row, 19, ' ', cell_format['content_def'])
                                    worksheet.write(row, 21, ' ', cell_format['content_def'])
                                    worksheet.write(row, 23, ' ', cell_format['content_def'])
                                    worksheet.write(row, 25, int(data['13']) - 17, cell_format['content_def'])
                                    worksheet.write(row, 27, int(data['13']) - 17, cell_format['content_def'])
                                    worksheet.write(row, 29, ' ', cell_format['content_def'])
                                    worksheet.write(row, 31, ' ', cell_format['content_def'])
                                
                                else :
                                    worksheet.write(row, 13, ' ', cell_format['content_def'])
                                    worksheet.write(row, 15, ' ', cell_format['content_def'])
                                    worksheet.write(row, 17, ' ', cell_format['content_def'])
                                    worksheet.write(row, 19, ' ', cell_format['content_def'])
                                    worksheet.write(row, 21, ' ', cell_format['content_def'])
                                    worksheet.write(row, 23, ' ', cell_format['content_def'])
                                    worksheet.write(row, 25, ' ', cell_format['content_def'])
                                    worksheet.write(row, 27, ' ', cell_format['content_def'])
                                    worksheet.write(row, 29, int(data['13']) - 21, cell_format['content_def'])
                                    worksheet.write(row, 31, int(data['13']) - 21, cell_format['content_def'])

                            elif (int(data['13']) > 14 and int(data['13']) < 18) :
                                if ("Apr" in bul) :
                                    if re.search("15 Apr", bul) or re.search("16 Apr", bul) or "29" in bul or "30" in bul :
                                        worksheet.write(row, 13, ' ', cell_format['content_def'])
                                        worksheet.write(row, 15, ' ', cell_format['content_def'])
                                        worksheet.write(row, 17, ' ', cell_format['content_def'])
                                        worksheet.write(row, 19, ' ', cell_format['content_def'])
                                        worksheet.write(row, 21, int(data['13']) - 12, cell_format['content_def'])
                                        worksheet.write(row, 23, int(data['13']) - 12, cell_format['content_def'])
                                        worksheet.write(row, 25, ' ', cell_format['content_def'])
                                        worksheet.write(row, 27, ' ', cell_format['content_def'])
                                        worksheet.write(row, 29, ' ', cell_format['content_def'])
                                        worksheet.write(row, 31, ' ', cell_format['content_def'])
                                    elif (int(data['13']) == 16) :
                                        if re.search("17 Apr", bul) or re.search("18 Apr", bul) or re.search("19 Apr", bul) or re.search("20 Apr", bul) or re.search("21 Apr", bul) :
                                            worksheet.write(row, 13, ' ', cell_format['content_def'])
                                            worksheet.write(row, 15, ' ', cell_format['content_def'])
                                            worksheet.write(row, 17, ' ', cell_format['content_def'])
                                            worksheet.write(row, 19, ' ', cell_format['content_def'])
                                            worksheet.write(row, 21, int(data['13']) - 13, cell_format['content_def'])
                                            worksheet.write(row, 23, int(data['13']) - 13, cell_format['content_def'])
                                            worksheet.write(row, 25, ' ', cell_format['content_def'])
                                            worksheet.write(row, 27, ' ', cell_format['content_def'])
                                            worksheet.write(row, 29, ' ', cell_format['content_def'])
                                            worksheet.write(row, 31, ' ', cell_format['content_def'])

                                        else :
                                            worksheet.write(row, 13, ' ', cell_format['content_def'])
                                            worksheet.write(row, 15, ' ', cell_format['content_def'])
                                            worksheet.write(row, 17, ' ', cell_format['content_def'])
                                            worksheet.write(row, 19, ' ', cell_format['content_def'])
                                            worksheet.write(row, 21, int(data['13']) - 12, cell_format['content_def'])
                                            worksheet.write(row, 23, int(data['13']) - 12, cell_format['content_def'])
                                            worksheet.write(row, 25, ' ', cell_format['content_def'])
                                            worksheet.write(row, 27, ' ', cell_format['content_def'])
                                            worksheet.write(row, 29, ' ', cell_format['content_def'])
                                            worksheet.write(row, 31, ' ', cell_format['content_def'])
                                            
                                    else :
                                        worksheet.write(row, 13, ' ', cell_format['content_def'])
                                        worksheet.write(row, 15, ' ', cell_format['content_def'])
                                        worksheet.write(row, 17, ' ', cell_format['content_def'])
                                        worksheet.write(row, 19, ' ', cell_format['content_def'])
                                        worksheet.write(row, 21, int(data['13']) - 13, cell_format['content_def'])
                                        worksheet.write(row, 23, int(data['13']) - 13, cell_format['content_def'])
                                        worksheet.write(row, 25, ' ', cell_format['content_def'])
                                        worksheet.write(row, 27, ' ', cell_format['content_def'])
                                        worksheet.write(row, 29, ' ', cell_format['content_def'])
                                        worksheet.write(row, 31, ' ', cell_format['content_def'])

                                else :
                                    worksheet.write(row, 13, ' ', cell_format['content_def'])
                                    worksheet.write(row, 15, ' ', cell_format['content_def'])
                                    worksheet.write(row, 17, ' ', cell_format['content_def'])
                                    worksheet.write(row, 19, ' ', cell_format['content_def'])
                                    worksheet.write(row, 21, ' ', cell_format['content_def'])
                                    worksheet.write(row, 23, ' ', cell_format['content_def'])
                                    worksheet.write(row, 25, int(data['13']) - 16, cell_format['content_def'])
                                    worksheet.write(row, 27, int(data['13']) - 16, cell_format['content_def'])
                                    worksheet.write(row, 29, ' ', cell_format['content_def'])
                                    worksheet.write(row, 31, ' ', cell_format['content_def'])

                            elif (int(data['13']) > 9 and int(data['13']) < 15) :
                                if ("Mar" in bul) :
                                    if re.search("01 Mar", bul) or re.search("02 Mar", bul) or re.search("03 Mar", bul) or re.search("04 Mar", bul) or re.search("05 Mar", bul) or re.search("13 Mar", bul) or re.search("14 Mar", bul) or re.search("27 Mar", bul) or re.search("28 Mar", bul) :
                                        worksheet.write(row, 13, ' ', cell_format['content_def'])
                                        worksheet.write(row, 15, ' ', cell_format['content_def'])
                                        worksheet.write(row, 17, int(data['13']) - 9, cell_format['content_def'])
                                        worksheet.write(row, 19, int(data['13']) - 9, cell_format['content_def'])
                                        worksheet.write(row, 21, ' ', cell_format['content_def'])
                                        worksheet.write(row, 23, ' ', cell_format['content_def'])
                                        worksheet.write(row, 25, ' ', cell_format['content_def'])
                                        worksheet.write(row, 27, ' ', cell_format['content_def'])
                                        worksheet.write(row, 29, ' ', cell_format['content_def'])
                                        worksheet.write(row, 31, ' ', cell_format['content_def'])
                                    elif re.search("15 Mar", bul) or re.search("16 Mar", bul) or re.search("17 Mar", bul) or re.search("18 Mar", bul) or re.search("19 Mar", bul) :
                                        worksheet.write(row, 13, ' ', cell_format['content_def'])
                                        worksheet.write(row, 15, ' ', cell_format['content_def'])
                                        worksheet.write(row, 17, int(data['13']) - 8, cell_format['content_def'])
                                        worksheet.write(row, 19, int(data['13']) - 8, cell_format['content_def'])
                                        worksheet.write(row, 21, ' ', cell_format['content_def'])
                                        worksheet.write(row, 23, ' ', cell_format['content_def'])
                                        worksheet.write(row, 25, ' ', cell_format['content_def'])
                                        worksheet.write(row, 27, ' ', cell_format['content_def'])
                                        worksheet.write(row, 29, ' ', cell_format['content_def'])
                                        worksheet.write(row, 31, ' ', cell_format['content_def'])

                                    elif (int(data['13']) == 11) :
                                        if re.search("20 Mar", bul) or re.search("21 Mar", bul) :
                                            worksheet.write(row, 13, ' ', cell_format['content_def'])
                                            worksheet.write(row, 15, ' ', cell_format['content_def'])
                                            worksheet.write(row, 17, int(data['13']) - 9, cell_format['content_def'])
                                            worksheet.write(row, 19, int(data['13']) - 9, cell_format['content_def'])
                                            worksheet.write(row, 21, ' ', cell_format['content_def'])
                                            worksheet.write(row, 23, ' ', cell_format['content_def'])
                                            worksheet.write(row, 25, ' ', cell_format['content_def'])
                                            worksheet.write(row, 27, ' ', cell_format['content_def'])
                                            worksheet.write(row, 29, ' ', cell_format['content_def'])
                                            worksheet.write(row, 31, ' ', cell_format['content_def'])

                                        else :
                                            worksheet.write(row, 13, ' ', cell_format['content_def'])
                                            worksheet.write(row, 15, ' ', cell_format['content_def'])
                                            worksheet.write(row, 17, int(data['13']) - 8, cell_format['content_def'])
                                            worksheet.write(row, 19, int(data['13']) - 8, cell_format['content_def'])
                                            worksheet.write(row, 21, ' ', cell_format['content_def'])
                                            worksheet.write(row, 23, ' ', cell_format['content_def'])
                                            worksheet.write(row, 25, ' ', cell_format['content_def'])
                                            worksheet.write(row, 27, ' ', cell_format['content_def'])
                                            worksheet.write(row, 29, ' ', cell_format['content_def'])
                                            worksheet.write(row, 31, ' ', cell_format['content_def'])

                                    elif ("15" in bul or "16" in bul or "17" in bul or "18" in bul or "19" in bul or "20" in bul or "21" in bul or "29" in bul or "30" in bul or "31" in bul) :
                                        if re.search("08 Mar", bul) or re.search("09 Mar", bul) or re.search("10 Mar", bul) or re.search("11 Mar", bul) or re.search("12 Mar", bul) or re.search("13 Mar", bul) or re.search("14 Mar", bul) :
                                            worksheet.write(row, 13, ' ', cell_format['content_def'])
                                            worksheet.write(row, 15, ' ', cell_format['content_def'])
                                            worksheet.write(row, 17, int(data['13']) - 8, cell_format['content_def'])
                                            worksheet.write(row, 19, int(data['13']) - 8, cell_format['content_def'])
                                            worksheet.write(row, 21, ' ', cell_format['content_def'])
                                            worksheet.write(row, 23, ' ', cell_format['content_def'])
                                            worksheet.write(row, 25, ' ', cell_format['content_def'])
                                            worksheet.write(row, 27, ' ', cell_format['content_def'])
                                            worksheet.write(row, 29, ' ', cell_format['content_def'])
                                            worksheet.write(row, 31, ' ', cell_format['content_def'])
                                        elif re.search("29 Mar", bul) or re.search("30 Mar", bul) or re.search("31 Mar", bul) :
                                            worksheet.write(row, 13, ' ', cell_format['content_def'])
                                            worksheet.write(row, 15, ' ', cell_format['content_def'])
                                            worksheet.write(row, 17, int(data['13']) - 8, cell_format['content_def'])
                                            worksheet.write(row, 19, int(data['13']) - 8, cell_format['content_def'])
                                            worksheet.write(row, 21, ' ', cell_format['content_def'])
                                            worksheet.write(row, 23, ' ', cell_format['content_def'])
                                            worksheet.write(row, 25, ' ', cell_format['content_def'])
                                            worksheet.write(row, 27, ' ', cell_format['content_def'])
                                            worksheet.write(row, 29, ' ', cell_format['content_def'])
                                            worksheet.write(row, 31, ' ', cell_format['content_def'])
                                        elif re.search("22 Mar", bul) or re.search("23 Mar", bul) or re.search("24 Mar", bul) or re.search("25 Mar", bul) or re.search("26 Mar", bul) :
                                            worksheet.write(row, 13, ' ', cell_format['content_def'])
                                            worksheet.write(row, 15, ' ', cell_format['content_def'])
                                            worksheet.write(row, 17, int(data['13']) - 8, cell_format['content_def'])
                                            worksheet.write(row, 19, int(data['13']) - 8, cell_format['content_def'])
                                            worksheet.write(row, 21, ' ', cell_format['content_def'])
                                            worksheet.write(row, 23, ' ', cell_format['content_def'])
                                            worksheet.write(row, 25, ' ', cell_format['content_def'])
                                            worksheet.write(row, 27, ' ', cell_format['content_def'])
                                            worksheet.write(row, 29, ' ', cell_format['content_def'])
                                            worksheet.write(row, 31, ' ', cell_format['content_def'])
                                        else :
                                            worksheet.write(row, 13, ' ', cell_format['content_def'])
                                            worksheet.write(row, 15, ' ', cell_format['content_def'])
                                            worksheet.write(row, 17, int(data['13']) - 9, cell_format['content_def'])
                                            worksheet.write(row, 19, int(data['13']) - 9, cell_format['content_def'])
                                            worksheet.write(row, 21, ' ', cell_format['content_def'])
                                            worksheet.write(row, 23, ' ', cell_format['content_def'])
                                            worksheet.write(row, 25, ' ', cell_format['content_def'])
                                            worksheet.write(row, 27, ' ', cell_format['content_def'])
                                            worksheet.write(row, 29, ' ', cell_format['content_def'])
                                            worksheet.write(row, 31, ' ', cell_format['content_def'])

                                    else :
                                        worksheet.write(row, 13, ' ', cell_format['content_def'])
                                        worksheet.write(row, 15, ' ', cell_format['content_def'])
                                        worksheet.write(row, 17, int(data['13']) - 8, cell_format['content_def'])
                                        worksheet.write(row, 19, int(data['13']) - 8, cell_format['content_def'])
                                        worksheet.write(row, 21, ' ', cell_format['content_def'])
                                        worksheet.write(row, 23, ' ', cell_format['content_def'])
                                        worksheet.write(row, 25, ' ', cell_format['content_def'])
                                        worksheet.write(row, 27, ' ', cell_format['content_def'])
                                        worksheet.write(row, 29, ' ', cell_format['content_def'])
                                        worksheet.write(row, 31, ' ', cell_format['content_def'])

                                else :
                                    if re.search("08 Apr", bul) or re.search("09 Apr", bul) or int(data['13']) == 13 :
                                        worksheet.write(row, 13, ' ', cell_format['content_def'])
                                        worksheet.write(row, 15, ' ', cell_format['content_def'])
                                        worksheet.write(row, 17, ' ', cell_format['content_def'])
                                        worksheet.write(row, 19, ' ', cell_format['content_def'])
                                        worksheet.write(row, 21, int(data['13']) - 12, cell_format['content_def'])
                                        worksheet.write(row, 23, int(data['13']) - 12, cell_format['content_def'])
                                        worksheet.write(row, 25, ' ', cell_format['content_def'])
                                        worksheet.write(row, 27, ' ', cell_format['content_def'])
                                        worksheet.write(row, 29, ' ', cell_format['content_def'])
                                        worksheet.write(row, 31, ' ', cell_format['content_def'])

                                    else :
                                        worksheet.write(row, 13, ' ', cell_format['content_def'])
                                        worksheet.write(row, 15, ' ', cell_format['content_def'])
                                        worksheet.write(row, 17, ' ', cell_format['content_def'])
                                        worksheet.write(row, 19, ' ', cell_format['content_def'])
                                        worksheet.write(row, 21, int(data['13']) - 13, cell_format['content_def'])
                                        worksheet.write(row, 23, int(data['13']) - 13, cell_format['content_def'])
                                        worksheet.write(row, 25, ' ', cell_format['content_def'])
                                        worksheet.write(row, 27, ' ', cell_format['content_def'])
                                        worksheet.write(row, 29, ' ', cell_format['content_def'])
                                        worksheet.write(row, 31, ' ', cell_format['content_def'])

                            else :
                                if ("Feb" in bul) :
                                    if re.search("13 Feb", bul) or re.search("14 Feb", bul) :
                                        worksheet.write(row, 13, 2, cell_format['content_def'])
                                        worksheet.write(row, 15, 2, cell_format['content_def'])
                                        worksheet.write(row, 17, ' ', cell_format['content_def'])
                                        worksheet.write(row, 19, ' ', cell_format['content_def'])
                                        worksheet.write(row, 21, ' ', cell_format['content_def'])
                                        worksheet.write(row, 23, ' ', cell_format['content_def'])
                                        worksheet.write(row, 25, ' ', cell_format['content_def'])
                                        worksheet.write(row, 27, ' ', cell_format['content_def'])
                                        worksheet.write(row, 29, ' ', cell_format['content_def'])
                                        worksheet.write(row, 31, ' ', cell_format['content_def'])

                                    elif (int(data['13']) == 7) :
                                        worksheet.write(row, 13, int(data['13']) - 4, cell_format['content_def'])
                                        worksheet.write(row, 15, int(data['13']) - 4, cell_format['content_def'])
                                        worksheet.write(row, 17, ' ', cell_format['content_def'])
                                        worksheet.write(row, 19, ' ', cell_format['content_def'])
                                        worksheet.write(row, 21, ' ', cell_format['content_def'])
                                        worksheet.write(row, 23, ' ', cell_format['content_def'])
                                        worksheet.write(row, 25, ' ', cell_format['content_def'])
                                        worksheet.write(row, 27, ' ', cell_format['content_def'])
                                        worksheet.write(row, 29, ' ', cell_format['content_def'])
                                        worksheet.write(row, 31, ' ', cell_format['content_def'])
                                        
                                    elif (int(data['13']) == 6) :
                                        if ("08" in bul or "09" in bul or "10" in bul or "11" in bul or "12" in bul or "13" in bul or "14" in bul) :
                                            worksheet.write(row, 13, 2, cell_format['content_def'])
                                            worksheet.write(row, 15, 2, cell_format['content_def'])
                                            worksheet.write(row, 17, ' ', cell_format['content_def'])
                                            worksheet.write(row, 19, ' ', cell_format['content_def'])
                                            worksheet.write(row, 21, ' ', cell_format['content_def'])
                                            worksheet.write(row, 23, ' ', cell_format['content_def'])
                                            worksheet.write(row, 25, ' ', cell_format['content_def'])
                                            worksheet.write(row, 27, ' ', cell_format['content_def'])
                                            worksheet.write(row, 29, ' ', cell_format['content_def'])
                                            worksheet.write(row, 31, ' ', cell_format['content_def'])
                                        elif ("01" in bul or "02" in bul or "03" in bul or "04" in bul or "05" in bul or "06" in bul or "07" in bul) :
                                            worksheet.write(row, 13, int(data['13']) - 5, cell_format['content_def'])
                                            worksheet.write(row, 15, int(data['13']) - 5, cell_format['content_def'])
                                            worksheet.write(row, 17, ' ', cell_format['content_def'])
                                            worksheet.write(row, 19, ' ', cell_format['content_def'])
                                            worksheet.write(row, 21, ' ', cell_format['content_def'])
                                            worksheet.write(row, 23, ' ', cell_format['content_def'])
                                            worksheet.write(row, 25, ' ', cell_format['content_def'])
                                            worksheet.write(row, 27, ' ', cell_format['content_def'])
                                            worksheet.write(row, 29, ' ', cell_format['content_def'])
                                            worksheet.write(row, 31, ' ', cell_format['content_def'])

                                        else :
                                            worksheet.write(row, 13, int(data['13']) - 4, cell_format['content_def'])
                                            worksheet.write(row, 15, int(data['13']) - 4, cell_format['content_def'])
                                            worksheet.write(row, 17, ' ', cell_format['content_def'])
                                            worksheet.write(row, 19, ' ', cell_format['content_def'])
                                            worksheet.write(row, 21, ' ', cell_format['content_def'])
                                            worksheet.write(row, 23, ' ', cell_format['content_def'])
                                            worksheet.write(row, 25, ' ', cell_format['content_def'])
                                            worksheet.write(row, 27, ' ', cell_format['content_def'])
                                            worksheet.write(row, 29, ' ', cell_format['content_def'])
                                            worksheet.write(row, 31, ' ', cell_format['content_def'])
                                    
                                    elif (int(data['13']) == 8) :
                                        if re.search("15 Feb", bul) or re.search("16 Feb", bul) or re.search("17 Feb", bul) or re.search("18 Feb", bul) or re.search("19 Feb", bul) or re.search("20 Feb", bul) or re.search("21", bul) :
                                            worksheet.write(row, 13, int(data['13']) - 5, cell_format['content_def'])
                                            worksheet.write(row, 15, int(data['13']) - 5, cell_format['content_def'])
                                            worksheet.write(row, 17, ' ', cell_format['content_def'])
                                            worksheet.write(row, 19, ' ', cell_format['content_def'])
                                            worksheet.write(row, 21, ' ', cell_format['content_def'])
                                            worksheet.write(row, 23, ' ', cell_format['content_def'])
                                            worksheet.write(row, 25, ' ', cell_format['content_def'])
                                            worksheet.write(row, 27, ' ', cell_format['content_def'])
                                            worksheet.write(row, 29, ' ', cell_format['content_def'])
                                            worksheet.write(row, 31, ' ', cell_format['content_def'])
                                        else :
                                            worksheet.write(row, 13, int(data['13']) - 4, cell_format['content_def'])
                                            worksheet.write(row, 15, int(data['13']) - 4, cell_format['content_def'])
                                            worksheet.write(row, 17, ' ', cell_format['content_def'])
                                            worksheet.write(row, 19, ' ', cell_format['content_def'])
                                            worksheet.write(row, 21, ' ', cell_format['content_def'])
                                            worksheet.write(row, 23, ' ', cell_format['content_def'])
                                            worksheet.write(row, 25, ' ', cell_format['content_def'])
                                            worksheet.write(row, 27, ' ', cell_format['content_def'])
                                            worksheet.write(row, 29, ' ', cell_format['content_def'])
                                            worksheet.write(row, 31, ' ', cell_format['content_def'])

                                    else :
                                        worksheet.write(row, 13, int(data['13']) - 4, cell_format['content_def'])
                                        worksheet.write(row, 15, int(data['13']) - 4, cell_format['content_def'])
                                        worksheet.write(row, 17, ' ', cell_format['content_def'])
                                        worksheet.write(row, 19, ' ', cell_format['content_def'])
                                        worksheet.write(row, 21, ' ', cell_format['content_def'])
                                        worksheet.write(row, 23, ' ', cell_format['content_def'])
                                        worksheet.write(row, 25, ' ', cell_format['content_def'])
                                        worksheet.write(row, 27, ' ', cell_format['content_def'])
                                        worksheet.write(row, 29, ' ', cell_format['content_def'])
                                        worksheet.write(row, 31, ' ', cell_format['content_def'])

                                elif ("Mar" in bul) :
                                    worksheet.write(row, 13, ' ', cell_format['content_def'])
                                    worksheet.write(row, 15, ' ', cell_format['content_def'])
                                    worksheet.write(row, 17, int(data['13']) - 8, cell_format['content_def'])
                                    worksheet.write(row, 19, int(data['13']) - 8, cell_format['content_def'])
                                    worksheet.write(row, 21, ' ', cell_format['content_def'])
                                    worksheet.write(row, 23, ' ', cell_format['content_def'])
                                    worksheet.write(row, 25, ' ', cell_format['content_def'])
                                    worksheet.write(row, 27, ' ', cell_format['content_def'])
                                    worksheet.write(row, 29, ' ', cell_format['content_def'])
                                    worksheet.write(row, 31, ' ', cell_format['content_def'])

                                else:
                                    worksheet.write(row, 13, ' ', cell_format['content_def'])
                                    worksheet.write(row, 15, ' ', cell_format['content_def'])
                                    worksheet.write(row, 17, ' ', cell_format['content_def'])
                                    worksheet.write(row, 19, ' ', cell_format['content_def'])
                                    worksheet.write(row, 21, ' ', cell_format['content_def'])
                                    worksheet.write(row, 23, ' ', cell_format['content_def'])
                                    worksheet.write(row, 25, ' ', cell_format['content_def'])
                                    worksheet.write(row, 27, ' ', cell_format['content_def'])
                                    worksheet.write(row, 29, ' ', cell_format['content_def'])
                                    worksheet.write(row, 31, ' ', cell_format['content_def'])
                                    worksheet.write(row, 32, ' ', cell_format['content_def'])
                                
                                worksheet.write(row, 16, ' ', cell_format['content_def'])
                                worksheet.write(row, 20, ' ', cell_format['content_def'])
                                worksheet.write(row, 24, ' ', cell_format['content_def'])
                                worksheet.write(row, 28, ' ', cell_format['content_def'])
                                worksheet.write(row, 32, ' ', cell_format['content_def']) 

                            if (data['14'] == None) :
                                worksheet.write(row, 14, ' ', cell_format['content_def'])

                            else :
                                if ("Feb" in bul) :
                                    worksheet.write(row, 14, data['14'], cell_format['content_right'])
                                    worksheet.write(row, 18, ' ', cell_format['content_def'])
                                    worksheet.write(row, 22, ' ', cell_format['content_def'])
                                    worksheet.write(row, 26, ' ', cell_format['content_def'])
                                    worksheet.write(row, 30, ' ', cell_format['content_def'])
                                    worksheet.write(row, 16, ' ', cell_format['content_def'])
                                    worksheet.write(row, 20, ' ', cell_format['content_def'])
                                    worksheet.write(row, 24, ' ', cell_format['content_def'])
                                    worksheet.write(row, 28, ' ', cell_format['content_def'])
                                    worksheet.write(row, 32, ' ', cell_format['content_def'])       
                                    palas += data['14']
                                elif ("Mar" in bul) :
                                    worksheet.write(row, 14, ' ', cell_format['content_def'])
                                    worksheet.write(row, 18, data['14'], cell_format['content_right'])
                                    worksheet.write(row, 22, ' ', cell_format['content_def'])
                                    worksheet.write(row, 26, ' ', cell_format['content_def'])
                                    worksheet.write(row, 30, ' ', cell_format['content_def'])
                                    worksheet.write(row, 16, ' ', cell_format['content_def'])
                                    worksheet.write(row, 20, ' ', cell_format['content_def'])
                                    worksheet.write(row, 24, ' ', cell_format['content_def'])
                                    worksheet.write(row, 28, ' ', cell_format['content_def'])
                                    worksheet.write(row, 32, ' ', cell_format['content_def']) 
                                    delas += data['14']
                                elif ("Apr" in bul) :
                                    worksheet.write(row, 14, ' ', cell_format['content_def'])
                                    worksheet.write(row, 18, ' ', cell_format['content_def'])
                                    worksheet.write(row, 22, data['14'], cell_format['content_right'])
                                    worksheet.write(row, 26, ' ', cell_format['content_def'])
                                    worksheet.write(row, 30, ' ', cell_format['content_def'])
                                    worksheet.write(row, 16, ' ', cell_format['content_def'])
                                    worksheet.write(row, 20, ' ', cell_format['content_def'])
                                    worksheet.write(row, 24, ' ', cell_format['content_def'])
                                    worksheet.write(row, 28, ' ', cell_format['content_def'])
                                    worksheet.write(row, 32, ' ', cell_format['content_def'])  
                                    dudu += data['14']
                                elif ("May" in bul) :
                                    worksheet.write(row, 14, ' ', cell_format['content_def'])
                                    worksheet.write(row, 18, ' ', cell_format['content_def'])
                                    worksheet.write(row, 22, ' ', cell_format['content_def'])
                                    worksheet.write(row, 26, data['14'], cell_format['content_right'])
                                    worksheet.write(row, 30, ' ', cell_format['content_def'])
                                    worksheet.write(row, 16, ' ', cell_format['content_def'])
                                    worksheet.write(row, 20, ' ', cell_format['content_def'])
                                    worksheet.write(row, 24, ' ', cell_format['content_def'])
                                    worksheet.write(row, 28, ' ', cell_format['content_def'])
                                    worksheet.write(row, 32, ' ', cell_format['content_def']) 
                                    dunam += data['14']
                                elif ("Jun" in bul) :
                                    worksheet.write(row, 14, ' ', cell_format['content_def'])
                                    worksheet.write(row, 18, ' ', cell_format['content_def'])
                                    worksheet.write(row, 22, ' ', cell_format['content_def'])
                                    worksheet.write(row, 26, ' ', cell_format['content_def'])
                                    worksheet.write(row, 30, data['14'], cell_format['content_right'])
                                    worksheet.write(row, 16, ' ', cell_format['content_def'])
                                    worksheet.write(row, 20, ' ', cell_format['content_def'])
                                    worksheet.write(row, 24, ' ', cell_format['content_def'])
                                    worksheet.write(row, 28, ' ', cell_format['content_def'])
                                    worksheet.write(row, 32, ' ', cell_format['content_def']) 
                                    tiluh += data['14']
                            
                        elif (self.periode == 2) :
                            if (int(data['13']) > 35) :
                                if re.search("05 Sep", bul) or re.search("06 Sep", bul) or re.search("07 Sep", bul) or re.search("12 Sep", bul) or re.search("13 Sep", bul) or re.search("14 Sep", bul) or re.search("26 Sep", bul) or re.search("27 Sep", bul) or re.search("28 Sep", bul) :
                                    worksheet.write(row, 13, ' ', cell_format['content_def'])
                                    worksheet.write(row, 15, ' ', cell_format['content_def'])
                                    worksheet.write(row, 17, ' ', cell_format['content_def'])
                                    worksheet.write(row, 19, ' ', cell_format['content_def'])
                                    worksheet.write(row, 21, ' ', cell_format['content_def'])
                                    worksheet.write(row, 23, ' ', cell_format['content_def'])
                                    worksheet.write(row, 25, ' ', cell_format['content_def'])
                                    worksheet.write(row, 27, ' ', cell_format['content_def'])
                                    worksheet.write(row, 29, int(data['13']) - 35, cell_format['content_def'])
                                    worksheet.write(row, 31, int(data['13']) - 35, cell_format['content_def'])
                                elif (int(data['13']) == 38) :
                                    if re.search("15 Sep", bul) or re.search("16 Sep", bul) or re.search("17 Sep", bul) or re.search("18 Sep", bul) or re.search("19 Sep", bul) or re.search("20 Sep", bul) or re.search("21 Sep", bul) :
                                        worksheet.write(row, 13, ' ', cell_format['content_def'])
                                        worksheet.write(row, 15, ' ', cell_format['content_def'])
                                        worksheet.write(row, 17, ' ', cell_format['content_def'])
                                        worksheet.write(row, 19, ' ', cell_format['content_def'])
                                        worksheet.write(row, 21, ' ', cell_format['content_def'])
                                        worksheet.write(row, 23, ' ', cell_format['content_def'])
                                        worksheet.write(row, 25, ' ', cell_format['content_def'])
                                        worksheet.write(row, 27, ' ', cell_format['content_def'])
                                        worksheet.write(row, 29, int(data['13']) - 35, cell_format['content_def'])
                                        worksheet.write(row, 31, int(data['13']) - 35, cell_format['content_def'])

                                    else :
                                        worksheet.write(row, 13, ' ', cell_format['content_def'])
                                        worksheet.write(row, 15, ' ', cell_format['content_def'])
                                        worksheet.write(row, 17, ' ', cell_format['content_def'])
                                        worksheet.write(row, 19, ' ', cell_format['content_def'])
                                        worksheet.write(row, 21, ' ', cell_format['content_def'])
                                        worksheet.write(row, 23, ' ', cell_format['content_def'])
                                        worksheet.write(row, 25, ' ', cell_format['content_def'])
                                        worksheet.write(row, 27, ' ', cell_format['content_def'])
                                        worksheet.write(row, 29, int(data['13']) - 34, cell_format['content_def'])
                                        worksheet.write(row, 31, int(data['13']) - 34, cell_format['content_def'])
                                else :
                                    worksheet.write(row, 13, ' ', cell_format['content_def'])
                                    worksheet.write(row, 15, ' ', cell_format['content_def'])
                                    worksheet.write(row, 17, ' ', cell_format['content_def'])
                                    worksheet.write(row, 19, ' ', cell_format['content_def'])
                                    worksheet.write(row, 21, ' ', cell_format['content_def'])
                                    worksheet.write(row, 23, ' ', cell_format['content_def'])
                                    worksheet.write(row, 25, ' ', cell_format['content_def'])
                                    worksheet.write(row, 27, ' ', cell_format['content_def'])
                                    worksheet.write(row, 29, int(data['13']) - 34, cell_format['content_def'])
                                    worksheet.write(row, 31, int(data['13']) - 34, cell_format['content_def'])

                            elif (int(data['13']) > 30 and int(data['13']) < 36) :
                                if ("Aug" in bul) :
                                    worksheet.write(row, 13, ' ', cell_format['content_def'])
                                    worksheet.write(row, 15, ' ', cell_format['content_def'])
                                    worksheet.write(row, 17, ' ', cell_format['content_def'])
                                    worksheet.write(row, 19, ' ', cell_format['content_def'])
                                    worksheet.write(row, 21, ' ', cell_format['content_def'])
                                    worksheet.write(row, 23, ' ', cell_format['content_def'])
                                    worksheet.write(row, 25, int(data['13']) - 30, cell_format['content_def'])
                                    worksheet.write(row, 27, int(data['13']) - 30, cell_format['content_def'])
                                    worksheet.write(row, 29, ' ', cell_format['content_def'])
                                    worksheet.write(row, 31, ' ', cell_format['content_def'])
                                else :
                                    worksheet.write(row, 13, ' ', cell_format['content_def'])
                                    worksheet.write(row, 15, ' ', cell_format['content_def'])
                                    worksheet.write(row, 17, ' ', cell_format['content_def'])
                                    worksheet.write(row, 19, ' ', cell_format['content_def'])
                                    worksheet.write(row, 21, ' ', cell_format['content_def'])
                                    worksheet.write(row, 23, ' ', cell_format['content_def'])
                                    worksheet.write(row, 25, ' ', cell_format['content_def'])
                                    worksheet.write(row, 27, ' ', cell_format['content_def'])
                                    worksheet.write(row, 29, int(data['13']) - 34, cell_format['content_def'])
                                    worksheet.write(row, 31, int(data['13']) - 34, cell_format['content_def'])


                            elif (int(data['13']) > 26 and int(data['13']) < 31) :
                                if ("Jul" in bul) :
                                    if re.search("08 Jul", bul) or re.search("09 Jul", bul) or re.search("10 Jul", bul) or re.search("15 Jul", bul) or re.search("22 Jul", bul) or re.search("23 Jul", bul) or re.search("24 Jul", bul) :
                                        worksheet.write(row, 13, ' ', cell_format['content_def'])
                                        worksheet.write(row, 15, ' ', cell_format['content_def'])
                                        worksheet.write(row, 17, ' ', cell_format['content_def'])
                                        worksheet.write(row, 19, ' ', cell_format['content_def'])
                                        worksheet.write(row, 21, int(data['13']) - 25, cell_format['content_def'])
                                        worksheet.write(row, 23, int(data['13']) - 25, cell_format['content_def'])
                                        worksheet.write(row, 25, ' ', cell_format['content_def'])
                                        worksheet.write(row, 27, ' ', cell_format['content_def'])
                                        worksheet.write(row, 29, ' ', cell_format['content_def'])
                                        worksheet.write(row, 31, ' ', cell_format['content_def'])
                                    elif re.search("11 Jul", bul) or re.search("12 Jul", bul) or re.search("13 Jul", bul) or re.search("14 Jul", bul) or re.search("25 Jul", bul) or re.search("26 Jul", bul) :
                                        worksheet.write(row, 13, ' ', cell_format['content_def'])
                                        worksheet.write(row, 15, ' ', cell_format['content_def'])
                                        worksheet.write(row, 17, ' ', cell_format['content_def'])
                                        worksheet.write(row, 19, ' ', cell_format['content_def'])
                                        worksheet.write(row, 21, int(data['13']) - 26, cell_format['content_def'])
                                        worksheet.write(row, 23, int(data['13']) - 26, cell_format['content_def'])
                                        worksheet.write(row, 25, ' ', cell_format['content_def'])
                                        worksheet.write(row, 27, ' ', cell_format['content_def'])
                                        worksheet.write(row, 29, ' ', cell_format['content_def'])
                                        worksheet.write(row, 31, ' ', cell_format['content_def'])
                                    elif "29" in bul or "30" in bul or "31" in bul :
                                        worksheet.write(row, 13, ' ', cell_format['content_def'])
                                        worksheet.write(row, 15, ' ', cell_format['content_def'])
                                        worksheet.write(row, 17, ' ', cell_format['content_def'])
                                        worksheet.write(row, 19, ' ', cell_format['content_def'])
                                        worksheet.write(row, 21, int(data['13']) - 25, cell_format['content_def'])
                                        worksheet.write(row, 23, int(data['13']) - 25, cell_format['content_def'])
                                        worksheet.write(row, 25, ' ', cell_format['content_def'])
                                        worksheet.write(row, 27, ' ', cell_format['content_def'])
                                        worksheet.write(row, 29, ' ', cell_format['content_def'])
                                        worksheet.write(row, 31, ' ', cell_format['content_def'])
                                    elif (int(data['13']) == 28) :
                                        if re.search("16 Jul", bul) or re.search("17 Jul", bul) or re.search("18 Jul", bul) or re.search("19 Jul", bul) :
                                            worksheet.write(row, 13, ' ', cell_format['content_def'])
                                            worksheet.write(row, 15, ' ', cell_format['content_def'])
                                            worksheet.write(row, 17, ' ', cell_format['content_def'])
                                            worksheet.write(row, 19, ' ', cell_format['content_def'])
                                            worksheet.write(row, 21, int(data['13']) - 25, cell_format['content_def'])
                                            worksheet.write(row, 23, int(data['13']) - 25, cell_format['content_def'])
                                            worksheet.write(row, 25, ' ', cell_format['content_def'])
                                            worksheet.write(row, 27, ' ', cell_format['content_def'])
                                            worksheet.write(row, 29, ' ', cell_format['content_def'])
                                            worksheet.write(row, 31, ' ', cell_format['content_def'])
                                        else :
                                            worksheet.write(row, 13, ' ', cell_format['content_def'])
                                            worksheet.write(row, 15, ' ', cell_format['content_def'])
                                            worksheet.write(row, 17, ' ', cell_format['content_def'])
                                            worksheet.write(row, 19, ' ', cell_format['content_def'])
                                            worksheet.write(row, 21, int(data['13']) - 26, cell_format['content_def'])
                                            worksheet.write(row, 23, int(data['13']) - 26, cell_format['content_def'])
                                            worksheet.write(row, 25, ' ', cell_format['content_def'])
                                            worksheet.write(row, 27, ' ', cell_format['content_def'])
                                            worksheet.write(row, 29, ' ', cell_format['content_def'])
                                            worksheet.write(row, 31, ' ', cell_format['content_def'])

                                    else :
                                        worksheet.write(row, 13, ' ', cell_format['content_def'])
                                        worksheet.write(row, 15, ' ', cell_format['content_def'])
                                        worksheet.write(row, 17, ' ', cell_format['content_def'])
                                        worksheet.write(row, 19, ' ', cell_format['content_def'])
                                        worksheet.write(row, 21, int(data['13']) - 26, cell_format['content_def'])
                                        worksheet.write(row, 23, int(data['13']) - 26, cell_format['content_def'])
                                        worksheet.write(row, 25, ' ', cell_format['content_def'])
                                        worksheet.write(row, 27, ' ', cell_format['content_def'])
                                        worksheet.write(row, 29, ' ', cell_format['content_def'])
                                        worksheet.write(row, 31, ' ', cell_format['content_def'])

                                else :
                                    worksheet.write(row, 13, ' ', cell_format['content_def'])
                                    worksheet.write(row, 15, ' ', cell_format['content_def'])
                                    worksheet.write(row, 17, ' ', cell_format['content_def'])
                                    worksheet.write(row, 19, ' ', cell_format['content_def'])
                                    worksheet.write(row, 21, ' ', cell_format['content_def'])
                                    worksheet.write(row, 23, ' ', cell_format['content_def'])
                                    worksheet.write(row, 25, int(data['13']) - 29, cell_format['content_def'])
                                    worksheet.write(row, 27, int(data['13']) - 29, cell_format['content_def'])
                                    worksheet.write(row, 29, ' ', cell_format['content_def'])
                                    worksheet.write(row, 31, ' ', cell_format['content_def'])

                            elif (int(data['13']) > 22 and int(data['13']) < 27) :
                                if ("Jun" in bul) :
                                    if re.search("08 Jun", bul) or re.search("09 Jun", bul) or re.search("10 Jun", bul) or re.search("11 Jun", bul) or re.search("12 Jun", bul) or re.search("15 Jun", bul) or re.search("22 Jun", bul) or re.search("23 Jun", bul) or re.search("24 Jun", bul) or re.search("25 Jun", bul) or re.search("26 Jun", bul) :
                                        worksheet.write(row, 13, ' ', cell_format['content_def'])
                                        worksheet.write(row, 15, ' ', cell_format['content_def'])
                                        worksheet.write(row, 17, int(data['13']) - 21, cell_format['content_def'])
                                        worksheet.write(row, 19, int(data['13']) - 21, cell_format['content_def'])
                                        worksheet.write(row, 21, ' ', cell_format['content_def'])
                                        worksheet.write(row, 23, ' ', cell_format['content_def'])
                                        worksheet.write(row, 25, ' ', cell_format['content_def'])
                                        worksheet.write(row, 27, ' ', cell_format['content_def'])
                                        worksheet.write(row, 29, ' ', cell_format['content_def'])
                                        worksheet.write(row, 31, ' ', cell_format['content_def'])
                                    elif re.search("13 Jun", bul) or re.search("14 Jun", bul) :
                                        worksheet.write(row, 13, ' ', cell_format['content_def'])
                                        worksheet.write(row, 15, ' ', cell_format['content_def'])
                                        worksheet.write(row, 17, int(data['13']) - 22, cell_format['content_def'])
                                        worksheet.write(row, 19, int(data['13']) - 22, cell_format['content_def'])
                                        worksheet.write(row, 21, ' ', cell_format['content_def'])
                                        worksheet.write(row, 23, ' ', cell_format['content_def'])
                                        worksheet.write(row, 25, ' ', cell_format['content_def'])
                                        worksheet.write(row, 27, ' ', cell_format['content_def'])
                                        worksheet.write(row, 29, ' ', cell_format['content_def'])
                                        worksheet.write(row, 31, ' ', cell_format['content_def'])
                                    elif re.search("14 Jun", bul) or "29" in bul or "30" in bul :
                                        worksheet.write(row, 13, ' ', cell_format['content_def'])
                                        worksheet.write(row, 15, ' ', cell_format['content_def'])
                                        worksheet.write(row, 17, int(data['13']) - 21, cell_format['content_def'])
                                        worksheet.write(row, 19, int(data['13']) - 21, cell_format['content_def'])
                                        worksheet.write(row, 21, ' ', cell_format['content_def'])
                                        worksheet.write(row, 23, ' ', cell_format['content_def'])
                                        worksheet.write(row, 25, ' ', cell_format['content_def'])
                                        worksheet.write(row, 27, ' ', cell_format['content_def'])
                                        worksheet.write(row, 29, ' ', cell_format['content_def'])
                                        worksheet.write(row, 31, ' ', cell_format['content_def'])
                                    elif (int(data['13']) == 24) :
                                        if re.search("16 Jun", bul) or re.search("17 Jun", bul) or re.search("18 Jun", bul) or re.search("19 Jun", bul) :
                                            worksheet.write(row, 13, ' ', cell_format['content_def'])
                                            worksheet.write(row, 15, ' ', cell_format['content_def'])
                                            worksheet.write(row, 17, int(data['13']) - 21, cell_format['content_def'])
                                            worksheet.write(row, 19, int(data['13']) - 21, cell_format['content_def'])
                                            worksheet.write(row, 21, ' ', cell_format['content_def'])
                                            worksheet.write(row, 23, ' ', cell_format['content_def'])
                                            worksheet.write(row, 25, ' ', cell_format['content_def'])
                                            worksheet.write(row, 27, ' ', cell_format['content_def'])
                                            worksheet.write(row, 29, ' ', cell_format['content_def'])
                                            worksheet.write(row, 31, ' ', cell_format['content_def'])
                                        else :
                                            worksheet.write(row, 13, ' ', cell_format['content_def'])
                                            worksheet.write(row, 15, ' ', cell_format['content_def'])
                                            worksheet.write(row, 17, int(data['13']) - 22, cell_format['content_def'])
                                            worksheet.write(row, 19, int(data['13']) - 22, cell_format['content_def'])
                                            worksheet.write(row, 21, ' ', cell_format['content_def'])
                                            worksheet.write(row, 23, ' ', cell_format['content_def'])
                                            worksheet.write(row, 25, ' ', cell_format['content_def'])
                                            worksheet.write(row, 27, ' ', cell_format['content_def'])
                                            worksheet.write(row, 29, ' ', cell_format['content_def'])
                                            worksheet.write(row, 31, ' ', cell_format['content_def'])

                                    else :
                                        worksheet.write(row, 13, ' ', cell_format['content_def'])
                                        worksheet.write(row, 15, ' ', cell_format['content_def'])
                                        worksheet.write(row, 17, int(data['13']) - 22, cell_format['content_def'])
                                        worksheet.write(row, 19, int(data['13']) - 22, cell_format['content_def'])
                                        worksheet.write(row, 21, ' ', cell_format['content_def'])
                                        worksheet.write(row, 23, ' ', cell_format['content_def'])
                                        worksheet.write(row, 25, ' ', cell_format['content_def'])
                                        worksheet.write(row, 27, ' ', cell_format['content_def'])
                                        worksheet.write(row, 29, ' ', cell_format['content_def'])
                                        worksheet.write(row, 31, ' ', cell_format['content_def'])

                                else :
                                    worksheet.write(row, 13, ' ', cell_format['content_def'])
                                    worksheet.write(row, 15, ' ', cell_format['content_def'])
                                    worksheet.write(row, 17, ' ', cell_format['content_def'])
                                    worksheet.write(row, 19, ' ', cell_format['content_def'])
                                    worksheet.write(row, 21, int(data['13']) - 25, cell_format['content_def'])
                                    worksheet.write(row, 23, int(data['13']) - 25, cell_format['content_def'])
                                    worksheet.write(row, 25, ' ', cell_format['content_def'])
                                    worksheet.write(row, 27, ' ', cell_format['content_def'])
                                    worksheet.write(row, 29, ' ', cell_format['content_def'])
                                    worksheet.write(row, 31, ' ', cell_format['content_def'])

                            else :
                                if ("May" in bul) :
                                    if re.search("02 May", bul) or re.search("03 May", bul) or re.search("04 May", bul) or re.search("05 May", bul) or re.search("06 May", bul) or re.search("09 May", bul) or re.search("10 May", bul) or re.search("11 May", bul) or re.search("12 May", bul) or re.search("13 May", bul) or re.search("14 May", bul) or re.search("23 May", bul) or re.search("24 May", bul) or re.search("25 May", bul) or re.search("26 May", bul) or re.search("27 May", bul) or re.search("28 May", bul) or re.search("30 May", bul) or re.search("31 May", bul) :
                                        worksheet.write(row, 13, int(data['13']) - 17, cell_format['content_def'])
                                        worksheet.write(row, 15, int(data['13']) - 17, cell_format['content_def'])
                                        worksheet.write(row, 17, ' ', cell_format['content_def'])
                                        worksheet.write(row, 19, ' ', cell_format['content_def'])
                                        worksheet.write(row, 21, ' ', cell_format['content_def'])
                                        worksheet.write(row, 23, ' ', cell_format['content_def'])
                                        worksheet.write(row, 25, ' ', cell_format['content_def'])
                                        worksheet.write(row, 27, ' ', cell_format['content_def'])
                                        worksheet.write(row, 29, ' ', cell_format['content_def'])
                                        worksheet.write(row, 31, ' ', cell_format['content_def'])
                                    
                                    elif re.search("08 May", bul) :
                                        worksheet.write(row, 13, int(data['13']) - 16, cell_format['content_def'])
                                        worksheet.write(row, 15, int(data['13']) - 16, cell_format['content_def'])
                                        worksheet.write(row, 17, ' ', cell_format['content_def'])
                                        worksheet.write(row, 19, ' ', cell_format['content_def'])
                                        worksheet.write(row, 21, ' ', cell_format['content_def'])
                                        worksheet.write(row, 23, ' ', cell_format['content_def'])
                                        worksheet.write(row, 25, ' ', cell_format['content_def'])
                                        worksheet.write(row, 27, ' ', cell_format['content_def'])
                                        worksheet.write(row, 29, ' ', cell_format['content_def'])
                                        worksheet.write(row, 31, ' ', cell_format['content_def'])

                                    elif (int(data['13']) == 17 or int(data['13']) == 21) :
                                        if re.search("07 May", bul) or re.search("08 May", bul) or re.search("09 May", bul) or re.search("10 May", bul) or re.search("11 May", bul) or re.search("12 May", bul) or re.search("13 May", bul) or re.search("14 May", bul) :
                                            worksheet.write(row, 13, int(data['13']) - 17, cell_format['content_def'])
                                            worksheet.write(row, 15, int(data['13']) - 17, cell_format['content_def'])
                                            worksheet.write(row, 17, ' ', cell_format['content_def'])
                                            worksheet.write(row, 19, ' ', cell_format['content_def'])
                                            worksheet.write(row, 21, ' ', cell_format['content_def'])
                                            worksheet.write(row, 23, ' ', cell_format['content_def'])
                                            worksheet.write(row, 25, ' ', cell_format['content_def'])
                                            worksheet.write(row, 27, ' ', cell_format['content_def'])
                                            worksheet.write(row, 29, ' ', cell_format['content_def'])
                                            worksheet.write(row, 31, ' ', cell_format['content_def'])
                                        else :
                                            worksheet.write(row, 13, int(data['13']) - 16, cell_format['content_def'])
                                            worksheet.write(row, 15, int(data['13']) - 16, cell_format['content_def'])
                                            worksheet.write(row, 17, ' ', cell_format['content_def'])
                                            worksheet.write(row, 19, ' ', cell_format['content_def'])
                                            worksheet.write(row, 21, ' ', cell_format['content_def'])
                                            worksheet.write(row, 23, ' ', cell_format['content_def'])
                                            worksheet.write(row, 25, ' ', cell_format['content_def'])
                                            worksheet.write(row, 27, ' ', cell_format['content_def'])
                                            worksheet.write(row, 29, ' ', cell_format['content_def'])
                                            worksheet.write(row, 31, ' ', cell_format['content_def'])

                                    elif (int(data['13']) == 18) :
                                        if re.search("07 May", bul) or re.search("08 May", bul) or re.search("09 May", bul) or re.search("10 May", bul) or re.search("11 May", bul) or re.search("12 May", bul) or re.search("13 May", bul) or re.search("14 May", bul) :
                                            worksheet.write(row, 13, int(data['13']) - 17, cell_format['content_def'])
                                            worksheet.write(row, 15, int(data['13']) - 17, cell_format['content_def'])
                                            worksheet.write(row, 17, ' ', cell_format['content_def'])
                                            worksheet.write(row, 19, ' ', cell_format['content_def'])
                                            worksheet.write(row, 21, ' ', cell_format['content_def'])
                                            worksheet.write(row, 23, ' ', cell_format['content_def'])
                                            worksheet.write(row, 25, ' ', cell_format['content_def'])
                                            worksheet.write(row, 27, ' ', cell_format['content_def'])
                                            worksheet.write(row, 29, ' ', cell_format['content_def'])
                                            worksheet.write(row, 31, ' ', cell_format['content_def'])

                                        else :
                                            worksheet.write(row, 13, int(data['13']) - 16, cell_format['content_def'])
                                            worksheet.write(row, 15, int(data['13']) - 16, cell_format['content_def'])
                                            worksheet.write(row, 17, ' ', cell_format['content_def'])
                                            worksheet.write(row, 19, ' ', cell_format['content_def'])
                                            worksheet.write(row, 21, ' ', cell_format['content_def'])
                                            worksheet.write(row, 23, ' ', cell_format['content_def'])
                                            worksheet.write(row, 25, ' ', cell_format['content_def'])
                                            worksheet.write(row, 27, ' ', cell_format['content_def'])
                                            worksheet.write(row, 29, ' ', cell_format['content_def'])
                                            worksheet.write(row, 31, ' ', cell_format['content_def'])
                                    
                                    elif (int(data['13']) == 19) :
                                        worksheet.write(row, 13, int(data['13']) - 16, cell_format['content_def'])
                                        worksheet.write(row, 15, int(data['13']) - 16, cell_format['content_def'])
                                        worksheet.write(row, 17, ' ', cell_format['content_def'])
                                        worksheet.write(row, 19, ' ', cell_format['content_def'])
                                        worksheet.write(row, 21, ' ', cell_format['content_def'])
                                        worksheet.write(row, 23, ' ', cell_format['content_def'])
                                        worksheet.write(row, 25, ' ', cell_format['content_def'])
                                        worksheet.write(row, 27, ' ', cell_format['content_def'])
                                        worksheet.write(row, 29, ' ', cell_format['content_def'])
                                        worksheet.write(row, 31, ' ', cell_format['content_def'])

                                    elif (int(data['13']) == 20) :
                                        if re.search("15 May", bul) or re.search("16 May", bul) or re.search("17 May", bul) or re.search("18 May", bul) or re.search("19 May", bul) or re.search("20 May", bul) or re.search("21 May", bul) :
                                            worksheet.write(row, 13, int(data['13']) - 17, cell_format['content_def'])
                                            worksheet.write(row, 15, int(data['13']) - 17, cell_format['content_def'])
                                            worksheet.write(row, 17, ' ', cell_format['content_def'])
                                            worksheet.write(row, 19, ' ', cell_format['content_def'])
                                            worksheet.write(row, 21, ' ', cell_format['content_def'])
                                            worksheet.write(row, 23, ' ', cell_format['content_def'])
                                            worksheet.write(row, 25, ' ', cell_format['content_def'])
                                            worksheet.write(row, 27, ' ', cell_format['content_def'])
                                            worksheet.write(row, 29, ' ', cell_format['content_def'])
                                            worksheet.write(row, 31, ' ', cell_format['content_def'])
                                        else :
                                            worksheet.write(row, 13, int(data['13']) - 16, cell_format['content_def'])
                                            worksheet.write(row, 15, int(data['13']) - 16, cell_format['content_def'])
                                            worksheet.write(row, 17, ' ', cell_format['content_def'])
                                            worksheet.write(row, 19, ' ', cell_format['content_def'])
                                            worksheet.write(row, 21, ' ', cell_format['content_def'])
                                            worksheet.write(row, 23, ' ', cell_format['content_def'])
                                            worksheet.write(row, 25, ' ', cell_format['content_def'])
                                            worksheet.write(row, 27, ' ', cell_format['content_def'])
                                            worksheet.write(row, 29, ' ', cell_format['content_def'])
                                            worksheet.write(row, 31, ' ', cell_format['content_def'])

                                    else :
                                        worksheet.write(row, 13, int(data['13']) - 16, cell_format['content_def'])
                                        worksheet.write(row, 15, int(data['13']) - 16, cell_format['content_def'])
                                        worksheet.write(row, 17, ' ', cell_format['content_def'])
                                        worksheet.write(row, 19, ' ', cell_format['content_def'])
                                        worksheet.write(row, 21, ' ', cell_format['content_def'])
                                        worksheet.write(row, 23, ' ', cell_format['content_def'])
                                        worksheet.write(row, 25, ' ', cell_format['content_def'])
                                        worksheet.write(row, 27, ' ', cell_format['content_def'])
                                        worksheet.write(row, 29, ' ', cell_format['content_def'])
                                        worksheet.write(row, 31, ' ', cell_format['content_def'])

                                elif ("Jun" in bul) :
                                    worksheet.write(row, 13, ' ', cell_format['content_def'])
                                    worksheet.write(row, 15, ' ', cell_format['content_def'])
                                    worksheet.write(row, 17, int(data['13']) - 21, cell_format['content_def'])
                                    worksheet.write(row, 19, int(data['13']) - 21, cell_format['content_def'])
                                    worksheet.write(row, 21, ' ', cell_format['content_def'])
                                    worksheet.write(row, 23, ' ', cell_format['content_def'])
                                    worksheet.write(row, 25, ' ', cell_format['content_def'])
                                    worksheet.write(row, 27, ' ', cell_format['content_def'])
                                    worksheet.write(row, 29, ' ', cell_format['content_def'])
                                    worksheet.write(row, 31, ' ', cell_format['content_def'])

                                else :
                                    worksheet.write(row, 13, ' ', cell_format['content_def'])
                                    worksheet.write(row, 15, ' ', cell_format['content_def'])
                                    worksheet.write(row, 17, ' ', cell_format['content_def'])
                                    worksheet.write(row, 19, ' ', cell_format['content_def'])
                                    worksheet.write(row, 21, ' ', cell_format['content_def'])
                                    worksheet.write(row, 23, ' ', cell_format['content_def'])
                                    worksheet.write(row, 25, ' ', cell_format['content_def'])
                                    worksheet.write(row, 27, ' ', cell_format['content_def'])
                                    worksheet.write(row, 29, ' ', cell_format['content_def'])
                                    worksheet.write(row, 31, ' ', cell_format['content_def'])
                                    worksheet.write(row, 32, ' ', cell_format['content_def'])   

                            if (data['14'] == None) :
                                worksheet.write(row, 14, ' ', cell_format['content_def'])
                            else :
                                if ("May" in bul) :
                                    worksheet.write(row, 14, data['14'], cell_format['content_right'])
                                    worksheet.write(row, 16, ' ', cell_format['content_right'])
                                    worksheet.write(row, 18, ' ', cell_format['content_def'])
                                    worksheet.write(row, 20, ' ', cell_format['content_def'])
                                    worksheet.write(row, 22, ' ', cell_format['content_def'])
                                    worksheet.write(row, 24, ' ', cell_format['content_def'])
                                    worksheet.write(row, 26, ' ', cell_format['content_def'])
                                    worksheet.write(row, 28, ' ', cell_format['content_def'])
                                    worksheet.write(row, 30, ' ', cell_format['content_def'])
                                    worksheet.write(row, 32, ' ', cell_format['content_def'])       
                                    palas += data['14']
                                elif ("Jun" in bul) :
                                    worksheet.write(row, 14, ' ', cell_format['content_def'])
                                    worksheet.write(row, 16, ' ', cell_format['content_def'])
                                    worksheet.write(row, 18, data['14'], cell_format['content_right'])
                                    worksheet.write(row, 20, ' ', cell_format['content_def'])
                                    worksheet.write(row, 22, ' ', cell_format['content_def'])
                                    worksheet.write(row, 24, ' ', cell_format['content_def'])
                                    worksheet.write(row, 26, ' ', cell_format['content_def'])
                                    worksheet.write(row, 28, ' ', cell_format['content_def'])
                                    worksheet.write(row, 30, ' ', cell_format['content_def'])
                                    worksheet.write(row, 32, ' ', cell_format['content_def'])
                                    delas += data['14']
                                elif ("Jul" in bul) :
                                    worksheet.write(row, 14, ' ', cell_format['content_def'])
                                    worksheet.write(row, 16, ' ', cell_format['content_def'])
                                    worksheet.write(row, 18, ' ', cell_format['content_def'])
                                    worksheet.write(row, 20, ' ', cell_format['content_def'])
                                    worksheet.write(row, 22, data['14'], cell_format['content_right'])
                                    worksheet.write(row, 24, ' ', cell_format['content_def'])
                                    worksheet.write(row, 26, ' ', cell_format['content_def'])
                                    worksheet.write(row, 28, ' ', cell_format['content_def'])
                                    worksheet.write(row, 30, ' ', cell_format['content_def'])
                                    worksheet.write(row, 32, ' ', cell_format['content_def'])
                                    dudu += data['14']
                                elif ("Aug" in bul) :
                                    worksheet.write(row, 14, ' ', cell_format['content_def'])
                                    worksheet.write(row, 16, ' ', cell_format['content_def'])
                                    worksheet.write(row, 18, ' ', cell_format['content_def'])
                                    worksheet.write(row, 20, ' ', cell_format['content_def'])
                                    worksheet.write(row, 22, ' ', cell_format['content_def'])
                                    worksheet.write(row, 24, ' ', cell_format['content_def'])
                                    worksheet.write(row, 26, data['14'], cell_format['content_right'])
                                    worksheet.write(row, 28, ' ', cell_format['content_def'])
                                    worksheet.write(row, 30, ' ', cell_format['content_def'])
                                    worksheet.write(row, 32, ' ', cell_format['content_def'])
                                    dunam += data['14']
                                elif ("Sep" in bul) :
                                    worksheet.write(row, 14, ' ', cell_format['content_def'])
                                    worksheet.write(row, 16, ' ', cell_format['content_def'])
                                    worksheet.write(row, 18, ' ', cell_format['content_def'])
                                    worksheet.write(row, 20, ' ', cell_format['content_def'])
                                    worksheet.write(row, 22, ' ', cell_format['content_def'])
                                    worksheet.write(row, 24, ' ', cell_format['content_def'])
                                    worksheet.write(row, 26, ' ', cell_format['content_def'])
                                    worksheet.write(row, 28, ' ', cell_format['content_def'])
                                    worksheet.write(row, 30, data['14'], cell_format['content_right'])
                                    worksheet.write(row, 32, ' ', cell_format['content_def'])
                                    tiluh += data['14']
                            
                        elif (self.periode == 3) :
                            if (int(data['13']) > 48) :
                                if re.search("08 Dec", bul) or re.search("09 Dec", bul) or re.search("10 Dec", bul) or re.search("11 Dec", bul) or re.search("15 Dec", bul) or re.search("16 Dec", bul) or re.search("17 Dec", bul) or re.search("18 Dec", bul) or re.search("22 Dec", bul) or re.search("23 Dec", bul) or re.search("24 Dec", bul) or re.search("25 Dec", bul) or re.search("29 Dec", bul) or re.search("30 Dec", bul) or re.search("31 Dec", bul) :
                                    worksheet.write(row, 13, ' ', cell_format['content_def'])
                                    worksheet.write(row, 15, ' ', cell_format['content_def'])
                                    worksheet.write(row, 17, ' ', cell_format['content_def'])
                                    worksheet.write(row, 19, ' ', cell_format['content_def'])
                                    worksheet.write(row, 21, ' ', cell_format['content_def'])
                                    worksheet.write(row, 23, ' ', cell_format['content_def'])
                                    worksheet.write(row, 25, ' ', cell_format['content_def'])
                                    worksheet.write(row, 27, ' ', cell_format['content_def'])
                                    worksheet.write(row, 29, int(data['13']) - 47, cell_format['content_def'])
                                    worksheet.write(row, 31, int(data['13']) - 47, cell_format['content_def'])
                                else :
                                    worksheet.write(row, 13, ' ', cell_format['content_def'])
                                    worksheet.write(row, 15, ' ', cell_format['content_def'])
                                    worksheet.write(row, 17, ' ', cell_format['content_def'])
                                    worksheet.write(row, 19, ' ', cell_format['content_def'])
                                    worksheet.write(row, 21, ' ', cell_format['content_def'])
                                    worksheet.write(row, 23, ' ', cell_format['content_def'])
                                    worksheet.write(row, 25, ' ', cell_format['content_def'])
                                    worksheet.write(row, 27, ' ', cell_format['content_def'])
                                    worksheet.write(row, 29, int(data['13']) - 48, cell_format['content_def'])
                                    worksheet.write(row, 31, int(data['13']) - 48, cell_format['content_def'])

                            elif (int(data['13']) > 44 and int(data['13']) < 49) :
                                if ("Nov" in bul) :
                                    if re.search("21 Nov", bul) or re.search("28 Nov", bul) :
                                        worksheet.write(row, 13, ' ', cell_format['content_def'])
                                        worksheet.write(row, 15, ' ', cell_format['content_def'])
                                        worksheet.write(row, 17, ' ', cell_format['content_def'])
                                        worksheet.write(row, 19, ' ', cell_format['content_def'])
                                        worksheet.write(row, 21, ' ', cell_format['content_def'])
                                        worksheet.write(row, 23, ' ', cell_format['content_def'])
                                        worksheet.write(row, 25, int(data['13']) - 44, cell_format['content_def'])
                                        worksheet.write(row, 27, int(data['13']) - 44, cell_format['content_def'])
                                        worksheet.write(row, 29, ' ', cell_format['content_def'])
                                        worksheet.write(row, 31, ' ', cell_format['content_def'])

                                    elif (int(data['13']) == 45) :
                                        if re.search("08 Nov", bul) or re.search("09 Nov", bul) or re.search("10 Nov", bul) or re.search("11 Nov", bul) or re.search("12 Nov", bul) or re.search("13 Nov", bul) :
                                            worksheet.write(row, 13, ' ', cell_format['content_def'])
                                            worksheet.write(row, 15, ' ', cell_format['content_def'])
                                            worksheet.write(row, 17, ' ', cell_format['content_def'])
                                            worksheet.write(row, 19, ' ', cell_format['content_def'])
                                            worksheet.write(row, 21, ' ', cell_format['content_def'])
                                            worksheet.write(row, 23, ' ', cell_format['content_def'])
                                            worksheet.write(row, 25, int(data['13']) - 43, cell_format['content_def'])
                                            worksheet.write(row, 27, int(data['13']) - 43, cell_format['content_def'])
                                            worksheet.write(row, 29, ' ', cell_format['content_def'])
                                            worksheet.write(row, 31, ' ', cell_format['content_def'])
                                        else :
                                            worksheet.write(row, 13, ' ', cell_format['content_def'])
                                            worksheet.write(row, 15, ' ', cell_format['content_def'])
                                            worksheet.write(row, 17, ' ', cell_format['content_def'])
                                            worksheet.write(row, 19, ' ', cell_format['content_def'])
                                            worksheet.write(row, 21, ' ', cell_format['content_def'])
                                            worksheet.write(row, 23, ' ', cell_format['content_def'])
                                            worksheet.write(row, 25, int(data['13']) - 44, cell_format['content_def'])
                                            worksheet.write(row, 27, int(data['13']) - 44, cell_format['content_def'])
                                            worksheet.write(row, 29, ' ', cell_format['content_def'])
                                            worksheet.write(row, 31, ' ', cell_format['content_def'])
                                        
                                    elif (int(data['13']) == 46) :
                                        if ("10" in bul or "11" in bul or "12" in bul or "13" in bul or "14" in bul) :
                                            worksheet.write(row, 13, ' ', cell_format['content_def'])
                                            worksheet.write(row, 15, ' ', cell_format['content_def'])
                                            worksheet.write(row, 17, ' ', cell_format['content_def'])
                                            worksheet.write(row, 19, ' ', cell_format['content_def'])
                                            worksheet.write(row, 21, ' ', cell_format['content_def'])
                                            worksheet.write(row, 23, ' ', cell_format['content_def'])
                                            worksheet.write(row, 25, int(data['13']) - 44, cell_format['content_def'])
                                            worksheet.write(row, 27, int(data['13']) - 44, cell_format['content_def'])
                                            worksheet.write(row, 29, ' ', cell_format['content_def'])
                                            worksheet.write(row, 31, ' ', cell_format['content_def'])
                                        elif ("15" in bul or "16" in bul or "17" in bul or "18" in bul or "19" in bul or "20" in bul or "21" in bul) :
                                            worksheet.write(row, 13, ' ', cell_format['content_def'])
                                            worksheet.write(row, 15, ' ', cell_format['content_def'])
                                            worksheet.write(row, 17, ' ', cell_format['content_def'])
                                            worksheet.write(row, 19, ' ', cell_format['content_def'])
                                            worksheet.write(row, 21, ' ', cell_format['content_def'])
                                            worksheet.write(row, 23, ' ', cell_format['content_def'])
                                            worksheet.write(row, 25, int(data['13']) - 43, cell_format['content_def'])
                                            worksheet.write(row, 27, int(data['13']) - 43, cell_format['content_def'])
                                            worksheet.write(row, 29, ' ', cell_format['content_def'])
                                            worksheet.write(row, 31, ' ', cell_format['content_def'])
                                        else :
                                            worksheet.write(row, 13, ' ', cell_format['content_def'])
                                            worksheet.write(row, 15, ' ', cell_format['content_def'])
                                            worksheet.write(row, 17, ' ', cell_format['content_def'])
                                            worksheet.write(row, 19, ' ', cell_format['content_def'])
                                            worksheet.write(row, 21, ' ', cell_format['content_def'])
                                            worksheet.write(row, 23, ' ', cell_format['content_def'])
                                            worksheet.write(row, 25, int(data['13']) - 44, cell_format['content_def'])
                                            worksheet.write(row, 27, int(data['13']) - 44, cell_format['content_def'])
                                            worksheet.write(row, 29, ' ', cell_format['content_def'])
                                            worksheet.write(row, 31, ' ', cell_format['content_def'])

                                    else :
                                        worksheet.write(row, 13, ' ', cell_format['content_def'])
                                        worksheet.write(row, 15, ' ', cell_format['content_def'])
                                        worksheet.write(row, 17, ' ', cell_format['content_def'])
                                        worksheet.write(row, 19, ' ', cell_format['content_def'])
                                        worksheet.write(row, 21, ' ', cell_format['content_def'])
                                        worksheet.write(row, 23, ' ', cell_format['content_def'])
                                        worksheet.write(row, 25, int(data['13']) - 43, cell_format['content_def'])
                                        worksheet.write(row, 27, int(data['13']) - 43, cell_format['content_def'])
                                        worksheet.write(row, 29, ' ', cell_format['content_def'])
                                        worksheet.write(row, 31, ' ', cell_format['content_def'])
                                    
                                else :
                                    worksheet.write(row, 13, ' ', cell_format['content_def'])
                                    worksheet.write(row, 15, ' ', cell_format['content_def'])
                                    worksheet.write(row, 17, ' ', cell_format['content_def'])
                                    worksheet.write(row, 19, ' ', cell_format['content_def'])
                                    worksheet.write(row, 21, ' ', cell_format['content_def'])
                                    worksheet.write(row, 23, ' ', cell_format['content_def'])
                                    worksheet.write(row, 25, ' ', cell_format['content_def'])
                                    worksheet.write(row, 27, ' ', cell_format['content_def'])
                                    worksheet.write(row, 29, int(data['13']) - 47, cell_format['content_def'])
                                    worksheet.write(row, 31, int(data['13']) - 47, cell_format['content_def'])

                            elif (int(data['13']) > 39 and int(data['13']) < 45) :
                                if ("Oct" in bul) :
                                    if re.search("10 Oct", bul) or re.search("11 Oct", bul) or re.search("12 Oct", bul) or re.search("13 Oct", bul) or re.search("14 Oct", bul) :
                                        worksheet.write(row, 13, ' ', cell_format['content_def'])
                                        worksheet.write(row, 15, ' ', cell_format['content_def'])
                                        worksheet.write(row, 17, ' ', cell_format['content_def'])
                                        worksheet.write(row, 19, ' ', cell_format['content_def'])
                                        worksheet.write(row, 21, int(data['13']) - 39, cell_format['content_def'])
                                        worksheet.write(row, 23, int(data['13']) - 39, cell_format['content_def'])
                                        worksheet.write(row, 25, ' ', cell_format['content_def'])
                                        worksheet.write(row, 27, ' ', cell_format['content_def'])
                                        worksheet.write(row, 29, ' ', cell_format['content_def'])
                                        worksheet.write(row, 31, ' ', cell_format['content_def'])

                                    elif (int(data['13']) == 40) :
                                        if ("8" in bul or "9" in bul) :
                                            worksheet.write(row, 13, ' ', cell_format['content_def'])
                                            worksheet.write(row, 15, ' ', cell_format['content_def'])
                                            worksheet.write(row, 17, ' ', cell_format['content_def'])
                                            worksheet.write(row, 19, ' ', cell_format['content_def'])
                                            worksheet.write(row, 21, int(data['13']) - 38, cell_format['content_def'])
                                            worksheet.write(row, 23, int(data['13']) - 38, cell_format['content_def'])
                                            worksheet.write(row, 25, ' ', cell_format['content_def'])
                                            worksheet.write(row, 27, ' ', cell_format['content_def'])
                                            worksheet.write(row, 29, ' ', cell_format['content_def'])
                                            worksheet.write(row, 31, ' ', cell_format['content_def'])
                                        
                                        else :
                                            worksheet.write(row, 13, ' ', cell_format['content_def'])
                                            worksheet.write(row, 15, ' ', cell_format['content_def'])
                                            worksheet.write(row, 17, ' ', cell_format['content_def'])
                                            worksheet.write(row, 19, ' ', cell_format['content_def'])
                                            worksheet.write(row, 21, int(data['13']) - 39, cell_format['content_def'])
                                            worksheet.write(row, 23, int(data['13']) - 39, cell_format['content_def'])
                                            worksheet.write(row, 25, ' ', cell_format['content_def'])
                                            worksheet.write(row, 27, ' ', cell_format['content_def'])
                                            worksheet.write(row, 29, ' ', cell_format['content_def'])
                                            worksheet.write(row, 31, ' ', cell_format['content_def'])
                                    elif ("22" in bul or "23" in bul or "24" in bul or ("25" in bul and "20" not in bul) or "26" in bul or "27" in bul or "28" in bul) :
                                        if ("17" in bul or "18 Oct" in bul or "19 Oct" in bul or "20 Oct" in bul or "21 Oct" in bul or "24 Oct" in bul or "25 Oct" in bul or "26 Oct" in bul or "27 Oct" in bul or "28 Oct" in bul or "31 Oct" in bul) :
                                            worksheet.write(row, 13, ' ', cell_format['content_def'])
                                            worksheet.write(row, 15, ' ', cell_format['content_def'])
                                            worksheet.write(row, 17, ' ', cell_format['content_def'])
                                            worksheet.write(row, 19, ' ', cell_format['content_def'])
                                            worksheet.write(row, 21, int(data['13']) - 39, cell_format['content_def'])
                                            worksheet.write(row, 23, int(data['13']) - 39, cell_format['content_def'])
                                            worksheet.write(row, 25, ' ', cell_format['content_def'])
                                            worksheet.write(row, 27, ' ', cell_format['content_def'])
                                            worksheet.write(row, 29, ' ', cell_format['content_def'])
                                            worksheet.write(row, 31, ' ', cell_format['content_def'])
                                        else :
                                            worksheet.write(row, 13, ' ', cell_format['content_def'])
                                            worksheet.write(row, 15, ' ', cell_format['content_def'])
                                            worksheet.write(row, 17, ' ', cell_format['content_def'])
                                            worksheet.write(row, 19, ' ', cell_format['content_def'])
                                            worksheet.write(row, 21, int(data['13']) - 38, cell_format['content_def'])
                                            worksheet.write(row, 23, int(data['13']) - 38, cell_format['content_def'])
                                            worksheet.write(row, 25, ' ', cell_format['content_def'])
                                            worksheet.write(row, 27, ' ', cell_format['content_def'])
                                            worksheet.write(row, 29, ' ', cell_format['content_def'])
                                            worksheet.write(row, 31, ' ', cell_format['content_def'])

                                    elif (int(data['13']) == 44) :
                                        worksheet.write(row, 13, ' ', cell_format['content_def'])
                                        worksheet.write(row, 15, ' ', cell_format['content_def'])
                                        worksheet.write(row, 17, ' ', cell_format['content_def'])
                                        worksheet.write(row, 19, ' ', cell_format['content_def'])
                                        worksheet.write(row, 21, int(data['13']) - 39, cell_format['content_def'])
                                        worksheet.write(row, 23, int(data['13']) - 39, cell_format['content_def'])
                                        worksheet.write(row, 25, ' ', cell_format['content_def'])
                                        worksheet.write(row, 27, ' ', cell_format['content_def'])
                                        worksheet.write(row, 29, ' ', cell_format['content_def'])
                                        worksheet.write(row, 31, ' ', cell_format['content_def'])

                                    else :
                                        worksheet.write(row, 13, ' ', cell_format['content_def'])
                                        worksheet.write(row, 15, ' ', cell_format['content_def'])
                                        worksheet.write(row, 17, ' ', cell_format['content_def'])
                                        worksheet.write(row, 19, ' ', cell_format['content_def'])
                                        worksheet.write(row, 21, int(data['13']) - 38, cell_format['content_def'])
                                        worksheet.write(row, 23, int(data['13']) - 38, cell_format['content_def'])
                                        worksheet.write(row, 25, ' ', cell_format['content_def'])
                                        worksheet.write(row, 27, ' ', cell_format['content_def'])
                                        worksheet.write(row, 29, ' ', cell_format['content_def'])
                                        worksheet.write(row, 31, ' ', cell_format['content_def'])

                                else :
                                    worksheet.write(row, 13, ' ', cell_format['content_def'])
                                    worksheet.write(row, 15, ' ', cell_format['content_def'])
                                    worksheet.write(row, 17, ' ', cell_format['content_def'])
                                    worksheet.write(row, 19, ' ', cell_format['content_def'])
                                    worksheet.write(row, 21, ' ', cell_format['content_def'])
                                    worksheet.write(row, 23, ' ', cell_format['content_def'])
                                    worksheet.write(row, 25, int(data['13']) - 43, cell_format['content_def'])
                                    worksheet.write(row, 27, int(data['13']) - 43, cell_format['content_def'])
                                    worksheet.write(row, 29, ' ', cell_format['content_def'])
                                    worksheet.write(row, 31, ' ', cell_format['content_def'])

                            elif (int(data['13']) > 35 and int(data['13']) < 40) :
                                if ("Sep" in bul) :
                                    if re.search("05 Sep", bul) or re.search("06 Sep", bul) or re.search("07 Sep", bul) or re.search("12 Sep", bul) or re.search("13 Sep", bul) or re.search("14 Sep", bul) or re.search("26 Sep", bul) or re.search("27 Sep", bul) or re.search("28 Sep", bul) :
                                        worksheet.write(row, 13, ' ', cell_format['content_def'])
                                        worksheet.write(row, 15, ' ', cell_format['content_def'])
                                        worksheet.write(row, 17, int(data['13']) - 35, cell_format['content_def'])
                                        worksheet.write(row, 19, int(data['13']) - 35, cell_format['content_def'])
                                        worksheet.write(row, 21, ' ', cell_format['content_def'])
                                        worksheet.write(row, 23, ' ', cell_format['content_def'])
                                        worksheet.write(row, 25, ' ', cell_format['content_def'])
                                        worksheet.write(row, 27, ' ', cell_format['content_def'])
                                        worksheet.write(row, 29, ' ', cell_format['content_def'])
                                        worksheet.write(row, 31, ' ', cell_format['content_def'])

                                    elif ("22" in bul or "23" in bul or "24" in bul or ("25" in bul and "20" not in bul) or "26" in bul or "27" in bul or "28" in bul) :
                                        if ("19 Sep" in bul or "20 Sep" in bul or "21" in bul) :
                                            worksheet.write(row, 13, ' ', cell_format['content_def'])
                                            worksheet.write(row, 15, ' ', cell_format['content_def'])
                                            worksheet.write(row, 17, int(data['13']) - 35, cell_format['content_def'])
                                            worksheet.write(row, 19, int(data['13']) - 35, cell_format['content_def'])
                                            worksheet.write(row, 21, ' ', cell_format['content_def'])
                                            worksheet.write(row, 23, ' ', cell_format['content_def'])
                                            worksheet.write(row, 25, ' ', cell_format['content_def'])
                                            worksheet.write(row, 27, ' ', cell_format['content_def'])
                                            worksheet.write(row, 29, ' ', cell_format['content_def'])
                                            worksheet.write(row, 31, ' ', cell_format['content_def'])
                                        else :
                                            worksheet.write(row, 13, ' ', cell_format['content_def'])
                                            worksheet.write(row, 15, ' ', cell_format['content_def'])
                                            worksheet.write(row, 17, int(data['13']) - 34, cell_format['content_def'])
                                            worksheet.write(row, 19, int(data['13']) - 34, cell_format['content_def'])
                                            worksheet.write(row, 21, ' ', cell_format['content_def'])
                                            worksheet.write(row, 23, ' ', cell_format['content_def'])
                                            worksheet.write(row, 25, ' ', cell_format['content_def'])
                                            worksheet.write(row, 27, ' ', cell_format['content_def'])
                                            worksheet.write(row, 29, ' ', cell_format['content_def'])
                                            worksheet.write(row, 31, ' ', cell_format['content_def'])

                                    else :
                                        worksheet.write(row, 13, ' ', cell_format['content_def'])
                                        worksheet.write(row, 15, ' ', cell_format['content_def'])
                                        worksheet.write(row, 17, int(data['13']) - 34, cell_format['content_def'])
                                        worksheet.write(row, 19, int(data['13']) - 34, cell_format['content_def'])
                                        worksheet.write(row, 21, ' ', cell_format['content_def'])
                                        worksheet.write(row, 23, ' ', cell_format['content_def'])
                                        worksheet.write(row, 25, ' ', cell_format['content_def'])
                                        worksheet.write(row, 27, ' ', cell_format['content_def'])
                                        worksheet.write(row, 29, ' ', cell_format['content_def'])
                                        worksheet.write(row, 31, ' ', cell_format['content_def'])

                                else :
                                    worksheet.write(row, 13, ' ', cell_format['content_def'])
                                    worksheet.write(row, 15, ' ', cell_format['content_def'])
                                    worksheet.write(row, 17, ' ', cell_format['content_def'])
                                    worksheet.write(row, 19, ' ', cell_format['content_def'])
                                    worksheet.write(row, 21, int(data['13']) - 38, cell_format['content_def'])
                                    worksheet.write(row, 23, int(data['13']) - 38, cell_format['content_def'])
                                    worksheet.write(row, 25, ' ', cell_format['content_def'])
                                    worksheet.write(row, 27, ' ', cell_format['content_def'])
                                    worksheet.write(row, 29, ' ', cell_format['content_def'])
                                    worksheet.write(row, 31, ' ', cell_format['content_def'])

                            else :
                                if ("Aug" in bul) :
                                    worksheet.write(row, 13, int(data['13']) - 30, cell_format['content_def'])
                                    worksheet.write(row, 15, int(data['13']) - 30, cell_format['content_def'])
                                    worksheet.write(row, 17, ' ', cell_format['content_def'])
                                    worksheet.write(row, 19, ' ', cell_format['content_def'])
                                    worksheet.write(row, 21, ' ', cell_format['content_def'])
                                    worksheet.write(row, 23, ' ', cell_format['content_def'])
                                    worksheet.write(row, 25, ' ', cell_format['content_def'])
                                    worksheet.write(row, 27, ' ', cell_format['content_def'])
                                    worksheet.write(row, 29, ' ', cell_format['content_def'])
                                    worksheet.write(row, 31, ' ', cell_format['content_def'])

                                elif ("Sep" in bul) :
                                    worksheet.write(row, 13, ' ', cell_format['content_def'])
                                    worksheet.write(row, 15, ' ', cell_format['content_def'])
                                    worksheet.write(row, 17, int(data['13']) - 34, cell_format['content_def'])
                                    worksheet.write(row, 19, int(data['13']) - 34, cell_format['content_def'])
                                    worksheet.write(row, 21, ' ', cell_format['content_def'])
                                    worksheet.write(row, 23, ' ', cell_format['content_def'])
                                    worksheet.write(row, 25, ' ', cell_format['content_def'])
                                    worksheet.write(row, 27, ' ', cell_format['content_def'])
                                    worksheet.write(row, 29, ' ', cell_format['content_def'])
                                    worksheet.write(row, 31, ' ', cell_format['content_def'])

                                else :
                                    worksheet.write(row, 13, ' ', cell_format['content_def'])
                                    worksheet.write(row, 15, ' ', cell_format['content_def'])
                                    worksheet.write(row, 17, ' ', cell_format['content_def'])
                                    worksheet.write(row, 19, ' ', cell_format['content_def'])
                                    worksheet.write(row, 21, ' ', cell_format['content_def'])
                                    worksheet.write(row, 23, ' ', cell_format['content_def'])
                                    worksheet.write(row, 25, ' ', cell_format['content_def'])
                                    worksheet.write(row, 27, ' ', cell_format['content_def'])
                                    worksheet.write(row, 29, ' ', cell_format['content_def'])
                                    worksheet.write(row, 31, ' ', cell_format['content_def'])
                                    worksheet.write(row, 32, ' ', cell_format['content_def'])   

                            if (data['14'] == None) :
                                worksheet.write(row, 14, ' ', cell_format['content_def'])
                            else :
                                if ("Aug" in bul) :
                                    worksheet.write(row, 14, data['14'], cell_format['content_right'])
                                    worksheet.write(row, 16, ' ', cell_format['content_right'])
                                    worksheet.write(row, 18, ' ', cell_format['content_def'])
                                    worksheet.write(row, 20, ' ', cell_format['content_def'])
                                    worksheet.write(row, 22, ' ', cell_format['content_def'])
                                    worksheet.write(row, 24, ' ', cell_format['content_def'])
                                    worksheet.write(row, 26, ' ', cell_format['content_def'])
                                    worksheet.write(row, 28, ' ', cell_format['content_def'])
                                    worksheet.write(row, 30, ' ', cell_format['content_def'])
                                    worksheet.write(row, 32, ' ', cell_format['content_def'])       
                                    palas += data['14']
                                elif ("Sep" in bul) :
                                    worksheet.write(row, 14, ' ', cell_format['content_def'])
                                    worksheet.write(row, 16, ' ', cell_format['content_def'])
                                    worksheet.write(row, 18, data['14'], cell_format['content_right'])
                                    worksheet.write(row, 20, ' ', cell_format['content_def'])
                                    worksheet.write(row, 22, ' ', cell_format['content_def'])
                                    worksheet.write(row, 24, ' ', cell_format['content_def'])
                                    worksheet.write(row, 26, ' ', cell_format['content_def'])
                                    worksheet.write(row, 28, ' ', cell_format['content_def'])
                                    worksheet.write(row, 30, ' ', cell_format['content_def'])
                                    worksheet.write(row, 32, ' ', cell_format['content_def'])
                                    delas += data['14']
                                elif ("Oct" in bul) :
                                    worksheet.write(row, 14, ' ', cell_format['content_def'])
                                    worksheet.write(row, 16, ' ', cell_format['content_def'])
                                    worksheet.write(row, 18, ' ', cell_format['content_def'])
                                    worksheet.write(row, 20, ' ', cell_format['content_def'])
                                    worksheet.write(row, 22, data['14'], cell_format['content_right'])
                                    worksheet.write(row, 24, ' ', cell_format['content_def'])
                                    worksheet.write(row, 26, ' ', cell_format['content_def'])
                                    worksheet.write(row, 28, ' ', cell_format['content_def'])
                                    worksheet.write(row, 30, ' ', cell_format['content_def'])
                                    worksheet.write(row, 32, ' ', cell_format['content_def'])
                                    dudu += data['14']
                                elif ("Nov" in bul) :
                                    worksheet.write(row, 14, ' ', cell_format['content_def'])
                                    worksheet.write(row, 16, ' ', cell_format['content_def'])
                                    worksheet.write(row, 18, ' ', cell_format['content_def'])
                                    worksheet.write(row, 20, ' ', cell_format['content_def'])
                                    worksheet.write(row, 22, ' ', cell_format['content_def'])
                                    worksheet.write(row, 24, ' ', cell_format['content_def'])
                                    worksheet.write(row, 26, data['14'], cell_format['content_right'])
                                    worksheet.write(row, 28, ' ', cell_format['content_def'])
                                    worksheet.write(row, 30, ' ', cell_format['content_def'])
                                    worksheet.write(row, 32, ' ', cell_format['content_def'])
                                    dunam += data['14']
                                elif ("Dec" in bul) :
                                    worksheet.write(row, 14, ' ', cell_format['content_def'])
                                    worksheet.write(row, 16, ' ', cell_format['content_def'])
                                    worksheet.write(row, 18, ' ', cell_format['content_def'])
                                    worksheet.write(row, 20, ' ', cell_format['content_def'])
                                    worksheet.write(row, 22, ' ', cell_format['content_def'])
                                    worksheet.write(row, 24, ' ', cell_format['content_def'])
                                    worksheet.write(row, 26, ' ', cell_format['content_def'])
                                    worksheet.write(row, 28, ' ', cell_format['content_def'])
                                    worksheet.write(row, 30, data['14'], cell_format['content_right'])
                                    worksheet.write(row, 32, ' ', cell_format['content_def'])
                                    tiluh += data['14']
                            
                        else :
                            if (int(data['13']) > 9 and int(data['13']) < 44) :
                                if int(data['13']) == 10 or re.search("13 Mar", bul) or re.search("14 Mar", bul) or re.search("20 Mar", bul) or re.search("21 Mar", bul) or re.search("27 Mar", bul) or re.search("28 Mar", bul) :
                                    if re.search("08 Mar", bul) or re.search("09 Mar", bul) or re.search("10 Mar", bul) or re.search("11 Mar", bul) or re.search("12 Mar", bul) :
                                        worksheet.write(row, 13, ' ', cell_format['content_def'])
                                        worksheet.write(row, 15, ' ', cell_format['content_def'])
                                        worksheet.write(row, 17, ' ', cell_format['content_def'])
                                        worksheet.write(row, 19, ' ', cell_format['content_def'])
                                        worksheet.write(row, 21, ' ', cell_format['content_def'])
                                        worksheet.write(row, 23, ' ', cell_format['content_def'])
                                        worksheet.write(row, 25, ' ', cell_format['content_def'])
                                        worksheet.write(row, 27, ' ', cell_format['content_def'])
                                        worksheet.write(row, 29, int(data['13']) - 8, cell_format['content_def'])
                                        worksheet.write(row, 31, int(data['13']) - 8, cell_format['content_def'])
                                    else :
                                        worksheet.write(row, 13, ' ', cell_format['content_def'])
                                        worksheet.write(row, 15, ' ', cell_format['content_def'])
                                        worksheet.write(row, 17, ' ', cell_format['content_def'])
                                        worksheet.write(row, 19, ' ', cell_format['content_def'])
                                        worksheet.write(row, 21, ' ', cell_format['content_def'])
                                        worksheet.write(row, 23, ' ', cell_format['content_def'])
                                        worksheet.write(row, 25, ' ', cell_format['content_def'])
                                        worksheet.write(row, 27, ' ', cell_format['content_def'])
                                        worksheet.write(row, 29, int(data['13']) - 9, cell_format['content_def'])
                                        worksheet.write(row, 31, int(data['13']) - 9, cell_format['content_def'])

                                else :
                                    worksheet.write(row, 13, ' ', cell_format['content_def'])
                                    worksheet.write(row, 15, ' ', cell_format['content_def'])
                                    worksheet.write(row, 17, ' ', cell_format['content_def'])
                                    worksheet.write(row, 19, ' ', cell_format['content_def'])
                                    worksheet.write(row, 21, ' ', cell_format['content_def'])
                                    worksheet.write(row, 23, ' ', cell_format['content_def'])
                                    worksheet.write(row, 25, ' ', cell_format['content_def'])
                                    worksheet.write(row, 27, ' ', cell_format['content_def'])
                                    worksheet.write(row, 29, int(data['13']) - 8, cell_format['content_def'])
                                    worksheet.write(row, 31, int(data['13']) - 8, cell_format['content_def'])

                            elif (int(data['13']) > 5 and int(data['13']) < 10) :
                                if ("Feb" in bul) :
                                    if re.search("06 Feb", bul) or re.search("07 Feb", bul) or re.search("13 Feb", bul) or re.search("14 Feb", bul) or re.search("20 Feb", bul) or re.search("21 Feb", bul) or re.search("27 Feb", bul) or re.search("28 Feb", bul) :
                                        worksheet.write(row, 13, ' ', cell_format['content_def'])
                                        worksheet.write(row, 15, ' ', cell_format['content_def'])
                                        worksheet.write(row, 17, ' ', cell_format['content_def'])
                                        worksheet.write(row, 19, ' ', cell_format['content_def'])
                                        worksheet.write(row, 21, ' ', cell_format['content_def'])
                                        worksheet.write(row, 23, ' ', cell_format['content_def'])
                                        worksheet.write(row, 25, int(data['13']) - 5, cell_format['content_def'])
                                        worksheet.write(row, 27, int(data['13']) - 5, cell_format['content_def'])
                                        worksheet.write(row, 29, ' ', cell_format['content_def'])
                                        worksheet.write(row, 31, ' ', cell_format['content_def'])
                                    else :
                                        worksheet.write(row, 13, ' ', cell_format['content_def'])
                                        worksheet.write(row, 15, ' ', cell_format['content_def'])
                                        worksheet.write(row, 17, ' ', cell_format['content_def'])
                                        worksheet.write(row, 19, ' ', cell_format['content_def'])
                                        worksheet.write(row, 21, ' ', cell_format['content_def'])
                                        worksheet.write(row, 23, ' ', cell_format['content_def'])
                                        worksheet.write(row, 25, int(data['13']) - 4, cell_format['content_def'])
                                        worksheet.write(row, 27, int(data['13']) - 4, cell_format['content_def'])
                                        worksheet.write(row, 29, ' ', cell_format['content_def'])
                                        worksheet.write(row, 31, ' ', cell_format['content_def'])

                                else :
                                    worksheet.write(row, 13, ' ', cell_format['content_def'])
                                    worksheet.write(row, 15, ' ', cell_format['content_def'])
                                    worksheet.write(row, 17, ' ', cell_format['content_def'])
                                    worksheet.write(row, 19, ' ', cell_format['content_def'])
                                    worksheet.write(row, 21, ' ', cell_format['content_def'])
                                    worksheet.write(row, 23, ' ', cell_format['content_def'])
                                    worksheet.write(row, 25, ' ', cell_format['content_def'])
                                    worksheet.write(row, 27, ' ', cell_format['content_def'])
                                    worksheet.write(row, 29, int(data['13']) - 8, cell_format['content_def'])
                                    worksheet.write(row, 31, int(data['13']) - 8, cell_format['content_def'])

                            elif ((int(data['13']) > 0 and int(data['13']) < 6)) :
                                if ("Jan" in bul) :
                                    if re.search("08 Jan", bul) or re.search("15 Jan", bul) or re.search("22 Jan", bul) or re.search("29 Jan", bul) :
                                        worksheet.write(row, 13, ' ', cell_format['content_def'])
                                        worksheet.write(row, 15, ' ', cell_format['content_def'])
                                        worksheet.write(row, 17, ' ', cell_format['content_def'])
                                        worksheet.write(row, 19, ' ', cell_format['content_def'])
                                        worksheet.write(row, 21, int(data['13']) + 1, cell_format['content_def'])
                                        worksheet.write(row, 23, int(data['13']) + 1, cell_format['content_def'])
                                        worksheet.write(row, 25, ' ', cell_format['content_def'])
                                        worksheet.write(row, 27, ' ', cell_format['content_def'])
                                        worksheet.write(row, 29, ' ', cell_format['content_def'])
                                        worksheet.write(row, 31, ' ', cell_format['content_def'])

                                    else :
                                        worksheet.write(row, 13, ' ', cell_format['content_def'])
                                        worksheet.write(row, 15, ' ', cell_format['content_def'])
                                        worksheet.write(row, 17, ' ', cell_format['content_def'])
                                        worksheet.write(row, 19, ' ', cell_format['content_def'])
                                        worksheet.write(row, 21, int(data['13']), cell_format['content_def'])
                                        worksheet.write(row, 23, int(data['13']), cell_format['content_def'])
                                        worksheet.write(row, 25, ' ', cell_format['content_def'])
                                        worksheet.write(row, 27, ' ', cell_format['content_def'])
                                        worksheet.write(row, 29, ' ', cell_format['content_def'])
                                        worksheet.write(row, 31, ' ', cell_format['content_def'])

                                else :
                                    worksheet.write(row, 13, ' ', cell_format['content_def'])
                                    worksheet.write(row, 15, ' ', cell_format['content_def'])
                                    worksheet.write(row, 17, ' ', cell_format['content_def'])
                                    worksheet.write(row, 19, ' ', cell_format['content_def'])
                                    worksheet.write(row, 21, ' ', cell_format['content_def'])
                                    worksheet.write(row, 23, ' ', cell_format['content_def'])
                                    worksheet.write(row, 25, int(data['13']) - 4, cell_format['content_def'])
                                    worksheet.write(row, 27, int(data['13']) - 4, cell_format['content_def'])
                                    worksheet.write(row, 29, ' ', cell_format['content_def'])
                                    worksheet.write(row, 31, ' ', cell_format['content_def'])

                            elif (int(data['13']) > 49 and int(data['13']) < 53) :
                                if ("Dec" in bul) :
                                    if re.search("12 Dec", bul) or re.search("13 Dec", bul) or re.search("14 Dec", bul) or re.search("19 Dec", bul) or re.search("20 Dec", bul) or re.search("21 Dec", bul) or re.search("26 Dec", bul) or re.search("27 Dec", bul) or re.search("28 Dec", bul) :
                                        worksheet.write(row, 13, ' ', cell_format['content_def'])
                                        worksheet.write(row, 15, ' ', cell_format['content_def'])
                                        worksheet.write(row, 17, int(data['13']) - 48, cell_format['content_def'])
                                        worksheet.write(row, 19, int(data['13']) - 48, cell_format['content_def'])
                                        worksheet.write(row, 21, ' ', cell_format['content_def'])
                                        worksheet.write(row, 23, ' ', cell_format['content_def'])
                                        worksheet.write(row, 25, ' ', cell_format['content_def'])
                                        worksheet.write(row, 27, ' ', cell_format['content_def'])
                                        worksheet.write(row, 29, ' ', cell_format['content_def'])
                                        worksheet.write(row, 31, ' ', cell_format['content_def'])
                                    else :
                                        worksheet.write(row, 13, ' ', cell_format['content_def'])
                                        worksheet.write(row, 15, ' ', cell_format['content_def'])
                                        worksheet.write(row, 17, int(data['13']) - 47, cell_format['content_def'])
                                        worksheet.write(row, 19, int(data['13']) - 47, cell_format['content_def'])
                                        worksheet.write(row, 21, ' ', cell_format['content_def'])
                                        worksheet.write(row, 23, ' ', cell_format['content_def'])
                                        worksheet.write(row, 25, ' ', cell_format['content_def'])
                                        worksheet.write(row, 27, ' ', cell_format['content_def'])
                                        worksheet.write(row, 29, ' ', cell_format['content_def'])
                                        worksheet.write(row, 31, ' ', cell_format['content_def'])

                                else :
                                    worksheet.write(row, 13, ' ', cell_format['content_def'])
                                    worksheet.write(row, 15, ' ', cell_format['content_def'])
                                    worksheet.write(row, 17, ' ', cell_format['content_def'])
                                    worksheet.write(row, 19, ' ', cell_format['content_def'])
                                    worksheet.write(row, 21, int(data['13']) - 51, cell_format['content_def'])
                                    worksheet.write(row, 23, int(data['13']) - 51, cell_format['content_def'])
                                    worksheet.write(row, 25, ' ', cell_format['content_def'])
                                    worksheet.write(row, 27, ' ', cell_format['content_def'])
                                    worksheet.write(row, 29, ' ', cell_format['content_def'])
                                    worksheet.write(row, 31, ' ', cell_format['content_def'])

                            else :
                                if ("Nov" in bul) :
                                    if re.search("07 Nov", bul) or re.search("14 Nov", bul) or re.search("21 Nov", bul) or re.search("28 Nov", bul) :
                                        worksheet.write(row, 13, int(data['13']) - 44, cell_format['content_def'])
                                        worksheet.write(row, 15, int(data['13']) - 44, cell_format['content_def'])
                                        worksheet.write(row, 17, ' ', cell_format['content_def'])
                                        worksheet.write(row, 19, ' ', cell_format['content_def'])
                                        worksheet.write(row, 21, ' ', cell_format['content_def'])
                                        worksheet.write(row, 23, ' ', cell_format['content_def'])
                                        worksheet.write(row, 25, ' ', cell_format['content_def'])
                                        worksheet.write(row, 27, ' ', cell_format['content_def'])
                                        worksheet.write(row, 29, ' ', cell_format['content_def'])
                                        worksheet.write(row, 31, ' ', cell_format['content_def'])
                                    else :
                                        worksheet.write(row, 13, int(data['13']) - 43, cell_format['content_def'])
                                        worksheet.write(row, 15, int(data['13']) - 43, cell_format['content_def'])
                                        worksheet.write(row, 17, ' ', cell_format['content_def'])
                                        worksheet.write(row, 19, ' ', cell_format['content_def'])
                                        worksheet.write(row, 21, ' ', cell_format['content_def'])
                                        worksheet.write(row, 23, ' ', cell_format['content_def'])
                                        worksheet.write(row, 25, ' ', cell_format['content_def'])
                                        worksheet.write(row, 27, ' ', cell_format['content_def'])
                                        worksheet.write(row, 29, ' ', cell_format['content_def'])
                                        worksheet.write(row, 31, ' ', cell_format['content_def'])

                                elif ("Dec" in bul) :
                                    if re.search("12 Dec", bul) or re.search("13 Dec", bul) or re.search("14 Dec", bul) or re.search("19 Dec", bul) or re.search("20 Dec", bul) or re.search("21 Dec", bul) or re.search("26 Dec", bul) or re.search("27 Dec", bul) or re.search("28 Dec", bul) :
                                        worksheet.write(row, 13, ' ', cell_format['content_def'])
                                        worksheet.write(row, 15, ' ', cell_format['content_def'])
                                        worksheet.write(row, 17, int(data['13']) - 48, cell_format['content_def'])
                                        worksheet.write(row, 19, int(data['13']) - 48, cell_format['content_def'])
                                        worksheet.write(row, 21, ' ', cell_format['content_def'])
                                        worksheet.write(row, 23, ' ', cell_format['content_def'])
                                        worksheet.write(row, 25, ' ', cell_format['content_def'])
                                        worksheet.write(row, 27, ' ', cell_format['content_def'])
                                        worksheet.write(row, 29, ' ', cell_format['content_def'])
                                        worksheet.write(row, 31, ' ', cell_format['content_def'])
                                    elif ("8" in bul or "9" in bul or "10" in bul or "11" in bul) :
                                        worksheet.write(row, 13, ' ', cell_format['content_def'])
                                        worksheet.write(row, 15, ' ', cell_format['content_def'])
                                        worksheet.write(row, 17, int(data['13']) - 47, cell_format['content_def'])
                                        worksheet.write(row, 19, int(data['13']) - 47, cell_format['content_def'])
                                        worksheet.write(row, 21, ' ', cell_format['content_def'])
                                        worksheet.write(row, 23, ' ', cell_format['content_def'])
                                        worksheet.write(row, 25, ' ', cell_format['content_def'])
                                        worksheet.write(row, 27, ' ', cell_format['content_def'])
                                        worksheet.write(row, 29, ' ', cell_format['content_def'])
                                        worksheet.write(row, 31, ' ', cell_format['content_def'])
                                    elif (int(data['13']) == 49) :
                                        worksheet.write(row, 13, ' ', cell_format['content_def'])
                                        worksheet.write(row, 15, ' ', cell_format['content_def'])
                                        worksheet.write(row, 17, int(data['13']) - 48, cell_format['content_def'])
                                        worksheet.write(row, 19, int(data['13']) - 48, cell_format['content_def'])
                                        worksheet.write(row, 21, ' ', cell_format['content_def'])
                                        worksheet.write(row, 23, ' ', cell_format['content_def'])
                                        worksheet.write(row, 25, ' ', cell_format['content_def'])
                                        worksheet.write(row, 27, ' ', cell_format['content_def'])
                                        worksheet.write(row, 29, ' ', cell_format['content_def'])
                                        worksheet.write(row, 31, ' ', cell_format['content_def'])
                                    else :
                                        worksheet.write(row, 13, ' ', cell_format['content_def'])
                                        worksheet.write(row, 15, ' ', cell_format['content_def'])
                                        worksheet.write(row, 17, int(data['13']) - 47, cell_format['content_def'])
                                        worksheet.write(row, 19, int(data['13']) - 47, cell_format['content_def'])
                                        worksheet.write(row, 21, ' ', cell_format['content_def'])
                                        worksheet.write(row, 23, ' ', cell_format['content_def'])
                                        worksheet.write(row, 25, ' ', cell_format['content_def'])
                                        worksheet.write(row, 27, ' ', cell_format['content_def'])
                                        worksheet.write(row, 29, ' ', cell_format['content_def'])
                                        worksheet.write(row, 31, ' ', cell_format['content_def'])

                                else :
                                    worksheet.write(row, 13, ' ', cell_format['content_def'])
                                    worksheet.write(row, 15, ' ', cell_format['content_def'])
                                    worksheet.write(row, 17, ' ', cell_format['content_def'])
                                    worksheet.write(row, 19, ' ', cell_format['content_def'])
                                    worksheet.write(row, 21, ' ', cell_format['content_def'])
                                    worksheet.write(row, 23, ' ', cell_format['content_def'])
                                    worksheet.write(row, 25, ' ', cell_format['content_def'])
                                    worksheet.write(row, 27, ' ', cell_format['content_def'])
                                    worksheet.write(row, 29, ' ', cell_format['content_def'])
                                    worksheet.write(row, 31, ' ', cell_format['content_def'])
                                    worksheet.write(row, 32, ' ', cell_format['content_def'])   

                            if (data['14'] == None) :
                                worksheet.write(row, 14, ' ', cell_format['content_def'])
                            else :
                                if ("Nov" in bul) :
                                    worksheet.write(row, 14, data['14'], cell_format['content_right'])
                                    worksheet.write(row, 16, ' ', cell_format['content_right'])
                                    worksheet.write(row, 18, ' ', cell_format['content_def'])
                                    worksheet.write(row, 20, ' ', cell_format['content_def'])
                                    worksheet.write(row, 22, ' ', cell_format['content_def'])
                                    worksheet.write(row, 24, ' ', cell_format['content_def'])
                                    worksheet.write(row, 26, ' ', cell_format['content_def'])
                                    worksheet.write(row, 28, ' ', cell_format['content_def'])
                                    worksheet.write(row, 30, ' ', cell_format['content_def'])
                                    worksheet.write(row, 32, ' ', cell_format['content_def'])       
                                    palas += data['14']
                                elif ("Dec" in bul) :
                                    worksheet.write(row, 14, ' ', cell_format['content_def'])
                                    worksheet.write(row, 16, ' ', cell_format['content_def'])
                                    worksheet.write(row, 18, data['14'], cell_format['content_right'])
                                    worksheet.write(row, 20, ' ', cell_format['content_def'])
                                    worksheet.write(row, 22, ' ', cell_format['content_def'])
                                    worksheet.write(row, 24, ' ', cell_format['content_def'])
                                    worksheet.write(row, 26, ' ', cell_format['content_def'])
                                    worksheet.write(row, 28, ' ', cell_format['content_def'])
                                    worksheet.write(row, 30, ' ', cell_format['content_def'])
                                    worksheet.write(row, 32, ' ', cell_format['content_def'])
                                    delas += data['14']
                                elif ("Jan" in bul) :
                                    worksheet.write(row, 14, ' ', cell_format['content_def'])
                                    worksheet.write(row, 16, ' ', cell_format['content_def'])
                                    worksheet.write(row, 18, ' ', cell_format['content_def'])
                                    worksheet.write(row, 20, ' ', cell_format['content_def'])
                                    worksheet.write(row, 22, data['14'], cell_format['content_right'])
                                    worksheet.write(row, 24, ' ', cell_format['content_def'])
                                    worksheet.write(row, 26, ' ', cell_format['content_def'])
                                    worksheet.write(row, 28, ' ', cell_format['content_def'])
                                    worksheet.write(row, 30, ' ', cell_format['content_def'])
                                    worksheet.write(row, 32, ' ', cell_format['content_def'])
                                    dudu += data['14']
                                elif ("Feb" in bul) :
                                    worksheet.write(row, 14, ' ', cell_format['content_def'])
                                    worksheet.write(row, 16, ' ', cell_format['content_def'])
                                    worksheet.write(row, 18, ' ', cell_format['content_def'])
                                    worksheet.write(row, 20, ' ', cell_format['content_def'])
                                    worksheet.write(row, 22, ' ', cell_format['content_def'])
                                    worksheet.write(row, 24, ' ', cell_format['content_def'])
                                    worksheet.write(row, 26, data['14'], cell_format['content_right'])
                                    worksheet.write(row, 28, ' ', cell_format['content_def'])
                                    worksheet.write(row, 30, ' ', cell_format['content_def'])
                                    worksheet.write(row, 32, ' ', cell_format['content_def'])
                                    dunam += data['14']
                                elif ("Mar" in bul) :
                                    worksheet.write(row, 14, ' ', cell_format['content_def'])
                                    worksheet.write(row, 16, ' ', cell_format['content_def'])
                                    worksheet.write(row, 18, ' ', cell_format['content_def'])
                                    worksheet.write(row, 20, ' ', cell_format['content_def'])
                                    worksheet.write(row, 22, ' ', cell_format['content_def'])
                                    worksheet.write(row, 24, ' ', cell_format['content_def'])
                                    worksheet.write(row, 26, ' ', cell_format['content_def'])
                                    worksheet.write(row, 28, ' ', cell_format['content_def'])
                                    worksheet.write(row, 30, data['14'], cell_format['content_right'])
                                    worksheet.write(row, 32, ' ', cell_format['content_def'])
                                    tiluh += data['14']
                            
                row += 1
                i += 1

            # i = 0
            # dpp = 0
            # nompo = 0
            # nomta = 0
            # suba = 0
            # hut = 0
            # palas = 0
            # delas = 0
            # dudu = 0
            # dunam = 0
            # row = 25
            # bul = 0
            # for data in contents :
            #     column = 1
            #     for key, value in data.items() :
            #         if (column == 2 or column == 7 or column == 8) :
            #             worksheet.write(row, column, value, cell_format['content_left'])
            #         # elif (column == 3) :
            #         #     if (value in daterange(start_dt, end_dt)) :
            #         #         worksheet.write(row, column, value, cell_format['content_left'])
            #         #     else :
            #         #         worksheet.write(row, column, value, cell_format['content_def'])
            #         elif (column == 5 or column == 6 or column == 10 or column == 12) :
            #             worksheet.write(row, column, value, cell_format['content_right'])
            #             if (column == 5) :
            #                 if (type(value) == 'int') :
            #                     dpp += value
            #                 else :
            #                     dpp += int(value)
            #             elif (column == 6) :
            #                 if (type(value) == 'int') :
            #                     nompo += value
            #                     hut += value
            #                 else :
            #                     nompo += int(value)
            #                     hut += int(value)
            #             elif (column == 10) :
            #                 if (value == None) :
            #                     nomta = nomta
            #                 else :
            #                     if (type(value) == 'int') :
            #                         nomta += value
            #                     else :
            #                         nomta += int(value)
            #             else :
            #                 if (value == None) :
            #                     suba = suba
            #                 else :
            #                     if (type(value) == 'int') :
            #                         suba += value
            #                         hut -= value
            #                     else :
            #                         suba += int(value)
            #                         hut -= int(value)
            #         elif (column == 11) :
            #             bul = value
            #             worksheet.write(row, column, value, cell_format['content_def'])
            #         elif (column == 13) :
            #                 if (value == None) :
            #                     o = 1
            #                     for o in range (1,17):
            #                         worksheet.write(row, column, ' ', cell_format['content_def'])
            #                         column += 1
            #                     column -= 14
            #                 else :
            #                     if (self.periode == 1) :
            #                         if (int(value) > 18 and int(value) < 24) :
            #                             o = 1
            #                             for o in range (1,9):
            #                                 if (column == 25 or column == 27) :
            #                                     p = int(value) - 18
            #                                     worksheet.write(row, column, p, cell_format['content_def'])
            #                                     column += 2
            #                                 elif (column == 29 or column == 31) :
            #                                     if ("May" in bul) :
            #                                         p = int(value) - 18
            #                                         worksheet.write(row, column - 4, p, cell_format['content_def'])
            #                                         worksheet.write(row, column, ' ', cell_format['content_def'])
            #                                         column += 2
            #                                     else :
            #                                         p = int(value) - 22
            #                                         worksheet.write(row, column, p, cell_format['content_def'])
            #                                         column += 2
            #                                 else :
            #                                     worksheet.write(row, column, ' ', cell_format['content_def'])
            #                                     column += 2
            #                             column -= 4
            #                         elif (int(value) > 13 and int(value) < 19) :
            #                             o = 1
            #                             for o in range (1,9):
            #                                 if (column == 21 or column == 23) :
            #                                     if ("Apr" not in bul) :
            #                                         worksheet.write(row, column, ' ', cell_format['content_def'])
            #                                         column += 2
            #                                     else :
            #                                         p = int(value) - 13
            #                                         worksheet.write(row, column, p, cell_format['content_def'])
            #                                         column += 2
            #                                 elif (column == 25 or column == 27) :
            #                                     if ("Apr" in bul) :
            #                                         p = int(value) - 13
            #                                         worksheet.write(row, column - 4, p, cell_format['content_def'])
            #                                         worksheet.write(row, column, ' ', cell_format['content_def'])
            #                                         column += 2
            #                                     else :
            #                                         p = int(value) - 17
            #                                         worksheet.write(row, column, p, cell_format['content_def'])
            #                                         column += 2
            #                                 else :
            #                                     if (column == 31) :
            #                                         continue
            #                                     else :
            #                                         worksheet.write(row, column, ' ', cell_format['content_def'])
            #                                         column += 2
            #                             column -= 8
            #                         elif (int(value) > 8 and int(value) < 14) :
            #                             o = 1
            #                             for o in range (1,9):
            #                                 if (column == 17 or column == 19) :
            #                                     if ("Mar" not in bul) :
            #                                         worksheet.write(row, column, ' ', cell_format['content_def'])
            #                                         column += 2
            #                                     else :
            #                                         p = int(value) - 8
            #                                         worksheet.write(row, column, p, cell_format['content_def'])
            #                                         column += 2
            #                                 elif (column == 21 or column == 23) :
            #                                     if ("Mar" in bul) :
            #                                         p = int(value) - 8
            #                                         worksheet.write(row, column - 4, p, cell_format['content_def'])
            #                                         worksheet.write(row, column, ' ', cell_format['content_def'])
            #                                         column += 2
            #                                     else :
            #                                         p = int(value) - 12
            #                                         worksheet.write(row, column, p, cell_format['content_def'])
            #                                         column += 2
            #                                 # worksheet.write(row, column - 2, ' ', cell_format['content_def'])
            #                                 # worksheet.write(row, column - 4, ' ', cell_format['content_def'])
            #                                 else :
            #                                     if (column == 31) :
            #                                         continue
            #                                     else :
            #                                         worksheet.write(row, column, ' ', cell_format['content_def'])
            #                                         column += 2
            #                             column -= 12
            #                         else :
            #                             o = 1
            #                             for o in range (1,9):
            #                                 if (column == 13 or column == 15) :
            #                                     if ("Feb" not in bul) :
            #                                         worksheet.write(row, column, ' ', cell_format['content_def'])
            #                                         column += 2
            #                                     else :
            #                                         p = int(value) - 3
            #                                         worksheet.write(row, column, p, cell_format['content_def'])
            #                                         column += 2
            #                                 elif (column == 17 or column == 19) :
            #                                     if ("Feb" in bul) :
            #                                         p = int(value) - 3
            #                                         worksheet.write(row, column - 4, p, cell_format['content_def'])
            #                                         worksheet.write(row, column, ' ', cell_format['content_def'])
            #                                         column += 2
            #                                     else :
            #                                         worksheet.write(row, column, ' ', cell_format['content_def'])
            #                                         column += 2
            #                                 else :
            #                                     worksheet.write(row, column, ' ', cell_format['content_def'])
            #                                     column += 2
            #                             column -= 16

            #                     elif (self.periode == 2) :
            #                         if (int(value) > 30 and int(value) < 36) :
            #                             o = 1
            #                             for o in range (1,9):
            #                                 if (column == 25 or column == 27) :
            #                                     if ("Aug" not in bul) :
            #                                         worksheet.write(row, column, ' ', cell_format['content_def'])
            #                                         column += 2
            #                                     else :
            #                                         p = int(value) - 30
            #                                         worksheet.write(row, column, p, cell_format['content_def'])
            #                                         column += 2
            #                                 elif (column == 29 or column == 31) :
            #                                     if ("Aug" in bul) :
            #                                         p = int(value) - 30
            #                                         worksheet.write(row, column - 4, p, cell_format['content_def'])
            #                                         worksheet.write(row, column, ' ', cell_format['content_def'])
            #                                         column += 2
            #                                     else :
            #                                         p = int(value) - 34
            #                                         worksheet.write(row, column, p, cell_format['content_def'])
            #                                         column += 2
            #                                 else :
            #                                     worksheet.write(row, column, ' ', cell_format['content_def'])
            #                                     column += 2
            #                             column -= 4
            #                         elif (int(value) > 26 and int(value) < 31) :
            #                             o = 1
            #                             for o in range (1,9):
            #                                 if (column == 21 or column == 23) :
            #                                     p = int(value) - 26
            #                                     worksheet.write(row, column, p, cell_format['content_def'])
            #                                     column += 2
            #                                 elif (column == 25 or column == 27) :
            #                                     if ("Jul" in bul) :
            #                                         p = int(value) - 26
            #                                         worksheet.write(row, column - 4, p, cell_format['content_def'])
            #                                         worksheet.write(row, column, ' ', cell_format['content_def'])
            #                                         column += 2
            #                                     elif ("Aug" in bul) :
            #                                         p = int(value) - 29
            #                                         worksheet.write(row, column, p, cell_format['content_def'])
            #                                         column += 2
            #                                     else :
            #                                         worksheet.write(row, column, ' ', cell_format['content_def'])
            #                                         column += 2
            #                                 else :
            #                                     if (column == 31) :
            #                                         continue
            #                                     else :
            #                                         worksheet.write(row, column, ' ', cell_format['content_def'])
            #                                         column += 2
            #                             column -= 8
            #                         elif (int(value) > 21 and int(value) < 27) :
            #                             o = 1
            #                             for o in range (1,9):
            #                                 if (column == 17 or column == 19) :
            #                                     if ("Jun" not in bul) :
            #                                         worksheet.write(row, column, ' ', cell_format['content_def'])
            #                                         column += 2
            #                                     else :
            #                                         p = int(value) - 21
            #                                         worksheet.write(row, column, p, cell_format['content_def'])
            #                                         column += 2
            #                                 elif (column == 21 or column == 23) :
            #                                     if ("Jun" in bul) :
            #                                         p = int(value) - 21
            #                                         worksheet.write(row, column - 4, p, cell_format['content_def'])
            #                                         worksheet.write(row, column, ' ', cell_format['content_def'])
            #                                         column += 2
            #                                     else :
            #                                         p = int(value) - 25
            #                                         worksheet.write(row, column, p, cell_format['content_def'])
            #                                         column += 2
            #                                 # worksheet.write(row, column - 2, ' ', cell_format['content_def'])
            #                                 # worksheet.write(row, column - 4, ' ', cell_format['content_def'])
            #                                 else :
            #                                     if (column == 31) :
            #                                         continue
            #                                     else :
            #                                         worksheet.write(row, column, ' ', cell_format['content_def'])
            #                                         column += 2
            #                             column -= 12
            #                         else :
            #                             o = 1
            #                             for o in range (1,9):
            #                                 if (column == 13 or column == 15) :
            #                                     if ("May" not in bul) :
            #                                         worksheet.write(row, column, ' ', cell_format['content_def'])
            #                                         column += 2
            #                                     else :
            #                                         p = int(value) - 17
            #                                         worksheet.write(row, column, p, cell_format['content_def'])
            #                                         column += 2
            #                                 elif (column == 17 or column == 19) :
            #                                     if ("May" in bul) :
            #                                         p = int(value) - 17
            #                                         worksheet.write(row, column - 4, p, cell_format['content_def'])
            #                                         worksheet.write(row, column, ' ', cell_format['content_def'])
            #                                         column += 2
            #                                     else :
            #                                         worksheet.write(row, column, ' ', cell_format['content_def'])
            #                                         column += 2
            #                                 else :
            #                                     worksheet.write(row, column, ' ', cell_format['content_def'])
            #                                     column += 2
            #                             column -= 16

            #                     elif (self.periode == 3) :
            #                         if (int(value) > 44 and int(value) < 50) :
            #                             o = 1
            #                             for o in range (1,9):
            #                                 if (column == 25 or column == 27) :
            #                                     if ("Nov" not in bul) :
            #                                         worksheet.write(row, column, ' ', cell_format['content_def'])
            #                                         column += 2
            #                                     else :
            #                                         p = int(value) - 44
            #                                         worksheet.write(row, column, p, cell_format['content_def'])
            #                                         column += 2
            #                                 elif (column == 29 or column == 31) :
            #                                     if ("Nov" in bul) :
            #                                         p = int(value) - 44
            #                                         worksheet.write(row, column - 4, p, cell_format['content_def'])
            #                                         worksheet.write(row, column, ' ', cell_format['content_def'])
            #                                         column += 2
            #                                     else :
            #                                         worksheet.write(row, column, ' ', cell_format['content_def'])
            #                                         column += 2
            #                                 else :
            #                                     worksheet.write(row, column, ' ', cell_format['content_def'])
            #                                     column += 2
            #                             column -= 4
            #                         elif (int(value) > 39 and int(value) < 45) :
            #                             o = 1
            #                             for o in range (1,9):
            #                                 if (column == 21 or column == 23) :
            #                                     if ("Oct" not in bul) :
            #                                         worksheet.write(row, column, ' ', cell_format['content_def'])
            #                                         column += 2
            #                                     else :
            #                                         p = int(value) - 39
            #                                         worksheet.write(row, column, p, cell_format['content_def'])
            #                                         column += 2
            #                                 elif (column == 25 or column == 27) :
            #                                     if ("Oct" in bul) :
            #                                         p = int(value) - 39
            #                                         worksheet.write(row, column - 4, p, cell_format['content_def'])
            #                                         worksheet.write(row, column, ' ', cell_format['content_def'])
            #                                         column += 2
            #                                     else :
            #                                         worksheet.write(row, column, ' ', cell_format['content_def'])
            #                                         column += 2
            #                                 else :
            #                                     if (column == 31) :
            #                                         continue
            #                                     else :
            #                                         worksheet.write(row, column, ' ', cell_format['content_def'])
            #                                         column += 2
            #                             column -= 8
            #                         elif (int(value) > 34 and int(value) < 40) :
            #                             o = 1
            #                             for o in range (1,9):
            #                                 if (column == 17 or column == 19) :
            #                                     if ("Sep" not in bul) :
            #                                         worksheet.write(row, column, ' ', cell_format['content_def'])
            #                                         column += 2
            #                                     else :
            #                                         p = int(value) - 34
            #                                         worksheet.write(row, column, p, cell_format['content_def'])
            #                                         column += 2
            #                                 elif (column == 21 or column == 23) :
            #                                     if ("Sep" in bul) :
            #                                         p = int(value) - 34
            #                                         worksheet.write(row, column - 4, p, cell_format['content_def'])
            #                                         worksheet.write(row, column, ' ', cell_format['content_def'])
            #                                         column += 2
            #                                     else :
            #                                         worksheet.write(row, column, ' ', cell_format['content_def'])
            #                                         column += 2
            #                                 else :
            #                                     if (column == 31) :
            #                                         continue
            #                                     else :
            #                                         worksheet.write(row, column, ' ', cell_format['content_def'])
            #                                         column += 2
            #                             column -= 12
            #                         else :
            #                             o = 1
            #                             for o in range (1,9):
            #                                 if (column == 13 or column == 15) :
            #                                     if ("Aug" not in bul) :
            #                                         worksheet.write(row, column, ' ', cell_format['content_def'])
            #                                         column += 2
            #                                     else :
            #                                         p = int(value) - 30
            #                                         worksheet.write(row, column, p, cell_format['content_def'])
            #                                         column += 2
            #                                 elif (column == 17 or column == 19) :
            #                                     if ("Aug" in bul) :
            #                                         p = int(value) - 30
            #                                         worksheet.write(row, column - 4, p, cell_format['content_def'])
            #                                         worksheet.write(row, column, ' ', cell_format['content_def'])
            #                                         column += 2
            #                                     else :
            #                                         worksheet.write(row, column, ' ', cell_format['content_def'])
            #                                         column += 2
            #                                 else :
            #                                     worksheet.write(row, column, ' ', cell_format['content_def'])
            #                                     column += 2
            #                             column -= 16

            #                     else :
            #                         if (int(value) > 3 and int(value) < 9) :
            #                             o = 1
            #                             for o in range (1,9):
            #                                 if (column == 25 or column == 27) :
            #                                     p = int(value) - 3
            #                                     worksheet.write(row, column, p, cell_format['content_def'])
            #                                     column += 2
            #                                 else :
            #                                     worksheet.write(row, column, ' ', cell_format['content_def'])
            #                                     column += 2
            #                             column -= 4
            #                         elif ((int(value) > 57 and int(value) < 60) or (int(value) > 0 and int(value) < 4)) :
            #                             if (int(value) == 58 or int(value) == 59):
            #                                 o = 1
            #                                 for o in range (1,9):
            #                                     if (column == 21 or column == 23) :
            #                                         p = int(value) - 57
            #                                         worksheet.write(row, column, p, cell_format['content_def'])
            #                                         column += 2
            #                                     else :
            #                                         if (column == 31) :
            #                                             continue
            #                                         else :
            #                                             worksheet.write(row, column, ' ', cell_format['content_def'])
            #                                             column += 2
            #                                 column -= 8
            #                             else :
            #                                 o = 1
            #                                 for o in range (1,9):
            #                                     if (column == 21 or column == 23) :
            #                                         p = int(value) + 2
            #                                         worksheet.write(row, column, p, cell_format['content_def'])
            #                                         column += 2
            #                                     else :
            #                                         if (column == 31) :
            #                                             continue
            #                                         else :
            #                                             worksheet.write(row, column, ' ', cell_format['content_def'])
            #                                             column += 2
            #                                 column -= 8
            #                         elif (int(value) > 52 and int(value) < 58) :
            #                             o = 1
            #                             for o in range (1,9):
            #                                 if (column == 17 or column == 19) :
            #                                     if ("Dec" not in bul) :
            #                                         worksheet.write(row, column, ' ', cell_format['content_def'])
            #                                         column += 2
            #                                     else :
            #                                         p = int(value) - 52
            #                                         worksheet.write(row, column, p, cell_format['content_def'])
            #                                         column += 2
            #                                 elif (column == 21 or column == 23) :
            #                                     if ("Dec" in bul) :
            #                                         p = int(value) - 52
            #                                         worksheet.write(row, column - 4, p, cell_format['content_def'])
            #                                         worksheet.write(row, column, ' ', cell_format['content_def'])
            #                                         column += 2
            #                                     else :
            #                                         worksheet.write(row, column, ' ', cell_format['content_def'])
            #                                         column += 2
            #                                 else :
            #                                     if (column == 31) :
            #                                         continue
            #                                     else :
            #                                         worksheet.write(row, column, ' ', cell_format['content_def'])
            #                                         column += 2
            #                             column -= 12
            #                         else :
            #                             o = 1
            #                             for o in range (1,9):
            #                                 if (column == 13 or column == 15) :
            #                                     if ("Nov" not in bul) :
            #                                         worksheet.write(row, column, ' ', cell_format['content_def'])
            #                                         column += 2
            #                                     else :
            #                                         p = int(value) - 49
            #                                         worksheet.write(row, column, p, cell_format['content_def'])
            #                                         column += 2
            #                                 elif (column == 17 or column == 19) :
            #                                     if ("Nov" in bul) :
            #                                         p = int(value) - 49
            #                                         worksheet.write(row, column - 4, p, cell_format['content_def'])
            #                                         worksheet.write(row, column, ' ', cell_format['content_def'])
            #                                         column += 2
            #                                     else :
            #                                         worksheet.write(row, column, ' ', cell_format['content_def'])
            #                                         column += 2
            #                                 else :
            #                                     worksheet.write(row, column, ' ', cell_format['content_def'])
            #                                     column += 2
            #                             column -= 16

            #         else :
            #             if (value == None) :
            #                 worksheet.write(row, column, ' ', cell_format['content_def'])
            #             else :
            #                 if (column == 14) :
            #                     o = 1
            #                     for o in range (1,9):
            #                         if (column == 14) :
            #                             worksheet.write(row, column, value, cell_format['content_right'])
            #                             worksheet.write(row, column + 14, ' ', cell_format['content_def'])
            #                             column += 2
            #                             palas += value
            #                         else :
            #                             worksheet.write(row, column, ' ', cell_format['content_def'])
            #                             column += 2 
            #                     column -= 14
            #                 elif (column == 18) :
            #                     o = 1
            #                     for o in range (1,7):
            #                         if (column == 18) :
            #                             worksheet.write(row, column, value, cell_format['content_right'])
            #                             worksheet.write(row, column - 2, ' ', cell_format['content_def'])
            #                             worksheet.write(row, column - 4, ' ', cell_format['content_def'])
            #                             column += 2
            #                             delas += value
            #                         else :
            #                             worksheet.write(row, column, ' ', cell_format['content_def'])
            #                             column += 2 
            #                     column -= 14
            #                 elif (column == 22) :
            #                     o = 1
            #                     for o in range (1,5):
            #                         if (column == 22) :
            #                             worksheet.write(row, column, value, cell_format['content_right'])
            #                             worksheet.write(row, column - 2, ' ', cell_format['content_def'])
            #                             worksheet.write(row, column - 4, ' ', cell_format['content_def'])
            #                             worksheet.write(row, column - 6, ' ', cell_format['content_def'])
            #                             worksheet.write(row, column - 8, ' ', cell_format['content_def'])
            #                             column += 2
            #                             dudu += value
            #                         else :
            #                             worksheet.write(row, column, ' ', cell_format['content_def'])
            #                             column += 2 
            #                     column -= 14
            #                 elif (column == 26) :
            #                     o = 1
            #                     for o in range (1,3):
            #                         if (column == 26) :
            #                             worksheet.write(row, column, value, cell_format['content_right'])
            #                             worksheet.write(row, column - 2, ' ', cell_format['content_def'])
            #                             worksheet.write(row, column - 4, ' ', cell_format['content_def'])
            #                             worksheet.write(row, column - 6, ' ', cell_format['content_def'])
            #                             worksheet.write(row, column - 8, ' ', cell_format['content_def'])
            #                             worksheet.write(row, column - 10, ' ', cell_format['content_def'])
            #                             worksheet.write(row, column - 12, ' ', cell_format['content_def'])
            #                             column += 2
            #                             dunam += value
            #                         else :
            #                             worksheet.write(row, column, ' ', cell_format['content_def'])
            #                             column += 2 
            #                     column -= 14
            #                 else :
            #                     worksheet.write(row, column, value, cell_format['content_def'])
            #         column += 1
            #     row += 1
            #     i += 1

        # wb = xw.Workbook(fp)
        # wb.sheets[0].range('C' + str(wb.sheets[0].cells.last_cell.row)).end('up').row
        # Set the autofilter.
        worksheet.autofilter('C25:AG25')

        # worksheet['F33'] = ["DPP", res[3]].sum()
        worksheet.merge_range(row, 2, row, 4, 'GRAND TOTAL', cell_format['content_left'])
        worksheet.write(row, 5, dpp, cell_format['content_right_bold'])
        worksheet.write(row, 6, nompo, cell_format['content_right_bold'])
        
        column = 13
        r = 13
        for r in range (13, 33) :
            if (column == 14 or column == 18 or column == 22 or column == 26 or column == 30) :
                if (column == 14) :
                    if(palas == 0) :
                        worksheet.write(row, column, '-', cell_format['content_def'])
                    else :
                        worksheet.write(row, 14, palas, cell_format['content_right_bold'])
                elif (column == 18) :
                    if(delas == 0) :
                        worksheet.write(row, column, '-', cell_format['content_def'])
                    else :
                        worksheet.write(row, 18, delas, cell_format['content_right_bold'])
                elif (column == 22) :
                    if(dudu == 0) :
                        worksheet.write(row, column, '-', cell_format['content_def'])
                    else :
                        worksheet.write(row, 22, dudu, cell_format['content_right_bold'])
                elif (column == 26) :
                    if(dunam == 0) :
                        worksheet.write(row, column, '-', cell_format['content_def'])
                    else :
                        worksheet.write(row, 26, dunam, cell_format['content_right_bold'])
                else :
                    if(tiluh == 0) :
                        worksheet.write(row, column, '-', cell_format['content_def'])
                    else :
                        worksheet.write(row, 30, tiluh, cell_format['content_right_bold'])
                column += 1
            else :
                worksheet.write(row, column, ' ', cell_format['content_def'])
                column += 1

        l = 7
        for l in range(7,13):
            if (l == 10) :
                worksheet.write(row, 10, nomta, cell_format['content_right_bold'])
            elif (l == 12) :
                worksheet.write(row, 12, suba, cell_format['content_right_bold'])
            else :
                worksheet.write(row, l, ' ', cell_format['content_left'])

        # A = date(2020, 10, 29)
        # Date = A.isocalendar()
        # Date = str(Date[1]-40)
  
        # worksheet.write(row + 2, 7, Date, cell_format['content_right_bold'])
        worksheet.merge_range(row + 2, 2, row + 2, 6, 'NOTE : UNTUK SUPPLIER YANG TIDAK TERCANTUM NOMINAL TAGIHANNYA, TANDANYA PO BARU TERBIT DAN BELUM DITAGIH SUPPLIER', cell_format['note'])
        worksheet.write(row + 3, 5, 'SISA HUTANG', cell_format['content_left_nb'])
        # worksheet[row,6] = '=(worksheet[row-3,6].value - worksheet[row-3,12].value)'
        # worksheet.write_formula('G48', '{=SUM(G29, G30)}')
        worksheet.write(row + 3, 6, hut, cell_format['content_right_nb'])
        # worksheet.write(row, 5, f"=SUM(F26:F{row - 1})")

        workbook.close()
        result = base64.encodestring(fp.getvalue())
        filename = 'PERIODE ' + str(self.date_start.strftime("%d %b %Y")) + ' - ' + str(self.date_end.strftime("%d %b %Y")) + ' LAPORAN RENCANA PEMBELIAN DAN PEMBAYARAN SUPPLIER.xlsx'
        self.write({'export_file':result, 'export_filename':filename})
        return {
            'name': "Export Complete, total %s records" % i,
            'type': 'ir.actions.act_window',
            'res_model': 'vit.pembelian_pembayaran_sup',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id'   : self.id,
            'views'    : [(False, 'form')],
            'target'   : 'new',
        }

