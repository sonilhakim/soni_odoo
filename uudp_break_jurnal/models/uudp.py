from odoo import models, fields, api
import datetime
from odoo.exceptions import UserError, AccessError, ValidationError
from odoo.addons.terbilang import terbilang
import logging
_logger = logging.getLogger(__name__)

class uudp_break(models.Model):
    _inherit = 'uudp'

    @api.multi
    def button_done_finance(self):
        if self.type == 'penyelesaian':
            if self.uudp_ids:
                if round(self.sisa_penyelesaian,2) > 0.0:
                    raise AccessError(_('Sisa penyelesaian harus tetap dimasukan ke detail penyelesaian !'))
                for ajuan in self.uudp_ids:
                    ajuan.create_journal_entry()

        # if self.type == 'penyelesaian':
        #     partner = self.ajuan_id.responsible_id.partner_id.id
        #     total_ajuan = 0
        #     now = datetime.datetime.now()
        #     total_ajuan = self.total_ajuan
        #     if self.uudp_ids:
                
        #         if round(self.sisa_penyelesaian,2) > 0.0:
        #             raise AccessError(_('Sisa penyelesaian harus tetap dimasukan ke detail penyelesaian !'))

        #         account_move_line = []
        #         total_debit = 0.0
        #         for ajuan in self.uudp_ids:
        #             if not ajuan.coa_debit:
        #                 raise UserError(_('Account atas %s belum di set!')%(ajuan.description))
        #             if ajuan.partner_id :
        #                 partner = ajuan.partner_id.id
        #             tag_id = False
        #             if ajuan.store_id :
        #                 tag_id = [(6, 0, [ajuan.store_id.account_analytic_tag_id.id])]
        #             ajuan_total = ajuan.sub_total
        #             #account debit
        #             if ajuan.sub_total > 0.0 :
        #                 account_move_line.append((0, 0 ,{'account_id'       : ajuan.coa_debit.id,
        #                                                  'partner_id'       : partner, 
        #                                                  'analytic_tag_ids' : tag_id,
        #                                                  'name'             : ajuan.description, 
        #                                                  'analytic_account_id': ajuan.analytic_account_id.id,
        #                                                  'debit'            : ajuan_total, 
        #                                                  'date_maturity'    : ajuan.actual_date})) #,
        #             elif ajuan.sub_total < 0.0 :
        #                 account_move_line.append((0, 0 ,{'account_id'       : ajuan.coa_debit.id,
        #                                                  'partner_id'       : partner, 
        #                                                  'analytic_tag_ids' : tag_id,
        #                                                  'name'             : ajuan.description, 
        #                                                  'analytic_account_id': ajuan.analytic_account_id.id,
        #                                                  'credit'            : -ajuan_total, 
        #                                                  'date_maturity'    : ajuan.actual_date})) #,
                    

        #             #account credit
        #             account_move_line.append((0, 0 ,{'account_id' : self.ajuan_id.coa_debit.id, 
        #                                         'partner_id': partner, 
        #                                         # 'analytic_account_id':ajuans.analytic_account_id.id,
        #                                         'name' : self.notes, 
        #                                         # 'credit' : total_ajuan, 
        #                                         'credit' : ajuan_total, 
        #                                         'date_maturity':self.date})) #, 

        #             #create journal entry
        #             # import pdb; pdb.set_trace()
        #             journal_id = self.ajuan_id.pencairan_id.journal_id
        #             if not journal_id :
        #                 journal_id = self.env['account.move'].sudo().search([('ref','ilike','%'+self.ajuan_id.name+'%')],limit=1)
        #                 if not journal_id :
        #                     raise AccessError(_('Journal pencairan tidak ditemukan !'))
        #                 journal_id = journal_id.journal_id
        #             data={"journal_id":journal_id.id,
        #                   "ref":self.name + ' - '+ self.ajuan_id.name,
        #                   "date":self.date,
        #                   "narration" : self.notes,
        #                   "company_id":self.company_id.id,
        #                   "line_ids":account_move_line,}

        #         journal_entry = self.env['account.move'].create(data)
        #         if journal_entry:
        #             journal_entry.post()
        #             self.write_state_line('done')
        #             self.ajuan_id.write({'selesai':True})
        #             self.post_mesages_uudp('Done')
        #             return self.write({'state' : 'done', 'journal_entry_id':journal_entry.id})
        #         else:
        #             raise AccessError(_('Gagal membuat journal entry') )
        #         return self.write({'state' : 'done'})
                    

class UudpLineBreak(models.Model):
    _inherit = 'uudp.detail'    

    actual_date = fields.Date(string="Actual Date", required=False, default=fields.Date.context_today,)
    

    @api.multi
    def create_journal_entry(self):
        partner = self.uudp_id.ajuan_id.responsible_id.partner_id.id
        
        account_move_line = []
        total_debit = 0.0
        analytic_account = 0
        for ajuan in self:
            if not ajuan.coa_debit:
                raise UserError(_('Account atas %s belum di set!')%(ajuan.description))
            if ajuan.partner_id :
                partner = ajuan.partner_id.id
            tag_id = False
            if ajuan.store_id :
                tag_id = [(6, 0, [ajuan.store_id.account_analytic_tag_id.id])]
            ajuan_total = ajuan.sub_total
            #account debit
            if ajuan.sub_total > 0.0 :
                account_move_line.append((0, 0 ,{'account_id'       : ajuan.coa_debit.id,
                                                 'partner_id'       : partner, 
                                                 'analytic_tag_ids' : tag_id,
                                                 'name'             : ajuan.description, 
                                                 'analytic_account_id': ajuan.analytic_account_id.id,
                                                 'debit'            : ajuan_total, 
                                                 'date_maturity'    : self.actual_date})) #,
            elif ajuan.sub_total < 0.0 :
                account_move_line.append((0, 0 ,{'account_id'       : ajuan.coa_debit.id,
                                                 'partner_id'       : partner, 
                                                 'analytic_tag_ids' : tag_id,
                                                 'name'             : ajuan.description, 
                                                 'analytic_account_id': ajuan.analytic_account_id.id,
                                                 'credit'            : -ajuan_total, 
                                                 'date_maturity'    : self.actual_date})) #,
            # total_debit += ajuan_total    
        
        
            #account credit
            analytic_account = ajuan.analytic_account_id.id
            if ajuan.sub_total > 0.0 :
                account_move_line.append((0, 0 ,{'account_id' : self.uudp_id.ajuan_id.coa_debit.id, 
                                            'partner_id': partner, 
                                            # 'analytic_account_id':ajuans.analytic_account_id.id,
                                            'name' : ajuan.description,
                                            # 'credit' : total_ajuan, 
                                            'credit' : ajuan_total, 
                                            'date_maturity':self.actual_date})) #,
            elif ajuan.sub_total < 0.0 : 
                account_move_line.append((0, 0 ,{'account_id' : self.uudp_id.ajuan_id.coa_debit.id, 
                                            'partner_id': partner, 
                                            # 'analytic_account_id':ajuans.analytic_account_id.id,
                                            'name' : ajuan.description,
                                            # 'credit' : total_ajuan, 
                                            'debit' : -ajuan_total, 
                                            'date_maturity':self.actual_date})) #,

            #create journal entry
            # import pdb; pdb.set_trace()
            journal_id = self.uudp_id.ajuan_id.pencairan_id.journal_id
            if not journal_id :
                journal_id = self.env['account.move'].sudo().search([('ref','ilike','%'+self.uudp_id.ajuan_id.name+'%')],limit=1)
                if not journal_id :
                    raise AccessError(_('Journal pencairan tidak ditemukan !'))
                journal_id = journal_id.journal_id
            data={"journal_id":journal_id.id,
                  "ref":self.uudp_id.name + ' - '+ self.uudp_id.ajuan_id.name,
                  "date":ajuan.actual_date,
                  "narration" : self.uudp_id.notes,
                  "company_id":self.uudp_id.company_id.id,
                  "line_ids":account_move_line,}

            journal_entry = self.env['account.move'].create(data)
            if journal_entry:
                journal_entry.post()
                self.uudp_id.write_state_line('done')
                self.uudp_id.ajuan_id.write({'selesai':True})
                self.uudp_id.post_mesages_uudp('Done')
                return self.uudp_id.write({'state' : 'done'})
            else:
                raise AccessError(_('Gagal membuat journal entry') )
            return self.uudp_id.write({'state' : 'done'})