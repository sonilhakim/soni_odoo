from odoo import models, fields, api, _
from odoo.exceptions import UserError
import datetime
import sys
import logging
_logger = logging.getLogger(__name__)
import pdb
from odoo.addons.terbilang import terbilang


class AccountInvoiceReportCustom(models.Model):
    _name = 'account.invoice'
    _inherit = 'account.invoice'

    terbilang = fields.Text(string='Terbilang', compute='_get_terbilang', store=True)
    surat_jalan = fields.Char(string='Surat Jalan')
    so_vendor = fields.Char(string='SO Vendor')
    efaktur = fields.Char(string="Faktur Pajak", required=False, )
    ttd = fields.Many2one(comodel_name="res.users", string="Penandatangan", required=False)
    reference = fields.Char(string='Payment Ref.', copy=False,
        help='The payment communication that will be automatically populated once the invoice validation. You can also write a free communication.')


    @api.multi
    @api.depends('amount_total', 'currency_id')
    def _get_terbilang(self):
        for rec in self:
            rec.terbilang = terbilang.terbilang(rec.amount_total, rec.currency_id.name, "id")

    @api.model
    def create(self, vals):
        record = super(AccountInvoiceReportCustom, self).create(vals)
        # import pdb; pdb.set_trace()
        for rec in record:
            if rec.stock_picking_id:
                sql = """SELECT sp.name
                    FROM account_invoice_line il
                    LEFT JOIN stock_picking sp ON il.picking_id = sp.id
                    LEFT JOIN account_invoice iv On il.invoice_id = iv.id
                    WHERE iv.id = %s
                    GROUP BY sp.id
                    """
                self.env.cr.execute(sql, (rec.id,))
                result = self.env.cr.fetchall()
                sj_list = []
                for res in result:
                    sj_list.append(res[0])
                sj = ', '.join(sj_list)
                sql1 = """UPDATE account_invoice set surat_jalan = %s WHERE id = %s"""
                self.env.cr.execute(sql1, (sj, rec.id,))
                # rec.surat_jalan = sj
        return record

    @api.multi
    def write(self, vals):
        for rec in self:
            res = super(AccountInvoiceReportCustom, self).write(vals)
            if rec.stock_picking_id:
                sql = """SELECT sp.name
                    FROM account_invoice_line il
                    LEFT JOIN stock_picking sp ON il.picking_id = sp.id
                    LEFT JOIN account_invoice iv On il.invoice_id = iv.id
                    WHERE iv.id = %s
                    GROUP BY sp.id
                    """
                self.env.cr.execute(sql, (rec.id,))
                result = self.env.cr.fetchall()
                sj_list = []
                for res in result:
                    sj_list.append(res[0])
                sj = ', '.join(sj_list)
                sql1 = """UPDATE account_invoice set surat_jalan = %s WHERE id = %s"""
                self.env.cr.execute(sql1, (str(sj), rec.id,))
                # rec.surat_jalan = sj
            return res

AccountInvoiceReportCustom()


class ResPartnerBankCabang(models.Model):
    _inherit = 'res.partner.bank'

    cabang = fields.Char('Cabang',)


ResPartnerBankCabang()
