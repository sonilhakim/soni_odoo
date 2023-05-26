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

class export_bmn(models.TransientModel):
    _name = 'vit.export_bmn'

    export_file = fields.Binary(string="Export File",  )
    export_filename = fields.Char(string="Export File",  )

    @api.multi
    def confirm_button(self):
        cr = self.env.cr

        headers = [
            "Nama",
            "Kategori",
            "Referensi",
            "Status Kepemilikan",
            "Kuantitas",
            "Nilai Kotor",
        ]


        mpath = get_module_path('account_asset_asset')

        # csvfile = open(mpath + '/static/fpk.csv', 'wb')
        csvfile = StringIO()
        csvwriter = csv.writer(csvfile, delimiter=';')
        csvwriter.writerow([h.upper() for h in headers])

        ass_obj = self.env['account.asset.asset']
        assets = ass_obj.search([('asset_id','=',False)])

        i=0

        for aset in assets:
            self.baris2(headers, csvwriter, aset)            
            i+=1

        cr.commit()
        # csvfile.close()
        # _logger.info(csvfile.getvalue().encode() )
        self.export_file = base64.b64encode(csvfile.getvalue().encode())
        self.export_filename = 'Export BMN %s.csv' % (time.strftime("%d%m%Y"))
        return {
            'name': "Export BMN Complete, total %s records" % i,
            'type': 'ir.actions.act_window',
            'res_model': 'vit.export_bmn',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'views': [(False, 'form')],
            'target': 'new',
        }
        # raise UserError("Export %s record(s) Done!" % i)


    def baris2(self, headers, csvwriter, aset):
        data = {
            'Nama': aset.name,
            'Kategori': aset.category_id.name,
            'Referensi': aset.code,
            'Status Kepemilikan': aset.status_kepemilikan,
            'Kuantitas': aset.qty,
            'Nilai Kotor': aset.value,
        }
        csvwriter.writerow([data[v] for v in headers])
