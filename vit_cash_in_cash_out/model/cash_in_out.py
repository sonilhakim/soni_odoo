#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft','Draft'),('open','Confirmed'),('done','Done'),('cancel','Cancel')]
from odoo import models, fields, api, _
import time
from datetime import datetime
from odoo.exceptions import UserError, Warning

class cash_in_out(models.Model):

    _name = "vit.cash_in_out"
    _description = "vit.cash_in_out"
    _inherit = ['mail.thread']

    name = fields.Char( required=True, default="New", readonly=True,  string="Name",  help="", )
    tanggal = fields.Date( string="Tanggal", required=True, default=lambda self:time.strftime("%Y-%m-%d"), readonly=True, states={"draft" : [("readonly",False)]},  help="", )
    state = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",  help="", )
    keterangan = fields.Text( string="Keterangan",  readonly=True, states={"draft" : [("readonly",False)]},  help="", )
    saldo_awal = fields.Float( string="Saldo Awal", default=1000000.0, help="", )
    saldo_akhir = fields.Float( string="Saldo Akhir", compute='compute_saldo_akhir', store=True, help="", )


    @api.model
    def create(self, vals):
        if not vals.get("name", False) or vals["name"] == "New":
            tanggal = datetime.strptime(vals["tanggal"], '%Y-%m-%d')
            # vals["name"] = self.env["ir.sequence"].next_by_code("vit.cash_in_out") + "/" + vals["tanggal"] or "Error Number!!!"
            vals["name"] = "CASH" + "/" + "IN" + "/" + "OUT" + "/" + tanggal.strftime('%d-%m-%Y') or "Error Number!!!"
        return super(cash_in_out, self).create(vals)

    @api.multi
    def action_confirm(self):
        self.action_reload()
        self.state = STATES[1][0]

    @api.multi
    def action_done(self):
        self.state = STATES[2][0]

    @api.multi
    def action_cancel(self):
        self.env.cr.execute("delete from vit_transaksi_cash where cash_in_out_id = %s"%(self.id,))
        self.state = STATES[3][0]

    @api.multi
    def action_draft(self):
        self.state = STATES[0][0]

    @api.multi
    def unlink(self):
        for me_id in self :
            if me_id.state != STATES[0][0]:
                raise UserError("Cannot delete non draft record!")
        return super(cash_in_out, self).unlink()

    transaksi_ids = fields.One2many(comodel_name="vit.transaksi_cash",  inverse_name="cash_in_out_id",  string="Transaksis",  readonly=True, states={"draft" : [("readonly",False)]},  help="", )
    kasir_id = fields.Many2one(comodel_name="res.users", string="Kasir", required=True, default=lambda self: self.env.uid, readonly=True, states={"draft" : [("readonly",False)]},  help="", )

    _sql_constraints = [
        ('tanggal_uniq', 'unique (tanggal)', 'Tanggal ini sudah ada di dokumen lain!')
    ]


    @api.multi
    def action_reload(self):
        for rec in self:
            transaksi = self.env['vit.transaksi_cash']
            sqld = "delete from vit_transaksi_cash where cash_in_out_id = %s"
            self.env.cr.execute(sqld, (rec.id,))

            # self.env['vit.transaksi_cash'].create({
            #                                         'name' : 'Saldo Awal',
            #                                         'tanggal' : rec.tanggal,
            #                                         'jumlah' : rec.saldo_awal,
            #                                         'cash_in_out_id' : rec.id,
            #                                         })

            sql = """
                SELECT aml.date, aa.id, aml.name, aml.balance, aml.ref
                FROM account_move_line aml
                LEFT JOIN account_account aa ON aml.account_id = aa.id
                LEFT JOIN account_move am ON aml.move_id = am.id
                LEFT JOIN account_move_line amj ON amj.move_id = am.id
                LEFT JOIN account_account aaj ON amj.account_id = aaj.id
                LEFT JOIN account_journal aj ON aj.default_debit_account_id = aaj.id
                WHERE aml.date = %s AND am.state = 'posted' AND aa.id != aaj.id AND aj.type = 'cash'
                """
            cr = self.env.cr
            cr.execute(sql, (rec.tanggal,))
            result = cr.fetchall()
            trans_ids = []
            i = 1
            for res in result:
                trans_ids.append((0,0,{
                                'sequence' : i,
                                'tanggal' : res[0],
                                'kode_transaksi' : res[1],
                                'name' : res[2],
                                'jumlah' : (res[3] * -1),
                                'no_voucher': res[4],
                                }))
                i+=1

            rec.write({ 'transaksi_ids' : trans_ids, })


    @api.depends('transaksi_ids.jumlah')
    def compute_saldo_akhir(self):
        for rec in self:
            for tr in rec.transaksi_ids:
                if tr.jumlah:
                    total_transaksi = sum( t.jumlah for t in rec.transaksi_ids)
                    rec.saldo_akhir = rec.saldo_awal + total_transaksi