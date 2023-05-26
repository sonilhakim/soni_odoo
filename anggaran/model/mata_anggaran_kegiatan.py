from odoo import tools
from odoo import api
from odoo import fields, models, api
import odoo.addons.decimal_precision as dp
import time
import logging
from odoo.tools.translate import _
from odoo.osv import expression

_logger = logging.getLogger(__name__)

class mata_anggaran_kegiatan(models.Model):
    _name = "anggaran.mata_anggaran_kegiatan"
    _description = 'mata anggaran kegiatan'

    name			= fields.Char(string='Nama', size=64, required=True, readonly=False)
    code			= fields.Char(string='Kode', size=64, required=True, readonly=False)
    kebijakan_id	= fields.Many2one(comodel_name='anggaran.kebijakan', string='Kebijakan',)
    category_id  	= fields.Many2one(comodel_name='anggaran.category', related='kebijakan_id.category_id', string=_("Kategori Kebijakan"), store=True)
    program_id	   	= fields.Many2one(comodel_name='anggaran.program', string='Program',)
    kegiatan_id 	= fields.Many2one(comodel_name='anggaran.kegiatan', string='Kegiatan',)
    unit_id 		= fields.Many2one(comodel_name='vit.unit_kerja', string='SUBSATKER',)
    cost_type_id	= fields.Many2one(comodel_name='anggaran.cost_type', string='Cost type',)
    coa_id   		= fields.Many2one(comodel_name='account.account', string='COA' )

    @api.onchange('unit_id','kegiatan_id','cost_type_id') # if these fields are changed, call method
    def on_change(self):
        if self.kegiatan_id.code != False and self.cost_type_id != False and self.unit_id != False:
            self.code = '650.1.%s.%s.%s'  % (self.kegiatan_id.code , self.cost_type_id.code , self.unit_id.name )
            self.name = self.cost_type_id.name

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

