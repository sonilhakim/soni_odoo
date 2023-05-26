from odoo import tools
from odoo import fields, models, api
import odoo.addons.decimal_precision as dp
import time
import logging
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)

class sumber_dana(models.Model):
	_name 		= "anggaran.sumber_dana"

	code   = fields.Char("Kode")
	name   = fields.Char("Nama")

