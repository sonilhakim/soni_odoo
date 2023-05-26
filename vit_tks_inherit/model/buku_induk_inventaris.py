#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft', 'Draft'),('open','Confirm'),('done','Done')]
from odoo import models, fields, api, _
import time
import datetime
from odoo.exceptions import UserError, Warning

class buku_induk_inventaris(models.Model):
    _name = "vit.buku_induk_inventaris"
    _inherit = "vit.buku_induk_inventaris"

    date  = fields.Date(string="Tanggal Pembukuan", required=False, default=lambda self:time.strftime("%Y-%m-%d"))
    status = fields.Selection(selection=[('draft', 'Draft'), ('confirm', 'Confirm'), ('open', 'Running'), ('close', 'Close')],  string="Status Inventaris",  readonly=True, states={"draft" : [("readonly",False)]},  help="")

    @api.model
    def create(self, vals):
        if not vals.get("name", False) or vals["name"] == "New":
            vals["name"] = self.env["ir.sequence"].next_by_code("vit.buku_induk_inventaris") or "Error Number!!!"
        return super(buku_induk_inventaris, self).create(vals)

    def action_confirm(self):
        self.state = STATES[1][0]

    def action_done(self):
        self.state = STATES[2][0]

    def action_draft(self):
        self.state = STATES[0][0]

    @api.multi
    def unlink(self):
        for me_id in self :
            if me_id.state != STATES[0][0]:
                raise UserError("Cannot delete non draft record!")
        return super(buku_induk_inventaris, self).unlink()

    def action_reload(self, ):
        sql = "delete from vit_buku_induk_inventaris_detail where buku_induk_id = %s"
        self.env.cr.execute(sql, (self.id,))
        sql = """
                insert into vit_buku_induk_inventaris_detail (name, code, type, jumlah, satuan, tahun_pembuatan, asal, kelengkapan_dokumen, tanggal_penyerahan_barang, kondisi, harga, buku_induk_id)
                select ast.name, ast.code, ast.tipe_barang, ast.qty, ast.satuan_id, ast.tahun_pembuatan, ast.asal, ast.kelengkapan_dokumen, ast.tgl_penyerahan_brg, ast.condition, ast.value, %s
                from account_asset_asset ast
                left join account_asset_category cat on ast.category_id = cat.id
                left join account_asset_category par on cat.parent_id = par.id
                left join account_asset_category pare on par.parent_id = pare.id
                left join account_asset_category parent on pare.parent_id = parent.id
                where ast.asset_id is null and parent.name = %s
                """
        if self.status:
                sql += " and ast.state = '%s' " %self.status
        # if self.kategori_id:
        #     sql += ' and ast.category_id = %s ' %self.kategori_id.id
        # if self.lokasi_id:
        #     sql += ' and ast.last_location_id = %s ' %self.lokasi_id.id

        self.env.cr.execute(sql, (self.id,'Inventaris'))

