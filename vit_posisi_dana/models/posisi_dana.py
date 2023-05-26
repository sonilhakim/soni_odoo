# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import Warning, UserError
import time
from datetime import date, datetime
import logging
_logger = logging.getLogger(__name__)

class PosisiDana(models.Model):
    _name = 'vit.posisi_dana'
    _description = 'vit.posisi_dana'

    name      = fields.Char(string='Posisi Dana')
    html      = fields.Html('HTML')
    

class PosisiDanaConf(models.Model):
    _name = 'vit.posisi_dana_config'
    _description = 'vit.posisi_dana_config'

    name = fields.Selection([('order_receive', 'Order Receive'), ('purchasing', 'PO Purchasing'), ('mitra_kerja', 'PO Mitrakerja'), ('aksep', 'Hutang Bank'), ('saldo', 'Saldo Bank'), ('piutang', 'Piutang Berjalan')], string='Posisi Keuangan')
    account_ids = fields.Many2many('account.account', string= 'Accounts')