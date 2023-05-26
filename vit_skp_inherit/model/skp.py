#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft','Draft'),('open','Diperiksa'),('done','Selesai'),('reject','Ditolak')]
from odoo import models, fields, api, _
from datetime import date
from odoo.exceptions import UserError, Warning

class skp(models.Model):
    _name = "vit.skp"
    _inherit = "vit.skp"

    name = fields.Char( required=True, default="Baru", readonly=True,  string="Name",  help="")
    tugas_tambahan_ids = fields.One2many(comodel_name="vit.skp_tugas_tambahan",  inverse_name="skp_id",  string="Tugas Tambahan",  readonly=True, states={"draft" : [("readonly",False)]},  help="")

    pns_nip = fields.Char( comodel_name="hr.employee", string="Pns nip", related='pns_id.nip', readonly=True, states={"draft" : [("readonly",True)]})
    pns_gender = fields.Selection( comodel_name="hr.employee", string="Pns gender", related='pns_id.gender', readonly=True)
    pns_temp_lahir = fields.Char( comodel_name="hr.employee", string="Pns tempat lahir", related='pns_id.place_of_birth', readonly=True)
    pns_tgl_lahir = fields.Date( comodel_name="hr.employee", string="Pns tanggal lahir", related='pns_id.birthday', readonly=True)
    pns_tmt_pensiun = fields.Date( comodel_name="hr.employee", string="Pns TMT pensiun", related='pns_id.tmt_pensiun', readonly=True)
    pns_usia = fields.Char( comodel_name="hr.employee", string="Pns usia", compute='get_usia', readonly=True)
    pns_tmt_cpns = fields.Date( comodel_name="hr.employee", string="Pns TMT cpns", related='pns_id.tmt_cpns', readonly=True)
    pns_tmt_pns = fields.Date( comodel_name="hr.employee", string="Pns TMT pns", related='pns_id.tmt_pns', readonly=True)
    pns_mk_thn = fields.Char( comodel_name="hr.employee", string="Pns MK thn", related='pns_id.mk_thn', readonly=True)
    pns_mk_bln = fields.Char( comodel_name="hr.employee", string="Pns MK bln", related='pns_id.mk_bln', readonly=True)
    pns_pangkat_gol_ruang = fields.Char( comodel_name="hr.employee", string="Pns pangkat gol ruang", related='pns_id.pangkat_gol_ruang', readonly=True, states={"draft" : [("readonly",True)]})
    pns_golongan_id = fields.Many2one( comodel_name="vit.golongan", string="Pns Golongan", related='pns_id.golongan_id', readonly=True)
    pns_tmt_golongan = fields.Date( comodel_name="hr.employee", string="Pns TMT golongan", related='pns_id.tmt_golongan', readonly=True)
    pns_jabatan_id = fields.Many2one(comodel_name="vit.jabatan",  string="Pns jabatan", related='pns_id.jabatan_id', readonly=True, states={"draft" : [("readonly",True)]})
    pns_tmt_jabatan = fields.Date( comodel_name="hr.employee", string="Pns TMT jabatan", related='pns_id.tmt_jabatan', readonly=True)
    
    pns_pts = fields.Many2one( comodel_name="res.company", string="Pns pts", related='pns_id.company_id', readonly=True)
    pns_pendidikan = fields.Many2one( comodel_name="vit.strata", string="Pns pendidikan", related='pns_id.pendidikan_terakhir', readonly=True)
    pns_almamater = fields.Char( comodel_name="hr.employee", string="Pns almamater", related='pns_id.study_school', readonly=True)
    pns_prog_studi = fields.Many2one( comodel_name="vit.program_studi", string="Pns Program Studi", related='pns_id.program_studi_id', readonly=True)
    pns_thn_lulus = fields.Char( comodel_name="hr.employee", string="Pns tahun lulus", related='pns_id.thn_lulus', readonly=True)

    pejabat_penilai_nip = fields.Char( comodel_name="hr.employee", string="Pejabat penilai nip", related='pejabat_penilai_id.nip', readonly=True, states={"draft" : [("readonly",True)]})
    pejabat_penilai_pangkat_gol_ruang = fields.Char( comodel_name="hr.employee", string="Pejabat penilai pangkat gol ruang", related='pejabat_penilai_id.pangkat_gol_ruang', readonly=True, states={"draft" : [("readonly",True)]})
    pejabat_penilai_golongan_id = fields.Many2one( comodel_name="vit.golongan", string="Pejabat penilai Golongan", related='pejabat_penilai_id.golongan_id', readonly=True)
    pejabat_penilai_unit_kerja_id = fields.Many2one(comodel_name="vit.unit_kerja",  string="Pejabat penilai unit kerja" , related='pejabat_penilai_id.unit_kerja_id',  readonly=True, states={"draft" : [("readonly",True)]})
    pejabat_penilai_jabatan_id = fields.Many2one(comodel_name="vit.jabatan", string="Pejabat penilai jabatan" , related='pejabat_penilai_id.jabatan_id',  readonly=True, states={"draft" : [("readonly",True)]})

    state = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",  help="")

    @api.model
    def create(self, vals):
        if not vals.get("name", False) or vals["name"] == "New":
            vals["name"] = self.env["ir.sequence"].next_by_code("vit.skp") or "Error Number!!!"
        return super(skp, self).create(vals)

    def action_confirm(self):
        self.state = STATES[1][0]

    def action_done(self):
        self.state = STATES[2][0]

    def action_reject(self):
        self.state = STATES[3][0]

    def action_draft(self):
        self.state = STATES[0][0]

    @api.multi
    def unlink(self):
        for me_id in self :
            if me_id.state != STATES[0][0]:
                raise UserError("Cannot delete non draft record!")
        return super(skp, self).unlink()

    def action_print_pengukuran(self, ):
        pass


    def action_print_penilaian(self, ):
        pass


    def action_print_skp(self, ):
        pass


    def action_hitung_rekapitulasi(self, ):
        pass

    # @api.depends('pns_id')
    # def get_pns_pendidikan(self):
    #     for skp in self :
    #         for pd in skp.pns_id.riwayat_pendidikan_ids:
    #             skp.pns_pts = pd.name
    #             skp.pns_pendidikan = pd.strata_id.name
    #             skp.pns_almamater = pd.institusi_id.name
    #             skp.pns_prog_studi = pd.major
    #             skp.pns_thn_lulus = pd.date_end

    @api.depends('pns_tgl_lahir')
    def get_usia(self):
        if self.pns_tgl_lahir:
            today = date.today()
            birthDate = self.pns_tgl_lahir
            age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day)) 
          
            self.pns_usia = str(age)+' tahun'

    @api.multi
    def compute_perkuliahan(self):
        for kul in self.perkuliahan_ids:
            kul.totak_sks_per_smt = (kul.sks * kul.jumlah_kelas)/kul.jumlah_dosen_pengampu

    @api.multi
    def rekap_perkuliahan(self):
        for skp in self:
            sql = "delete from vit_skp_rekapitulasi_perkuliahan where skp_id = %s"
            skp.env.cr.execute(sql, (skp.id,))
            data = []            
            sql1 = """select
                        sum(k.sks), sum(k.totak_sks_per_smt), s.id
                    from
                        vit_skp_perkuliahan k
                    left join
                        vit_semester s on k.semester_id = s.id
                    where k.skp_id = %s and s.name = %s
                    group by s.id
                    """
            cr = self.env.cr
            cr.execute(sql1, (skp.id,'Ganjil'))
            result1 = cr.fetchall()

            for res1 in result1:
                # for rekap1 in self.rekapitulasi_ids.search([('skp_id','=',self.id),('semester_id.name','=','Ganjil')]):
                #     rekap1.sks_riil = res1[0]
                #     rekap1.ak_10_sks_pertama = res1[0]
                #     rekap1.ak_sks_berikutnya = res1[0]/2
                #     rekap1.ak_jumlah = rekap1.ak_10_sks_pertama + rekap1.ak_sks_berikutnya

                data.append({
                        'name' : 'Semester Ganjil',
                        'sks' : res1[0],
                        'sks_riil' : res1[1],
                        'ak_10_sks_pertama' : res1[1],
                        'ak_sks_berikutnya' : res1[1]/2,
                        'ak_jumlah' : res1[1] + (res1[1]/2),
                        'semester_id' : res1[2],
                        'skp_id' : skp.id,
                        })

            sql = """select
                        sum(k.sks), sum(k.totak_sks_per_smt), s.id
                    from
                        vit_skp_perkuliahan k
                    left join
                        vit_semester s on k.semester_id = s.id
                    where k.skp_id = %s and s.name = %s
                    group by s.id
                    """
            cr = skp.env.cr
            cr.execute(sql, (skp.id,'Genap'))
            result = cr.fetchall()

            for res in result:
                # for rekap in self.rekapitulasi_ids.search([('skp_id','=',self.id),('semester_id.name','=','Genap')]):
                #     rekap.sks_riil = res[0]
                #     rekap.ak_10_sks_pertama = res[0]
                #     rekap.ak_sks_berikutnya = res[0]/2
                #     rekap.ak_jumlah = rekap.ak_10_sks_pertama + rekap.ak_sks_berikutnya
                data.append({
                        'name' : 'Semester Genap',
                        'sks' : res[0],
                        'sks_riil' : res[1],
                        'ak_10_sks_pertama' : res[1],
                        'ak_sks_berikutnya' : res[1]/2,
                        'ak_jumlah' : res[1] + (res[1]/2),
                        'semester_id' : res[2],
                        'skp_id' : skp.id,
                        })

            skp.env['vit.skp_rekapitulasi_perkuliahan'].create(data)


    @api.multi
    def compute_seminar(self):
        for sem in self.seminar_ids:
            sem.ak = sem.pelaksanaan

    @api.multi
    def compute_kkn(self):
        for kkn in self.kkn_pkn_pkl_ids:
            kkn.jumlah = kkn.semester_genap + kkn.semester_ganjil
            kkn.ak = kkn.jumlah

    @api.multi
    def compute_disertasi(self):
        for dts in self.disertasi_thesis_skripsi_ids:
            dts.ak_pembimbing_utama = dts.jumlah_lulusan_pembimbing_utama
            dts.ak_pembimbing_pembantu = dts.jumlah_lulusan_pembimbing_pembantu/2
            dts.ak_total = dts.ak_pembimbing_utama + dts.ak_pembimbing_pembantu

    @api.multi
    def compute_penguji(self):
        for uji in self.penguji_ids:
            uji.ak_ketua_penguji = uji.jumlah_mhs_ketua_penguji
            uji.ak_anggota_penguji = uji.jumlah_mhs_anggota_penguji/2
            uji.ak_total = uji.ak_ketua_penguji + uji.ak_anggota_penguji

    @api.multi
    def compute_membina(self):
        for bna in self.membina_ids:
            bna.jumlah = bna.semester_genap + bna.semester_ganjil
            bna.ak = bna.jumlah

    @api.multi
    def compute_mpk(self):
        for mpk in self.mengembangkan_program_kuliah_ids:
            mpk.jumlah = mpk.semester_genap + mpk.semester_ganjil
            mpk.ak = mpk.jumlah

    @api.multi
    def compute_mbk(self):
        for mbk in self.mengembangkan_bahan_kuliah_ids:
            mbk.ak_jumlah = mbk.jumlah * mbk.ak_per_bahan_kuliah

    @api.multi
    def rekap_rbk(self):
        for skp in self:
            sql = "delete from vit_skp_rekapitulasi_mengembangkan_bahan_kuliah where skp_id = %s"
            skp.env.cr.execute(sql, (skp.id,))
            data = []            
            sql1 = """select
                        sum(mbk.jumlah), sum(mbk.ak_jumlah)
                    from
                        vit_skp_mengembangkan_bahan_kuliah mbk
                    left join
                        vit_semester s on mbk.semester_id = s.id
                    where mbk.skp_id = %s and s.name = %s
                    """
            cr = self.env.cr
            cr.execute(sql1, (skp.id,'Ganjil'))
            result1 = cr.fetchall()

            for res1 in result1:
                data.append({
                        'name' : 'Semester Ganjil',
                        'naskah' : res1[0],
                        'ak' : res1[1],
                        'skp_id' : skp.id,
                        })

            sql = """select
                        sum(mbk.jumlah), sum(mbk.ak_jumlah)
                    from
                        vit_skp_mengembangkan_bahan_kuliah mbk
                    left join
                        vit_semester s on mbk.semester_id = s.id
                    where mbk.skp_id = %s and s.name = %s
                    """
            cr = skp.env.cr
            cr.execute(sql, (skp.id,'Genap'))
            result = cr.fetchall()

            for res in result:
                data.append({
                        'name' : 'Semester Genap',
                        'naskah' : res[0],
                        'ak' : res[1],
                        'skp_id' : skp.id,
                        })

            skp.env['vit.skp_rekapitulasi_mengembangkan_bahan_kuliah'].create(data)

    @api.multi
    def compute_oil(self):
        for oil in self.orasi_ilmiah_ids:
            oil.jumlah = oil.semester_genap + oil.semester_ganjil
            oil.ak = oil.jumlah * 5

    @api.multi
    def compute_jpt(self):
        for jpt in self.jabatan_pt_ids:
            jpt.jumlah_angka_kredit = jpt.hasil * jpt.angka_kredit

    @api.multi
    def rekap_jpt(self):
        for skp in self:
            sql = "delete from vit_skp_rekapitulasi_jabatan_pt where skp_id = %s"
            skp.env.cr.execute(sql, (skp.id,))
            data = []
            sql1 = """select
                        sum(jpt.jumlah_angka_kredit), sum(jpt.hasil)
                    from
                        vit_skp_jabatan_pt jpt
                    left join
                        vit_semester s on jpt.semester_id = s.id
                    where jpt.skp_id = %s and s.name = %s
                    """
            cr = self.env.cr
            cr.execute(sql1, (skp.id,'Ganjil'))
            result1 = cr.fetchall()

            for res1 in result1:
                data.append({
                        'name' : 'Semester Ganjil',
                        'satuan_hasil' : res1[1],
                        'jumlah_angka_kredit' : res1[0],
                        'skp_id' : skp.id,
                        })

            sql = """select
                        sum(jpt.jumlah_angka_kredit), sum(jpt.hasil)
                    from
                        vit_skp_jabatan_pt jpt
                    left join
                        vit_semester s on jpt.semester_id = s.id
                    where jpt.skp_id = %s and s.name = %s
                    """
            cr = skp.env.cr
            cr.execute(sql, (skp.id,'Genap'))
            result = cr.fetchall()

            for res in result:
                data.append({
                        'name' : 'Semester Genap',
                        'satuan_hasil' : res[1],
                        'jumlah_angka_kredit' : res[0],
                        'skp_id' : skp.id,
                        })

            skp.env['vit.skp_rekapitulasi_jabatan_pt'].create(data)

    @api.multi
    def compute_mbd(self):
        for mbd in self.membimbing_dosen_ids:
            mbd.jumlah = mbd.semester_genap + mbd.semester_ganjil
            mbd.ak = mbd.jumlah * 2

    @api.multi
    def compute_det(self):
        for det in self.detasering_ids:
            det.jumlah = det.semester_genap + det.semester_ganjil
            det.ak = det.jumlah

    @api.multi
    def compute_pd(self):
        for pd in self.pengembangan_diri_ids:
            pd.jumlah = pd.semester_genap + pd.semester_ganjil
            pd.jumlah_ak = pd.jumlah * pd.ak

    @api.multi
    def compute_plt(self):
        for plt in self.penelitian_ids:
            plt.ak_jumlah_peneliti_mandiri = plt.jumlah_peneliti_mandiri * plt.ak_karya_ilmiah_jurnal
            plt.ak_jumlah_peneliti_utama = (plt.jumlah_peneliti_utama * plt.ak_karya_ilmiah_jurnal) * 0.6
            plt.ak_jumlah_peneliti_anggota = (plt.jumlah_peneliti_anggota * plt.ak_karya_ilmiah_jurnal) * 0.4
            plt.ak_jumlah = plt.ak_jumlah_peneliti_mandiri + plt.ak_jumlah_peneliti_utama + plt.ak_jumlah_peneliti_anggota

    @api.multi
    def compute_abd(self):
        for abd in self.pengabdian_ids:
            abd.ak_jumlah = abd.jumlah_program * abd.ak_program

    @api.multi
    def compute_tgs(self):
        for tgs in self.tugas_tambahan_ids:
            tgs.jumlah = tgs.semester_genap + tgs.semester_ganjil
            tgs.ak = tgs.jumlah