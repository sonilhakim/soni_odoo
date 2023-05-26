#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft','Draft'),('open','Diperiksa'),('done','Selesai'),('reject','Ditolak')]
from odoo import models, fields, api, _
import time
import datetime
from odoo.exceptions import UserError, Warning

class penilaian_skp(models.Model):

    _name = "vit.penilaian_skp"
    _description = "vit.penilaian_skp"
    name = fields.Char( required=True, default="Baru", readonly=True,  string="Name",  help="")
    state = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",  help="")
    tanggal = fields.Date( string="Tanggal",  readonly=True, states={"draft" : [("readonly",False)]}, default=lambda self:time.strftime("%Y-%m-%d"), help="")
    pns_id = fields.Many2one(comodel_name="hr.employee",  string="Pns",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    pns_nip = fields.Char( string="Pns nip", related='pns_id.nip', readonly=True, help="")
    pns_pangkat_gol_ruang = fields.Char( comodel_name="hr.employee", string="Pns pangkat gol ruang", related='pns_id.pangkat_gol_ruang', readonly=True, states={"draft" : [("readonly",True)]})
    pns_jabatan_id = fields.Many2one(comodel_name="vit.jabatan",  string="Pns jabatan", related='pns_id.jabatan_id', readonly=True, states={"draft" : [("readonly",True)]})
    pns_unit_kerja_id = fields.Many2one(comodel_name="vit.unit_kerja",  string="Pns unit kerja" , related='pns_id.unit_kerja_id',  readonly=True, states={"draft" : [("readonly",True)]})
    pejabat_penilai_id = fields.Many2one(comodel_name="hr.employee",  string="Pejabat penilai",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    pejabat_penilai_nip = fields.Char( string="Pejabat penilai nip", related='pejabat_penilai_id.nip', readonly=True, help="")
    pejabat_penilai_pangkat_gol_ruang = fields.Char( comodel_name="hr.employee", string="Pejabat penilai pangkat gol ruang", related='pejabat_penilai_id.pangkat_gol_ruang', readonly=True, states={"draft" : [("readonly",True)]})
    pejabat_penilai_jabatan_id = fields.Many2one(comodel_name="vit.jabatan",  string="Pejabat penilai jabatan", related='pejabat_penilai_id.jabatan_id', readonly=True, states={"draft" : [("readonly",True)]})
    pejabat_penilai_unit_kerja_id = fields.Many2one(comodel_name="vit.unit_kerja",  string="Pejabat penilai unit kerja" , related='pejabat_penilai_id.unit_kerja_id',  readonly=True, states={"draft" : [("readonly",True)]})
    atasan_pejabat_penilai_id = fields.Many2one(comodel_name="hr.employee",  string="Atasan Pejabat penilai",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    atasan_pejabat_penilai_nip = fields.Char( string="Atasan Pejabat penilai nip", related='atasan_pejabat_penilai_id.nip', readonly=True, help="")
    atasan_pejabat_penilai_pangkat_gol_ruang = fields.Char( comodel_name="hr.employee", string="Atasan Pejabat penilai pangkat gol ruang", related='atasan_pejabat_penilai_id.pangkat_gol_ruang', readonly=True, states={"draft" : [("readonly",True)]})
    atasan_pejabat_penilai_jabatan_id = fields.Many2one(comodel_name="vit.jabatan",  string="Atasan Pejabat penilai jabatan", related='atasan_pejabat_penilai_id.jabatan_id', readonly=True, states={"draft" : [("readonly",True)]})
    atasan_pejabat_penilai_unit_kerja_id = fields.Many2one(comodel_name="vit.unit_kerja",  string="Atasan Pejabat penilai unit kerja" , related='atasan_pejabat_penilai_id.unit_kerja_id',  readonly=True, states={"draft" : [("readonly",True)]})
    def action_print_pengukuran(self, ):
        pass


    def action_print_penilaian(self, ):
        pass


    def action_print_skp(self, ):
        pass


    def action_hitung_rekapitulasi(self, ):
        pass

    tahun_akademik_id = fields.Many2one(comodel_name="vit.tahun_akademik",  string="Tahun akademik",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    unsur_penilaian_ids = fields.One2many(comodel_name="vit.unsur_penilaian_skp",  inverse_name="penilaian_skp_id",  string="Unsur Penilaian",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    perilaku_kerja_ids = fields.One2many(comodel_name="vit.perilaku_kerja_skp",  inverse_name="penilaian_skp_id",  string="Perilaku Kerja",  readonly=True, states={"draft" : [("readonly",False)]},  help="")

    nilai_perilaku_kerja_rata_rata = fields.Float('Nilai Perilaku Kerja', compute="_compute_nilai_rata")
    jumlah_nilai_perilaku_kerja = fields.Float('Jumlah', compute="_compute_nilai_rata")
    nilai_prestasi_kerja = fields.Float('Nilai Prestasi Kerja', compute="_compute_jumlah", store=True)

    @api.model
    def create(self, vals):
        if not vals.get("name", False) or vals["name"] == "New":
            vals["name"] = self.env["ir.sequence"].next_by_code("vit.penilaian_skp") or "Error Number!!!"
        return super(penilaian_skp, self).create(vals)

    @api.multi
    def action_confirm(self):
        self.state = STATES[1][0]

    @api.multi
    def action_done(self):
        self.state = STATES[2][0]

    def action_reject(self):
        self.state = STATES[3][0]

    @api.multi
    def action_draft(self):
        self.state = STATES[0][0]

    @api.multi
    def unlink(self):
        for me_id in self :
            if me_id.state != STATES[0][0]:
                raise UserError("Cannot delete non draft record!")
        return super(penilaian_skp, self).unlink()

    @api.one
    @api.depends('perilaku_kerja_ids.nilai')
    def _compute_nilai_rata(self):
        self.jumlah_nilai_perilaku_kerja = sum(line.nilai for line in self.perilaku_kerja_ids)
        i = 0
        for line in self.perilaku_kerja_ids:
            i += 1
            self.nilai_perilaku_kerja_rata_rata = self.jumlah_nilai_perilaku_kerja/i

    @api.one
    @api.depends('unsur_penilaian_ids.jumlah')
    def _compute_jumlah(self):
        self.nilai_prestasi_kerja = sum(line.jumlah for line in self.unsur_penilaian_ids)


class unsur_penilaian_skp(models.Model):
    _name = "vit.unsur_penilaian_skp"
    _description = "vit.unsur_penilaian_skp"

    name = fields.Selection( selection=[('skp', 'Sasaran Kerja Pegawai'),('perilaku','Perilaku Kerja')], required=True, string="Nama",  help="")
    
    nilai_capaian   = fields.Float('Nilai', compute="_compute_nilai", store=True)
    persentase      = fields.Float('Persentase (%)')
    jumlah          = fields.Float('Jumlah', compute="_compute_nilai", store=True)

    penilaian_skp_id = fields.Many2one('vit.penilaian_skp', string='Penilaian SKP')

    @api.one
    @api.depends('name','persentase')
    def _compute_nilai(self):
        if self.name == 'skp':
            if ((self.penilaian_skp_id.pns_id==False) or (self.penilaian_skp_id.pejabat_penilai_id==False) or (self.penilaian_skp_id.tahun_akademik_id==False)):
                raise UserError("Pns, Pejabat Penilai dan Tahun AKademik tidak boleh kosong!")
            cr = self.env.cr
            sql = """
                    select tar.nilai_capaian_skp
                    from vit_target_skp tar                     
                    left join hr_employee pns on tar.pns_id = pns.id
                    left join hr_employee pjb on tar.pejabat_penilai_id = pjb.id
                    left join vit_tahun_akademik tak on tar.tahun_akademik_id = tak.id
                    where pns.id = %s and pjb.id = %s and tak.id = %s and tar.state = 'done'
                    """
            # import pdb; pdb.set_trace()
            cr.execute(sql, (self.penilaian_skp_id.pns_id.id, self.penilaian_skp_id.pejabat_penilai_id.id, self.penilaian_skp_id.tahun_akademik_id.id))
            result = cr.fetchall()
            for res in result:
                self.nilai_capaian = res[0]
            self.jumlah = self.nilai_capaian * (self.persentase/100)            

        if self.name == 'perilaku':
            self.nilai_capaian = self.penilaian_skp_id.nilai_perilaku_kerja_rata_rata
            self.jumlah = self.nilai_capaian * (self.persentase/100)

           


class perilaku_kerja_skp(models.Model):
    _name = "vit.perilaku_kerja_skp"
    _description = "vit.perilaku_kerja_skp"

    name = fields.Char( required=True, string="Nama",  help="")
    
    nilai           = fields.Float('Nilai')
    keterangan      = fields.Char('Keterangan')

    penilaian_skp_id = fields.Many2one('vit.penilaian_skp', string='Penilaian SKP')
