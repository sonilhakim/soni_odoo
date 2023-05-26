from odoo import tools
from odoo import fields, models, api
import odoo.addons.decimal_precision as dp
import time
import logging
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)
LAP_STATES =[('draft','Draft'),('open','Verifikasi'), ('reject','Ditolak'),
                 ('done','Disetujui')]

class lap_pkk(models.Model):
	_name 		= "anggaran.lap_pkk"

	name				= fields.Char('Nomor', required=True, default='/')
	unit_id				= fields.Many2one(comodel_name='vit.unit_kerja', string='SUBSATKER')
	tahun_id  			= fields.Many2one(comodel_name='account.fiscal.year', string='Tahun')
	rka_kegiatan_id 	= fields.Many2one(comodel_name='anggaran.rka_kegiatan', string='Kegiatan')
	kebijakan_id		= fields.Many2one(comodel_name="anggaran.kebijakan", related='rka_kegiatan_id.kebijakan_id', string="Kebijakan", store=True)
	program_id			= fields.Many2one(comodel_name="anggaran.program", related='rka_kegiatan_id.kegiatan_id.program_id', string="Program", store=True)
	state             	= fields.Selection(string='Status',selection=LAP_STATES,readonly=True,required=True,default=LAP_STATES[0][0])
	lap_pkk_line_ids	= fields.One2many(comodel_name='anggaran.lap_pkk_detail',inverse_name='lap_pkk_id',string='Label', ondelete="cascade")
	
	@api.multi
	def action_draft(self):
		#set to "draft" state
		return self.write({'state':LAP_STATES[0][0]})
	@api.multi
	def action_confirm(self):
		#set to "confirmed" state
		return self.write({'state':LAP_STATES[1][0]})
	@api.multi
	def action_reject(self):
		#set to "done" state
		return self.write({'state':LAP_STATES[2][0]})
	@api.multi
	def action_done(self):
		#set to "done" state
		return self.write({'state':LAP_STATES[3][0]})
	# @api.model
	# def create(self, vals):
	# 	vals['name'] = self.env['ir.sequence'].next_by_code('anggaran.lap_pkk')
	# 	return super(biaya, self).create(vals)

class lap_pkk_detail(models.Model):
	_name 		= "anggaran.lap_pkk_detail"

	lap_pkk_id				= fields.Many2one(comodel_name='anggaran.lap_pkk', string='Lap PKK')
	input_rencana			= fields.Float("Input Rencana")
	input_realisasi			= fields.Float("Input Realisasi")
	proses_rencana			= fields.Float("Input Rencana")
	proses_realisasi		= fields.Float("Input Realisasi")
	output_rencana			= fields.Float("Input Rencana")
	output_realisasi		= fields.Float("Input Realisasi")
	cap_thn_lalu_rencana 	= fields.Float("Capaian Tahun Lalu Rencana")
	cap_thn_lalu_realisasi	= fields.Float("Capaian Tahun Lalu Realisasi")
	pct_capaian_target 		= fields.Float("Persen Capaian Target Renstra")
	outcome 				= fields.Float("Outcome")

