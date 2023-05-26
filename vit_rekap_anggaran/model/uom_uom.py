#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class uom_uom(models.Model):

    _name = "uom.uom"
    _description = "uom.uom"

    _inherit = "uom.uom"


