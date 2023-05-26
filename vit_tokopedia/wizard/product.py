from odoo import api, fields, models, _
import time
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

class export_product_wizard(models.TransientModel):
    _name = 'vit.export_product'
    
    export_file = fields.Binary(string="Export File",  )
    export_filename = fields.Char(string="Export File",  )

    # @api.multi
    # def confirm_button(self):
    #     """
    #     export product yang is_exported = False
    #     update setelah export
    #     :return: 
    #     """
    #     cr = self.env.cr

    #     headers = [
    #         "Nama Produk*",
    #         "SKU",
    #         "Kategory*",
    #         "Deskripsi Produk",
    #         "Harga*(Rp)",
    #         "Berat*(Gram)",
    #         "Pemesanan Minimum*",
    #         "Status*",
    #         "Jumlah Stok*",
    #         "Etalase",
    #         "Preorder",
    #         "Waktu Proses Preorder",
    #         "Kondisi*",
    #         "Gambar 1",
    #         "Gambar 2",
    #         "Gambar 3",
    #         "Gambar 4",
    #         "Gambar 5",
    #         "URL Video Produk 1",
    #         "URL Video Produk 2",
    #         "URL Video Produk 3",
    #     ]

    #     mpath = get_module_path('vit_export')

    #     # csvfile = open(mpath + '/static/product.csv', 'wb')
    #     csvfile = StringIO()
    #     csvwriter = csv.writer(csvfile, delimiter=',')
    #     csvwriter.writerow([h.upper() for h in headers])

    #     product = self.env['product.template']
    #     products = product.search([('is_exported','=',False)])
    #     i=0
        
    #     for prod in products:
    #         data = {
    #             "Nama Produk*"          : prod.name,
    #             "SKU"                   : prod.default_code,
    #             "Kategory*"             : prod.categ_id.name,
    #             "Deskripsi Produk"      : prod.name,
    #             "Harga*(Rp)"            : prod.lst_price,
    #             "Berat*(Gram)"          : prod.berat,
    #             "Pemesanan Minimum*"    : prod.pesan,
    #             "Status*"               : prod.status,
    #             "Jumlah Stok*"          : prod.jumlah,
    #             "Etalase"               : prod.etalase,
    #             "Preorder"              : prod.preorder,
    #             "Waktu Proses Preorder" : prod.waktu_preorder,
    #             "Kondisi*"              : prod.kondisi,
    #             "Gambar 1"              : prod.gambar_1,
    #             "Gambar 2"              : prod.gambar_2,
    #             "Gambar 3"              : prod.gambar_3,
    #             "Gambar 4"              : prod.gambar_4,
    #             "Gambar 5"              : prod.gambar_5,
    #             "URL Video Produk 1"    : prod.url_1,
    #             "URL Video Produk 2"    : prod.url_2,
    #             "URL Video Produk 3"    : prod.url_3,
    #         }
    #         csvwriter.writerow([data[v] for v in headers])

    #         prod.is_exported=True
    #         prod.date_exported=time.strftime("%Y-%m-%d %H:%M:%S")
    #         i+=1

    #     cr.commit()
    #     # csvfile.close()

    #     # raise UserError("Export %s record(s) Done!" % i)

    #     self.export_file = base64.b64encode(csvfile.getvalue().encode())
    #     self.export_filename = 'Export-%s.csv' % time.strftime("%Y%m%d_%H%M%S")
    #     return {
    #         'name': "Export Complete, total %s records" % i,
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'vit.export_product',
    #         'view_mode': 'form',
    #         'view_type': 'form',
    #         'res_id': self.id,
    #         'views': [(False, 'form')],
    #         'target': 'new',
    #     }
    def cell_format(self, workbook):
        cell_format = {}
        cell_format['header'] = workbook.add_format({
            'font_size': 14,
            'font_color': 'white',
            'align': 'center',
            'bg_color': '#006400',
        })
        cell_format['content'] = workbook.add_format({
            'font_size': 11,
            'border': False,
        })
        cell_format['info'] = workbook.add_format({
            'font_size': 20,
        })
        return cell_format, workbook

    @api.multi
    def get_datas(self):
        res = {}
        headers = [
            "Nama Produk*",
            "SKU",
            "Kategory*",
            "Deskripsi Produk",
            "Harga*(Rp)",
            "Berat*(Gram)",
            "Pemesanan Minimum*",
            "Status*",
            "Jumlah Stok*",
            "Etalase",
            "Preorder",
            "Waktu Proses Preorder",
            "Kondisi*",
            "Gambar 1",
            "Gambar 2",
            "Gambar 3",
            "Gambar 4",
            "Gambar 5",
            "URL Video Produk 1",
            "URL Video Produk 2",
            "URL Video Produk 3",
        ]

        values = []
        products = self.env['product.template'].search([('is_exported','=',False), ('tokopedia_ok','=',True)])
        for prod in products:
            values.append({
                "Nama Produk*"          : prod.name,
                "SKU"                   : prod.default_code,
                "Kategory*"             : prod.tokped_categ_id.code,
                "Deskripsi Produk"      : prod.desk,
                "Harga*(Rp)"            : str(prod.lst_price),
                "Berat*(Gram)"          : str(prod.berat),
                "Pemesanan Minimum*"    : str(prod.pesan),
                "Status*"               : prod.status,
                "Jumlah Stok*"          : str(prod.qty_available),
                "Etalase"               : prod.etalase,
                "Preorder"              : prod.preorder,
                "Waktu Proses Preorder" : str(prod.waktu_preorder),
                "Kondisi*"              : prod.kondisi,
                "Gambar 1"              : prod.gambar_1,
                "Gambar 2"              : prod.gambar_2,
                "Gambar 3"              : prod.gambar_3,
                "Gambar 4"              : prod.gambar_4,
                "Gambar 5"              : prod.gambar_5,
                "URL Video Produk 1"    : prod.url_1,
                "URL Video Produk 2"    : prod.url_2,
                "URL Video Produk 3"    : prod.url_3,

            })
            prod.is_exported=True
            prod.date_exported=time.strftime("%Y-%m-%d %H:%M:%S")
        res['Template Impor Produk (new)'] = [headers, values]        
        return res

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
            headers, contents = header_content
            worksheet = workbook.add_worksheet(sheet)
            worksheet.set_column('A:ZZ', 30)
            column_length = len(headers)

            column = 0
            row = 0
            worksheet.write(row, column, 'Tokopedia - Template Impor Produk', cell_format['info'])
            row = 1
            worksheet.write(row, column, 'Masukkan informasi produk pada file ini. Anda dapat upload sampai dengan 150 produk dalam satu file.')
            row = 2
            worksheet.write(row, column, 'Kolom dengan tanda (*) wajib diisi.')

            column = 0
            row = 4
            for col in headers :
                worksheet.write(row, column, col, cell_format['header'])
                column += 1
            i = 0
            row = 5
            for data in contents :
                column = 0
                for key, value in data.items():
                    worksheet.write(row, column, value, cell_format['content'])
                    column += 1
                row += 1
                i += 1

        workbook.close()
        result = base64.encodestring(fp.getvalue())
        filename = 'Export-%s.xlsx' % time.strftime("%Y%m%d_%H%M%S")
        self.write({'export_file':result, 'export_filename':filename})
        return {
            'name': "Export Complete, total %s records" % i,
            'type': 'ir.actions.act_window',
            'res_model': 'vit.export_product',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'views': [(False, 'form')],
            'target': 'new',
        }
