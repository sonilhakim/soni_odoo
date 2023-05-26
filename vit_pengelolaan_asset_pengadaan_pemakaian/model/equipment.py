# -*- coding: utf-8 -*-

from datetime import date, datetime, timedelta

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT

class MaintenanceEquipmentPemakaian(models.Model):
    _name = 'maintenance.equipment'
    _inherit = 'maintenance.equipment'

    aset_id = fields.Many2one(comodel_name="account.asset.asset",  string="Aset",  help="")
    pemakaian_id = fields.Many2one(comodel_name="vit.pemakaian_aset",  string="Pemakaian",  help="")
    kategori_id = fields.Many2one(comodel_name="account.asset.category",  string="Kategori Aset",  help="")
    unit_kerja_id = fields.Many2one(comodel_name="vit.unit_kerja",  string="SUBSATKER",  track_visibility='onchange')
    location_id = fields.Many2one(comodel_name="vit.location", string="Digunakan di Lokasi", track_visibility='onchange')
    asset_assign_to = fields.Selection(
        [('subsatker', 'SUBSATKER'), ('employee', 'Employee'), ('other', 'Other')],
        string='Used By',
        required=True,
        default='employee')

    @api.model
    def create(self, vals):
        res = super(MaintenanceEquipmentPemakaian, self).create(vals)
        asset = self.env['account.asset.asset'].search([('id','=', vals["aset_id"])])
        asset.update({
            'pemakai_id': vals["employee_id"],
            'last_location_id': vals["location_id"],
            'unit_kerja_pemakai_id': vals["unit_kerja_id"],
            'used': 'sudah',
            })
        return res

    @api.onchange('aset_id')
    def onchange_name(self):
        for eq in self:
            eq.name = eq.aset_id.name
            eq.kategori_id = eq.aset_id.category_id.id
            eq.partner_id = eq.aset_id.partner_id.id
            eq.warranty_date = eq.aset_id.warranty_date
    
    @api.onchange('equipment_assign_to')
    def _onchange_equipment_assign_to(self):
        if self.equipment_assign_to == 'employee':
            self.unit_kerja_id = False
        if self.equipment_assign_to == 'subsatker':
            self.employee_id = False
        self.assign_date = fields.Date.context_today(self)
  