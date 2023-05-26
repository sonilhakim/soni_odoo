from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class Refpendapat(models.Model):
    _name = "vit.pendapat"
    _inherit = "vit.pendapat"

    jenis_pendapatan_lain = fields.Many2one( "vit.jenis_pendapatan_lain","Jenis Pendapatan Lain",  help="")