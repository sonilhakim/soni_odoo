from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.tools.float_utils import float_compare
import time
import pytz
import datetime
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
_logger = logging.getLogger(__name__)

class POThdBTBWizard(models.TransientModel):
    _name    = 'vit.po_thd_btb'
    _inherit = 'report.report_xlsx.abstract'

    export_file     = fields.Binary(string="Export File",  )
    export_filename = fields.Char(string="Export File",  )

    current_date    = datetime.date.today()
    date_start      = fields.Date(string='Start Date', required=True)
    date_end        = fields.Date(string='End Date', required=True)

    # commercial_partner_id = fields.Many2one(comodel_name="res.partner", string="Vendor", default=lambda self: self.env.uid, track_visibility='onchange', readonly=True)

    def cell_format(self, workbook):
        cell_format = {}
        cell_format['header'] = workbook.add_format({
            'font_size': 11,
            'border': True,
            'align': 'center',
            'bg_color': '#f8ccad',
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
        cell_format['content_right'] = workbook.add_format({
            'font_size': 11,
            'border': True,
            'align': 'right',
        })
        cell_format['content_hide'] = workbook.add_format({
            'font_color': '#FFFFFF',
        })
        cell_format['info_1'] = workbook.add_format({
            'font_size': 17,
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
        return cell_format, workbook

    @api.multi
    def get_datas(self):
        rec = {}
        contents = [{
            "1" :"NO",
            "2" :"NAMA BARANG",
            "3" :"QTY",
            "4" :"SAT",
            "5" :"NO PO",
            "6" :"NO BTB",
            "7" :"QTY BTB",
            "8" :"SISA PO",
            "9" :"NO INQUIRY",
            "10":"DEPT",
        }]

        # values = []
        # purchase = self.env['purchase.order'].search([('date_order','>=',self.date_start), ('date_order','<=',self.date_end)])
        sql = """SELECT (pt.name) as nama_barang, (pol.product_qty) as qty, (u.name) as satuan, (po.name) as no_po, (sp.name) as no_btb, ((sm.product_uom_qty/u1.factor)*u.factor) as qty_btb, (pol.qty_received) as qty_received, (mig.name) as no_inquiry, (mig1.name) as no_inquiry1, (mig2.name) as no_inquiry2, (hd.complete_name) as dept 
                FROM purchase_order_line pol
                LEFT JOIN purchase_order po ON pol.order_id = po.id
                LEFT JOIN stock_move sm ON sm.purchase_line_id = pol.id
                LEFT JOIN stock_picking sp ON sm.picking_id = sp.id
                LEFT JOIN product_product pp ON pol.product_id = pp.id
                LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
                LEFT JOIN uom_uom u ON pol.product_uom = u.id
                LEFT JOIN uom_uom u1 ON sm.product_uom = u1.id
                LEFT JOIN account_analytic_tag_purchase_order_line_rel apl ON apl.purchase_order_line_id = pol.id
                LEFT JOIN account_analytic_tag aat ON apl.account_analytic_tag_id = aat.id
                LEFT JOIN vit_marketing_inquery_garmen mig ON mig.analytic_tag_id = aat.id
                LEFT JOIN vit_purchase_order_garmen pog ON po.po_id = pog.id
                LEFT JOIN vit_marketing_sph_garmen msg ON pog.sph_id = msg.id
                LEFT JOIN vit_marketing_proposal mp ON msg.proposal_id = mp.id
                LEFT JOIN vit_marketing_inquery_garmen mig1 ON mp.inquery_id = mig1.id
                LEFT JOIN vit_marketing_inquery_garmen mig2 ON po.inquery_id = mig2.id
                LEFT JOIN purchase_requisition te ON po.requisition_id = te.id
                LEFT JOIN vit_product_request pr ON pr.name = te.origin
                LEFT JOIN hr_department hd ON pr.department_id = hd.id
                WHERE po.date_order >= %s AND po.date_order <= %s
                GROUP BY mig.id, mig1.id, mig2.id, hd.id, pr.id, po.id, pt.id, u.id, u1.id, sp.id, pol.id, sm.id 
                ORDER BY mig.id, mig1.id, mig2.id
                """
        self.env.cr.execute(sql, (self.date_start,self.date_end))
        result = self.env.cr.dictfetchall()
        line_ids = []
        i = 1
        for res in result:
            # sisa_po = ''
            # if res['sisa_po']:
            #     if res['sisa_po'] < 0.0:
            #         sisa_po = "+" + str(res['sisa_po'] * -1)
            #     elif res['sisa_po'] > 0.0:
            #         sisa_po = "-" + str(res['sisa_po'] * 1)
            # else:
            #     sisa_po = 0.0
            if res['qty_received']:
                sisa_po = res['qty'] -  res['qty_received']
            else:
                sisa_po = res['qty'] - 0.0

            if res['qty_btb']:
                qty_btb = res['qty_btb']
            else:
                qty_btb = 0.0

            if res['no_inquiry']:
                no_inquiry = res['no_inquiry']
            elif not res['no_inquiry'] and res['no_inquiry1']:
                no_inquiry = res['no_inquiry1']
            elif not res['no_inquiry'] and res['no_inquiry1'] and res['no_inquiry2']:
                no_inquiry = res['no_inquiry2']
            else :
                no_inquiry = ''

            contents.append({
                "1" : str(i),
                "2" : res['nama_barang'],
                "3" : res['qty'],
                "4" : res['satuan'],
                "5" : res['no_po'],
                "6" : res['no_btb'],
                "7" : "{:.2f}".format(qty_btb) or 0.0,
                "8" : sisa_po,
                "9" : no_inquiry,
                "10": res['dept'],

            })
            i += 1
        rec['Lap PO Bukti Terima Barang'] = [contents]        
        return rec

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
            worksheet.set_column('C:C', 60)
            worksheet.set_column('D:D', 8)
            worksheet.set_column('E:E', 7)
            worksheet.set_column('F:F', 10)
            worksheet.set_column('G:G', 15)
            worksheet.set_column('H:H', 8)
            worksheet.set_column('I:I', 8)
            worksheet.set_column('J:J', 12)
            worksheet.set_column('K:K', 15)
            column_length = len(contents)
            # worksheet.set_row_pixels(16, 9)
            # worksheet.set_row_pixels(18, 12)
            # worksheet.set_row_pixels(20, 9)  
            
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
            worksheet.merge_range('B17:K17', ' ', cell_format['space'])
            worksheet.merge_range('B18:K18', 'REKAPITULASI PURCHASE ORDER TERHADAP BUKTI TERIMA BARANG', cell_format['info_1'])
            worksheet.merge_range('B19:K19', ' ', cell_format['space'])
            worksheet.merge_range('B20:K20', 'Periode'+' '+self.date_start.strftime('%d %b %Y')+' s.d '+self.date_end.strftime('%d %b %Y'), cell_format['info_2'])
            worksheet.merge_range('B21:K21', ' ', cell_format['space'])

            # column = 1
            i   = 0
            row = 21
            # for col in headers :
            #     if (column == 11) :
            #         worksheet.write(row, column, col, cell_format['content_hide'])
            #     else :
            #         worksheet.write(row, column, col, cell_format['header'])
            #     column += 1
            # i = 0
            # row = 22
            for data in contents[0] :
                # column = 1
                if i == 0 :
                    worksheet.write(row, 1, data['1'], cell_format['header'])
                    worksheet.write(row, 2, data['2'], cell_format['header'])
                    worksheet.write(row, 3, data['3'], cell_format['header'])
                    worksheet.write(row, 4, data['4'], cell_format['header'])
                    worksheet.write(row, 5, data['5'], cell_format['header'])
                    worksheet.write(row, 6, data['6'], cell_format['header'])
                    worksheet.write(row, 7, data['7'], cell_format['header'])
                    worksheet.write(row, 8, data['8'], cell_format['header'])
                    worksheet.write(row, 9, data['9'], cell_format['header'])
                    worksheet.write(row, 10, data['10'], cell_format['header'])
                else:
                    worksheet.write(row, 1, data['1'], cell_format['content_def'])
                    worksheet.write(row, 2, data['2'], cell_format['content_left'])
                    worksheet.write(row, 3, data['3'], cell_format['content_right'])
                    worksheet.write(row, 4, data['4'], cell_format['content_def'])
                    worksheet.write(row, 5, data['5'], cell_format['content_left'])
                    worksheet.write(row, 6, data['6'], cell_format['content_left'])
                    worksheet.write(row, 7, data['7'], cell_format['content_right'])
                    worksheet.write(row, 8, data['8'], cell_format['content_right'])
                    worksheet.write(row, 9, data['9'], cell_format['content_def'])
                    worksheet.write(row, 10, data['10'], cell_format['content_def'])
                # for key, value in data.items() :
                #     if (column == 2) :
                #         worksheet.write(row, 2, value, cell_format['content_left'])
                #     elif (column == 3 or column == 7 or column == 8) :
                #         worksheet.write(row, column, value, cell_format['content_right'])
                #     elif (column == 11) :
                #         worksheet.write(row, column, value, cell_format['content_hide'])
                #     else :
                #         worksheet.write(row, column, value, cell_format['content_def'])
                    
                #     column += 1
                row += 1
                i += 1

        # wb = xw.Workbook(fp)
        # wb.sheets[0].range('C' + str(wb.sheets[0].cells.last_cell.row)).end('up').row
        # Set the autofilter.
        worksheet.autofilter('C21:K16000')

        workbook.close()
        result = base64.encodestring(fp.getvalue())
        filename = 'Rekap PO terhadap BTB-%s.xlsx' % time.strftime("%Y%m%d_%H%M%S")
        self.write({'export_file':result, 'export_filename':filename})
        return {
            'name': "Export Complete, total %s records" % i,
            'type': 'ir.actions.act_window',
            'res_model': 'vit.po_thd_btb',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id'   : self.id,
            'views'    : [(False, 'form')],
            'target'   : 'new',
        }
