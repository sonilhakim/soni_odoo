from odoo import tools
from odoo import fields,models,api
from odoo.tools.translate import _
from odoo.exceptions import UserError


class MetodePengukuran(models.Model):
    _name = "vit.metode.pengukuran"
    _description = "vit.metode.pengukuran"

    name = fields.Char(string='Method Name', required=True)
    active = fields.Boolean(default=True, help="Set active to false to hide the method without removing it.")
    