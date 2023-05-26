from odoo import api,fields,models,_

class account_invoice(models.Model):
    _inherit = 'account.invoice'
    
    payment_journal_id = fields.Many2one('account.journal',string="Payment Journal")
    sale_ids = fields.Many2many('sale.order')