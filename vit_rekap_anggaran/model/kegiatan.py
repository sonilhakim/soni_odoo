#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class kegiatan(models.Model):

    _name = "anggaran.kegiatan"
    _description = "anggaran.kegiatan"

    _inherit = "anggaran.kegiatan"


