# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import Warning, UserError
import time
from datetime import date, datetime
import logging
_logger = logging.getLogger(__name__)

class PosisiDanaWizard(models.TransientModel):
    _name = 'vit.posisi_dana_wizard'
    _description = 'vit.posisi_dana_wizard'

    def _get_years(self):
        this_year = datetime.today().year
        results = sorted([(str(x), str(x)) for x in range(this_year - 5, this_year + 2)],reverse = True)
        return results
        
    year   = fields.Selection(_get_years,string="Tahun 1")
    c_year = fields.Selection(_get_years,string="Tahun 2")
    

    @api.multi
    def load_posisi_dana(self, ):
        for pod in self:
            current_date  = date.today()
            thn = str(pod.year)
            p1_date_start = current_date.strftime(thn +'-01-01')
            p1_date_end = current_date.strftime(thn +'-03-31')
            p2_date_start = current_date.strftime(thn +'-04-01')
            p2_date_end = current_date.strftime(thn +'-06-30')
            p3_date_start = current_date.strftime(thn +'-07-01')
            p3_date_end = current_date.strftime(thn +'-09-30')
            p4_date_start = current_date.strftime(thn +'-10-01')
            p4_date_end = current_date.strftime(thn +'-12-31')

            c_thn = str(pod.c_year)
            p1x_date_start = current_date.strftime(c_thn +'-01-01')
            p1x_date_end = current_date.strftime(c_thn +'-03-31')
            p2x_date_start = current_date.strftime(c_thn +'-04-01')
            p2x_date_end = current_date.strftime(c_thn +'-06-30')
            p3x_date_start = current_date.strftime(c_thn +'-07-01')
            p3x_date_end = current_date.strftime(c_thn +'-09-30')
            p4x_date_start = current_date.strftime(c_thn +'-10-01')
            p4x_date_end = current_date.strftime(c_thn +'-12-31')

            or_1 = 0.0
            or_2 = 0.0
            or_3 = 0.0
            or_4 = 0.0
            or_1x = 0.0
            or_2x = 0.0
            or_3x = 0.0
            or_4x = 0.0

            inv_1 = 0.0
            inv_2 = 0.0
            inv_3 = 0.0
            inv_4 = 0.0
            inv_1x = 0.0
            inv_2x = 0.0
            inv_3x = 0.0
            inv_4x = 0.0

            po_1 = 0.0
            po_2 = 0.0
            po_3 = 0.0
            po_4 = 0.0
            po_1x = 0.0
            po_2x = 0.0
            po_3x = 0.0
            po_4x = 0.0

            invp_1 = 0.0
            invp_2 = 0.0
            invp_3 = 0.0
            invp_4 = 0.0
            invp_1x = 0.0
            invp_2x = 0.0
            invp_3x = 0.0
            invp_4x = 0.0

            pos_1 = 0.0
            pos_2 = 0.0
            pos_3 = 0.0
            pos_4 = 0.0
            pos_1x = 0.0
            pos_2x = 0.0
            pos_3x = 0.0
            pos_4x = 0.0

            invs_1 = 0.0
            invs_2 = 0.0
            invs_3 = 0.0
            invs_4 = 0.0
            invs_1x = 0.0
            invs_2x = 0.0
            invs_3x = 0.0
            invs_4x = 0.0

            aksep1 = 0.0
            aksep2 = 0.0
            aksep3 = 0.0
            aksep4 = 0.0
            aksep1x = 0.0
            aksep2x = 0.0
            aksep3x = 0.0
            aksep4x = 0.0

            saldo1 = 0.0
            saldo2 = 0.0
            saldo3 = 0.0
            saldo4 = 0.0
            saldo1x = 0.0
            saldo2x = 0.0
            saldo3x = 0.0
            saldo4x = 0.0

            pb_1 = 0.0
            pb_2 = 0.0
            pb_3 = 0.0
            pb_4 = 0.0
            pb_1x = 0.0
            pb_2x = 0.0
            pb_3x = 0.0
            pb_4x = 0.0

            sqlo = """
                select 
                (select sum(pog1.total_price)
                    from vit_purchase_order_garmen pog1
                    where pog1.date >= %s and pog1.date <= %s and pog1.po_payung_id is null) as periode_1,
                (select sum(inv1.amount_total - inv1.residual)
                    from account_invoice inv1
                    left join vit_purchase_order_garmen pog1 on inv1.or_id = pog1.id
                    where pog1.date >= %s and pog1.date <= %s and inv1.state != 'draft' and inv1.type = 'out_invoice') as periode_1a,
                (select sum(pog2.total_price)
                    from vit_purchase_order_garmen pog2
                    where pog2.date >= %s and pog2.date <= %s and pog2.po_payung_id is null) as periode_2,
                (select sum(inv2.amount_total - inv2.residual)
                    from account_invoice inv2
                    left join vit_purchase_order_garmen pog2 on inv2.or_id = pog2.id
                    where pog2.date >= %s and pog2.date <= %s and inv2.state != 'draft' and inv2.type = 'out_invoice') as periode_2a,
                (select sum(pog3.total_price)
                    from vit_purchase_order_garmen pog3
                    where pog3.date >= %s and pog3.date <= %s and pog3.po_payung_id is null) as periode_3,
                (select sum(inv3.amount_total - inv3.residual)
                    from account_invoice inv3
                    left join vit_purchase_order_garmen pog3 on inv3.or_id = pog3.id
                    where pog3.date >= %s and pog3.date <= %s and inv3.state != 'draft' and inv3.type = 'out_invoice') as periode_3a,
                (select sum(pog4.total_price)
                    from vit_purchase_order_garmen pog4
                    where pog4.date >= %s and pog4.date <= %s and pog4.po_payung_id is null) as periode_4, 
                (select sum(inv4.amount_total - inv4.residual)
                    from account_invoice inv4
                    left join vit_purchase_order_garmen pog4 on inv4.or_id = pog4.id
                    where pog4.date >= %s and pog4.date <= %s and inv4.state != 'draft' and inv4.type = 'out_invoice') as periode_4a,
                (select sum(pog1x.total_price)
                    from vit_purchase_order_garmen pog1x
                    where pog1x.date >= %s and pog1x.date <= %s and pog1x.po_payung_id is null) as periode_1x,
                (select sum(inv1x.amount_total - inv1x.residual)
                    from account_invoice inv1x
                    left join vit_purchase_order_garmen pog1x on inv1x.or_id = pog1x.id
                    where pog1x.date >= %s and pog1x.date <= %s and inv1x.state != 'draft' and inv1x.type = 'out_invoice') as periode_1ax,
                (select sum(pog2x.total_price)
                    from vit_purchase_order_garmen pog2x
                    where pog2x.date >= %s and pog2x.date <= %s and pog2x.po_payung_id is null) as periode_2x,
                (select sum(inv2x.amount_total - inv2x.residual)
                    from account_invoice inv2x
                    left join vit_purchase_order_garmen pog2x on inv2x.or_id = pog2x.id
                    where pog2x.date >= %s and pog2x.date <= %s and inv2x.state != 'draft' and inv2x.type = 'out_invoice') as periode_2ax,
                (select sum(pog3x.total_price)
                    from vit_purchase_order_garmen pog3x
                    where pog3x.date >= %s and pog3x.date <= %s and pog3x.po_payung_id is null) as periode_3x,
                (select sum(inv3x.amount_total - inv3x.residual)
                    from account_invoice inv3x
                    left join vit_purchase_order_garmen pog3x on inv3x.or_id = pog3x.id
                    where pog3x.date >= %s and pog3x.date <= %s and inv3x.state != 'draft' and inv3x.type = 'out_invoice') as periode_3ax,
                (select sum(pog4x.total_price)
                    from vit_purchase_order_garmen pog4x
                    where pog4x.date >= %s and pog4x.date <= %s and pog4x.po_payung_id is null) as periode_4x, 
                (select sum(inv4x.amount_total - inv4x.residual)
                    from account_invoice inv4x
                    left join vit_purchase_order_garmen pog4x on inv4x.or_id = pog4x.id
                    where pog4x.date >= %s and pog4x.date <= %s and inv4x.state != 'draft' and inv4x.type = 'out_invoice') as periode_4ax
                """
            cro = self.env.cr
            cro.execute(sqlo, (p1_date_start,p1_date_end,p1_date_start,p1_date_end,p2_date_start,p2_date_end,p2_date_start,p2_date_end,p3_date_start,p3_date_end,p3_date_start,p3_date_end,p4_date_start,p4_date_end,p4_date_start,p4_date_end,
                p1x_date_start,p1x_date_end,p1x_date_start,p1x_date_end,p2x_date_start,p2x_date_end,p2x_date_start,p2x_date_end,p3x_date_start,p3x_date_end,p3x_date_start,p3x_date_end,p4x_date_start,p4x_date_end,p4x_date_start,p4x_date_end))
            resulto = cro.fetchall()
            # import pdb;pdb.set_trace()
            if resulto[0][0] == None:
                or_1 = 0.0
            else:
                or_1 = resulto[0][0]
            if resulto[0][1] == None:
                inv_1 = 0.0
            else:
                inv_1 = resulto[0][1]
            if resulto[0][2] == None:
                or_2 = 0.0
            else:
                or_2 = resulto[0][2]
            if resulto[0][3] == None:
                inv_2 = 0.0
            else:
                inv_2 = resulto[0][3]
            if resulto[0][4] == None:
                or_3 = 0.0
            else:
                or_3 = resulto[0][4]
            if resulto[0][5] == None:
                inv_3 = 0.0
            else:
                inv_3 = resulto[0][5]
            if resulto[0][6] == None:
                or_4 = 0.0
            else:
                or_4 = resulto[0][6]
            if resulto[0][7] == None:
                inv_4 = 0.0
            else:
                inv_4 = resulto[0][7]
            sisao1 = (or_1 - inv_1)
            sisao2 = (or_2 - inv_2)
            sisao3 = (or_3 - inv_3)
            sisao4 = (or_4 - inv_4)

            if resulto[0][8] == None:
                or_1x = 0.0
            else:
                or_1x = resulto[0][8]
            if resulto[0][9] == None:
                inv_1x = 0.0
            else:
                inv_1x = resulto[0][9]
            if resulto[0][10] == None:
                or_2x = 0.0
            else:
                or_2x = resulto[0][10]
            if resulto[0][11] == None:
                inv_2x = 0.0
            else:
                inv_2x = resulto[0][11]
            if resulto[0][12] == None:
                or_3x = 0.0
            else:
                or_3x = resulto[0][12]
            if resulto[0][13] == None:
                inv_3x = 0.0
            else:
                inv_3x = resulto[0][13]
            if resulto[0][14] == None:
                or_4x = 0.0
            else:
                or_4x = resulto[0][14]
            if resulto[0][15] == None:
                inv_4x = 0.0
            else:
                inv_4x = resulto[0][15]
            sisao1x = (or_1x - inv_1x)
            sisao2x = (or_2x - inv_2x)
            sisao3x = (or_3x - inv_3x)
            sisao4x = (or_4x - inv_4x)
            
            # insert PO Purchase
            sqlp = """
                select 
                (select sum(po1.amount_total)
                    from purchase_order po1
                    left join res_partner rp on po1.partner_id = rp.id
                    where po1.date_order >= %s and po1.date_order <= %s and po1.state = 'purchase' and rp.is_mitra_kerja is not true) as periode_1,
                (select sum(inv1.amount_total - inv1.residual)
                    from account_invoice inv1
                    left join purchase_order po1 on inv1.po_id = po1.id
                    left join res_partner rp on po1.partner_id = rp.id
                    where po1.date_order >= %s and po1.date_order <= %s and po1.state = 'purchase' and inv1.state != 'draft' and rp.is_mitra_kerja is not true and inv1.type = 'in_invoice') as periode_1a,
                (select sum(po2.amount_total)
                    from purchase_order po2
                    left join res_partner rp on po2.partner_id = rp.id
                    where po2.date_order >= %s and po2.date_order <= %s and po2.state = 'purchase' and rp.is_mitra_kerja is not true) as periode_2,
                (select sum(inv2.amount_total - inv2.residual)
                    from account_invoice inv2
                    left join purchase_order po2 on inv2.po_id = po2.id
                    left join res_partner rp on po2.partner_id = rp.id
                    where po2.date_order >= %s and po2.date_order <= %s and po2.state = 'purchase' and inv2.state != 'draft' and rp.is_mitra_kerja is not true and inv2.type = 'in_invoice') as periode_2a,
                (select sum(po3.amount_total)
                    from purchase_order po3
                    left join res_partner rp on po3.partner_id = rp.id
                    where po3.date_order >= %s and po3.date_order <= %s and po3.state = 'purchase' and rp.is_mitra_kerja is not true) as periode_3,
                (select sum(inv3.amount_total - inv3.residual)
                    from account_invoice inv3
                    left join purchase_order po3 on inv3.po_id = po3.id
                    left join res_partner rp on po3.partner_id = rp.id
                    where po3.date_order >= %s and po3.date_order <= %s and po3.state = 'purchase' and inv3.state != 'draft' and rp.is_mitra_kerja is not true and inv3.type = 'in_invoice') as periode_3a,
                (select sum(po4.amount_total)
                    from purchase_order po4
                    left join res_partner rp on po4.partner_id = rp.id
                    where po4.date_order >= %s and po4.date_order <= %s and po4.state = 'purchase' and rp.is_mitra_kerja is not true) as periode_4, 
                (select sum(inv4.amount_total - inv4.residual)
                    from account_invoice inv4
                    left join purchase_order po4 on inv4.po_id = po4.id
                    left join res_partner rp on po4.partner_id = rp.id
                    where po4.date_order >= %s and po4.date_order <= %s and po4.state = 'purchase' and rp.is_mitra_kerja is not true and inv4.state != 'draft' and inv4.type = 'in_invoice') as periode_4a,
                (select sum(po1x.amount_total)
                    from purchase_order po1x
                    left join res_partner rpx on po1x.partner_id = rpx.id
                    where po1x.date_order >= %s and po1x.date_order <= %s and po1x.state = 'purchase' and rpx.is_mitra_kerja is not true) as periode_1x,
                (select sum(inv1x.amount_total - inv1x.residual)
                    from account_invoice inv1x
                    left join purchase_order po1x on inv1x.po_id = po1x.id
                    left join res_partner rpx on po1x.partner_id = rpx.id
                    where po1x.date_order >= %s and po1x.date_order <= %s and po1x.state = 'purchase' and inv1x.state != 'draft' and rpx.is_mitra_kerja is not true and inv1x.type = 'in_invoice') as periode_1ax,
                (select sum(po2x.amount_total)
                    from purchase_order po2x
                    left join res_partner rpx on po2x.partner_id = rpx.id
                    where po2x.date_order >= %s and po2x.date_order <= %s and po2x.state = 'purchase' and rpx.is_mitra_kerja is not true) as periode_2x,
                (select sum(inv2x.amount_total - inv2x.residual)
                    from account_invoice inv2x
                    left join purchase_order po2x on inv2x.po_id = po2x.id
                    left join res_partner rpx on po2x.partner_id = rpx.id
                    where po2x.date_order >= %s and po2x.date_order <= %s and po2x.state = 'purchase' and inv2x.state != 'draft' and rpx.is_mitra_kerja is not true and inv2x.type = 'in_invoice') as periode_2ax,
                (select sum(po3x.amount_total)
                    from purchase_order po3x
                    left join res_partner rpx on po3x.partner_id = rpx.id
                    where po3x.date_order >= %s and po3x.date_order <= %s and po3x.state = 'purchase' and rpx.is_mitra_kerja is not true) as periode_3x,
                (select sum(inv3x.amount_total - inv3x.residual)
                    from account_invoice inv3x
                    left join purchase_order po3x on inv3x.po_id = po3x.id
                    left join res_partner rpx on po3x.partner_id = rpx.id
                    where po3x.date_order >= %s and po3x.date_order <= %s and po3x.state = 'purchase' and inv3x.state != 'draft' and rpx.is_mitra_kerja is not true and inv3x.type = 'in_invoice') as periode_3ax,
                (select sum(po4x.amount_total)
                    from purchase_order po4x
                    left join res_partner rpx on po4x.partner_id = rpx.id
                    where po4x.date_order >= %s and po4x.date_order <= %s and po4x.state = 'purchase' and rpx.is_mitra_kerja is not true) as periode_4x, 
                (select sum(inv4x.amount_total - inv4x.residual)
                    from account_invoice inv4x
                    left join purchase_order po4x on inv4x.po_id = po4x.id
                    left join res_partner rpx on po4x.partner_id = rpx.id
                    where po4x.date_order >= %s and po4x.date_order <= %s and po4x.state = 'purchase' and rpx.is_mitra_kerja is not true and inv4x.state != 'draft' and inv4x.type = 'in_invoice') as periode_4ax
                """
            crp = self.env.cr
            crp.execute(sqlp, (p1_date_start,p1_date_end,p1_date_start,p1_date_end,p2_date_start,p2_date_end,p2_date_start,p2_date_end,p3_date_start,p3_date_end,p3_date_start,p3_date_end,p4_date_start,p4_date_end,p4_date_start,p4_date_end,
                p1x_date_start,p1x_date_end,p1x_date_start,p1x_date_end,p2x_date_start,p2x_date_end,p2x_date_start,p2x_date_end,p3x_date_start,p3x_date_end,p3x_date_start,p3x_date_end,p4x_date_start,p4x_date_end,p4x_date_start,p4x_date_end))
            resultp = crp.fetchall()
            if resultp[0][0] == None:
                po_1 = 0.0
            else:
                po_1 = resultp[0][0]
            if resultp[0][1] == None:
                invp_1 = 0.0
            else:
                invp_1 = resultp[0][1]
            if resultp[0][2] == None:
                po_2 = 0.0
            else:
                po_2 = resultp[0][2]
            if resultp[0][3] == None:
                invp_2 = 0.0
            else:
                invp_2 = resultp[0][3]
            if resultp[0][4] == None:
                po_3 = 0.0
            else:
                po_3 = resultp[0][4]
            if resultp[0][5] == None:
                invp_3 = 0.0
            else:
                invp_3 = resultp[0][5]
            if resultp[0][6] == None:
                po_4 = 0.0
            else:
                po_4 = resultp[0][6]
            if resultp[0][7] == None:
                invp_4 = 0.0
            else:
                invp_4 = resultp[0][7]
            sisap1 = (po_1 - invp_1)
            sisap2 = (po_2 - invp_2)
            sisap3 = (po_3 - invp_3)
            sisap4 = (po_4 - invp_4)

            if resultp[0][8] == None:
                po_1x = 0.0
            else:
                po_1x = resultp[0][8]
            if resultp[0][9] == None:
                invp_1x = 0.0
            else:
                invp_1x = resultp[0][9]
            if resultp[0][10] == None:
                po_2x = 0.0
            else:
                po_2x = resultp[0][10]
            if resultp[0][11] == None:
                invp_2x = 0.0
            else:
                invp_2x = resultp[0][11]
            if resultp[0][12] == None:
                po_3x = 0.0
            else:
                po_3x = resultp[0][12]
            if resultp[0][13] == None:
                invp_3x = 0.0
            else:
                invp_3x = resultp[0][13]
            if resultp[0][14] == None:
                po_4x = 0.0
            else:
                po_4x = resultp[0][14]
            if resultp[0][15] == None:
                invp_4x = 0.0
            else:
                invp_4x = resultp[0][15]
            sisap1x = (po_1x - invp_1x)
            sisap2x = (po_2x - invp_2x)
            sisap3x = (po_3x - invp_3x)
            sisap4x = (po_4x - invp_4x)
            
            # insert PO Mitrakerja
            sqls = """
                select 
                (select sum(po1.amount_total)
                    from purchase_order po1
                    left join res_partner rp on po1.partner_id = rp.id
                    where po1.date_order >= %s and po1.date_order <= %s and po1.state = 'purchase' and rp.is_mitra_kerja is true) as periode_1,
                (select sum(inv1.amount_total - inv1.residual)
                    from account_invoice inv1
                    left join purchase_order po1 on inv1.po_id = po1.id
                    left join res_partner rp on po1.partner_id = rp.id
                    where po1.date_order >= %s and po1.date_order <= %s and po1.state = 'purchase' and rp.is_mitra_kerja is true and inv1.state != 'draft' and inv1.type = 'in_invoice') as periode_1a,
                (select sum(po2.amount_total)
                    from purchase_order po2
                    left join res_partner rp on po2.partner_id = rp.id
                    where po2.date_order >= %s and po2.date_order <= %s and po2.state = 'purchase' and rp.is_mitra_kerja is true) as periode_2,
                (select sum(inv2.amount_total - inv2.residual)
                    from account_invoice inv2
                    left join purchase_order po2 on inv2.po_id = po2.id
                    left join res_partner rp on po2.partner_id = rp.id
                    where po2.date_order >= %s and po2.date_order <= %s and po2.state = 'purchase' and rp.is_mitra_kerja is true and inv2.state != 'draft' and inv2.type = 'in_invoice') as periode_2a,
                (select sum(po3.amount_total)
                    from purchase_order po3
                    left join res_partner rp on po3.partner_id = rp.id
                    where po3.date_order >= %s and po3.date_order <= %s and po3.state = 'purchase' and rp.is_mitra_kerja is true) as periode_3,
                (select sum(inv3.amount_total - inv3.residual)
                    from account_invoice inv3
                    left join purchase_order po3 on inv3.po_id = po3.id
                    left join res_partner rp on po3.partner_id = rp.id
                    where po3.date_order >= %s and po3.date_order <= %s and po3.state = 'purchase' and rp.is_mitra_kerja is true and inv3.state != 'draft' and inv3.type = 'in_invoice') as periode_3a,
                (select sum(po4.amount_total)
                    from purchase_order po4
                    left join res_partner rp on po4.partner_id = rp.id
                    where po4.date_order >= %s and po4.date_order <= %s and po4.state = 'purchase' and rp.is_mitra_kerja is true) as periode_4, 
                (select sum(inv4.amount_total - inv4.residual)
                    from account_invoice inv4
                    left join purchase_order po4 on inv4.po_id = po4.id
                    left join res_partner rp on po4.partner_id = rp.id
                    where po4.date_order >= %s and po4.date_order <= %s and po4.state = 'purchase' and rp.is_mitra_kerja is true and inv4.state != 'draft' and inv4.type = 'in_invoice') as periode_4a,
                (select sum(po1x.amount_total)
                    from purchase_order po1x
                    left join res_partner rpx on po1x.partner_id = rpx.id
                    where po1x.date_order >= %s and po1x.date_order <= %s and po1x.state = 'purchase' and rpx.is_mitra_kerja is true) as periode_1x,
                (select sum(inv1x.amount_total - inv1x.residual)
                    from account_invoice inv1x
                    left join purchase_order po1x on inv1x.po_id = po1x.id
                    left join res_partner rpx on po1x.partner_id = rpx.id
                    where po1x.date_order >= %s and po1x.date_order <= %s and po1x.state = 'purchase' and rpx.is_mitra_kerja is true and inv1x.state != 'draft' and inv1x.type = 'in_invoice') as periode_1ax,
                (select sum(po2x.amount_total)
                    from purchase_order po2x
                    left join res_partner rpx on po2x.partner_id = rpx.id
                    where po2x.date_order >= %s and po2x.date_order <= %s and po2x.state = 'purchase' and rpx.is_mitra_kerja is true) as periode_2x,
                (select sum(inv2x.amount_total - inv2x.residual)
                    from account_invoice inv2x
                    left join purchase_order po2x on inv2x.po_id = po2x.id
                    left join res_partner rpx on po2x.partner_id = rpx.id
                    where po2x.date_order >= %s and po2x.date_order <= %s and po2x.state = 'purchase' and rpx.is_mitra_kerja is true and inv2x.state != 'draft' and inv2x.type = 'in_invoice') as periode_2ax,
                (select sum(po3x.amount_total)
                    from purchase_order po3x
                    left join res_partner rpx on po3x.partner_id = rpx.id
                    where po3x.date_order >= %s and po3x.date_order <= %s and po3x.state = 'purchase' and rpx.is_mitra_kerja is true) as periode_3x,
                (select sum(inv3x.amount_total - inv3x.residual)
                    from account_invoice inv3x
                    left join purchase_order po3x on inv3x.po_id = po3x.id
                    left join res_partner rpx on po3x.partner_id = rpx.id
                    where po3x.date_order >= %s and po3x.date_order <= %s and po3x.state = 'purchase' and rpx.is_mitra_kerja is true and inv3x.state != 'draft' and inv3x.type = 'in_invoice') as periode_3ax,
                (select sum(po4x.amount_total)
                    from purchase_order po4x
                    left join res_partner rpx on po4x.partner_id = rpx.id
                    where po4x.date_order >= %s and po4x.date_order <= %s and po4x.state = 'purchase' and rpx.is_mitra_kerja is true) as periode_4x, 
                (select sum(inv4x.amount_total - inv4x.residual)
                    from account_invoice inv4x
                    left join purchase_order po4x on inv4x.po_id = po4x.id
                    left join res_partner rpx on po4x.partner_id = rpx.id
                    where po4x.date_order >= %s and po4x.date_order <= %s and po4x.state = 'purchase' and rpx.is_mitra_kerja is true and inv4x.state != 'draft' and inv4x.type = 'in_invoice') as periode_4ax
                """
            crs = self.env.cr
            crs.execute(sqls, (p1_date_start,p1_date_end,p1_date_start,p1_date_end,p2_date_start,p2_date_end,p2_date_start,p2_date_end,p3_date_start,p3_date_end,p3_date_start,p3_date_end,p4_date_start,p4_date_end,p4_date_start,p4_date_end,
                p1x_date_start,p1x_date_end,p1x_date_start,p1x_date_end,p2x_date_start,p2x_date_end,p2x_date_start,p2x_date_end,p3x_date_start,p3x_date_end,p3x_date_start,p3x_date_end,p4x_date_start,p4x_date_end,p4x_date_start,p4x_date_end))
            results = crs.fetchall()
            # import pdb;pdb.set_trace()
            if results[0][0] == None:
                pos_1 = 0.0
            else:
                pos_1 = results[0][0]
            if results[0][1] == None:
                invs_1 = 0.0
            else:
                invs_1 = results[0][1]
            if results[0][2] == None:
                pos_2 = 0.0
            else:
                pos_2 = results[0][2]
            if results[0][3] == None:
                invs_2 = 0.0
            else:
                invs_2 = results[0][3]
            if results[0][4] == None:
                pos_3 = 0.0
            else:
                pos_3 = results[0][4]
            if results[0][5] == None:
                invs_3 = 0.0
            else:
                invs_3 = results[0][5]
            if results[0][6] == None:
                pos_4 = 0.0
            else:
                pos_4 = results[0][6]
            if results[0][7] == None:
                invs_4 = 0.0
            else:
                invs_4 = results[0][7]
            sisas1 = (pos_1 - invs_1)
            sisas2 = (pos_2 - invs_2)
            sisas3 = (pos_3 - invs_3)
            sisas4 = (pos_4 - invs_4)

            if results[0][8] == None:
                pos_1x = 0.0
            else:
                pos_1x = results[0][8]
            if results[0][9] == None:
                invs_1x = 0.0
            else:
                invs_1x = results[0][9]
            if results[0][10] == None:
                pos_2x = 0.0
            else:
                pos_2x = results[0][10]
            if results[0][11] == None:
                invs_2x = 0.0
            else:
                invs_2x = results[0][11]
            if results[0][12] == None:
                pos_3x = 0.0
            else:
                pos_3x = results[0][12]
            if results[0][13] == None:
                invs_3x = 0.0
            else:
                invs_3x = results[0][13]
            if results[0][14] == None:
                pos_4x = 0.0
            else:
                pos_4x = results[0][14]
            if results[0][15] == None:
                invs_4x = 0.0
            else:
                invs_4x = results[0][15]
            sisas1x = (pos_1x - invs_1x)
            sisas2x = (pos_2x - invs_2x)
            sisas3x = (pos_3x - invs_3x)
            sisas4x = (pos_4x - invs_4x)
            
            
            # insert Hutang Bank
            sqlb = """select 
                (select abs(sum(aml1.balance))
                    from account_move_line aml1
                    left join account_move am1 on aml1.move_id = am1.id
                    left join account_account aa1 on aml1.account_id = aa1.id
                    left join account_account_vit_posisi_dana_config_rel aapd1 on aapd1.account_account_id = aa1.id
                    left join vit_posisi_dana_config pdc1 on aapd1.vit_posisi_dana_config_id = pdc1.id
                    where aml1.date >= %s and aml1.date <= %s and am1.state = 'posted' and pdc1.name = 'aksep') as periode_1,
                (select abs(sum(aml2.balance))
                    from account_move_line aml2
                    left join account_move am2 on aml2.move_id = am2.id
                    left join account_account aa2 on aml2.account_id = aa2.id
                    left join account_account_vit_posisi_dana_config_rel aapd2 on aapd2.account_account_id = aa2.id
                    left join vit_posisi_dana_config pdc2 on aapd2.vit_posisi_dana_config_id = pdc2.id
                    where aml2.date >= %s and aml2.date <= %s and am2.state = 'posted' and pdc2.name = 'aksep') as periode_2,
                (select abs(sum(aml3.balance))
                    from account_move_line aml3
                    left join account_move am3 on aml3.move_id = am3.id
                    left join account_account aa3 on aml3.account_id = aa3.id
                    left join account_account_vit_posisi_dana_config_rel aapd3 on aapd3.account_account_id = aa3.id
                    left join vit_posisi_dana_config pdc3 on aapd3.vit_posisi_dana_config_id = pdc3.id
                    where aml3.date >= %s and aml3.date <= %s and am3.state = 'posted' and pdc3.name = 'aksep') as periode_3,
                (select abs(sum(aml4.balance))
                    from account_move_line aml4
                    left join account_move am4 on aml4.move_id = am4.id
                    left join account_account aa4 on aml4.account_id = aa4.id
                    left join account_account_vit_posisi_dana_config_rel aapd4 on aapd4.account_account_id = aa4.id
                    left join vit_posisi_dana_config pdc4 on aapd4.vit_posisi_dana_config_id = pdc4.id
                    where aml4.date >= %s and aml4.date <= %s and am4.state = 'posted' and pdc4.name = 'aksep') as periode_4,
                (select abs(sum(aml1x.balance))
                    from account_move_line aml1x
                    left join account_move am1x on aml1x.move_id = am1x.id
                    left join account_account aa1x on aml1x.account_id = aa1x.id
                    left join account_account_vit_posisi_dana_config_rel aapd1x on aapd1x.account_account_id = aa1x.id
                    left join vit_posisi_dana_config pdc1x on aapd1x.vit_posisi_dana_config_id = pdc1x.id
                    where aml1x.date >= %s and aml1x.date <= %s and am1x.state = 'posted' and pdc1x.name = 'aksep') as periode_1x,
                (select abs(sum(aml2x.balance))
                    from account_move_line aml2x
                    left join account_move am2x on aml2x.move_id = am2x.id
                    left join account_account aa2x on aml2x.account_id = aa2x.id
                    left join account_account_vit_posisi_dana_config_rel aapd2x on aapd2x.account_account_id = aa2x.id
                    left join vit_posisi_dana_config pdc2x on aapd2x.vit_posisi_dana_config_id = pdc2x.id
                    where aml2x.date >= %s and aml2x.date <= %s and am2x.state = 'posted' and pdc2x.name = 'aksep') as periode_2x,
                (select abs(sum(aml3x.balance))
                    from account_move_line aml3x
                    left join account_move am3x on aml3x.move_id = am3x.id
                    left join account_account aa3x on aml3x.account_id = aa3x.id
                    left join account_account_vit_posisi_dana_config_rel aapd3x on aapd3x.account_account_id = aa3x.id
                    left join vit_posisi_dana_config pdc3x on aapd3x.vit_posisi_dana_config_id = pdc3x.id
                    where aml3x.date >= %s and aml3x.date <= %s and am3x.state = 'posted' and pdc3x.name = 'aksep') as periode_3x,
                (select abs(sum(aml4x.balance))
                    from account_move_line aml4x
                    left join account_move am4x on aml4x.move_id = am4x.id
                    left join account_account aa4x on aml4x.account_id = aa4x.id
                    left join account_account_vit_posisi_dana_config_rel aapd4x on aapd4x.account_account_id = aa4x.id
                    left join vit_posisi_dana_config pdc4x on aapd4x.vit_posisi_dana_config_id = pdc4x.id
                    where aml4x.date >= %s and aml4x.date <= %s and am4x.state = 'posted' and pdc4x.name = 'aksep') as periode_4x
                """
            crb = self.env.cr
            crb.execute(sqlb, (p1_date_start,p1_date_end,p2_date_start,p2_date_end,p3_date_start,p3_date_end,p4_date_start,p4_date_end,
                p1x_date_start,p1x_date_end,p2x_date_start,p2x_date_end,p3x_date_start,p3x_date_end,p4x_date_start,p4x_date_end))
            resultb = crb.fetchall()
            if resultb[0][0] == None:
                aksep1 = 0.0
            else:
                aksep1 = resultb[0][0]
            if resultb[0][1] == None:
                aksep2 = 0.0
            else:
                aksep2 = resultb[0][1]
            if resultb[0][2] == None:
                aksep3 = 0.0
            else:
                aksep3 = resultb[0][2]
            if resultb[0][3] == None:
                aksep4 = 0.0
            else:
                aksep4 = resultb[0][3]

            if resultb[0][4] == None:
                aksep1x = 0.0
            else:
                aksep1x = resultb[0][4]
            if resultb[0][5] == None:
                aksep2x = 0.0
            else:
                aksep2x = resultb[0][5]
            if resultb[0][6] == None:
                aksep3x = 0.0
            else:
                aksep3x = resultb[0][6]
            if resultb[0][7] == None:
                aksep4x = 0.0
            else:
                aksep4x = resultb[0][7]

            

            # insert Saldo Bank
            sqlsb = """select 
                (select sum(aml1.balance)
                    from account_move_line aml1
                    left join account_move am1 on aml1.move_id = am1.id
                    left join account_account aa1 on aml1.account_id = aa1.id
                    left join account_account_vit_posisi_dana_config_rel aapd1 on aapd1.account_account_id = aa1.id
                    left join vit_posisi_dana_config pdc1 on aapd1.vit_posisi_dana_config_id = pdc1.id
                    left join account_journal aj1 on am1.journal_id = aj1.id
                    where aml1.date <= %s and am1.state = 'posted' and pdc1.name = 'saldo' and aj1.type = 'bank') as periode_1,
                (select sum(aml2.balance)
                    from account_move_line aml2
                    left join account_move am2 on aml2.move_id = am2.id
                    left join account_account aa2 on aml2.account_id = aa2.id
                    left join account_account_vit_posisi_dana_config_rel aapd2 on aapd2.account_account_id = aa2.id
                    left join vit_posisi_dana_config pdc2 on aapd2.vit_posisi_dana_config_id = pdc2.id
                    left join account_journal aj2 on am2.journal_id = aj2.id
                    where aml2.date <= %s and am2.state = 'posted' and pdc2.name = 'saldo' and aj2.type = 'bank') as periode_2,
                (select sum(aml3.balance)
                    from account_move_line aml3
                    left join account_move am3 on aml3.move_id = am3.id
                    left join account_account aa3 on aml3.account_id = aa3.id
                    left join account_account_vit_posisi_dana_config_rel aapd3 on aapd3.account_account_id = aa3.id
                    left join vit_posisi_dana_config pdc3 on aapd3.vit_posisi_dana_config_id = pdc3.id
                    left join account_journal aj3 on am3.journal_id = aj3.id
                    where aml3.date <= %s and am3.state = 'posted' and pdc3.name = 'saldo' and aj3.type = 'bank') as periode_3,
                (select sum(aml4.balance)
                    from account_move_line aml4
                    left join account_move am4 on aml4.move_id = am4.id
                    left join account_account aa4 on aml4.account_id = aa4.id
                    left join account_account_vit_posisi_dana_config_rel aapd4 on aapd4.account_account_id = aa4.id
                    left join vit_posisi_dana_config pdc4 on aapd4.vit_posisi_dana_config_id = pdc4.id
                    left join account_journal aj4 on am4.journal_id = aj4.id
                    where aml4.date <= %s and am4.state = 'posted' and pdc4.name = 'saldo' and aj4.type = 'bank') as periode_4,
                (select sum(aml1x.balance)
                    from account_move_line aml1x
                    left join account_move am1x on aml1x.move_id = am1x.id
                    left join account_account aa1x on aml1x.account_id = aa1x.id
                    left join account_account_vit_posisi_dana_config_rel aapd1x on aapd1x.account_account_id = aa1x.id
                    left join vit_posisi_dana_config pdc1x on aapd1x.vit_posisi_dana_config_id = pdc1x.id
                    left join account_journal aj1x on am1x.journal_id = aj1x.id
                    where aml1x.date <= %s and am1x.state = 'posted' and pdc1x.name = 'saldo' and aj1x.type = 'bank') as periode_1x,
                (select sum(aml2x.balance)
                    from account_move_line aml2x
                    left join account_move am2x on aml2x.move_id = am2x.id
                    left join account_account aa2x on aml2x.account_id = aa2x.id
                    left join account_account_vit_posisi_dana_config_rel aapd2x on aapd2x.account_account_id = aa2x.id
                    left join vit_posisi_dana_config pdc2x on aapd2x.vit_posisi_dana_config_id = pdc2x.id
                    left join account_journal aj2x on am2x.journal_id = aj2x.id
                    where aml2x.date <= %s and am2x.state = 'posted' and pdc2x.name = 'saldo' and aj2x.type = 'bank') as periode_2x,
                (select sum(aml3x.balance)
                    from account_move_line aml3x
                    left join account_move am3x on aml3x.move_id = am3x.id
                    left join account_account aa3x on aml3x.account_id = aa3x.id
                    left join account_account_vit_posisi_dana_config_rel aapd3x on aapd3x.account_account_id = aa3x.id
                    left join vit_posisi_dana_config pdc3x on aapd3x.vit_posisi_dana_config_id = pdc3x.id
                    left join account_journal aj3x on am3x.journal_id = aj3x.id
                    where aml3x.date <= %s and am3x.state = 'posted' and pdc3x.name = 'saldo' and aj3x.type = 'bank') as periode_3x,
                (select sum(aml4x.balance)
                    from account_move_line aml4x
                    left join account_move am4x on aml4x.move_id = am4x.id
                    left join account_account aa4x on aml4x.account_id = aa4x.id
                    left join account_account_vit_posisi_dana_config_rel aapd4x on aapd4x.account_account_id = aa4x.id
                    left join vit_posisi_dana_config pdc4x on aapd4x.vit_posisi_dana_config_id = pdc4x.id
                    left join account_journal aj4x on am4x.journal_id = aj4x.id
                    where aml4x.date <= %s and am4x.state = 'posted' and pdc4x.name = 'saldo' and aj4x.type = 'bank') as periode_4x
                """
            crsb = self.env.cr
            crsb.execute(sqlsb, (p1_date_end,p2_date_end,p3_date_end,p4_date_end,
                p1x_date_end,p2x_date_end,p3x_date_end,p4x_date_end))
            resultsb = crsb.fetchall()
            if resultsb[0][0] == None:
                saldo1 = 0.0
            else:
                saldo1 = resultsb[0][0]
            if resultsb[0][1] == None:
                saldo2 = 0.0
            else:
                saldo2 = resultsb[0][1]
            if resultsb[0][2] == None:
                saldo3 = 0.0
            else:
                saldo3 = resultsb[0][2]
            if resultsb[0][3] == None:
                saldo4 = 0.0
            else:
                saldo4 = resultsb[0][3]

            if resultsb[0][4] == None:
                saldo1x = 0.0
            else:
                saldo1x = resultsb[0][4]
            if resultsb[0][5] == None:
                saldo2x = 0.0
            else:
                saldo2x = resultsb[0][5]
            if resultsb[0][6] == None:
                saldo3x = 0.0
            else:
                saldo3x = resultsb[0][6]
            if resultsb[0][7] == None:
                saldo4x = 0.0
            else:
                saldo4x = resultsb[0][7]

            # insert saldo
            # saldo1 = sd1
            # saldo2 = sd1 + sd2
            # saldo3 = sd1 + sd2 + sd3
            # saldo4 = sd1 + sd2 + sd3 + sd4

            # saldo1 = sd1
            # saldo2 = sd1 + sd2
            # saldo3 = sd1 + sd2 + sd3
            # saldo4 = sd1 + sd2 + sd3 + sd4

            

            # insert balance
            balance1 = sisao1 - sisap1 - sisas1 - aksep1 + saldo1
            balance2 = sisao2 - sisap2 - sisas2 - aksep2 + saldo2
            balance3 = sisao3 - sisap3 - sisas3 - aksep3 + saldo3
            balance4 = sisao4 - sisap4 - sisas4 - aksep4 + saldo4

            balance1x = sisao1x - sisap1x - sisas1x - aksep1x + saldo1x
            balance2x = sisao2x - sisap2x - sisas2x - aksep2x + saldo2x
            balance3x = sisao3x - sisap3x - sisas3x - aksep3x + saldo3x
            balance4x = sisao4x - sisap4x - sisas4x - aksep4x + saldo4x

            

            # insert akumulasi
            aku1 = balance1
            aku2 = balance1 + balance2
            aku3 = aku2 + balance3
            aku4 = aku3 + balance4

            aku1x = balance1x
            aku2x = balance1x + balance2x
            aku3x = aku2x + balance3x
            aku4x = aku3x + balance4x

            grand_or = or_1 + or_2 + or_3 + or_4 + or_1x + or_2x + or_3x + or_4x
            grand_or_inv = inv_1 + inv_2 + inv_3 + inv_4 + inv_1x + inv_2x + inv_3x + inv_4x
            grand_or_sisa = sisao1 + sisao2 + sisao3 + sisao4 + sisao1x + sisao2x + sisao3x + sisao4x
            grand_po_data = po_1 + po_2 + po_3 + po_4 + po_1x + po_2x + po_3x + po_4x
            grand_po_bayar = invp_1 + invp_2 + invp_3 + invp_4 + invp_1x + invp_2x + invp_3x + invp_4x
            grand_po_sisa = sisap1 + sisap2 + sisap3 + sisap4 + sisap1x + sisap2x + sisap3x + sisap4x
            grand_mk_data = pos_1 + pos_2 + pos_3 + pos_4 + pos_1x + pos_2x + pos_3x + pos_4x
            grand_mk_bayar = invs_1 + invs_2 + invs_3 + invs_4 + invs_1x + invs_2x + invs_3x + invs_4x
            grand_mk_sisa = sisas1 + sisas2 + sisas3 + sisas4 + sisas1x + sisas2x + sisas3x + sisas4x
            grand_aksep_data = aksep1 + aksep2 + aksep3 + aksep4 + aksep1x + aksep2x + aksep3x + aksep4x
            grand_saldo_data = saldo4x
            grand_balance_data = balance1 + balance2 + balance3 + balance4 + balance1x + balance2x + balance3x + balance4x
            grand_akumulasi_data = aku4 + aku4x
            grand_piutang_data = pb_1 + pb_2 + pb_3 + pb_4 + pb_1x + pb_2x + pb_3x + pb_4x

            
            # insert Piutang berjalan
            sqlpb = """
                select 
                (select sum(aml1.balance)
                    from account_move_line aml1
                    left join account_move am1 on aml1.move_id = am1.id
                    left join account_invoice inv1 on inv1.move_id =am1.id
                    left join account_account aa1 on aml1.account_id = aa1.id
                    left join account_account_vit_posisi_dana_config_rel aapd1 on aapd1.account_account_id = aa1.id
                    left join vit_posisi_dana_config pdc1 on aapd1.vit_posisi_dana_config_id = pdc1.id
                    where inv1.date_invoice >= %s and inv1.date_invoice <= %s and inv1.state = 'open' and pdc1.name = 'piutang') as periode_1,
                (select sum(aml2.balance)
                    from account_move_line aml2
                    left join account_move am2 on aml2.move_id = am2.id
                    left join account_invoice inv2 on inv2.move_id =am2.id
                    left join account_account aa2 on aml2.account_id = aa2.id
                    left join account_account_vit_posisi_dana_config_rel aapd2 on aapd2.account_account_id = aa2.id
                    left join vit_posisi_dana_config pdc2 on aapd2.vit_posisi_dana_config_id = pdc2.id
                    where inv2.date_invoice >= %s and inv2.date_invoice <= %s and inv2.state = 'open' and pdc2.name = 'piutang') as periode_2,
                (select sum(aml3.balance)
                    from account_move_line aml3
                    left join account_move am3 on aml3.move_id = am3.id
                    left join account_invoice inv3 on inv3.move_id =am3.id
                    left join account_account aa3 on aml3.account_id = aa3.id
                    left join account_account_vit_posisi_dana_config_rel aapd3 on aapd3.account_account_id = aa3.id
                    left join vit_posisi_dana_config pdc3 on aapd3.vit_posisi_dana_config_id = pdc3.id
                    where inv3.date_invoice >= %s and inv3.date_invoice <= %s and inv3.state = 'open' and pdc3.name = 'piutang') as periode_3,
                (select sum(aml4.balance)
                    from account_move_line aml4
                    left join account_move am4 on aml4.move_id = am4.id
                    left join account_invoice inv4 on inv4.move_id =am4.id
                    left join account_account aa4 on aml4.account_id = aa4.id
                    left join account_account_vit_posisi_dana_config_rel aapd4 on aapd4.account_account_id = aa4.id
                    left join vit_posisi_dana_config pdc4 on aapd4.vit_posisi_dana_config_id = pdc4.id
                    where inv4.date_invoice >= %s and inv4.date_invoice <= %s and inv4.state = 'open' and pdc4.name = 'piutang') as periode_4,
                (select sum(aml1x.balance)
                    from account_move_line aml1x
                    left join account_move am1x on aml1x.move_id = am1x.id
                    left join account_invoice inv1x on inv1x.move_id =am1x.id
                    left join account_account aa1x on aml1x.account_id = aa1x.id
                    left join account_account_vit_posisi_dana_config_rel aapd1x on aapd1x.account_account_id = aa1x.id
                    left join vit_posisi_dana_config pdc1x on aapd1x.vit_posisi_dana_config_id = pdc1x.id
                    where inv1x.date_invoice >= %s and inv1x.date_invoice <= %s and inv1x.state = 'open' and pdc1x.name = 'piutang') as periode_1x,
                (select sum(aml2x.balance)
                    from account_move_line aml2x
                    left join account_move am2x on aml2x.move_id = am2x.id
                    left join account_invoice inv2x on inv2x.move_id =am2x.id
                    left join account_account aa2x on aml2x.account_id = aa2x.id
                    left join account_account_vit_posisi_dana_config_rel aapd2x on aapd2x.account_account_id = aa2x.id
                    left join vit_posisi_dana_config pdc2x on aapd2x.vit_posisi_dana_config_id = pdc2x.id
                    where inv2x.date_invoice >= %s and inv2x.date_invoice <= %s and inv2x.state = 'open' and pdc2x.name = 'piutang') as periode_2x,
                (select sum(aml3x.balance)
                    from account_move_line aml3x
                    left join account_move am3x on aml3x.move_id = am3x.id
                    left join account_invoice inv3x on inv3x.move_id =am3x.id
                    left join account_account aa3x on aml3x.account_id = aa3x.id
                    left join account_account_vit_posisi_dana_config_rel aapd3x on aapd3x.account_account_id = aa3x.id
                    left join vit_posisi_dana_config pdc3x on aapd3x.vit_posisi_dana_config_id = pdc3x.id
                    where inv3x.date_invoice >= %s and inv3x.date_invoice <= %s and inv3x.state = 'open' and pdc3x.name = 'piutang') as periode_3x,
                (select sum(aml4x.balance)
                    from account_move_line aml4x
                    left join account_move am4x on aml4x.move_id = am4x.id
                    left join account_invoice inv4x on inv4x.move_id =am4x.id
                    left join account_account aa4x on aml4x.account_id = aa4x.id
                    left join account_account_vit_posisi_dana_config_rel aapd4x on aapd4x.account_account_id = aa4x.id
                    left join vit_posisi_dana_config pdc4x on aapd4x.vit_posisi_dana_config_id = pdc4x.id
                    where inv4x.date_invoice >= %s and inv4x.date_invoice <= %s and inv4x.state = 'open' and pdc4x.name = 'piutang') as periode_4x
                """
            crpb = self.env.cr
            crpb.execute(sqlpb, (p1_date_start,p1_date_end,p2_date_start,p2_date_end,p3_date_start,p3_date_end,p4_date_start,p4_date_end,
                p1x_date_start,p1x_date_end,p2x_date_start,p2x_date_end,p3x_date_start,p3x_date_end,p4x_date_start,p4x_date_end))
            resultpb = crpb.fetchall()
            if resultpb[0][0] == None:
                pb_1 = 0.0
            else:
                pb_1 = resultpb[0][0]
            if resultpb[0][1] == None:
                pb_2 = 0.0
            else:
                pb_2 = resultpb[0][1]
            if resultpb[0][2] == None:
                pb_3 = 0.0
            else:
                pb_3 = resultpb[0][2]
            if resultpb[0][3] == None:
                pb_4 = 0.0
            else:
                pb_4 = resultpb[0][3]

            if resultpb[0][4] == None:
                pb_1x = 0.0
            else:
                pb_1x = resultpb[0][4]
            if resultpb[0][5] == None:
                pb_2x = 0.0
            else:
                pb_2x = resultpb[0][5]
            if resultpb[0][6] == None:
                pb_3x = 0.0
            else:
                pb_3x = resultpb[0][6]
            if resultpb[0][7] == None:
                pb_4x = 0.0
            else:
                pb_4x = resultpb[0][7]

           
            tahun = "<table style='font-size:12px'><tbody><tr><th style='border:1px solid #000000'><br></th><th style='border-left:1px solid #000000;border-top:1px solid #000000'><br></th><th style='border-top:1px solid #000000;padding:5px;text-align:right;color:#000000'>Tahun&nbsp;%s</th><th style='border-top:1px solid #000000'><br></th><th style='border-top:1px solid #000000'><br></th><th style='border-left:1px solid #000000;border-top:1px solid #000000'><br></th><th style='border-top:1px solid #000000;text-align:right;color:#000000'>Tahun&nbsp;%s</th><th style='border-top:1px solid #000000'><br></th><th style='border-top:1px solid #000000'><br></th><th style='border-right:1px solid #000000;border-left:1px solid #000000;border-top:1px solid #000000'><br></th></tr>" % (pod.year,pod.c_year)
            header = "<tr style='background-color:#d3d3d3'><th style='border:1px solid #000000;padding-left:5px;color:#000000'>Posisi Keuangan</th><th style='border:1px solid #000000;text-align:center;width:9%;color:#000000'>Periode 1 <br>(Jan-Mar)</th><th style='border:1px solid #000000;text-align:center;width:9%;color:#000000'>Periode 2 <br>(Apr-Jun)</th><th style='border:1px solid #000000;text-align:center;width:9%;color:#000000'>Periode 3 <br>(Jul-Sep)</th><th style='border:1px solid #000000;text-align:center;width:9%;color:#000000'>Periode 4 <br>(Okt-Dec)</th><th style='border:1px solid #000000;text-align:center;width:9%;color:#000000'>Periode 1 <br>(Jan-Mar)</th><th style='border:1px solid #000000;text-align:center;width:9%;color:#000000'>Periode 2 <br>(Apr-Jun)</th><th style='border:1px solid #000000;text-align:center;width:9%;color:#000000'>Periode 3 <br>(Jul-Sep)</th><th style='border:1px solid #000000;text-align:center;width:9%;color:#000000'>Periode 4 <br>(Okt-Dec)</th><th style='border:1px solid #000000;text-align:center;width:11%;color:#000000'>Grand Total</th></tr>"
            or_data = "<tr><td style='border-left:1px solid #000000;border-bottom:1px solid #9C9C94;padding:5px;color:#000000'>Order Receive (OR)</td><td style='border-left:1px solid #000000;border-bottom:1px solid #9C9C94;text-align:right;padding:5px;color:#000000'>%s</td><td style='border-left:1px solid #000000;border-bottom:1px solid #9C9C94;text-align:right;padding:5px;color:#000000'>%s</td><td style='border-left:1px solid #000000;border-bottom:1px solid #9C9C94;text-align:right;padding:5px;color:#000000'>%s</td><td style='border-left:1px solid #000000;border-bottom:1px solid #9C9C94;text-align:right;padding:5px;color:#000000'>%s</td><td style='border-left:1px solid #000000;border-bottom:1px solid #9C9C94;text-align:right;padding:5px;color:#000000'>%s</td><td style='border-left:1px solid #000000;border-bottom:1px solid #9C9C94;text-align:right;padding:5px;color:#000000'>%s</td><td style='border-left:1px solid #000000;border-bottom:1px solid #9C9C94;text-align:right;padding:5px;color:#000000'>%s</td><td style='border-left:1px solid #000000;border-bottom:1px solid #9C9C94;text-align:right;padding:5px;color:#000000'>%s</td><td style='border-left:1px solid #000000;border-right:1px solid #000000;border-bottom:1px solid #9C9C94;padding:5px;text-align:right;color:#000000'>%s</td></tr>" % ("{:,.2f}".format(or_1),"{:,.2f}".format(or_2),"{:,.2f}".format(or_3),"{:,.2f}".format(or_4),"{:,.2f}".format(or_1x),"{:,.2f}".format(or_2x),"{:,.2f}".format(or_3x),"{:,.2f}".format(or_4x),"{:,.2f}".format(grand_or))
            or_bayar = "<tr><td style='border-left:1px solid #000000;border-bottom:1px solid #9C9C94;padding:5px;color:#000000'>Sudah dibayar</td><td style='border-left:1px solid #000000;border-bottom:1px solid #9C9C94;text-align:right;padding:5px;color:#000000'>%s</td><td style='border-left:1px solid #000000;border-bottom:1px solid #9C9C94;text-align:right;padding:5px;color:#000000'>%s</td><td style='border-left:1px solid #000000;border-bottom:1px solid #9C9C94;text-align:right;padding:5px;color:#000000'>%s</td><td style='border-left:1px solid #000000;border-bottom:1px solid #9C9C94;text-align:right;padding:5px;color:#000000'>%s</td><td style='border-left:1px solid #000000;border-bottom:1px solid #9C9C94;text-align:right;padding:5px;color:#000000'>%s</td><td style='border-left:1px solid #000000;border-bottom:1px solid #9C9C94;text-align:right;padding:5px;color:#000000'>%s</td><td style='border-left:1px solid #000000;border-bottom:1px solid #9C9C94;text-align:right;padding:5px;color:#000000'>%s</td><td style='border-left:1px solid #000000;border-bottom:1px solid #9C9C94;text-align:right;padding:5px;color:#000000'>%s</td><td style='border-left:1px solid #000000;border-right:1px solid #000000;border-bottom:1px solid #9C9C94;padding:5px;text-align:right;color:#000000'>%s</td></tr>" % ("{:,.2f}".format(inv_1),"{:,.2f}".format(inv_2),"{:,.2f}".format(inv_3),"{:,.2f}".format(inv_4),"{:,.2f}".format(inv_1x),"{:,.2f}".format(inv_2x),"{:,.2f}".format(inv_3x),"{:,.2f}".format(inv_4x),"{:,.2f}".format(grand_or_inv))
            or_sisa = "<tr style='background-color: #dcdcdc;'><td style='border-left:1px solid #000000;border-bottom:1px solid #000000;padding:5px;color:#000000'><b>Sisa</b></td><td style='border-left:1px solid #000000;border-bottom:1px solid #000000;text-align:right;padding:5px;color:#000000'><b>%s</b></td><td style='border-left:1px solid #000000;border-bottom:1px solid #000000;text-align:right;padding:5px;color:#000000'><b>%s</b></td><td style='border-left:1px solid #000000;border-bottom:1px solid #000000;text-align:right;padding:5px;color:#000000'><b>%s</b></td><td style='border-left:1px solid #000000;border-bottom:1px solid #000000;text-align:right;padding:5px;color:#000000'><b>%s</b></td><td style='border-left:1px solid #000000;border-bottom:1px solid #000000;text-align:right;padding:5px;color:#000000'><b>%s</b></td><td style='border-left:1px solid #000000;border-bottom:1px solid #000000;text-align:right;padding:5px;color:#000000'><b>%s</b></td><td style='border-left:1px solid #000000;border-bottom:1px solid #000000;text-align:right;padding:5px;color:#000000'><b>%s</b></td><td style='border-left:1px solid #000000;border-bottom:1px solid #000000;text-align:right;padding:5px;color:#000000'><b>%s</b></td><td style='border-left:1px solid #000000;border-right:1px solid #000000;border-bottom:1px solid #000000;padding:5px;text-align:right;color:#000000'>%s</td></tr>" % ("{:,.2f}".format(sisao1),"{:,.2f}".format(sisao2),"{:,.2f}".format(sisao3),"{:,.2f}".format(sisao4),"{:,.2f}".format(sisao1x),"{:,.2f}".format(sisao2x),"{:,.2f}".format(sisao3x),"{:,.2f}".format(sisao4x),"{:,.2f}".format(grand_or_sisa))
            po_data = "<tr><td style='border-left:1px solid #000000;border-bottom:1px solid #9C9C94;padding:5px;color:#000000'>PO Purchasing</td><td style='border-left:1px solid #000000;border-bottom:1px solid #9C9C94;text-align:right;padding:5px;color:#000000'>%s</td><td style='border-left:1px solid #000000;border-bottom:1px solid #9C9C94;text-align:right;padding:5px;color:#000000'>%s</td><td style='border-left:1px solid #000000;border-bottom:1px solid #9C9C94;text-align:right;padding:5px;color:#000000'>%s</td><td style='border-left:1px solid #000000;border-bottom:1px solid #9C9C94;text-align:right;padding:5px;color:#000000'>%s</td><td style='border-left:1px solid #000000;border-bottom:1px solid #9C9C94;text-align:right;padding:5px;color:#000000'>%s</td><td style='border-left:1px solid #000000;border-bottom:1px solid #9C9C94;text-align:right;padding:5px;color:#000000'>%s</td><td style='border-left:1px solid #000000;border-bottom:1px solid #9C9C94;text-align:right;padding:5px;color:#000000'>%s</td><td style='border-left:1px solid #000000;border-bottom:1px solid #9C9C94;text-align:right;padding:5px;color:#000000'>%s</td><td style='border-left:1px solid #000000;border-right:1px solid #000000;border-bottom:1px solid #9C9C94;padding:5px;text-align:right;color:#000000'>%s</td></tr>" % ("{:,.2f}".format(po_1),"{:,.2f}".format(po_2),"{:,.2f}".format(po_3),"{:,.2f}".format(po_4),"{:,.2f}".format(po_1x),"{:,.2f}".format(po_2x),"{:,.2f}".format(po_3x),"{:,.2f}".format(po_4x),"{:,.2f}".format(grand_po_data))
            po_bayar = "<tr><td style='border-left:1px solid #000000;border-bottom:1px solid #9C9C94;padding:5px;color:#000000'>Sudah dibayar</td><td style='border-left:1px solid #000000;border-bottom:1px solid #9C9C94;text-align:right;padding:5px;color:#000000'>%s</td><td style='border-left:1px solid #000000;border-bottom:1px solid #9C9C94;text-align:right;padding:5px;color:#000000'>%s</td><td style='border-left:1px solid #000000;border-bottom:1px solid #9C9C94;text-align:right;padding:5px;color:#000000'>%s</td><td style='border-left:1px solid #000000;border-bottom:1px solid #9C9C94;text-align:right;padding:5px;color:#000000'>%s</td><td style='border-left:1px solid #000000;border-bottom:1px solid #9C9C94;text-align:right;padding:5px;color:#000000'>%s</td><td style='border-left:1px solid #000000;border-bottom:1px solid #9C9C94;text-align:right;padding:5px;color:#000000'>%s</td><td style='border-left:1px solid #000000;border-bottom:1px solid #9C9C94;text-align:right;padding:5px;color:#000000'>%s</td><td style='border-left:1px solid #000000;border-bottom:1px solid #9C9C94;text-align:right;padding:5px;color:#000000'>%s</td><td style='border-left:1px solid #000000;border-right:1px solid #000000;border-bottom:1px solid #9C9C94;padding:5px;text-align:right;color:#000000'>%s</td></tr>" % ("{:,.2f}".format(invp_1),"{:,.2f}".format(invp_2),"{:,.2f}".format(invp_3),"{:,.2f}".format(invp_4),"{:,.2f}".format(invp_1x),"{:,.2f}".format(invp_2x),"{:,.2f}".format(invp_3x),"{:,.2f}".format(invp_4x),"{:,.2f}".format(grand_po_bayar))
            po_sisa = "<tr style='background-color: #dcdcdc;'><td style='border-left:1px solid #000000;border-bottom:1px solid #000000;padding:5px;color:#000000'><b>Sisa</b></td><td style='border-left:1px solid #000000;border-bottom:1px solid #000000;text-align:right;padding:5px;color:#000000'><b>%s</b></td><td style='border-left:1px solid #000000;border-bottom:1px solid #000000;text-align:right;padding:5px;color:#000000'><b>%s</b></td><td style='border-left:1px solid #000000;border-bottom:1px solid #000000;text-align:right;padding:5px;color:#000000'><b>%s</b></td><td style='border-left:1px solid #000000;border-bottom:1px solid #000000;text-align:right;padding:5px;color:#000000'><b>%s</b></td><td style='border-left:1px solid #000000;border-bottom:1px solid #000000;text-align:right;padding:5px;color:#000000'><b>%s</b></td><td style='border-left:1px solid #000000;border-bottom:1px solid #000000;text-align:right;padding:5px;color:#000000'><b>%s</b></td><td style='border-left:1px solid #000000;border-bottom:1px solid #000000;text-align:right;padding:5px;color:#000000'><b>%s</b></td><td style='border-left:1px solid #000000;border-bottom:1px solid #000000;text-align:right;padding:5px;color:#000000'><b>%s</b></td><td style='border-left:1px solid #000000;border-right:1px solid #000000;border-bottom:1px solid #000000;padding:5px;text-align:right;color:#000000'>%s</td></tr>" % ("{:,.2f}".format(sisap1),"{:,.2f}".format(sisap2),"{:,.2f}".format(sisap3),"{:,.2f}".format(sisap4),"{:,.2f}".format(sisap1x),"{:,.2f}".format(sisap2x),"{:,.2f}".format(sisap3x),"{:,.2f}".format(sisap4x),"{:,.2f}".format(grand_po_sisa))
            mk_data = "<tr><td style='border-left:1px solid #000000;border-bottom:1px solid #9C9C94;padding:5px;color:#000000'>PO Mitrakerja (Subcon)</td><td style='border-left:1px solid #000000;border-bottom:1px solid #9C9C94;text-align:right;padding:5px;color:#000000'>%s</td><td style='border-left:1px solid #000000;border-bottom:1px solid #9C9C94;text-align:right;padding:5px;color:#000000'>%s</td><td style='border-left:1px solid #000000;border-bottom:1px solid #9C9C94;text-align:right;padding:5px;color:#000000'>%s</td><td style='border-left:1px solid #000000;border-bottom:1px solid #9C9C94;text-align:right;padding:5px;color:#000000'>%s</td><td style='border-left:1px solid #000000;border-bottom:1px solid #9C9C94;text-align:right;padding:5px;color:#000000'>%s</td><td style='border-left:1px solid #000000;border-bottom:1px solid #9C9C94;text-align:right;padding:5px;color:#000000'>%s</td><td style='border-left:1px solid #000000;border-bottom:1px solid #9C9C94;text-align:right;padding:5px;color:#000000'>%s</td><td style='border-left:1px solid #000000;border-bottom:1px solid #9C9C94;text-align:right;padding:5px;color:#000000'>%s</td><td style='border-left:1px solid #000000;border-right:1px solid #000000;border-bottom:1px solid #9C9C94;padding:5px;text-align:right;color:#000000'>%s</td></tr>" % ("{:,.2f}".format(pos_1),"{:,.2f}".format(pos_2),"{:,.2f}".format(pos_3),"{:,.2f}".format(pos_4),"{:,.2f}".format(pos_1x),"{:,.2f}".format(pos_2x),"{:,.2f}".format(pos_3x),"{:,.2f}".format(pos_4x),"{:,.2f}".format(grand_mk_data))
            mk_bayar = "<tr><td style='border-left:1px solid #000000;border-bottom:1px solid #9C9C94;padding:5px;color:#000000'>Sudah dibayar</td><td style='border-left:1px solid #000000;border-bottom:1px solid #9C9C94;text-align:right;padding:5px;color:#000000'>%s</td><td style='border-left:1px solid #000000;border-bottom:1px solid #9C9C94;text-align:right;padding:5px;color:#000000'>%s</td><td style='border-left:1px solid #000000;border-bottom:1px solid #9C9C94;text-align:right;padding:5px;color:#000000'>%s</td><td style='border-left:1px solid #000000;border-bottom:1px solid #9C9C94;text-align:right;padding:5px;color:#000000'>%s</td><td style='border-left:1px solid #000000;border-bottom:1px solid #9C9C94;text-align:right;padding:5px;color:#000000'>%s</td><td style='border-left:1px solid #000000;border-bottom:1px solid #9C9C94;text-align:right;padding:5px;color:#000000'>%s</td><td style='border-left:1px solid #000000;border-bottom:1px solid #9C9C94;text-align:right;padding:5px;color:#000000'>%s</td><td style='border-left:1px solid #000000;border-bottom:1px solid #9C9C94;text-align:right;padding:5px;color:#000000'>%s</td><td style='border-left:1px solid #000000;border-right:1px solid #000000;border-bottom:1px solid #9C9C94;padding:5px;text-align:right;color:#000000'>%s</td></tr>" % ("{:,.2f}".format(invs_1),"{:,.2f}".format(invs_2),"{:,.2f}".format(invs_3),"{:,.2f}".format(invs_4),"{:,.2f}".format(invs_1x),"{:,.2f}".format(invs_2x),"{:,.2f}".format(invs_3x),"{:,.2f}".format(invs_4x),"{:,.2f}".format(grand_mk_bayar))
            mk_sisa = "<tr style='background-color: #dcdcdc;'><td style='border-left:1px solid #000000;padding:5px;color:#000000'><b>Sisa</b></td><td style='border-left:1px solid #000000;text-align:right;padding:5px;color:#000000'><b>%s</b></td><td style='border-left:1px solid #000000;border-bottom:1px solid #000000;text-align:right;padding:5px;color:#000000'><b>%s</b></td><td style='border-left:1px solid #000000;border-bottom:1px solid #000000;text-align:right;padding:5px;color:#000000'><b>%s</b></td><td style='border-left:1px solid #000000;border-bottom:1px solid #000000;text-align:right;padding:5px;color:#000000'><b>%s</b></td><td style='border-left:1px solid #000000;border-bottom:1px solid #000000;text-align:right;padding:5px;color:#000000'><b>%s</b></td><td style='border-left:1px solid #000000;border-bottom:1px solid #000000;text-align:right;padding:5px;color:#000000'><b>%s</b></td><td style='border-left:1px solid #000000;border-bottom:1px solid #000000;text-align:right;padding:5px;color:#000000'><b>%s</b></td><td style='border-left:1px solid #000000;border-bottom:1px solid #000000;text-align:right;padding:5px;color:#000000'><b>%s</b></td><td style='border-left:1px solid #000000;border-right:1px solid #000000;border-bottom:1px solid #000000;padding:5px;text-align:right;color:#000000'>%s</td></tr>" % ("{:,.2f}".format(sisas1),"{:,.2f}".format(sisas2),"{:,.2f}".format(sisas3),"{:,.2f}".format(sisas4),"{:,.2f}".format(sisas1x),"{:,.2f}".format(sisas2x),"{:,.2f}".format(sisas3x),"{:,.2f}".format(sisas4x),"{:,.2f}".format(grand_mk_sisa))
            aksep_data = "<tr><td style='border:1px solid #000000;padding:5px;color:#000000'>Aksep (Hutang Bank)</td><td style='border:1px solid #000000;text-align:right;padding:5px;color:#000000'>%s</td><td style='border:1px solid #000000;text-align:right;padding:5px;color:#000000'>%s</td><td style='border:1px solid #000000;text-align:right;padding:5px;color:#000000'>%s</td><td style='border:1px solid #000000;text-align:right;padding:5px;color:#000000'>%s</td><td style='border:1px solid #000000;text-align:right;padding:5px;color:#000000'>%s</td><td style='border:1px solid #000000;text-align:right;padding:5px;color:#000000'>%s</td><td style='border:1px solid #000000;text-align:right;padding:5px;color:#000000'>%s</td><td style='border:1px solid #000000;text-align:right;padding:5px;color:#000000'>%s</td><td style='border:1px solid #000000;text-align:right;padding:5px;color:#000000'>%s</td></tr>" % ("{:,.2f}".format(aksep1),"{:,.2f}".format(aksep2),"{:,.2f}".format(aksep3),"{:,.2f}".format(aksep4),"{:,.2f}".format(aksep1x),"{:,.2f}".format(aksep2x),"{:,.2f}".format(aksep3x),"{:,.2f}".format(aksep4x),"{:,.2f}".format(grand_aksep_data))
            saldo_data = "<tr><td style='border:1px solid #000000;padding:5px;color:#000000'>Saldo Bank</td><td style='border:1px solid #000000;text-align:right;padding:5px;color:#000000'>%s</td><td style='border:1px solid #000000;text-align:right;padding:5px;color:#000000'>%s</td><td style='border:1px solid #000000;text-align:right;padding:5px;color:#000000'>%s</td><td style='border:1px solid #000000;text-align:right;padding:5px;color:#000000'>%s</td><td style='border:1px solid #000000;text-align:right;padding:5px;color:#000000'>%s</td><td style='border:1px solid #000000;text-align:right;padding:5px;color:#000000'>%s</td><td style='border:1px solid #000000;text-align:right;padding:5px;color:#000000'>%s</td><td style='border:1px solid #000000;text-align:right;padding:5px;color:#000000'>%s</td><td style='border:1px solid #000000;text-align:right;padding:5px;color:#000000'>%s</td></tr>" % ("{:,.2f}".format(saldo1),"{:,.2f}".format(saldo2),"{:,.2f}".format(saldo3),"{:,.2f}".format(saldo4),"{:,.2f}".format(saldo1x),"{:,.2f}".format(saldo2x),"{:,.2f}".format(saldo3x),"{:,.2f}".format(saldo4x),"{:,.2f}".format(grand_saldo_data))
            balance_data = "<tr style='background-color: #e5e4e2;'><td style='border:1px solid #000000;padding:5px;color:#000000'><b>Balance</b></td><td style='border:1px solid #000000;text-align:right;padding:5px;color:#000000'><b>%s</b></td><td style='border:1px solid #000000;text-align:right;padding:5px;color:#000000'><b>%s</b></td><td style='border:1px solid #000000;text-align:right;padding:5px;color:#000000'><b>%s</b></td><td style='border:1px solid #000000;text-align:right;padding:5px;color:#000000'><b>%s</b></td><td style='border:1px solid #000000;text-align:right;padding:5px;color:#000000'><b>%s</b></td><td style='border:1px solid #000000;text-align:right;padding:5px;color:#000000'><b>%s</b></td><td style='border:1px solid #000000;text-align:right;padding:5px;color:#000000'><b>%s</b></td><td style='border:1px solid #000000;text-align:right;padding:5px;color:#000000'><b>%s</b></td><td style='border:1px solid #000000;text-align:right;padding:5px;color:#000000'><b>%s</b></td></tr>" % ("{:,.2f}".format(balance1),"{:,.2f}".format(balance2),"{:,.2f}".format(balance3),"{:,.2f}".format(balance4),"{:,.2f}".format(balance1x),"{:,.2f}".format(balance2x),"{:,.2f}".format(balance3x),"{:,.2f}".format(balance4x),"{:,.2f}".format(grand_balance_data))
            akumulasi_data = "<tr style='background-color: #e5e4e2;'><td style='border:1px solid #000000;padding:5px;color:#000000'><b>Akumulasi</b></td><td style='border:1px solid #000000;text-align:right;padding:5px;color:#000000'><b>%s</b></td><td style='border:1px solid #000000;text-align:right;padding:5px;color:#000000'><b>%s</b></td><td style='border:1px solid #000000;text-align:right;padding:5px;color:#000000'><b>%s</b></td><td style='border:1px solid #000000;text-align:right;padding:5px;color:#000000'><b>%s</b></td><td style='border:1px solid #000000;text-align:right;padding:5px;color:#000000'><b>%s</b></td><td style='border:1px solid #000000;text-align:right;padding:5px;color:#000000'><b>%s</b></td><td style='border:1px solid #000000;text-align:right;padding:5px;color:#000000'><b>%s</b></td><td style='border:1px solid #000000;text-align:right;padding:5px;color:#000000'><b>%s</b></td><td style='border:1px solid #000000;text-align:right;padding:5px;color:#000000'><b>%s</b></td></tr>" % ("{:,.2f}".format(aku1),"{:,.2f}".format(aku2),"{:,.2f}".format(aku3),"{:,.2f}".format(aku4),"{:,.2f}".format(aku1x),"{:,.2f}".format(aku2x),"{:,.2f}".format(aku3x),"{:,.2f}".format(aku4x),"{:,.2f}".format(grand_akumulasi_data))
            blank_line = "<tr><td style='border:1px solid #000000;height:20px'></td><td style='border:1px solid #000000'></td><td style='border:1px solid #000000'></td><td style='border:1px solid #000000'></td><td style='border:1px solid #000000'></td><td style='border:1px solid #000000'></td><td style='border:1px solid #000000'></td><td style='border:1px solid #000000'></td><td style='border:1px solid #000000'></td><td style='border:1px solid #000000'></td></tr>"
            piutang_data = "<tr><td style='border:1px solid #000000;padding:5px;color:#000000'>Piutang Berjalan</td><td style='border:1px solid #000000;text-align:right;padding:5px;color:#000000'>%s</td><td style='border:1px solid #000000;text-align:right;padding:5px;color:#000000'>%s</td><td style='border:1px solid #000000;text-align:right;padding:5px;color:#000000'>%s</td><td style='border:1px solid #000000;text-align:right;padding:5px;color:#000000'>%s</td><td style='border:1px solid #000000;text-align:right;padding:5px;color:#000000'>%s</td><td style='border:1px solid #000000;text-align:right;padding:5px;color:#000000'>%s</td><td style='border:1px solid #000000;text-align:right;padding:5px;color:#000000'>%s</td><td style='border:1px solid #000000;text-align:right;padding:5px;color:#000000'>%s</td><td style='border:1px solid #000000;text-align:right;padding:5px;color:#000000'>%s</td></tr>" % ("{:,.2f}".format(pb_1),"{:,.2f}".format(pb_2),"{:,.2f}".format(pb_3),"{:,.2f}".format(pb_4),"{:,.2f}".format(pb_1x),"{:,.2f}".format(pb_2x),"{:,.2f}".format(pb_3x),"{:,.2f}".format(pb_4x),"{:,.2f}".format(grand_piutang_data))
            footer = "</table>"
            
            html = tahun + header + or_data + or_bayar + or_sisa + po_data + po_bayar + po_sisa + mk_data + mk_bayar + mk_sisa + aksep_data + saldo_data + balance_data + akumulasi_data + blank_line + piutang_data + footer

            sqld = "delete from vit_posisi_dana"
            self.env.cr.execute(sqld, )

            posisi_dana = self.env["vit.posisi_dana"]

            # sql = """
            #     insert into vit_posisi_dana (name, html)
            #     select %s, %s
            #     """
            # self.env.cr.execute(sql, ('Posisi Dana ' + pod.year + '-' + pod.c_year,html))
            data = {
                'name' : 'Posisi Dana ' + pod.year + '-' + pod.c_year,
                'html' : html,
                }
            pd_id = posisi_dana.create(data)
            form_view_id = self.env.ref('vit_posisi_dana.view_vit_posisi_dana_form').id
            action = self.env.ref('vit_posisi_dana.action_vit_posisi_dana').read()[0]
            form_view = [(self.env.ref('vit_posisi_dana.view_vit_posisi_dana_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = pd_id.id
            return action
