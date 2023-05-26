from odoo import models, fields, api, _
from odoo.exceptions import UserError
import datetime
import sys
import logging
_logger = logging.getLogger(__name__)
import pdb


class VitProductRequest(models.Model):
	_inherit = "vit.product.request"

	sample_id = fields.Many2one('vit.sample_approval', string='Sample Approval')
