from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class payment_kasbon(models.Model):

    _name = "account.payment"
    _description = "account.payment"

    _inherit = "account.payment"

    kasbon_id = fields.Many2one(comodel_name="vit.kasbon_pb",  string="Kasbon",  help="", )
    nomor = fields.Integer(string="No.")

    @api.model
    def default_get(self, fields):
        rec = super(payment_kasbon, self).default_get(fields)
        # import pdb;pdb.set_trace()
        active_id = self._context.get('active_id')
        active_model = self._context.get('active_model')

        # Check for selected kasbon
        if not active_id or active_model != 'vit.kasbon_pb':
            return rec
        
        kasbon = self.env['vit.kasbon_pb'].browse(active_id)
        if kasbon:
            journal = self.env['account.journal'].search([('type','=','cash')], limit=1)
            kasbon_amount = kasbon.pinjaman - kasbon.angsuran

            rec.update({
                'amount': abs(kasbon_amount),
                'payment_type': 'inbound',
                'partner_id': kasbon.employee_id.address_id.id,
                'partner_type': 'customer',
                'communication': kasbon.name,
                'journal_id': journal.id,
            })

        return rec

    def action_validate_invoice_payment(self):
        res = super(payment_kasbon, self).action_validate_invoice_payment()
        inv = self.env['account.invoice'].search([('id','in',self.invoice_ids.ids)], limit=1)
        if inv.type== 'in_invoice' and inv.kasbon_id:
        	inv.kasbon_id.pencairan = inv.kasbon_id.pencairan + self.amount

        # if inv.type== 'out_invoice' and inv.kasbon_id:
        # 	inv.kasbon_id.angsuran = inv.kasbon_id.angsuran + self.amount

        # 	if inv.kasbon_id.angsuran == inv.kasbon_id.pinjaman:
        # 		inv.kasbon_id.action_lunas()

        return res

    def action_validate_kasbon_payment(self):
        if self.kasbon_id:
          self.kasbon_id.angsuran = self.kasbon_id.angsuran + self.amount
          angsurans = self.env['account.payment'].search([('kasbon_id','=',self.kasbon_id.id),('payment_type', '=', 'inbound')])
          self.nomor = len(angsurans)

          if self.kasbon_id.angsuran == self.kasbon_id.pinjaman:
              self.kasbon_id.action_lunas()

        return self.post()