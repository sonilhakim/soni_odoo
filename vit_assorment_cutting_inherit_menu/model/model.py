# -*- coding: utf-8 -*-
import time
from odoo import models, fields, api
import csv
from odoo.modules import get_module_path
from odoo.exceptions import UserError
from xlrd import open_workbook
import copy
import pdb
import xlwt
import logging
from io import StringIO
import base64
_logger = logging.getLogger(__name__)

class boq_po_garmen_ac(models.Model):
    _name = 'vit.boq_po_garmen_line'
    _inherit = 'vit.boq_po_garmen_line'

    @api.multi
    def import_excel(self):
        data = base64.b64decode(self.import_file)
        wb = open_workbook(file_contents=data)
        all_datas = []
        for s in wb.sheets():
            for row in range(s.nrows):
                data_row = []
                for col in range(s.ncols):
                    value = (s.cell(row, col).value)
                    data_row.append(value)
                all_datas.append(data_row)
        