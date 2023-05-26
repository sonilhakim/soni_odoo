# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import Warning, UserError
import time
from datetime import datetime
import logging
_logger = logging.getLogger(__name__)

class MrpProductionMD(models.Model):
    _inherit = "mrp.production"

    # @api.onchange('company_id')
    # def _onchange_company_id(self):
    @api.multi
    def load_gm_reporting(self, ):
        for pro in self:
            item_report = self.env['vit.item_reporting'].sudo().search([])
            final_line = []
            line = []
            for record in item_report:
                line = [0, 0, {
                    "no": record.no,
                    "name": record.name,
                }]
                final_line.append(line)
            pro.gm_report_ids = final_line
            pro.default_gm_reporting = True

    gm_report_ids = fields.One2many("vit.gm_reporting", 'mrp_pro_id', 'GM Reporting', readonly=True, states={'confirmed': [('readonly', False)]})
    default_gm_reporting = fields.Boolean('Default GM Reporting')

class VitItemReporting(models.Model):
    _name = 'vit.item_reporting'
    _description = 'Item Reporting'

    name        = fields.Char(string='Item')
    no          = fields.Integer('No')

class VitGMreporting(models.Model):
    _name = 'vit.gm_reporting'
    _description = 'GM Reporting'    

    name        = fields.Char(string='Item')
    doc         = fields.Binary( string="Attachment",  help="")
    doc_name    = fields.Char( string="Document Name",)
    date        = fields.Date( string="Tgl", required=False, default=lambda self: time.strftime("%Y-%m-%d"), help="")
    notes       = fields.Text('Keterangan')
    no          = fields.Integer('No')
    mrp_pro_id  = fields.Many2one("mrp.production", "Worksheet")
