from odoo import tools
from odoo import fields, models, api
import odoo.addons.decimal_precision as dp
import time
import logging
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)

class lap_pdana(models.Model):
	_name 		= "anggaran.lap_pdana"

	unit_id		  			= fields.Many2one(comodel_name='vit.unit_kerja', string='Unit')
	tahun_id		  		= fields.Many2one(comodel_name='account.fiscal.year', string='Tahun')
	rka_coa_id		 		= fields.Many2one(comodel_name='anggaran.rka_coa', string='No Akun')
	kebijakan_id			= fields.Many2one(comodel_name="anggaran.kebijakan", string="Kebijakan", related="rka_coa_id.rka_kegiatan_id.kebijakan_id", store=True)
	anggaran  				= fields.Float(related="rka_coa_id.total", string="Anggaran", store=True)
	realisasi_bln_ini		= fields.Float("Realisasi Bulan Ini")
	realisasi_sd_bln_ini	= fields.Float("Realisasi sd. Bulan Ini")
