# -*- coding: utf-8 -*-

import time
from datetime import datetime, timedelta
import dateutil.parser
from dateutil import relativedelta
import pytz
from odoo import api, models, fields, _
import base64
import io
# import barcode
# from barcode.writer import ImageWriter
try:
    import qrcode

except ImportError:
    _logger.debug('ImportError')


class StickerPolybagStoreWizard(models.TransientModel):
    _name = "sticker.polybag.store.wizard"

    wizard_polybags    = fields.One2many('sticker.polybag.wizard.line', 'sp_wiz_id', string='SP Wizard')


    @api.multi
    def _compute_w_lines(self):
        # import pdb;pdb.set_trace()
        store_id = self._context.get('active_id', False)
        if store_id:
            str_obj = self.env['vit.kasir_store']
            store = str_obj.browse(store_id)
            sql = """SELECT pk.id, ksl.polybag_target
                FROM vit_kasir_store_line ksl
                LEFT JOIN vit_kasir_store ks ON ksl.store_id = ks.id
                LEFT JOIN vit_pengukuran_karyawan pk ON ksl.pengukuran_karyawan_target = pk.id
                WHERE ks.id = %s
                GROUP BY pk.id, ksl.polybag_target
                """
            self.env.cr.execute(sql, (store.id,))
            result = self.env.cr.fetchall()
            polybag_ids = []
            for res in result:
                polybag_ids.append((0,0,{
                        'pengukuran_karyawan'   : res[0],
                        'polybag'               : res[1],
                    }))

            data = {
                'wizard_polybags': polybag_ids,
            }
            self.write(data)
   
    @api.multi
    def action_print_report(self):
        self._compute_w_lines()
        report_action = self.env.ref(
            'vit_kasir_store.report_sticker_polybag_store'
        ).report_action(self)
        report_action['close_on_report_download']=True

        return report_action

StickerPolybagStoreWizard()

class StickerPolybagWizardLine(models.TransientModel):
    _name = "sticker.polybag.wizard.line"

    pengukuran_karyawan = fields.Many2one('vit.pengukuran_karyawan', 'Pengukuran Karyawan')
    polybag = fields.Char(string="Polybag")
    sp_wiz_id = fields.Many2one('sticker.polybag.store.wizard', 'SP Wizard')
    qr_code = fields.Binary('QR Code', compute="_generate_qr_code")

    @api.one
    @api.depends('polybag')
    def _generate_qr_code(self):
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=20, border=4)
        if self.polybag :
            qr.add_data(self.polybag)
            qr.make(fit=True)
            img = qr.make_image()
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            qrcode_img = base64.b64encode(buffer.getvalue())
            self.update({'qr_code': qrcode_img,})
            
        # try:
        #     barcode = self.env['ir.actions.report'].barcode('Code128', self.nik, width=300, height=50,humanreadable=0)
        # except (ValueError, AttributeError):
        #     raise UserWarning('Cannot convert into barcode.')
        # barcode = base64.b64encode(barcode)
        # self.qr_code = barcode
        
        # barcode_format = barcode.get_barcode_class('code128')
        # my_barcode  = barcode_format(self.polybag, writer=ImageWriter())
        # barcode_png = my_barcode.save('barcode')
        # with open(barcode_png, "rb") as imageFile:
        #     x_barcode = base64.b64encode(imageFile.read())
        #     self.update({'qr_code': x_barcode ,})

StickerPolybagWizardLine()