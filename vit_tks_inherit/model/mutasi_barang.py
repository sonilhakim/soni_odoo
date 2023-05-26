#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft', 'Draft'),('open','Confirm'),('done','Done')]
from odoo import models, fields, api, _
import time
import datetime
from odoo.exceptions import UserError, Warning

class mutasi_barang(models.Model):
    _name = "vit.mutasi_barang"
    _inherit = "vit.mutasi_barang"

    date  = fields.Date(string="Tanggal Pembukuan", required=False,
                              default=lambda self:time.strftime("%Y-%m-%d"))

    @api.model
    def create(self, vals):
        if not vals.get("name", False) or vals["name"] == "New":
            vals["name"] = self.env["ir.sequence"].next_by_code("vit.mutasi_barang") or "Error Number!!!"
        return super(mutasi_barang, self).create(vals)

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
        return super(mutasi_barang, self).unlink()

    def action_reload(self, ):
        sql = "delete from vit_mutasi_detail where mutasi_id = %s"
        self.env.cr.execute(sql, (self.id,))
        sql = """
                insert into vit_mutasi_detail (name, kode_barang, type, no_sertifikat, asal, tahun_perolehan, kondisi, lokasi_awal, lokasi_akhir, keterangan, transfer_id, mutasi_id)
                select ast.name, ast.code, ast.tipe_barang, ast.number, ast.asal, ast.tahun_pembuatan, ast.condition, loc.name, lok.name, tl.description, tf.id, %s
                from vit_transfer_line tl
                left join vit_transfer tf on tl.transfer_id = tf.id
                left join account_asset_asset ast on tl.asset_id = ast.id
                left join vit_location loc on tf.location_id = loc.id
                left join vit_location lok on tf.location_dest_id = lok.id
                where tf.date > %s and tf.date < %s and tf.state = %s
                """            
        self.env.cr.execute(sql, (self.id, self.start_date, self.end_date, 'done'))

