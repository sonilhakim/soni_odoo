from odoo import tools
from odoo import fields, models, api
import odoo.addons.decimal_precision as dp
import time
import logging
from odoo.tools.translate import _
from odoo.osv import expression

_logger = logging.getLogger(__name__)

class jurusan(models.Model):
    _name 		= "anggaran.jurusan"

    code        = fields.Char(string='Kode', required=True)
    name        = fields.Char(string='Nama', required=True) 
    jurusan_id  = fields.Many2one(comodel_name='anggaran.jurusan', string='Jurusan', required=False),
    fakultas_id = fields.Many2one(comodel_name='anggaran.fakultas', string='Fakultas', required=True)
    income_ids	= fields.One2many(comodel_name='anggaran.jurusan_income',inverse_name='jurusan_id',string='Incomes', ondelete="cascade")


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

class jurusan_income(models.Model):
    _name 		= "anggaran.jurusan_income"

    # def _ftotal_spp(self, cr, uid, ids, field, arg, context=None):
    # 	results = {}

    # 	for inc in self.browse(cr, uid, ids, context=context):
    # 		results[inc.id] = inc.jumlah * inc.tarif_spp

    # 	return results	

    # def _ftotal_bpp(self, cr, uid, ids, field, arg, context=None):
    # 	results = {}

    # 	for inc in self.browse(cr, uid, ids, context=context):
    # 		results[inc.id] = inc.jumlah * inc.tarif_bpp

    # 	return results	

    # def _ftotal(self, cr, uid, ids, field, arg, context=None):
    # 	results = {}

    # 	for inc in self.browse(cr, uid, ids, context=context):
    # 		results[inc.id] = inc.total_bpp + inc.total_spp

    # 	return results

    jurusan_id		= fields.Many2one(comodel_name='anggaran.jurusan', string='Jurusan')
    tahun_akademik	= fields.Many2one(comodel_name='anggaran.tahun_akademik', string='Tahun Akademik')
    angkatan		= fields.Many2one(comodel_name='anggaran.tahun_akademik', string='Angkatan')
    jumlah			= fields.Integer('Jumlah Mhs. Aktif')
    tarif_bpp		= fields.Integer('Tarif BPP')
    tarif_spp		= fields.Integer('Tarif SPP')
    total_bpp		= fields.Integer(compute="_ftotal_bpp", string="Total BPP")
    total_spp		= fields.Integer(compute="_ftotal_spp", string="Total SPP")
    total			= fields.Integer(compute="_ftotal", string="Total")

    @api.depends('jumlah','tarif_bpp')
    def _ftotal_bpp(self):
        for rec in self:
            rec.total_bpp = rec.jumlah * rec.tarif_bpp

    @api.depends('jumlah','tarif_spp')
    def _ftotal_spp(self):
        for rec in self:
            rec.total_spp = rec.jumlah * rec.tarif_spp

    @api.depends('total_bpp','total_spp')
    def _ftotal(self):
        for rec in self:
            rec.total = rec.total_bpp + rec.tarif_spp
    # total_bpp		= fields.function(_ftotal_bpp, type='integer', string="Total BPP")
    # total_spp		= fields.function(_ftotal_spp, type='integer', string="Total SPP")
    # total			= fields.function(_ftotal, type='integer', string="Total")



class tahun_akademik(models.Model):
    _name 		= "anggaran.tahun_akademik"

    code	= fields.Char("Code")
    name	= fields.Char("Tahun Akademik")



