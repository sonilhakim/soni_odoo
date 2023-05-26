import copy
import ast

from odoo import models, fields, api, _
from odoo.tools.safe_eval import safe_eval
from odoo.tools.misc import formatLang
from odoo.tools import float_is_zero, ustr
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
from odoo.osv import expression
from odoo.tools.pycompat import izip
import logging
_logger = logging.getLogger(__name__)


class AccountFinancialReportLine(models.Model):
    _inherit = "account.financial.html.report.line"

    balance = fields.Float('Balance')
    credit = fields.Float('Credit')
    debit = fields.Float('debit')


    @api.multi
    def compute_balance(self, obj, currency_table, financial_report, type='balance', linesDict=None):
        if linesDict is None:
            linesDict = {}
        fields = dict((fn, 0.0) for fn in ['debit', 'credit', 'balance'])
        if type == 'balance':
            fields = obj._get_balance(linesDict, currency_table, financial_report)[0]
            linesDict[obj.code] = self
        elif type in ['sum', 'sum_if_pos', 'sum_if_neg']:
            if type == 'sum_if_neg':
                obj = obj.with_context(sum_if_neg=True)
            if type == 'sum_if_pos':
                obj = obj.with_context(sum_if_pos=True)
            if obj._name == 'account.financial.html.report.line':
                fields = obj._get_sum(currency_table, financial_report)
                self.amount_residual = fields['amount_residual']
            elif obj._name == 'account.move.line':
                self.amount_residual = 0.0
                field_names = ['debit', 'credit', 'balance', 'amount_residual']
                res = obj.env['account.financial.html.report.line']._compute_line(currency_table, financial_report)
                for field in field_names:
                    fields[field] = res[field]
                self.amount_residual = fields['amount_residual']
        elif type == 'not_computed':
            for field in fields:
                fields[field] = obj.get(field, 0)
            self.amount_residual = obj.get('amount_residual', 0)
        elif type == 'null':
            self.amount_residual = 0.0
        self.balance = fields['balance']
        self.credit = fields['credit']
        self.debit = fields['debit']