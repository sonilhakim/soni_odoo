from odoo import fields,api,models,_
from datetime import datetime
from datetime import timedelta
from odoo.osv import expression
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.exceptions import ValidationError

class AccountBankStatementLine(models.Model):
    _inherit = "account.bank.statement.line"

    # @api.multi
    # def get_move_lines_for_reconciliation_widget(self, excluded_ids=None, str=False, offset=0, limit=None):
    #     """ Returns move lines for the bank statement reconciliation widget, formatted as a list of dicts """
    #     try :
    #         aml_recs = self.get_move_lines_for_reconciliation(excluded_ids=excluded_ids, str=str, offset=offset, limit=limit)
    #         aml_recs = aml_recs.filtered(lambda inv_ln :inv_ln.invoice_id.payment_journal_id.id == self.statement_id.journal_id.id)
    #         target_currency = self.currency_id or self.journal_id.currency_id or self.journal_id.company_id.currency_id
    #         return aml_recs.prepare_move_lines_for_reconciliation_widget(target_currency=target_currency, target_date=self.date)
    #     except Exception,e:
    #         raise ValidationError(_("Error:%s"%e))

    def get_move_lines_for_reconciliation(self, excluded_ids=None, str=False, offset=0, limit=None, additional_domain=None, overlook_partner=False):
        """ Return account.move.line records which can be used for bank statement reconciliation.

            :param excluded_ids:
            :param str:
            :param offset:
            :param limit:
            :param additional_domain:
            :param overlook_partner:
        """
        # Blue lines = payment on bank account not assigned to a statement yet
        reconciliation_aml_accounts = [self.journal_id.default_credit_account_id.id, self.journal_id.default_debit_account_id.id]
        # tambah param  date dan company_id yang sama
        # import pdb;pdb.set_trace()
        # date = datetime.strptime(self.date,"%Y-%m-%d")
        # tigaharilalu = timedelta(days=-3)
        # tiga = date+tigaharilalu
        # max_date = tiga.strftime(DEFAULT_SERVER_DATETIME_FORMAT)[:10]
        max_date = '2018-11-23'
       # import pdb;pdb.set_trace()
        # domain_reconciliation = ['&', '&', ('statement_id', '=', False), ('account_id', 'in', reconciliation_aml_accounts), ('payment_id','<>', False)]
        domain_reconciliation = ['&', '&', ('statement_id', '=', False), 
                                ('account_id', 'in', reconciliation_aml_accounts), 
                                ('payment_id','<>', False),
                                ('company_id','=',self.company_id.id)]

        # Black lines = unreconciled & (not linked to a payment or open balance created by statement
        domain_matching = ['&', ('reconciled', '=', False), '|', ('payment_id','=',False), ('statement_id', '<>', False)]
        if self.partner_id.id or overlook_partner:
            domain_matching = expression.AND([domain_matching, [('account_id.internal_type', 'in', ['payable', 'receivable'])]])
        else:
            # TODO : find out what use case this permits (match a check payment, registered on a journal whose account type is other instead of liquidity)
            domain_matching = expression.AND([domain_matching, [('account_id.reconcile', '=', True)]])

        # Let's add what applies to both
        domain = expression.OR([domain_reconciliation, domain_matching])
        #import pdb;pdb.set_trace()
        if self.partner_id.id and not overlook_partner:
            domain = expression.AND([domain, [('partner_id', '=', self.partner_id.id)]])

        journal = self.statement_id.journal_id
        if journal.is_wesel or journal.is_virtual_account or journal.is_transfer:
            if self.partner_id.id and not overlook_partner:
                invoice_ids = self.env['account.invoice'].search([
                                    ('state','not in',('draft','cancel','paid')),
                                    ('company_id','=',self.statement_id.company_id.id),
                                    ('partner_id', '=', self.partner_id.id), 
                                    '|',
                                    ('payment_journal_id','=',self.statement_id.journal_id.id),
                                    ('payment_journal_id.type','=','cash')                  
                                ],order='date_invoice asc')
            else :
                invoice_ids = self.env['account.invoice'].search([
                                    ('state','not in',('draft','cancel','paid')),
                                    ('company_id','=',self.statement_id.company_id.id),                               
                                    '|', 
                                    ('payment_journal_id','=',self.statement_id.journal_id.id),
                                    ('payment_journal_id.type','=','cash')                 
                                ],order='date_invoice asc')
            if invoice_ids :
                #domain = expression.OR([domain, ['|',('invoice_id','in',(invoice_ids.ids)),('invoice_id.payment_journal_id','=',False)]])
                domain = expression.AND([domain, [('invoice_id','in',(invoice_ids.ids)),('date','>=',max_date)]])
                #domain = expression.AND([domain, [('invoice_id','in',(invoice_ids.ids))]])
            elif self.journal_id.company_id.name != 'COSMETIC':
                domain = expression.AND([domain, [('date','>=',max_date)]])
        else :
            if self.amount > 0.0 and self.partner_id.id and not overlook_partner:
                invoice_ids = self.env['account.invoice'].search([
                                    ('partner_id', '=', self.partner_id.id), 
                                    ('state','not in',('draft','cancel','paid')),
                                    ('company_id','=',self.statement_id.company_id.id),
                                    ('payment_journal_id','=',self.statement_id.journal_id.id)                   
                                ],order='date_invoice asc')
                if not invoice_ids :
                    invoice_ids = self.env['account.invoice'].search([
                                    ('partner_id', '=', self.partner_id.id), 
                                    ('state','not in',('draft','cancel','paid')),
                                    ('company_id','=',self.statement_id.company_id.id),
                                    ('payment_journal_id','=',False)                     
                                ],order='date_invoice asc')
                if invoice_ids :
                    domain = expression.OR([domain, [('invoice_id','in',(invoice_ids.ids)),('account_id.internal_type', 'in', ['payable', 'receivable'])]])
                # elif self.journal_id.company_id.name != 'COSMETIC' :
                #     domain = expression.AND([domain, [('date','>=',max_date)]])
        # else :
        #     domain = expression.OR([domain, [('invoice_id.payment_journal_id','=',False)]])

        # Domain factorized for all reconciliation use cases
        ctx = dict(self._context or {})
        ctx['bank_statement_line'] = self
        generic_domain = self.env['account.move.line'].with_context(ctx).domain_move_lines_for_reconciliation(excluded_ids=excluded_ids, str=str)
        domain = expression.AND([domain, generic_domain])

        # Domain from caller
        if additional_domain is None:
            additional_domain = []
        else:
            additional_domain = expression.normalize_domain(additional_domain)
        domain = expression.AND([domain, additional_domain])

        return self.env['account.move.line'].search(domain, offset=offset, limit=limit, order="date_maturity asc, id asc")


    # @api.multi
    # def get_move_lines_for_reconciliation_widget(self, excluded_ids=None, str=False, offset=0, limit=None):
    #     """ Returns move lines for the bank statement reconciliation widget, formatted as a list of dicts """
    #     """
    #     Pada waktu bank reconcile, untuk 
    #     Jurnal VA dan WESEL, munculkan juga invoice yang payment type Cash
    #     """
    #     try :
    #         aml_recs = self.get_move_lines_for_reconciliation(excluded_ids=excluded_ids, str=str, offset=offset, limit=limit)
    #         journal_ids = self.env['account.journal'].search([
    #             '|',
    #             ('is_wesel','=',True),
    #             ('is_virtual_account','=',True),
    #             ('company_id','=',self.statement_id.journal_id.company_id.id),
    #         ])
    #         if self.statement_id.journal_id.id in journal_ids.ids :
    #             invoice_ids = self.env['account.invoice'].search([
    #                 ('state','not in',('draft','cancel','paid')),
    #                 ('company_id','=',self.statement_id.company_id.id),
    #                 '|',
    #                 ('payment_journal_id','=',self.statement_id.journal_id.id),
    #                 ('payment_journal_id.type','=','cash'),
    #                 order='date_invoice asc'
    #             ])
    #             aml_recs = aml_recs.filtered(lambda inv_ln : not inv_ln.invoice_id.payment_journal_id or inv_ln.invoice_id.id in invoice_ids.ids)
    #         else :
    #             aml_recs = aml_recs.filtered(lambda inv_ln : not inv_ln.invoice_id.payment_journal_id or inv_ln.invoice_id.payment_journal_id.id == self.statement_id.journal_id.id)
            
    #         #aml_recs = aml_recs.filtered(lambda inv_ln : inv_ln.company_id.id == self.statement_id.company_id.id )# company di cek di fungsi sebelumnya
    #         # aml_recs = aml_recs.filtered(lambda inv_ln : inv_ln.account_id.internal_type in ['receivable','payable'] )# receivable
    #         target_currency = self.currency_id or self.journal_id.currency_id or self.journal_id.company_id.currency_id
    #         return aml_recs.prepare_move_lines_for_reconciliation_widget(target_currency=target_currency, target_date=self.date)
    #     except Exception,e:
    #         raise ValidationError(_("Error:%s"%e))

    # @api.multi
    # def get_move_lines_for_reconciliation_widget(self, excluded_ids=None, str=False, offset=0, limit=None):
    #     """ Returns move lines for the bank statement reconciliation widget, formatted as a list of dicts """
    #     try :
    #         aml_recs = self.get_move_lines_for_reconciliation(excluded_ids=excluded_ids, str=str, offset=offset, limit=limit)
    #         aml_recs = aml_recs.filtered(lambda inv_ln : not inv_ln.invoice_id.payment_journal_id or inv_ln.invoice_id.payment_journal_id.id == self.statement_id.journal_id.id)
            
    #         #aml_recs = aml_recs.filtered(lambda inv_ln : inv_ln.company_id.id == self.statement_id.company_id.id )# company di cek di fungsi sebelumnya
    #         # aml_recs = aml_recs.filtered(lambda inv_ln : inv_ln.account_id.internal_type in ['receivable','payable'] )# receivable
    #         target_currency = self.currency_id or self.journal_id.currency_id or self.journal_id.company_id.currency_id
    #         return aml_recs.prepare_move_lines_for_reconciliation_widget(target_currency=target_currency, target_date=self.date)
    #     except Exception,e:
    #         raise ValidationError(_("Error:%s"%e))