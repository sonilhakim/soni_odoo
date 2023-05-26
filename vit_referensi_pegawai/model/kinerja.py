from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class kinerja_bidang_pendidikanref(models.Model):
	_name = "vit.kinerja_bidang_pendidikan"
	_inherit = "vit.kinerja_bidang_pendidikan"

	jenis_kegiatan1_id = fields.Many2one(comodel_name="vit.jenis_kegiatan",  string="Jenis Kegiatan",  help="")
	jenis_buku_id = fields.Many2one(comodel_name="vit.jenis_buku",  string="Jenis Buku",  help="")
	jenis_doc_id = fields.Many2one(comodel_name="vit.jenis_dokumen",  string="Jenis Dokumen",  help="")

	sks_dosen = fields.Many2one(comodel_name="vit.sks_dosen",  string="SKS Dosen",  help="")
	nilai_sks = fields.Float( string="SKS",  help="")

	@api.onchange('sks_dosen')
	def onchange_sks(self):
		for x in self:
			x.nilai_sks = x.sks_dosen.nilai

kinerja_bidang_pendidikanref()

class kinerja_bidang_penelitianref(models.Model):
	_name = "vit.kinerja_bidang_penelitian"
	_inherit = "vit.kinerja_bidang_penelitian"

	jenis_kegiatan1_id = fields.Many2one(comodel_name="vit.jenis_kegiatan",  string="Jenis Kegiatan",  help="")
	jenis_buku_id = fields.Many2one(comodel_name="vit.jenis_buku",  string="Jenis Buku",  help="")
	jenis_doc_id = fields.Many2one(comodel_name="vit.jenis_dokumen",  string="Jenis Dokumen",  help="")

	sks_dosen = fields.Many2one(comodel_name="vit.sks_dosen",  string="SKS Dosen",  help="")
	nilai_sks = fields.Float( string="SKS",  help="")

	@api.onchange('sks_dosen')
	def onchange_sks(self):
		for x in self:
			x.nilai_sks = x.sks_dosen.nilai

kinerja_bidang_penelitianref()

class kinerja_bidang_pengabdianref(models.Model):
	_name = "vit.kinerja_bidang_pengabdian"
	_inherit = "vit.kinerja_bidang_pengabdian"

	jenis_kegiatan1_id = fields.Many2one(comodel_name="vit.jenis_kegiatan",  string="Jenis Kegiatan",  help="")
	jenis_buku_id = fields.Many2one(comodel_name="vit.jenis_buku",  string="Jenis Buku",  help="")
	jenis_doc_id = fields.Many2one(comodel_name="vit.jenis_dokumen",  string="Jenis Dokumen",  help="")

	sks_dosen = fields.Many2one(comodel_name="vit.sks_dosen",  string="SKS Dosen",  help="")
	nilai_sks = fields.Float( string="SKS",  help="")

	@api.onchange('sks_dosen')
	def onchange_sks(self):
		for x in self:
			x.nilai_sks = x.sks_dosen.nilai


kinerja_bidang_pengabdianref()

class kinerja_kewajiban_khususref(models.Model):
	_name = "vit.kinerja_kewajiban_khusus"
	_inherit = "vit.kinerja_kewajiban_khusus"

	jenis_kegiatan1_id = fields.Many2one(comodel_name="vit.jenis_kegiatan",  string="Jenis Kegiatan",  help="")
	jenis_buku_id = fields.Many2one(comodel_name="vit.jenis_buku",  string="Jenis Buku",  help="")
	jenis_doc_id = fields.Many2one(comodel_name="vit.jenis_dokumen",  string="Jenis Dokumen",  help="")

	sks_dosen = fields.Many2one(comodel_name="vit.sks_dosen",  string="SKS Dosen",  help="")
	nilai_sks = fields.Float( string="SKS",  help="")

	@api.onchange('sks_dosen')
	def onchange_sks(self):
		for x in self:
			x.nilai_sks = x.sks_dosen.nilai

kinerja_kewajiban_khususref()

class kinerja_penunjangref(models.Model):
	_name = "vit.kinerja_penunjang"
	_inherit = "vit.kinerja_penunjang"

	jenis_kegiatan1_id = fields.Many2one(comodel_name="vit.jenis_kegiatan",  string="Jenis Kegiatan",  help="")
	jenis_buku_id = fields.Many2one(comodel_name="vit.jenis_buku",  string="Jenis Buku",  help="")
	jenis_doc_id = fields.Many2one(comodel_name="vit.jenis_dokumen",  string="Jenis Dokumen",  help="")

	sks_dosen = fields.Many2one(comodel_name="vit.sks_dosen",  string="SKS Dosen",  help="")
	nilai_sks = fields.Float( string="SKS",  help="")

	@api.onchange('sks_dosen')
	def onchange_sks(self):
		for x in self:
			x.nilai_sks = x.sks_dosen.nilai

kinerja_penunjangref()