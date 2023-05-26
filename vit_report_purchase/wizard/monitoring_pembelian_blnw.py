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

class MonitoringPembelianWizard(models.TransientModel):
    _name    = 'vit.monitoring_pembelian_bln'
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

    str_bulan = fields.Char(string='Month Name', compute='get_date_start_end', store=True)
    bulan = fields.Selection([
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

    @api.depends('bulan','year')
    def get_date_start_end(self):
        for ra in self:
            current_date  = datetime.date.today()
            thn = str(ra.year)
            if ra.bulan == 1:
                ra.date_start = self.current_date.strftime(thn +'-01-01')
                ra.date_end = self.current_date.strftime(thn +'-01-31')
                ra.str_bulan = 'JANUARI'
            if ra.bulan == 2:
                ra.date_start = self.current_date.strftime(thn +'-02-01')
                ra.date_end = self.current_date.strftime(thn +'-02-28') or self.current_date.strftime(thn +'-02-29')
                ra.str_bulan = 'FEBRUARI'
            if ra.bulan == 3:
                ra.date_start = self.current_date.strftime(thn +'-03-01')
                ra.date_end = self.current_date.strftime(thn +'-03-31')
                ra.str_bulan = 'MARET'
            if ra.bulan == 4:
                ra.date_start = self.current_date.strftime(thn +'-04-01')
                ra.date_end = self.current_date.strftime(thn +'-04-30')
                ra.str_bulan = 'APRIL'
            if ra.bulan == 5:
                ra.date_start = self.current_date.strftime(thn +'-05-01')
                ra.date_end = self.current_date.strftime(thn +'-05-31')
                ra.str_bulan = 'MEI'
            if ra.bulan == 6:
                ra.date_start = self.current_date.strftime(thn +'-06-01')
                ra.date_end = self.current_date.strftime(thn +'-06-30')
                ra.str_bulan = 'JUNI'
            if ra.bulan == 7:
                ra.date_start = self.current_date.strftime(thn +'-07-01')
                ra.date_end = self.current_date.strftime(thn +'-07-31')
                ra.str_bulan = 'JULI'
            if ra.bulan == 8:
                ra.date_start = self.current_date.strftime(thn +'-08-01')
                ra.date_end = self.current_date.strftime(thn +'-08-31')
                ra.str_bulan = 'AGUSTUS'
            if ra.bulan == 9:
                ra.date_start = self.current_date.strftime(thn +'-09-01')
                ra.date_end = self.current_date.strftime(thn +'-09-30')
                ra.str_bulan = 'SEPTEMBER'
            if ra.bulan == 10:
                ra.date_start = self.current_date.strftime(thn +'-10-01')
                ra.date_end = self.current_date.strftime(thn +'-10-31')
                ra.str_bulan = 'OKTOBER'
            if ra.bulan == 11:
                ra.date_start = self.current_date.strftime(thn +'-11-01')
                ra.date_end = self.current_date.strftime(thn +'-11-30')
                ra.str_bulan = 'NOVEMBER'
            if ra.bulan == 12:
                ra.date_start = self.current_date.strftime(thn +'-12-01')
                ra.date_end = self.current_date.strftime(thn +'-12-31')
                ra.str_bulan = 'DESEMBER'

    # commercial_partner_id = fields.Many2one(comodel_name="res.partner", string="Vendor", default=lambda self: self.env.uid, track_visibility='onchange', readonly=True)

    def cell_format(self, workbook):
        cell_format = {}
        cell_format['header'] = workbook.add_format({
            'font_size': 11,
            'border': True,
            'bottom': 6,
            'top': 2,
            'align': 'center',
            'bg_color': '#D9D9D9',
            'valign': 'vcenter',
            'bold': True,
        })
        cell_format['header_lc'] = workbook.add_format({
            'font_size': 11,
            'border': True,
            'bottom': 6,
            'left': 2,
            'top': 2,
            'align': 'center',
            'bg_color': '#D9D9D9',
            'valign': 'vcenter',
            'bold': True,
        })
        cell_format['header_rc'] = workbook.add_format({
            'font_size': 11,
            'border': True,
            'bottom': 6,
            'right': 2,
            'top': 2,
            'align': 'center',
            'bg_color': '#D9D9D9',
            'valign': 'vcenter',
            'bold': True,
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
        cell_format['content_def'] = workbook.add_format({
            'font_size': 11,
            'border': True,
            'align': 'center',
            'bottom': 1,
        })
        cell_format['content_def_ki'] = workbook.add_format({
            'font_size': 11,
            'border': True,
            'align': 'center',
            'bottom': 1,
            'left': 2,
        })
        cell_format['content_left'] = workbook.add_format({
            'font_size': 11,
            'border': True,
            'align': 'left',
            'bottom': 1,
        })
        cell_format['content_left_ka'] = workbook.add_format({
            'font_size': 11,
            'border': True,
            'align': 'left',
            'bottom': 1,
            'right': 2,
        })
        cell_format['content_left_nb'] = workbook.add_format({
            'font_size': 11,
            'border': False,
            'align': 'left',
            'bottom': 1,
        })
        cell_format['content_right'] = workbook.add_format({
            'font_size': 11,
            'border': True,
            'align': 'right',
            'bottom': 1,
        })
        cell_format['content_right_nb'] = workbook.add_format({
            'font_size': 11,
            'border': False,
            'align': 'right',
            'bottom': 2,
        })
        cell_format['content_right_bold'] = workbook.add_format({
            'font_size': 11,
            'border': True,
            'align': 'right',
            'bold': True,
            'bottom': 2,
        })
        cell_format['content_hide'] = workbook.add_format({
            'font_color': '#D9D9D9',
            'bg_color': '#D9D9D9',
            'border': True,
        })
        cell_format['content_hide_ki'] = workbook.add_format({
            'font_color': '#D9D9D9',
            'bg_color': '#D9D9D9',
            'border': True,
            'left' : 2,
        })
        cell_format['info_1'] = workbook.add_format({
            'font_size': 26,
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
                "2" :"NO.PR",
                "3" :"TGL.PR",
                "4" :"NO.OR",
                "5" :"NO ITEM",
                "6" :"ITEM",
                "7" :"REQ.QTY",
                "8" :"REQ.UNIT",
                "9" :"NO.PO",
                "10":"TGL.PO",
                "11":"SUPPLIER",
                "12":"ORDER QTY",
                "13":"ORDER UNIT",
                "14":"HARGA",
                "15":"PPN (10/11%)",
                "16":"TOTAL",
                "17":"REC.QTY",
                "18":"REC.UNIT",
                "19":"NO.BTB",
                "20":"TGL.BTB",
                "21":"NO",
                "22":"NILAI",
                "23":"JT",
                "24":"TGL.BAYAR",

        }]

        # values = []
        # purchase = self.env['purchase.order'].search([('date_order','>=',self.date_start), ('date_order','<=',self.date_end)])
        # if (self.periode == 1) :
        sql = """SELECT (pr.name) as no_pr, (to_char(pr.date :: DATE, 'DD Mon YYYY')) as tgl_pr, (pog.name) as no_or, (pt.default_code) as no_item, (pt.name) as nama_item, (prl.product_qty) as req_qty, (u.name) as satuan, (po.name) as no_po, (to_char(po.date_order :: DATE, 'DD Mon YYYY')) as tgl_po, (rp.name) as supplier, (pol.product_qty) as order_qty, (u1.name) as satuan1, (pol.price_unit) as harga, (pol.price_tax) as ppn, (pol.price_total) as total, (sm.product_uom_qty) as qty_btb, (u2.name) as satuan2, (sp.name) as no_btb, (to_char(sp.date_done :: DATE, 'DD Mon YYYY')) as tgl_btb, (bill.number) as no_bill, (sum(bl.price_subtotal)) as nilai, (to_char(bill.date_due :: DATE, 'DD Mon YYYY')) as tgl_jt, (to_char(pay.payment_date :: DATE, 'DD Mon YYYY')) as tgl_byr
                FROM vit_product_request_line prl
                LEFT JOIN vit_product_request pr ON pr.id = prl.product_request_id
                LEFT JOIN purchase_requisition te ON pr.name = te.origin
                LEFT JOIN purchase_order po1 ON po1.requisition_id = te.id
                LEFT JOIN purchase_order_line pol ON prl.product_id = pol.product_id AND po1.id = pol.order_id
                LEFT JOIN purchase_order po ON pol.order_id = po.id
                LEFT JOIN stock_picking sp1 ON po.name = sp1.origin
                LEFT JOIN stock_move sm ON prl.product_id = sm.product_id AND sm.picking_id = sp1.id
                LEFT JOIN stock_picking sp ON sm.picking_id = sp.id
                LEFT JOIN account_invoice bill1 ON po.name = bill1.origin
                LEFT JOIN account_invoice_line bl ON prl.product_id = bl.product_id AND bl.invoice_id = bill1.id
                LEFT JOIN account_invoice bill ON bl.invoice_id = bill.id
                LEFT JOIN product_product pp ON prl.product_id = pp.id
                LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
                LEFT JOIN uom_uom u ON pol.product_uom = u.id
                LEFT JOIN uom_uom u1 ON prl.product_uom_id = u1.id
                LEFT JOIN uom_uom u2 ON sm.product_uom = u2.id
                LEFT JOIN vit_purchase_order_garmen pog ON po.po_id = pog.id
                LEFT JOIN account_payment pay ON pay.communication = bill.name
                LEFT JOIN res_partner rp ON po.partner_id = rp.id
                WHERE pr.date >= %s AND pr.date <= %s
                GROUP BY pr.id, prl.id, po.id, pol.id, pt.id, u.id, u1.id, u2.id, pog.id, rp.id, sp.id, sm.id, bill.id, bl.id, pay.id
                ORDER BY pr.date
                """
        self.env.cr.execute(sql, (self.date_start,self.date_end))
        result = self.env.cr.dictfetchall()
        line_ids = []
        i = 1
        for res in result:

            contents.append({
                "1" : str(i),
                "2" : res['no_pr'],
                "3" : res['tgl_pr'],
                "4" : res['no_or'],
                "5" : res['no_item'],
                "6" : res['nama_item'],
                "7" : res['req_qty'],
                "8" : res['satuan1'],
                "9" : res['no_po'],
                "10": res['tgl_po'],
                "11": res['supplier'],
                "12": res['order_qty'],
                "13": res['satuan'],
                "14": res['harga'],
                "15": res['ppn'],
                "16": res['total'],
                "17": res['qty_btb'],
                "18": res['satuan2'],
                "19": res['no_btb'],
                "20": res['tgl_btb'],
                "21": res['no_bill'],
                "22": res['nilai'],
                "23": res['tgl_jt'],
                "24": res['tgl_byr'],

            })
            i += 1
        rec[str(self.str_bulan) + ' ' + str(self.year)] = [contents]        
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
            worksheet.set_column('C:C', 32)
            worksheet.set_column('D:D', 12)
            worksheet.set_column('E:E', 16)
            worksheet.set_column('F:F', 27)
            worksheet.set_column('G:G', 55)
            worksheet.set_column('H:H', 38)
            worksheet.set_column('I:I', 12)
            worksheet.set_column('J:J', 12)
            worksheet.set_column('K:L', 16)
            worksheet.set_column('M:M', 35)
            worksheet.set_column('N:O', 12)
            worksheet.set_column('P:R', 16)
            worksheet.set_column('S:T', 12)
            worksheet.set_column('U:U', 18)
            worksheet.set_column('V:V', 16)
            worksheet.set_column('W:Z', 12)
            worksheet.set_column('AA:AA', 16)
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
            worksheet.merge_range('B17:AA17', ' ', cell_format['space'])
            worksheet.merge_range('B18:AA18', 'LAPORAN MONITORING PEMBELIAN', cell_format['info_1'])
            worksheet.merge_range('B19:AA19', ' ', cell_format['space'])
            worksheet.merge_range('B20:AA20', 'PER' + ' ' + self.str_bulan + ' / '+ str(self.year), cell_format['info_1'])
            worksheet.merge_range('B21:AA21', ' ', cell_format['space'])

            column = 1
            # row += 1
            n = 1
            for n in range(1,27) :
                if (column == 1) :
                    worksheet.write(23, column, ' ', cell_format['content_hide_ki'])
                else :
                    worksheet.write(23, column, ' ', cell_format['content_hide'])    
                column += 1

            i = 0
            j = 1
            # dpp = 0
            # nompo = 0
            # nomta = 0
            # suba = 0
            # hut = 0
            # palas = 0
            # delas = 0
            # dudu = 0
            # dunam = 0
            row = 21
            # bul = 0
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
                    worksheet.merge_range(row, 1, 22, 1, data['1'], cell_format['header_lc'])
                    worksheet.merge_range(row, 2, 22, 2, data['2'], cell_format['header'])
                    worksheet.merge_range(row, 3, 22, 3, data['3'], cell_format['header'])
                    worksheet.merge_range(row, 4, 22, 4, data['4'], cell_format['header'])
                    worksheet.merge_range(row, 5, 22, 5, data['5'], cell_format['header'])
                    worksheet.merge_range(row, 6, 22, 6, data['6'], cell_format['header'])
                    worksheet.merge_range(row, 7, 22, 7, 'NOTE', cell_format['header'])
                    worksheet.merge_range(row, 8, 22, 8, data['7'], cell_format['header'])
                    worksheet.merge_range(row, 9, 22, 9, data['8'], cell_format['header'])
                    worksheet.merge_range(row, 10, 22, 10, data['9'], cell_format['header'])
                    worksheet.merge_range(row, 11, 22, 11, data['10'], cell_format['header'])
                    worksheet.merge_range(row, 12, 22, 12, data['11'], cell_format['header'])
                    worksheet.merge_range(row, 13, 22, 13, data['12'], cell_format['header'])
                    worksheet.merge_range(row, 14, 22, 14, data['13'], cell_format['header'])
                    worksheet.merge_range(row, 15, 22, 15, data['14'], cell_format['header'])
                    worksheet.merge_range(row, 16, 22, 16, data['15'], cell_format['header'])
                    worksheet.merge_range(row, 17, 22, 17, data['16'], cell_format['header'])
                    worksheet.merge_range(row, 18, 22, 18, data['17'], cell_format['header'])
                    worksheet.merge_range(row, 19, 22, 19, data['18'], cell_format['header'])
                    worksheet.merge_range(row, 20, 22, 20, data['19'], cell_format['header'])
                    worksheet.merge_range(row, 21, 22, 21, data['20'], cell_format['header'])
                    worksheet.merge_range(row, 22, row, 25, 'VOUCHER', cell_format['header'])
                    worksheet.write(22, 22, 'NO', cell_format['header'])
                    worksheet.write(22, 23, 'NILAI', cell_format['header'])
                    worksheet.write(22, 24, 'JT', cell_format['header'])
                    worksheet.write(22, 25, 'TGL BAYAR', cell_format['header'])
                    worksheet.merge_range(row, 26, 22, 26, 'KETERANGAN', cell_format['header_rc'])
                    row += 2
                    
                else:
                    worksheet.write(row, 1, data['1'], cell_format['content_def_ki'])
                    worksheet.write(row, 2, data['2'], cell_format['content_def'])
                    worksheet.write(row, 3, data['3'], cell_format['content_def'])
                    worksheet.write(row, 4, data['4'], cell_format['content_def'])
                    worksheet.write(row, 5, data['5'], cell_format['content_def'])
                    worksheet.write(row, 6, data['6'], cell_format['content_left'])
                    worksheet.write(row, 7, ' ', cell_format['content_left'])
                    worksheet.write(row, 8, data['7'], cell_format['content_def'])
                    worksheet.write(row, 9, data['8'], cell_format['content_def'])
                    worksheet.write(row, 10, data['9'], cell_format['content_def'])
                    worksheet.write(row, 11, data['10'], cell_format['content_def'])
                    worksheet.write(row, 12, data['11'], cell_format['content_left'])
                    worksheet.write(row, 13, data['12'], cell_format['content_def'])
                    worksheet.write(row, 14, data['13'], cell_format['content_def'])
                    worksheet.write(row, 15, data['14'], cell_format['content_right'])
                    worksheet.write(row, 16, data['15'], cell_format['content_right'])
                    worksheet.write(row, 17, data['16'], cell_format['content_right'])
                    worksheet.write(row, 18, data['17'], cell_format['content_def'])
                    worksheet.write(row, 19, data['18'], cell_format['content_def'])
                    worksheet.write(row, 20, data['19'], cell_format['content_def'])
                    worksheet.write(row, 21, data['20'], cell_format['content_def'])
                    worksheet.write(row, 22, data['21'], cell_format['content_def'])
                    worksheet.write(row, 23, data['22'], cell_format['content_right'])
                    worksheet.write(row, 24, data['23'], cell_format['content_left'])
                    worksheet.write(row, 25, data['24'], cell_format['content_def'])
                    worksheet.write(row, 26, ' ', cell_format['content_left_ka'])           
                row += 1
                i += 1

        # Set the autofilter.
        worksheet.autofilter('C24:AA24')

        workbook.close()
        result = base64.encodestring(fp.getvalue())
        filename = 'LAPORAN MONITORING PEMBELIAN BULAN ' + self.str_bulan + '.xlsx'
        self.write({'export_file':result, 'export_filename':filename})
        return {
            'name'     : "Export Complete, total %s records" % i,
            'type'     : 'ir.actions.act_window',
            'res_model': 'vit.monitoring_pembelian_bln',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id'   : self.id,
            'views'    : [(False, 'form')],
            'target'   : 'new',
        }

