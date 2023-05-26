#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class doc_history(models.Model):

    _name = "vit.doc_history"
    _description = "vit.doc_history"
    name = fields.Char( required=True, string="Name",  help="")


    doc_id = fields.Many2one(comodel_name="vit.doc",  string="Doc",  help="")
    user_id = fields.Many2one(comodel_name="res.users",  string="User",  help="")
