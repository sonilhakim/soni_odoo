from odoo import api, fields, models, _
import time
from datetime import date, datetime
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

class ReportMutasiBankKasWizard(models.TransientModel):
    _name = 'vit.report_mutasi_bank_kas_wizard'


    date           = fields.Date( string="Date", required=True, default=lambda self: time.strftime("%Y-%m-%d"),)
    saldo_awal     = fields.Float(string="Saldo Awal")
    total_mutasi_d = fields.Float( string="Mutasi D")
    total_mutasi_c = fields.Float( string="Mutasi C")
    saldo_akhir    = fields.Float( string="Saldo Akhir")
    total_d        = fields.Float( string="Total D")
    total_c        = fields.Float( string="Total C")
    
    journal_id     = fields.Many2one('account.journal', string='Jurnal', required=True)
    user_id        = fields.Many2one('res.users', 'User', default=lambda self: self.env.user)
    cabang_id      = fields.Many2one( comodel_name="res.company", string="Cabang", required=True)
    mb_lines       = fields.One2many('vit.report_mutasi_bank_kas_line','mb_wizard_id', 'Mutasi Bank/Kas Lines')

    @api.onchange('user_id')
    def onchange_cabang(self):
        if self.user_id:
            self.cabang_id = self.user_id.company_id.id

    def get_raw_datas(self):        
        self.env.cr.execute("""INSERT INTO vit_raw_data_line (bukti,label,debit,credit,mb_wizard_id)
            SELECT 
                (CASE 
                    WHEN aml.is_bmk IS TRUE THEN bmk.name
                    WHEN aml.is_bmb IS TRUE THEN bmb.name
                    ELSE am.name
                END) as bukti,
                (CASE 
                    WHEN aml.is_bmk IS TRUE THEN em.name
                    WHEN aml.is_bmb IS TRUE THEN em.name
                    ELSE aml.name
                END) as label,
                aml.credit as debit, aml.debit as credit, %s        
            FROM account_move_line aml
            LEFT JOIN account_account aa ON aml.account_id = aa.id
            LEFT JOIN account_move am ON aml.move_id = am.id
            LEFT JOIN account_move_line amj ON amj.move_id = am.id
            LEFT JOIN account_account aaj ON amj.account_id = aaj.id
            LEFT JOIN res_company rc ON aml.company_id = rc.id
            LEFT JOIN daftar_penagihan_faktur dpf ON aml.penagihan_faktur_id = dpf.id
            LEFT JOIN daftar_bukti_masuk_kas bmk ON dpf.bukti_masuk_kas_id = bmk.id
            LEFT JOIN daftar_bukti_masuk_bank bmb ON dpf.bukti_masuk_bank_id = bmb.id
            LEFT JOIN hr_employee em ON dpf.employee_id = em.id
            WHERE aml.date = '%s' AND am.state = 'posted' AND aa.id != aaj.id AND aaj.id = %s AND rc.id = %s
            GROUP BY am.id, aml.id, bmk.name, bmb.name, em.name
            """ % (self.id,self.date,self.journal_id.default_account_id.id,self.cabang_id.id,))

    def get_datas(self):
        # import pdb;pdb.set_trace()
        self.get_raw_datas()
        cra = self.env.cr
        cr = self.env.cr

        sqla = """SELECT sum(sa.balance) as saldo_awal
                FROM account_move_line sa
                LEFT JOIN account_account saa ON sa.account_id = saa.id
                LEFT JOIN account_move ams ON sa.move_id = ams.id
                LEFT JOIN res_company rcs ON sa.company_id = rcs.id
                WHERE sa.date < %s AND ams.state = 'posted' AND saa.id = %s AND rcs.id = %s
                """
        cra.execute(sqla, (self.date,self.journal_id.default_account_id.id,self.cabang_id.id,))
        recorda = cra.fetchall()
        debsa = 0.0
        cresa = 0.0
        saldo_awal = 0.0
        saldo_akhir = 0.0
        for reca in recorda:
            if reca[0] == None:
                saldo_awal = 0.0
            else:
                saldo_awal = reca[0]

        #     if reca[1] == None:
        #         cresa = 0.0
        #     else:
        #         cresa = reca[1] * -1

        # saldo_awal = (debsa - cresa) * 1

        sql = """SELECT rdl.bukti as jnl, rdl.label as lbl, sum(rdl.debit) as debit, sum(rdl.credit) as credit                
                FROM vit_raw_data_line rdl
                LEFT JOIN vit_report_mutasi_bank_kas_wizard mbk ON rdl.mb_wizard_id = mbk.id
                WHERE mbk.id = %s
                GROUP BY rdl.bukti, rdl.label
                """
        cr.execute(sql, (self.id,))
        record = cr.fetchall()
        lines = []
        deb = 0.0
        kre = 0.0
        total_mutasi_d = 0.0
        total_mutasi_c = 0.0
        total_d = 0.0
        total_c = 0.0
        for rec in record:
            if rec[2] == None:
                deb = 0.0
            else:
                deb = rec[2]
                total_mutasi_d = sum(rec[2] for rec in record)

            if rec[3] == None:
                kre = 0.0
            else:
                kre = rec[3]
                total_mutasi_c = sum(rec[3] for rec in record)

            lines.append((0,0,{
                            'bukti' : rec[0],
                            'label' : rec[1],
                            'debit' : deb,
                            'credit': kre,
                        }))

        total_d = saldo_awal + total_mutasi_d
        saldo_akhir = total_d - total_mutasi_c
        total_c = total_mutasi_c + saldo_akhir

        self.write({
                'saldo_awal'     : saldo_awal,
                'total_mutasi_d' : total_mutasi_d,
                'total_mutasi_c' : total_mutasi_c,
                'saldo_akhir'    : saldo_akhir,
                'total_d'        : total_d,
                'total_c'        : total_c,
                'mb_lines'       : lines,
            })


    def confirm_button(self):
        self.get_datas()
        report_action = self.env.ref(
            'vit_report_mutasi_bank_n_kas.report_mutasi_bank_kas'
        ).report_action(self)
        report_action['close_on_report_download']=True

        return report_action

ReportMutasiBankKasWizard()

class ReportMutasiBankKasLine(models.TransientModel):
    _name = 'vit.report_mutasi_bank_kas_line'

    bukti = fields.Char(string="No. Bukti")
    label = fields.Char(string="Label")
    debit = fields.Float(string="Debet")
    credit = fields.Float(string="Kredit")

    mb_wizard_id = fields.Many2one('vit.report_mutasi_bank_kas_wizard', string='MB Wizard')

ReportMutasiBankKasLine()

class RawdataLine(models.TransientModel):
    _name = 'vit.raw_data_line'

    bukti = fields.Char(string="No. Bukti")
    label = fields.Char(string="Label")
    debit = fields.Float(string="Debet")
    credit = fields.Float(string="Kredit")

    mb_wizard_id = fields.Many2one('vit.report_mutasi_bank_kas_wizard', string='MB Wizard')

RawdataLine()