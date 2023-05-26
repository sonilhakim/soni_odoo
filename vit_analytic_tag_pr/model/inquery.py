from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class inquery_garmen_analytic_tag(models.Model):

    _name = "vit.marketing_inquery_garmen"
    _inherit = "vit.marketing_inquery_garmen"

    analytic_tag_id = fields.Many2one('account.analytic.tag', string='Analytic Tag')


    @api.model
    def create(self, values):
        res = super(inquery_garmen_analytic_tag, self).create(values)
        # import pdb;pdb.set_trace()
        tag_name = '[' + res.name+ ']' +' '+ res.project
        analytic_tag = self.env['account.analytic.tag'].search([('name','=', tag_name)])
        data = []
        if analytic_tag:
            data = {'name': analytic_tag.name, 'company_id': res.company_id.id,}
        else:
            data = {'name': tag_name, 'company_id': res.company_id.id,}
        tag = analytic_tag.create(data)
        res.analytic_tag_id = tag.id
        return res
