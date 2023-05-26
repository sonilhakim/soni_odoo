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
    _name = 'vit.export_anggaran'
    
    export_file = fields.Binary(string="Export File",  )
    export_filename = fields.Char(string="Export File",  )

    unit_id         = fields.Many2one(comodel_name='vit.unit_kerja', string="Unit")
    rka_id          = fields.Many2one(comodel_name='anggaran.rka', string='Dasar Anggaran')

    @api.multi
    def get_datas(self):
        res = {}
        headers = [
            "Kode",
            "Uraian",
            "Volume",
            "Satuan",
            "Harga*(Rp)",
            "Jumlah"
        ]

        values = []
        ang_obj = self.env['anggaran.rka']
        rkas = ang_obj.search([('id','=',self.rka_id.id)])
        for rka in rkas:
            values.append({
                    'Kode': '',
                    'Uraian': rka.unit_id.name,
                    'Volume': '',
                    'Satuan': '',
                    'Harga*(Rp)': '',
                    'Jumlah': rka.anggaran,
                })
            for keg in rka['rka_kegiatan_ids']:
                values.append({
                    'Kode': keg.program_id.code,
                    'Uraian': keg.program_id.name,
                    'Volume': '',
                    'Satuan': '',
                    'Harga*(Rp)': '',
                    'Jumlah': keg.anggaran,
                })
                values.append({
                    'Kode': keg.kegiatan_id.code,
                    'Uraian': keg.kegiatan_id.name,
                    'Volume': '',
                    'Satuan': '',
                    'Harga*(Rp)': '',
                    'Jumlah': keg.anggaran,
                })
                values.append({
                    'Kode': '',
                    'Uraian': keg.indikator,
                    'Volume': '',
                    'Satuan': '',
                    'Harga*(Rp)': '',
                    'Jumlah': keg.anggaran,
                })
                for mak in keg['rka_coa_ids']:
                    values.append({
                        'Kode': mak.mak_id.code,
                        'Uraian': mak.mak_id.name,
                        'Volume': '',
                        'Satuan': '',
                        'Harga*(Rp)': '',
                        'Jumlah': mak.total,
                    })
                    for det in mak['rka_detail_ids']:
                        for vol in det.rka_volume_ids: 
                            values.append({
                                'Kode': '',
                                'Uraian': det.keterangan,
                                'Volume': vol.volume,
                                'Satuan': vol.volume_uom,
                                'Harga*(Rp)': det.tarif,
                                'Jumlah': det.volume_total
                            })
            
        res['%s' % self.unit_id.name] = [headers, values]        
        return res

    @api.multi
    def confirm_button(self):
        self.ensure_one()
        datas = self.get_datas()
        if not datas :
            raise Warning("Data tidak ditemukan.")
        fp = BytesIO()
        workbook = xlsxwriter.Workbook(fp)
        # cell_format, workbook = self.cell_format(workbook)
        for sheet, header_content in datas.items():
            headers, contents = header_content
            worksheet = workbook.add_worksheet(sheet)
            worksheet.set_column('A:ZZ', 30)
            column_length = len(headers)

            column = 0
            row = 0
            for col in headers :
                worksheet.write(row, column, col)
                column += 1
            i = 0
            row = 1
            for data in contents :
                column = 0
                for key, value in data.items():
                    worksheet.write(row, column, value)
                    column += 1
                row += 1
                i += 1


        workbook.close()
        result = base64.encodestring(fp.getvalue())
        filename = 'Export Anggaran %s-%s.xlsx' % (self.unit_id.name,time.strftime("%d%m%Y"))
        self.write({'export_file':result, 'export_filename':filename})
        return {
            'name': "Export Complete, total %s records" % i,
            'type': 'ir.actions.act_window',
            'res_model': 'vit.export_anggaran',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'views': [(False, 'form')],
            'target': 'new',
        }