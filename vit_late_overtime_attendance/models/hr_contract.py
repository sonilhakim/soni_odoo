from odoo import api, fields, models, _

class HRContract(models.Model):
    _inherit = "hr.contract"

    t_lembur_1h = fields.Float('Tj Lembur 1 Jam')
    t_lembur_1_5h = fields.Float('Tj Lembur 1.5 Jam')
    t_lembur_2h = fields.Float('Tj Lembur 2 Jam')
    t_lembur_2_5h = fields.Float('Tj Lembur 2.5 Jam')
    t_lembur_3h = fields.Float('Tj Lembur 3 Jam')
    t_lembur_3_5h = fields.Float('Tj Lembur 3.5 Jam')
    t_lembur_4h = fields.Float('Tj Lembur 4 Jam')
    t_lembur_4_5h = fields.Float('Tj Lembur 4.5 Jam')
    t_lembur_5_7h = fields.Float('Tj Lembur 5 - 7 Jam')
    t_lembur_2s = fields.Float('Tj Lembur Double Shift')

    potongan_tlmbt_5 = fields.Float('Potongan Terlambat 5 mnt')
    potongan_tlmbt_10 = fields.Float('Potongan Terlambat 10 mnt')
    potongan_tlmbt_15 = fields.Float('Potongan Terlambat 15 mnt')
    potongan_tlmbt_20 = fields.Float('Potongan Terlambat 20 mnt')

HRContract()