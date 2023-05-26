#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class to_user(models.Model):

    _name = "vit.to_user"
    _description = "vit.to_user"
    name = fields.Char( required=True, string="Name",  help="")
    read_status = fields.Boolean( string="Read status",  help="")


    doc_id = fields.Many2one(comodel_name="vit.doc",  string="Doc",  help="")
    user_id = fields.Many2one(comodel_name="res.users",  string="User",  help="")
