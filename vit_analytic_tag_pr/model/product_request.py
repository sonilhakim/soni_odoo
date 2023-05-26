from odoo import tools
from odoo import fields,models,api

class ProductRequestAtag(models.Model):
    _name           = "vit.product.request"
    _inherit        = "vit.product.request"

    analytic_tag_id = fields.Many2one('account.analytic.tag', string='Analytic Tag')

    @api.model
    def create(self, values):
        res = super(ProductRequestAtag, self).create(values)
        # import pdb;pdb.set_trace()
        cr = self.env.cr
        if res.partner_id and res.project_description:
            sql = """SELECT tag.id
                FROM vit_marketing_inquery_garmen iq
                LEFT JOIN account_analytic_tag tag ON iq.analytic_tag_id = tag.id
                WHERE iq.partner_id = %s AND iq.project = %s
                """
            cr.execute(sql, (res.partner_id.id,res.project_description))
            analytic_tag = cr.fetchall()
            for tag in analytic_tag:
                res.analytic_tag_id = tag[0]
        return res


    def action_create_pr(self):
        res = super(ProductRequestAtag, self).action_create_pr()
        for pr in self:
            if pr.analytic_tag_id:
                purchase_requisition_line = self.env['purchase.requisition.line'].search([('requisition_id','=',res.id)])
                for pl in purchase_requisition_line:
                    pl.analytic_tag_ids = [(6,0,[pr.analytic_tag_id.id])]

                return res