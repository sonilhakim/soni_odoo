#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.osv import expression
from odoo.exceptions import UserError, Warning

class kpi_aspek(models.Model):
    _name = "vit.kpi_aspek"
    _description = "vit.kpi_aspek"
    _order = "code"

    name = fields.Char( required=True, string="Name", index=True,  help="")
    code = fields.Char( string="Code", required=True, index=True, help="")
    not_include = fields.Boolean( "Not Included", help="If true, aspek not included in Total KPI") 

    company_id    = fields.Many2one( comodel_name="res.company",  string="Company", required=True, index=True, default=lambda self: self.env.user.company_id.id)
    parent_aspek_id = fields.Many2one(comodel_name="vit.kpi_aspek",  string="Parent Aspek",  help="")

    _sql_constraints = [
        ('code_per_company_uniq', 'unique (code,company_id)', 'The code of the aspek must be unique per company !')
    ]

    @api.model
    def default_get(self, default_fields):
        default_name = self._context.get('default_name')
        default_code = self._context.get('default_code')
        if default_name and not default_code:
            try:
                default_code = int(default_name)
            except ValueError:
                pass
            if default_code:
                default_name = False
        contextual_self = self.with_context(default_name=default_name, default_code=default_code)
        return super(kpi_aspek, contextual_self).default_get(default_fields)


    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('code', '=ilike', name.split(' ')[0] + '%'), ('name', operator, name)]
            if operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = ['&', '!'] + domain[1:]
        account_ids = self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)
        return self.browse(account_ids).name_get()


    @api.multi
    def name_get(self):
        result = []
        for aspek in self:
            name = aspek.code + ' ' + aspek.name
            result.append((aspek.id, name))
        return result

