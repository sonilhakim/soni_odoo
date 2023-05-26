from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_mitra_kerja = fields.Boolean('Is Mitra Kerja', default=False)

class PurchaseOrdermk(models.Model):
    _inherit = 'purchase.order'

    is_subcon = fields.Boolean('Subcon', related='partner_id.is_mitra_kerja', store=True)