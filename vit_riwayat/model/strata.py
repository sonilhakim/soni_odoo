#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _

class strata(models.Model):

    _name = "vit.strata"
    _description = "vit.strata"
    name = fields.Char( required=True, string="Name",  help="")


