from odoo import tools
from odoo import fields, models
from odoo import api
import odoo.addons.decimal_precision as dp
import time
import logging
from odoo.tools.translate import _
from odoo.osv import expression

_logger = logging.getLogger(__name__)

class unit(models.Model):
    _name 		= "anggaran.unit"

    code		= fields.Char('Kode', required=True, select=True)
    name		= fields.Char('Nama', required=True)
    fakultas_id	= fields.Many2one(comodel_name='anggaran.fakultas', string='Fakultas')
    jurusan_id  = fields.Many2one(comodel_name='anggaran.jurusan', string='Jurusan')
    company_id  = fields.Many2one(comodel_name='res.company', string='Universitas', required=True)
    

    @api.onchange('fakultas_id','jurusan_id') # if these fields are changed, call method
    def on_change(self):

        if self.jurusan_id.id != False :
            self.code = '%s'  % (self.jurusan_id.code  )
            self.name = 'Unit Kerja %s' % (self.jurusan_id.name )
        
        elif self.fakultas_id.id != False :
            self.code = '%s'  % (self.fakultas_id.code  )
            self.name = 'Unit Kerja Fakultas %s' % (self.fakultas_id.name )

    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):

        args = args or []
        domain = []
        if name:
            domain = ['|', ('code', operator, name), ('name', operator, name)]
            if operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = ['&', '!'] + domain[1:]
        rec_ids = self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)
        return self.browse(rec_ids).name_get()


    @api.multi
    def name_get(self):
        result = []
        for rec in self:
            name = rec.code + ' ' + rec.name
            result.append((rec.id, name))
        return result

