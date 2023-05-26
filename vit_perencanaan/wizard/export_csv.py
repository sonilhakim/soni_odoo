from odoo import api, fields, models, _
import time
import csv
from odoo.modules import get_modules, get_module_path
from odoo.exceptions import UserError
import copy
import logging
from io import StringIO
import base64

_logger = logging.getLogger(__name__)

class efaktur_pk_wizard(models.TransientModel):
    _name = 'vit.export_anggaran'

    export_file     = fields.Binary(string="Export File",  )
    export_filename = fields.Char(string="Export File",  )

    unit_id         = fields.Many2one(comodel_name='vit.unit_kerja', string="SUBSATKER")
    rka_id          = fields.Many2one(comodel_name='anggaran.rka', string='Dasar Anggaran')

    # @api.multi
    # def confirm_button(self):
    #     ang = self.env['anggaran.rka']
    #     ang.action_report()
        
    #     cr = self.env.cr

    #     headers = [
    #         "Kode",
    #         "Uraian",
    #         "Volume",
    #         "Satuan",
    #         "Harga",
    #         "Jumlah"
    #     ]


    #     mpath = get_module_path('anggaran_rka')

    #     # csvfile = open(mpath + '/static/fpk.csv', 'wb')
    #     csvfile = StringIO()
    #     csvwriter = csv.writer(csvfile, delimiter=';')
    #     csvwriter.writerow([h.upper() for h in headers])

    #     ang_obj = self.env['anggaran.rka']
    #     rkas = ang_obj.search([('id','=',self.rka_id.id)])

    #     i=0

    #     for rka in rkas:
    #         self.baris2(headers, csvwriter, rka)
    #         for td in rka['rka_tridharma_ids']:
    #             self.baris3(headers, csvwriter, td)
    #             for kro in td['rka_kro_ids']:
    #                 self.baris4(headers, csvwriter, kro)
    #                 for ro in kro['rka_ro_ids']:
    #                     self.baris5(headers, csvwriter, ro)
    #                     for kom in ro['rka_komp_ids']:
    #                         if kom.komponen_id:
    #                             self.baris6(headers, csvwriter, kom)
    #                         for sub in kom['rka_sub_ids']:
    #                             if sub.subkomponen_id:
    #                                 self.baris7(headers, csvwriter, sub)
    #                             for mak in sub['rka_mak_ids']:
    #                                 self.baris8(headers, csvwriter, mak)
    #                                 for det in mak['rka_det_ids']:
    #                                     self.baris9(headers, csvwriter, det)
            
    #                 i+=1

    #     cr.commit()
    #     # csvfile.close()
    #     # _logger.info(csvfile.getvalue().encode() )
    #     self.export_file = base64.b64encode(csvfile.getvalue().encode())
    #     self.export_filename = 'Export Anggaran %s-%s.csv' % (self.unit_id.name,time.strftime("%d%m%Y"))
    #     return {
    #         'name': "Export Anggaran Complete, total %s records" % i,
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'vit.export_anggaran',
    #         'view_mode': 'form',
    #         'view_type': 'form',
    #         'res_id': self.id,
    #         'views': [(False, 'form')],
    #         'target': 'new',
    #     }
    #     # raise UserError("Export %s record(s) Done!" % i)


    # def baris2(self, headers, csvwriter, rka):
    #     data = {
    #         'Kode': '',
    #         'Uraian': rka.unit_id.name,
    #         'Volume': '',
    #         'Satuan': '',
    #         'Harga': '',
    #         'Jumlah': rka.anggaran,
    #     }
    #     csvwriter.writerow([data[v] for v in headers])

    # def baris3(self, headers, csvwriter, td):
    #     data = {
    #         'Kode': td.tridharma_id.code,
    #         'Uraian': td.tridharma_id.name,
    #         'Volume': '',
    #         'Satuan': '',
    #         'Harga': '',
    #         'Jumlah': td.anggaran,
    #     }
    #     csvwriter.writerow([data[v] for v in headers])

    # def baris4(self, headers, csvwriter, kro):
    #     data = {
    #         'Kode': kro.category_id.code,
    #         'Uraian': kro.category_id.name,
    #         'Volume': '',
    #         'Satuan': '',
    #         'Harga': '',
    #         'Jumlah': kro.anggaran,
    #     }
    #     csvwriter.writerow([data[v] for v in headers])

    # def baris5(self, headers, csvwriter, ro):
    #     data = {
    #         'Kode': '',
    #         'Uraian': ro.indikator,
    #         'Volume': '',
    #         'Satuan': '',
    #         'Harga': '',
    #         'Jumlah': ro.anggaran,
    #     }
    #     csvwriter.writerow([data[v] for v in headers])

    # def baris6(self, headers, csvwriter, kom):
    #     data = {
    #         'Kode': kom.komponen_id.code,
    #         'Uraian': kom.komponen_id.name,
    #         'Volume': '',
    #         'Satuan': '',
    #         'Harga': '',
    #         'Jumlah': kom.total,
    #     }
    #     csvwriter.writerow([data[v] for v in headers])

    # def baris7(self, headers, csvwriter, sub):
    #     data = {
    #         'Kode': sub.subkomponen_id.code,
    #         'Uraian': sub.subkomponen_id.name,
    #         'Volume': '',
    #         'Satuan': '',
    #         'Harga': '',
    #         'Jumlah': sub.total,
    #     }
    #     csvwriter.writerow([data[v] for v in headers])

    # def baris8(self, headers, csvwriter, mak):
    #     data = {
    #         'Kode': mak.mak_id.code,
    #         'Uraian': mak.mak_id.name,
    #         'Volume': '',
    #         'Satuan': '',
    #         'Harga': '',
    #         'Jumlah': mak.total,
    #     }
    #     csvwriter.writerow([data[v] for v in headers])

    # def baris9(self, headers, csvwriter, det):
    #     data = {
    #         'Kode': '',
    #         'Uraian': det.keterangan,
    #         'Volume': det.jumlah,
    #         'Satuan': det.uom_volume,
    #         'Harga': det.tarif,
    #         'Jumlah': det.volume_total,
    #     }
    #     csvwriter.writerow([data[v] for v in headers])

    @api.multi
    def confirm_button(self):
        
        cr = self.env.cr

        headers = [
            "Kode",
            "Uraian",
            "Volume",
            "Satuan",
            "Harga",
            "Jumlah"
        ]


        mpath = get_module_path('anggaran_rka')

        # csvfile = open(mpath + '/static/fpk.csv', 'wb')
        csvfile = StringIO()
        csvwriter = csv.writer(csvfile, delimiter=';')
        csvwriter.writerow([h.upper() for h in headers])

        ang_obj = self.env['anggaran.rka']
        rkas = ang_obj.search([('id','=',self.rka_id.id)])

        i=0

        for rka in rkas:
            self.baris2(headers, csvwriter, rka)
            for keg in rka['rka_kegiatan_ids']:
                self.baris3(headers, csvwriter, keg)
                self.baris4(headers, csvwriter, keg)
                self.baris5(headers, csvwriter, keg)
                for mak in keg['rka_coa_ids']:
                    if mak.komponen_id:
                        self.baris6(headers, csvwriter, mak)
                    if mak.subkomponen_id:
                        self.baris7(headers, csvwriter, mak)
                    self.baris8(headers, csvwriter, mak)
                    for det in mak['rka_detail_ids']:
                        self.baris9(headers, csvwriter, det)
            
                    i+=1

        cr.commit()
        # csvfile.close()
        # _logger.info(csvfile.getvalue().encode() )
        self.export_file = base64.b64encode(csvfile.getvalue().encode())
        self.export_filename = 'Export Anggaran %s-%s.csv' % (self.unit_id.name,time.strftime("%d%m%Y"))
        return {
            'name': "Export Anggaran Complete, total %s records" % i,
            'type': 'ir.actions.act_window',
            'res_model': 'vit.export_anggaran',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'views': [(False, 'form')],
            'target': 'new',
        }
        # raise UserError("Export %s record(s) Done!" % i)


    def baris2(self, headers, csvwriter, rka):
        data = {
            'Kode': '',
            'Uraian': rka.unit_id.name,
            'Volume': '',
            'Satuan': '',
            'Harga': '',
            'Jumlah': rka.anggaran,
        }
        csvwriter.writerow([data[v] for v in headers])

    def baris3(self, headers, csvwriter, keg):
        data = {
            'Kode': keg.tridharma_id.code,
            'Uraian': keg.tridharma_id.name,
            'Volume': '',
            'Satuan': '',
            'Harga': '',
            'Jumlah': keg.anggaran,
        }
        csvwriter.writerow([data[v] for v in headers])

    def baris4(self, headers, csvwriter, keg):
        data = {
            'Kode': keg.category_id.code,
            'Uraian': keg.category_id.name,
            'Volume': '',
            'Satuan': '',
            'Harga': '',
            'Jumlah': keg.anggaran,
        }
        csvwriter.writerow([data[v] for v in headers])

    def baris5(self, headers, csvwriter, keg):
        data = {
            'Kode': '',
            'Uraian': keg.indikator,
            'Volume': '',
            'Satuan': '',
            'Harga': '',
            'Jumlah': keg.anggaran,
        }
        csvwriter.writerow([data[v] for v in headers])

    def baris6(self, headers, csvwriter, mak):
        data = {
            'Kode': mak.komponen_id.code,
            'Uraian': mak.komponen_id.name,
            'Volume': '',
            'Satuan': '',
            'Harga': '',
            'Jumlah': mak.total,
        }
        csvwriter.writerow([data[v] for v in headers])

    def baris7(self, headers, csvwriter, mak):
        data = {
            'Kode': mak.subkomponen_id.code,
            'Uraian': mak.subkomponen_id.name,
            'Volume': '',
            'Satuan': '',
            'Harga': '',
            'Jumlah': mak.total,
        }
        csvwriter.writerow([data[v] for v in headers])

    def baris8(self, headers, csvwriter, mak):
        data = {
            'Kode': mak.mak_id.code,
            'Uraian': mak.mak_id.name,
            'Volume': '',
            'Satuan': '',
            'Harga': '',
            'Jumlah': mak.total,
        }
        csvwriter.writerow([data[v] for v in headers])

    def baris9(self, headers, csvwriter, det):
        data = {
            'Kode': '',
            'Uraian': det.keterangan,
            'Volume': det.jumlah,
            'Satuan': det.uom_volume,
            'Harga': det.tarif,
            'Jumlah': det.volume_total,
        }
        csvwriter.writerow([data[v] for v in headers])