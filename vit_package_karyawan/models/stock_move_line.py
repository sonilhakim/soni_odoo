from odoo import api, fields, models, tools, _


class StockMoveLineKaryawan(models.Model):
    _inherit = "stock.move.line"

    nama_karyawan = fields.Char( string="Karyawan", related="lot_id.karyawan", store=True,)
