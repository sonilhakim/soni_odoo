port models, fields, api, _
from odoo.exceptions import UserError
import time
import datetime
from datetime import datetime, timedelta
import dateutil.parser
import pytz
import sys
import logging
_logger = logging.getLogger(__name__)
import pdb

class RekapPembelianCash(models.Model):
    _name          = 'vit.rekap_pembelian_cash'
    _description   = 'vit.rekap_pembelian_cash'

    name            = fields.Char(string='Name')
    
    current_date    = datetime.date.today()
    date_start      = fields.Date(string='Start Date', required=True)
    date_end        = fields.Date(string='End Date', required=True)

    # partner_id        = fields.Many2one(comodel_name="res.partner", string="Vendor", default=lambda self: self.env.uid, track_visibility='onchange', readonly=True)
    user_id               = fields.Many2one(comodel_name="res.users", string="User", default=lambda self: self.env.uid, track_visibility='onchange', readonly=True)
    company_id            = fields.Many2one(comodel_name="res.company",  string="Company", related='user_id.company_id', readonly=True,  help="")
    commercial_partner_id = fields.Many2one(comodel_name="res.partner", string="Vendor", default=lambda self: self.env.uid, track_visibility='onchange', readonly=True)
    user_obj              = self.env['res.users'].search([('id', '=', data['context']['uid'])])

    @api.multi
    def action_reload(self, ):
        sql = "delete from vit_remunerasi_pegawai_ids where remunerasi_id = %s"
        self.env.cr.execute(sql, (self.id,))
        sql = """
                insert into vit_remunerasi_pegawai_ids (karyawan_id, remunerasi_id)
                select id, %s
                from hr_employee
                """
        self.env.cr.execute(sql, (self.id,))

class RekapPembelianCashLine(models.Model):
    _name = 'vit.rekap_pembelian_cash_line'
    _description = "vit.rekap_pembelian_cash_line"