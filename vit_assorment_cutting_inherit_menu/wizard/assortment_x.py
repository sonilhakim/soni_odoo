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

class assortment_cutting_wizard(models.TransientModel):
    _name = 'vit.assortment_cutting_wizard'
    
    export_file = fields.Binary(string="Export File",  )
    export_filename = fields.Char(string="Export File",  )

    def cell_format(self, workbook):
        cell_format = {}
        cell_format['header'] = workbook.add_format({
            'align': 'center',
        })
        cell_format['content'] = workbook.add_format({
            'border': False,
        })
        cell_format['info'] = workbook.add_format({
            'font_size': 20,
        })
        return cell_format, workbook

    @api.multi
    def get_datas(self):
        styles_id = self._context.get('active_id', False)
        res = {}
        if styles_id:
            st_obj = self.env['vit.boq_po_garmen_line']
            headers = [
                "Size",
                "QTY PER",
                "panjang baju",
                "panjang tangan",
                "panjang dada",
                "lingkar pinggang",
                "lingkat pinggul",
                "QTY PCS",
                "Serial Number",
            ]

            styles = st_obj.browse(styles_id)
            cr = self.env.cr
            for st in styles:
                sql = """SELECT pav.name, count(lt.id), itm.size, lt.name
                    FROM vit_data_pengukuran_item itm
                    LEFT JOIN stock_production_lot lt ON itm.lot_id = lt.id
                    LEFT JOIN vit_boq_po_garmen_line st ON lt.style_id = st.id
                    LEFT JOIN product_product pp ON lt.product_id = pp.id
                    LEFT JOIN product_attribute_value_product_product_rel ppr ON ppr.product_product_id = pp.id
                    LEFT JOIN product_attribute_value pav ON ppr.product_attribute_value_id = pav.id
                    WHERE st.id = %s
                    GROUP BY pav.name, itm.size, lt.name
                    """
                cr.execute(sql, (st.id,))
                record = cr.fetchall()
                values = []
                for rec in record:
                    values.append({
                        "Size"             : rec[0],
                        "QTY PER"          : rec[1],
                        "panjang baju"     : rec[2],
                        "panjang tangan"   : rec[2],
                        "panjang dada"     : rec[2],
                        "lingkar pinggang" : rec[2],
                        "lingkat pinggul"  : rec[2],
                        "QTY PCS"          : 1,
                        "Serial Number"    : rec[3],
                    })
                    # prod.is_exported=True
                    # prod.date_exported=time.strftime("%Y-%m-%d %H:%M:%S")
                res['Assortmen Cutting'] = [headers, values]        
                return res

    @api.multi
    def confirm_button(self):
        styles_id = self._context.get('active_id', False)
        self.ensure_one()
        datas = self.get_datas()
        if not datas :
            raise Warning("Data tidak ditemukan.")
        fp = BytesIO()
        workbook = xlsxwriter.Workbook(fp)
        cell_format, workbook = self.cell_format(workbook)
        st_obj = self.env['vit.boq_po_garmen_line']
        for sheet, header_content in datas.items():
            headers, contents = header_content
            worksheet = workbook.add_worksheet(sheet)
            worksheet.set_column('A:ZZ', 15)
            column_length = len(headers)

            column = 3
            row = 0
            worksheet.write(row, column, 'ASSORTMENT CUTTING', cell_format['info'])
            styles = st_obj.browse(styles_id)
            for st in styles:
                column = 0
                row = 1
                worksheet.write(row, column, 'Company Name :')
                column = 1
                row = 1
                worksheet.write(row, column, '%s' %st.po_id.partner_id.name)
                column = 0
                row = 2
                worksheet.write(row, column, 'Style:')
                column = 1
                row = 2
                worksheet.write(row, column, '%s' %st.product_id.name)
                column = 0
                row = 3
                worksheet.write(row, column, 'Total PCS:')
                column = 1
                row = 3
                worksheet.write(row, column, '%s' %len(st.lot_ids))
                column = 0
                row = 4
                worksheet.write(row, column, 'Total SET:')
                column = 1
                row = 4
                worksheet.write(row, column, '%s' %len(st.lot_ids))

            column = 0
            row = 6
            for col in headers :
                worksheet.write(row, column, col, cell_format['header'])
                column += 1
            i = 0
            row = 7
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
            'res_model': 'vit.assortment_cutting_wizard',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'views': [(False, 'form')],
            'target': 'new',
        }
