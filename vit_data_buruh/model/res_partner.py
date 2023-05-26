#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class res_partner(models.Model):

    _name = "res.partner"
    _description = "res.partner"

    _inherit = "res.partner"


    buruh = fields.Boolean(string="Buruh",  help="", )
