#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class transaksi_cash(models.Model):

    _name = "vit.transaksi_cash"
    _description = "vit.transaksi_cash"
    name = fields.Char( string="Nama",  help="", )
    tanggal = fields.Date( string="Tanggal",  help="", )
    jumlah = fields.Float( string="Jumlah",  help="", )
    keterangan = fields.Char( string="Keterangan",  help="", )
    no_voucher = fields.Char( string="No voucher",  help="", )
    display_type = fields.Selection([('line_section', "Section"), ('line_note', "Note")], default=False, help="")
    sequence   = fields.Integer( default=1, help="")
    nomor   = fields.Integer(string="No.", compute='compute_nomor', store=True, help="")

    cash_in_out_id = fields.Many2one(comodel_name="vit.cash_in_out",  string="Cash in out",  help="", ondelete="cascade" )
    kode_transaksi = fields.Many2one(comodel_name="account.account",  string="Kode transaksi",  help="", )


    @api.depends('sequence')
    def compute_nomor(self):
    	for t in self:
    		if t.sequence:
    			t.nomor = t.sequence