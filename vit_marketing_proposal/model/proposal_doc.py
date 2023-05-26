#!/usr/bin/python
#-*- coding: utf-8 -*-
import time
from odoo import models, fields, api, _

class proposal_doc(models.Model):

    _name = "vit.proposal_doc"
    _description = "vit.proposal_doc"
    name = fields.Char( required=False, string="Description",  help="")
    doc = fields.Binary( string="Document Name",  help="")
    doc_name = fields.Char( string="Document Name",)
    date = fields.Date( string="Date", default=lambda self: time.strftime("%Y-%m-%d"), help="")


    proposal_id = fields.Many2one(comodel_name="vit.marketing_proposal",  string="Proposal",  help="")
