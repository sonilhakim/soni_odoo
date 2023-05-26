# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
import datetime
import sys
import logging
_logger = logging.getLogger(__name__)
import pdb


class VitDataPengukurandesc(models.Model):
    _inherit = 'vit.data_pengukuran'

    description = fields.Text( 'Description', related="style_id.description", translate=True)