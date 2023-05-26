from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.safe_eval import safe_eval

from odoo.addons import decimal_precision as dp

class HrSalaryRuleRemunerasi(models.Model):
    _inherit = 'hr.salary.rule'

    remun_type = fields.Selection([
    			('jik', 'Jenis Insentif Kinerja'),
    			('jik_sub', 'Jenis Sub Insentif Kinerja'),
    			('grade', 'Grade'),
                ('pnbp', 'Gaji PNBP'),
                ('pir', 'PIR'),
    			('tk_hadir', 'Tunkin Kehadiran'),
    			('tk_lambat', 'Tunkin Terlambat'),
    			('tk_pulang', 'Tunkin Pulang'),
    			('tk_potongan', 'Pemotongan Tunkin'),
    			], 'Tipe Remunerasi',)