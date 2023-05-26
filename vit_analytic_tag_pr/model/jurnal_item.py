from odoo import api, fields, models, _
from odoo.exceptions import UserError

class AccountMoveLineAT(models.Model):
    _name = "account.move.line"
    _inherit = "account.move.line"

    @api.model
    def create(self, values):
        res = super(AccountMoveLineAT, self).create(values)
        # import pdb;pdb.set_trace()
        cr = self.env.cr
        if res.move_id.ref and res.move_id.journal_id.name == 'Stock Journal':
            sql = """SELECT tag.id
                FROM stock_move sm
                LEFT JOIN account_analytic_tag tag ON sm.analytic_tag_id = tag.id
                LEFT JOIN stock_picking sp ON sm.picking_id = sp.id
                WHERE sp.name = %s AND sm.analytic_tag_id IS NOT NULL
                """
            cr.execute(sql, (res.move_id.ref,))
            analytic_tag = cr.fetchall()
            for tag in analytic_tag:
                res.analytic_tag_ids = [(6,0,[tag[0]])]
        return res