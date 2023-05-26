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
_logger = logging.getLogger(__name__)

class RekapPembelianCashWizard(models.TransientModel):
    _name    = 'vit.rekap_pembelian_cash'
    _inherit = 'report.report_xlsx.abstract'
    # _inherit = 'res.partner'

    export_file     = fields.Binary(string="Export File",  )
    export_filename = fields.Char(string="Export File",  )

    current_date    = datetime.date.today()
    date_start      = fields.Date(string='Start Date', required=True)
    date_end        = fields.Date(string='End Date', required=True)

    # commercial_partner_id = fields.Many2one(comodel_name="res.partner", string="Vendor", default=lambda self: self.env.uid, track_visibility='onchange', readonly=True)
    
    # company_id      = fields.Many2one("Company", default=True)

    def cell_format(self, workbook):
        cell_format = {}
        cell_format['header'] = workbook.add_format({
            'font_size': 12,
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
            'font_size': 13,
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
            "1":"NO",
            "2":"NAMA BARANG",
            "3":"QTY",
            "4":"SATUAN",
            "5":"NO PR",
            "6":"NO PO",
            "7":"HARGA",
            "8":"SUPPLIER",
            "9":"KETERANGAN",
        }]
        # conten = [{"NO","NAMA BARANG","QTY","SATUAN",}]
        # import pdb;pdb.set_trace()
        #values = []
        # purchase = self.env['purchase.order'].search([('date_order','>=',self.date_start), ('date_order','<=',self.date_end)])
        sql = """SELECT (pt.name) as nama_barang, (sum(pol.product_qty)) as qty, (u.name) as satuan, (pr.name) as no_pr, (po.name) as no_po, (pol.price_unit) as harga, (rp.name) as supplier
                FROM purchase_order_line pol
                LEFT JOIN purchase_order po ON pol.order_id = po.id
                LEFT JOIN purchase_requisition te ON po.requisition_id = te.id
                LEFT JOIN vit_product_request pr ON pr.name = te.origin
                LEFT JOIN product_product pp ON pol.product_id = pp.id
                LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
                LEFT JOIN uom_uom u ON pol.product_uom = u.id
                LEFT JOIN res_partner rp ON po.partner_id = rp.id
                WHERE po.date_order >= %s AND po.date_order <= %s
                GROUP BY pt.name, u.id, pol.price_unit, pr.name, rp.name, po.name
                ORDER BY rp.name
                """
        self.env.cr.execute(sql, (self.date_start,self.date_end))
        result = self.env.cr.dictfetchall()
        line_ids = []
        i = 1
        for res in result:
            
            contents.append({
                "1":str(i),
                "2":res['nama_barang'],
                "3":res['qty'],
                "4":res['satuan'],
                "5":res['no_pr'],
                "6":res['no_po'],
                "7":res['harga'],
                "8":res['supplier'],
                "9":'',

            })
            i += 1
        rec['Rekap Pembelian Cash'] = [contents]        
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
            worksheet.set_column('B:B', 8)
            worksheet.set_column('C:C', 60)
            worksheet.set_column('D:D', 10)
            worksheet.set_column('E:E', 12)
            worksheet.set_column('F:F', 30)
            worksheet.set_column('G:G', 15)
            worksheet.set_column('H:H', 13)
            worksheet.set_column('I:J', 35)
            column_length = len(contents)
            # worksheet.set_row_pixels(16, 9)
            # worksheet.set_row_pixels(17, 30)
            # worksheet.set_row_pixels(18, 9)
            # worksheet.set_row_pixels(19, 23)
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
            worksheet.write('C13', user_obj.company_id.zip)
            worksheet.merge_range('B14:C14', user_obj.company_id.state_id.name)
            worksheet.merge_range('B15:C15', user_obj.company_id.country_id.name)
            worksheet.merge_range('B17:J17', ' ', cell_format['space'])
            worksheet.merge_range('B18:J18', 'REKAP BELANJA CASH', cell_format['info_1'])
            worksheet.merge_range('B19:J19', ' ', cell_format['space'])
            worksheet.merge_range('B20:J20', 'Periode'+' '+self.date_start.strftime('%d %b %Y')+' s.d '+self.date_end.strftime('%d %b %Y'), cell_format['info_2'])
            worksheet.merge_range('B21:J21', ' ', cell_format['space'])

            # column = 1
            # row = 21
            # for con in contents :
            #     worksheet.write(row, column, col, cell_format['header'])
            #     column += 1
            
            i = 0
            row = 21
            for data in contents[0] :
                # import pdb;pdb.set_trace()
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
                else:
                    worksheet.write(row, 1, data['1'], cell_format['content_def'])
                    worksheet.write(row, 2, data['2'], cell_format['content_left'])
                    worksheet.write(row, 3, data['3'], cell_format['content_right'])
                    worksheet.write(row, 4, data['4'], cell_format['content_def'])
                    worksheet.write(row, 5, data['5'], cell_format['content_left'])
                    worksheet.write(row, 6, data['6'], cell_format['content_left'])
                    worksheet.write(row, 7, data['7'], cell_format['content_right'])
                    worksheet.write(row, 8, data['8'], cell_format['content_left'])
                    worksheet.write(row, 9, data['9'], cell_format['content_def'])
                
                
                # column = 1
                # for value in data:
                #     if (column == 2 or column == 5 or column == 6 or column == 8) :
                #         worksheet.write(row, column, value, cell_format['content_left'])
                #     elif (column == 3 or column == 7) :
                #         worksheet.write(row, column, value, cell_format['content_right'])
                #     else :
                #         worksheet.write(row, column, value, cell_format['content_def'])

                #     column += 1
                row += 1
                i += 1

            worksheet.autofilter('B22:J22')

            row     += 2
            worksheet.write(row, 5, 'Bogor,'+' ' + self.current_date.strftime('%d %b %Y'), cell_format['footer'])
            
            row += 2
            worksheet.write(row, 2, 'Dibuat oleh,', cell_format['footer'])
            worksheet.write(row, 5, 'Mengetahui,', cell_format['footer'])
            worksheet.write(row, 8, 'Menyetujui,', cell_format['footer'])
            
            row += 6
            worksheet.write(row, 2, 'Adm Purchasing', cell_format['footer'])
            worksheet.write(row, 5, 'Head of Purchasing', cell_format['footer'])
            worksheet.write(row, 8, 'GM Marketing', cell_format['footer'])

        workbook.close()
        result = base64.encodestring(fp.getvalue())
        filename = 'Rekap Pembelian Cash-%s.xlsx' % time.strftime("%Y%m%d_%H%M%S")
        self.write({'export_file':result, 'export_filename':filename})
        return {
            'name': "Export Complete, total %s records" % i,
            'type': 'ir.actions.act_window',
            'res_model': 'vit.rekap_pembelian_cash',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'views': [(False, 'form')],
            'target': 'new',
        }
