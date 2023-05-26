#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft','Draft'),('open','Confirmed'),('done','Done'),('cancel','Cancel')]
from odoo import models, fields, api, _
import time
from datetime import datetime
from odoo.exceptions import UserError, Warning

class rekap_data_buruh(models.Model):

    _name = "vit.rekap_data_buruh"
    _description = "vit.rekap_data_buruh"
    _inherit = ['mail.thread']

    name = fields.Char( required=True, default="New", readonly=True,  string="Name",  help="", )
    start_date = fields.Date( string="Start date", required=True, default=lambda self:time.strftime("%Y-%m-%d"), readonly=True, states={"draft" : [("readonly",False)]},  help="", )
    end_date = fields.Date( string="End date", required=True, readonly=True, states={"draft" : [("readonly",False)]},  help="", )
    total_upah = fields.Float( string="Total Upah", readonly=True, states={"draft" : [("readonly",False)]},  help="", )
    note = fields.Text( string="Keterangan",  readonly=True, states={"draft" : [("readonly",False)]},  help="", )
    state = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",  help="", )
    count_daftar = fields.Integer(string='Hitung Daftar', compute='_get_daftar')


    @api.model
    def create(self, vals):
        if not vals.get("name", False) or vals["name"] == "New":
            vals["name"] = self.env["ir.sequence"].next_by_code("vit.rekap_data_buruh") or "Error Number!!!"
        return super(rekap_data_buruh, self).create(vals)

    def action_confirm(self):
        self._compute_total_upah()
        self.load_data()
        self.state = STATES[1][0]

    def action_done(self):
        self.state = STATES[2][0]

    def action_cancel(self):
        sqld = "delete from vit_rekap_daftar_buruh where rekap_data_id = %s"
        self.env.cr.execute(sqld, (self.id,))
        self.state = STATES[3][0]

    def action_draft(self):
        self.state = STATES[0][0]

    @api.multi
    def unlink(self):
        for me_id in self :
            if me_id.state != STATES[0][0]:
                raise UserError("Cannot delete non draft record!")
        return super(rekap_data_buruh, self).unlink()

    rekap_daftar_ids = fields.One2many(comodel_name="vit.rekap_daftar_buruh",  inverse_name="rekap_data_id",  string="Rekap daftars",  readonly=True, states={"draft" : [("readonly",False)],"open" : [("readonly",False)]},  help="", )
    user_id = fields.Many2one(comodel_name="res.users", string="User", required=True, default=lambda self: self.env.uid, readonly=True, states={"draft" : [("readonly",False)]},  help="", )

    def _get_daftar(self):
        for rec in self:
            daftar_ids = self.env['vit.rekap_daftar_buruh'].search([('rekap_data_id','=',rec.id)])
            if daftar_ids:
                rec.count_daftar = len(set(daftar_ids.ids))

    # @api.onchange('end_date')
    def _compute_total_upah(self):
        for rec in self :
            product = self.env['product.product'].search([('name', 'in', ('Ongkos Bongkar','Ongkos Muat','Ongkos Bongkar Muat','Ongkos Oper')), ('type', '=', 'service')])
            result = 0.0
            if rec.end_date:
                # import pdb;pdb.set_trace()
                sql = """
                    SELECT sum(ail.price_subtotal)
                    FROM account_invoice_line ail
                    LEFT JOIN account_invoice ai ON ail.invoice_id = ai.id
                    WHERE ai.date Between %s AND %s AND ail.product_id IN %s AND ai.type = 'in_invoice' 
                    """
                self.env.cr.execute(sql, (rec.start_date,rec.end_date, (tuple(product.ids,))))
                result = self.env.cr.fetchone()
            if result:
                rec.total_upah = result[0]


    @api.multi
    def load_data(self):
        for rec in self :
            sqld = "delete from vit_rekap_daftar_buruh where rekap_data_id = %s"
            self.env.cr.execute(sqld, (rec.id,))

            sql = """
                SELECT rp.id, sum(bl.uang_makan), sum(bl.potongan), count(bl.id)
                FROM vit_daftar_buruh bl
                LEFT JOIN vit_data_buruh db ON bl.data_buruh_id = db.id
                LEFT JOIN res_partner rp ON bl.buruh_id = rp.id
                WHERE db.tanggal Between %s AND %s AND db.state = 'done'
                GROUP BY rp.id
                """
            self.env.cr.execute(sql, (rec.start_date,rec.end_date,))
            result = self.env.cr.fetchall()
            details = []
            for res in result:
                # import pdb;pdb.set_trace()
                details.append((0,0,{
                                'buruh_id'  : res[0],
                                'potongan'  : res[1] + res[2],
                                'hadir'     : res[3],
                                }))

            rec.write({ 'rekap_daftar_ids' : details, })


    @api.multi
    def compute_upah(self):
        for rec in self :
            upah = 0.0
            with_mandor = self.env['vit.rekap_daftar_buruh'].search([('rekap_data_id','=',rec.id),('mandor','=',True)])
            not_mandor = self.env['vit.rekap_daftar_buruh'].search([('rekap_data_id','=',rec.id),('mandor','=',False)])
            pembagi = sum(l.hadir for l in rec.rekap_daftar_ids)
            pembagi_m = sum(l.hadir for l in not_mandor)
            # import pdb;pdb.set_trace()
            if with_mandor:
                persen_mandor = rec.total_upah * 20 / 100
                upah = (rec.total_upah - persen_mandor) / pembagi_m
            else:
                upah = rec.total_upah / pembagi

            for line in rec.rekap_daftar_ids:
                if line.mandor:
                    line.upah = round(persen_mandor)
                    line.total = round(persen_mandor - line.potongan)
                else:
                    line.upah = round(upah * line.hadir)
                    line.total = round(upah - line.potongan)