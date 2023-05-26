from odoo import api, fields, models, _
import time
from odoo.exceptions import UserError, Warning
import logging
from dateutil import relativedelta
_logger = logging.getLogger(__name__)
from datetime import datetime, timedelta
import pdb


class asset(models.Model):
    _name = 'account.asset.asset'
    _inherit = 'account.asset.asset'

    
    @api.multi
    def validate(self):
        res = super(asset, self).validate()
        if self.asset_id:

            obj = self.env['product.product'].search([('name','=',self.name)])
            account_id = obj.property_account_income_id
            object_account_move = self.env['account.move']
            
            line_ids = [
                (0, 0, {
                    'account_id' : self.category_id.account_asset_id.id,
                    'debit' : self.value,
                    'credit' : 0,
                }),
                (0, 0, {
                    'account_id' : account_id.id,
                    'debit' : 0,
                    'credit' : self.value,
                })]
            data = {
                'journal_id' : self.category_id.journal_id.id,
                'date' : time.strftime("%Y-%m-%d"),
                'ref' : self.name,
                'line_ids' : line_ids,
            }
            records = object_account_move.create(data)
            # object_account_move.browse(records.id).action_post()
            records.post()
            vals = {
                    'journal_asset': records.id,
                }
            self.write(vals)
        return res

    