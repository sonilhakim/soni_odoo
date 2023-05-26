from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ProductionLotUkur(models.Model):
    _name = 'stock.production.lot'
    _inherit = 'stock.production.lot'

    pengukuran_karyawan = fields.Many2one('vit.pengukuran_karyawan', 'Pengukuran')