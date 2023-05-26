from odoo import models, fields, api, _
import time
import logging
import odoo.addons.decimal_precision as dp
import datetime

class account_voucher(models.Model):
    _inherit = 'account.voucher'
    
    ####################################################################################
    # create payment
    # invoice_id: yang mau dibayar
    # journal_id: payment method
    ####################################################################################
    @api.depends
    def create_payment(self):
        voucher_lines = []
        
        move_line_id = self.env['account.move.line'].search([('move_id.id', '=', self.move_id.id)])
        move_lines = self.env['account.move.line']
        move_line = move_lines[0]  # yang AR saja
        
        #payment supplier
        if type == 'payment':
            line_amount = amount
            line_type = 'dr'
            journal_account = journal.default_credit_account_id.id
        #receive customer
        else:
            line_amount = amount
            line_type = 'cr'
            journal_account = journal.default_debit_account_id.id
            
        voucher_lines.append((0, 0, {
            'move_line_id': move_line.id,
            'account_id': move_line.account_id.id,
            'amount_original': line_amount,
            'amount_unreconciled': line_amount,
            'reconcile': True,
            'amount': line_amount,
            'type': line_type,
            'name': move_line.name,
            'company_id': company_id
        }))
        
        voucher_id = self.env['account.voucher'].create({
            'partner_id' : partner_id,
            'amount' 		: amount,
            'account_id'	: journal_account,
            'journal_id'	: journal.id,
            'reference' 	: 'Payment giro ' + name,
            'name' 			: 'Payment giro ' + name,
            'company_id' 	: company_id,
            'type'			: type,
            'line_ids'		: voucher_lines
        })
        _logger.info("   created payment id:%d" % (voucher_id) )
        return voucher_id
    
    ####################################################################################
    # set done
    ####################################################################################
    # @api.multi
    # def payment_confirm(self):
    #     wf_service = self.signal_workflow('proforma_voucher')
    #     wf_service.trg_validate('account.voucher', 'proforma_voucher')
    #     return wf_service
    
    
    ####################################################################################
    # find invoice by number
    ####################################################################################
    @api.multi
    def find_invoice_by_number(self):
        invoice_obj = self.env['account.invoice']
        invoice_id = invoice_obj.search([('number' ,'=', number)])
        invoice = invoice_obj.env(invoice_id)
        return invoice
    
    ####################################################################################
    # find journal by code
    ####################################################################################
    @api.multi
    def find_journal_by_code(self):
        journal_obj = self.env['account.journal']
        journal_id = journal_obj.search([('code', '=', code)])
        journal = journal_obj.env(journal_id)
        return journal