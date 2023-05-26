#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft','Draft'),('open','Diperiksa'),('done','Selesai'),('reject','Ditolak')]
from odoo import models, fields, api, _
from datetime import date
import time
from odoo.exceptions import UserError, Warning

class mutasiskp(models.Model):
    _name = "vit.mutasi_skp"
    _description = "vit.mutasi_skp"

    name = fields.Char( required=True, default="New", readonly=True,  string="Name",  help="")
    state = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",  help="")

    tanggal = fields.Date( string="Tanggal",  readonly=True, states={"draft" : [("readonly",False)]}, default=lambda self:time.strftime("%Y-%m-%d"), help="")
    lokasi = fields.Char( string="Lokasi",  readonly=True, states={"draft" : [("readonly",False)]},  help="")

    pns_nip = fields.Char( comodel_name="hr.employee", string="Pns nip", related='pns_id.nip', readonly=True,)
    pns_golongan_id = fields.Many2one( comodel_name="vit.golongan", string="Pns Golongan", related='pns_id.golongan_id', readonly=True, )
    pns_jabatan_id = fields.Many2one(comodel_name="vit.jabatan",  string="Pns jabatan", related='pns_id.jabatan_id', readonly=True, )
    
    tahun_akademik_id = fields.Many2one(comodel_name="vit.tahun_akademik",  string="Tahun akademik",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    pns_id = fields.Many2one(comodel_name="hr.employee",  string="Pns",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    pns_unit_kerja_id = fields.Many2one(comodel_name="vit.unit_kerja",  string="Pns unit kerja", related='pns_id.unit_kerja_id', readonly=True, help="")
    
    perkuliahan_ids = fields.One2many(comodel_name="vit.skp_perkuliahan_mut",  inverse_name="mutasi_skp_id",  string="Perkuliahan",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    seminar_ids = fields.One2many(comodel_name="vit.skp_seminar_mut",  inverse_name="mutasi_skp_id",  string="Seminar",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    kkn_pkn_pkl_ids = fields.One2many(comodel_name="vit.skp_kkn_pkn_pkl_mut",  inverse_name="mutasi_skp_id",  string="Kkn pkn pkl",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    disertasi_thesis_skripsi_ids = fields.One2many(comodel_name="vit.skp_disertasi_mut",  inverse_name="mutasi_skp_id",  string="Disertasi thesis skripsi",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    penguji_ids = fields.One2many(comodel_name="vit.skp_penguji_mut",  inverse_name="mutasi_skp_id",  string="Penguji",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    membina_ids = fields.One2many(comodel_name="vit.skp_membina_mut",  inverse_name="mutasi_skp_id",  string="Membina",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    mengembangkan_program_kuliah_ids = fields.One2many(comodel_name="vit.skp_mengembangkan_program_kuliah_mut",  inverse_name="mutasi_skp_id",  string="Mengembangkan program kuliah",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    mengembangkan_bahan_kuliah_ids = fields.One2many(comodel_name="vit.skp_mengembangkan_bahan_kuliah_mut",  inverse_name="mutasi_skp_id",  string="Mengembangkan bahan kuliah",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    orasi_ilmiah_ids = fields.One2many(comodel_name="vit.skp_orasi_ilmiah_mut",  inverse_name="mutasi_skp_id",  string="Orasi ilmiah",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    jabatan_pt_ids = fields.One2many(comodel_name="vit.skp_jabatan_pt_mut",  inverse_name="mutasi_skp_id",  string="Jabatan pt",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    membimbing_dosen_ids = fields.One2many(comodel_name="vit.skp_membimbing_dosen_mut",  inverse_name="mutasi_skp_id",  string="Membimbing dosen",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    detasering_ids = fields.One2many(comodel_name="vit.skp_detasering_mut",  inverse_name="mutasi_skp_id",  string="Detasering",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    pengembangan_diri_ids = fields.One2many(comodel_name="vit.skp_pengembangan_diri_mut",  inverse_name="mutasi_skp_id",  string="Pengembangan diri",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    penelitian_ids = fields.One2many(comodel_name="vit.skp_penelitian_mut",  inverse_name="mutasi_skp_id",  string="Penelitian",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    pengabdian_ids = fields.One2many(comodel_name="vit.skp_pengabdian_mut",  inverse_name="mutasi_skp_id",  string="Pengabdian",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    rekapitulasi_ids = fields.One2many(comodel_name="vit.skp_rekapitulasi_perkuliahan_mut",  inverse_name="mutasi_skp_id",  string="Rekapitulasi",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    rekapitulasi_mengembangkan_bahan_kuliah_ids = fields.One2many(comodel_name="vit.skp_rekapitulasi_mengembangkan_bahan_kuliah_mut",  inverse_name="mutasi_skp_id",  string="Rekapitulasi mengembangkan bahan kuliah",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    rekapitulasi_jabatan_pt_ids = fields.One2many(comodel_name="vit.skp_rekapitulasi_jabatan_pt_mut",  inverse_name="mutasi_skp_id",  string="Rekapitulasi jabatan pt",  readonly=True, states={"draft" : [("readonly",False)]},  help="")

    @api.model
    def create(self, vals):
        if not vals.get("name", False) or vals["name"] == "New":
            vals["name"] = self.env["ir.sequence"].next_by_code("vit.mutasi_skp") or "Error Number!!!"
        return super(mutasiskp, self).create(vals)

    @api.multi
    def action_confirm(self):
        self.state = STATES[1][0]

    @api.multi
    def action_done(self):
        for kul in self.perkuliahan_ids:
            sql = """
                update vit_skp_perkuliahan
                set name = %s, sks = %s, jumlah_kelas = %s, jumlah_dosen_pengampu = %s, totak_sks_per_smt = %s, semester_id = %s
                where id = %s and skp_id = %s
                """
            # import pdb; pdb.set_trace()
            self.env.cr.execute(sql, (kul.name, kul.sks, kul.jumlah_kelas, kul.jumlah_dosen_pengampu, kul.totak_sks_per_smt, kul.semester_id.id, kul.skp_perkuliahan_id.id, kul.skp_id.id))

        for sem in self.seminar_ids:
            sql = """
                update vit_skp_seminar
                set name = %s, pelaksanaan = %s, ak = %s, semester_id = %s
                where id = %s and skp_id = %s
                """
            self.env.cr.execute(sql, (sem.name, sem.pelaksanaan, sem.ak, sem.semester_id.id, sem.skp_seminar_id.id, sem.skp_id.id))

        for kkn in self.kkn_pkn_pkl_ids:
            sql = """
                update vit_skp_kkn_pkn_pkl
                set name = %s, semester_genap = %s, semester_ganjil = %s, jumlah = %s, ak = %s, jenis_kkn_id = %s
                where id = %s and skp_id = %s
                """
            self.env.cr.execute(sql, (kkn.name, kkn.semester_genap, kkn.semester_ganjil, kkn.jumlah, kkn.ak, kkn.jenis_kkn_id.id, kkn.skp_kkn_pkn_pkl_id.id, kkn.skp_id.id))
               
        for dis in self.disertasi_thesis_skripsi_ids:
            sql = """
                update vit_skp_disertasi
                set name = %s, jumlah_lulusan_pembimbing_utama = %s, jumlah_lulusan_pembimbing_pembantu = %s, ak_pembimbing_utama = %s, ak_pembimbing_pembantu = %s, ak_total = %s, jenis_disertasi_id = %s, semester_id = %s
                where id = %s and skp_id = %s
                """
            self.env.cr.execute(sql, (dis.name, dis.jumlah_lulusan_pembimbing_utama, dis.jumlah_lulusan_pembimbing_pembantu, dis.ak_pembimbing_utama, dis.ak_pembimbing_pembantu, dis.ak_total, dis.jenis_disertasi_id.id, dis.semester_id.id, dis.skp_disertasi_id.id, dis.skp_id.id))

        for uji in self.penguji_ids:
            sql = """
                update vit_skp_penguji
                set name = %s, jumlah_mhs_ketua_penguji = %s, jumlah_mhs_anggota_penguji = %s, ak_ketua_penguji = %s, ak_anggota_penguji = %s, ak_total = %s, semester_id = %s
                where id = %s and skp_id = %s
                """
            self.env.cr.execute(sql, (uji.name, uji.jumlah_mhs_ketua_penguji, uji.jumlah_mhs_anggota_penguji, uji.ak_ketua_penguji, uji.ak_anggota_penguji, uji.ak_total, uji.semester_id.id, uji.skp_penguji_id.id, uji.skp_id.id))
        
        for bna in self.membina_ids:
            sql = """
                update vit_skp_membina
                set name = %s, semester_genap = %s, semester_ganjil = %s, jumlah = %s, ak = %s
                where id = %s and skp_id = %s
                """
            self.env.cr.execute(sql, (bna.name, bna.semester_genap, bna.semester_ganjil, bna.jumlah, bna.ak, bna.skp_membina_id.id, bna.skp_id.id))
        
        for mpk in self.mengembangkan_program_kuliah_ids:
            sql = """
                update vit_skp_mengembangkan_program_kuliah
                set name = %s, semester_genap = %s, semester_ganjil = %s, jumlah = %s, ak = %s
                where id = %s and skp_id = %s
                """
            self.env.cr.execute(sql, (mpk.name, mpk.semester_genap, mpk.semester_ganjil, mpk.jumlah, mpk.ak, mpk.skp_mengembangkan_program_kuliah_id.id, mpk.skp_id.id))
        
        for mbk in self.mengembangkan_bahan_kuliah_ids:
            sql = """
                update vit_skp_mengembangkan_bahan_kuliah
                set name = %s, jumlah = %s, ak_per_bahan_kuliah = %s, ak_jumlah = %s, semester_id = %s
                where id = %s and skp_id = %s
                """
            self.env.cr.execute(sql, (mbk.name, mbk.jumlah, mbk.ak_per_bahan_kuliah, mbk.ak_jumlah, mbk.semester_id.id, mbk.skp_mengembangkan_bahan_kuliah_id.id, mbk.skp_id.id))
        
        for oil in self.orasi_ilmiah_ids:
            sql = """
                update vit_skp_orasi_ilmiah
                set name = %s, semester_genap = %s, semester_ganjil = %s, jumlah = %s, ak = %s
                where id = %s and skp_id = %s
                """
            self.env.cr.execute(sql, (oil.name, oil.semester_genap, oil.semester_ganjil, oil.jumlah, oil.ak, oil.skp_orasi_ilmiah_id.id, oil.skp_id.id))
        
        for jab in self.jabatan_pt_ids:
            sql = """
                update vit_skp_jabatan_pt
                set name = %s, hasil = %s, satuan_hasil = %s, angka_kredit = %s, jumlah_angka_kredit = %s, semester_id = %s
                where id = %s and skp_id = %s
                """
            self.env.cr.execute(sql, (jab.name, jab.hasil, jab.satuan_hasil, jab.angka_kredit, jab.jumlah_angka_kredit, jab.semester_id.id, jab.skp_jabatan_pt_id.id, jab.skp_id.id))
        
        for bim in self.membimbing_dosen_ids:
            sql = """
                update vit_skp_membimbing_dosen
                set name = %s, semester_genap = %s, semester_ganjil = %s, jumlah = %s, ak = %s
                where id = %s and skp_id = %s
                """
            self.env.cr.execute(sql, (bim.name, bim.semester_genap, bim.semester_ganjil, bim.jumlah, bim.ak, bim.skp_membimbing_dosen_id.id, bim.skp_id.id))
        
        for det in self.detasering_ids:
            sql = """
                update vit_skp_detasering
                set name = %s, semester_genap = %s, semester_ganjil = %s, jumlah = %s, ak = %s
                where id = %s and skp_id = %s
                """
            self.env.cr.execute(sql, (det.name, det.semester_genap, det.semester_ganjil, det.jumlah, det.ak, det.skp_detasering_id.id, det.skp_id.id))
        
        for pd in self.pengembangan_diri_ids:
            sql = """
                update vit_skp_pengembangan_diri
                set name = %s, semester_genap = %s, semester_ganjil = %s, jumlah = %s, jumlah_ak = %s, ak = %s
                where id = %s and skp_id = %s
                """
            self.env.cr.execute(sql, (pd.name, pd.semester_genap, pd.semester_ganjil, pd.jumlah, pd.jumlah_ak, pd.ak, pd.skp_pengembangan_diri_id.id, pd.skp_id.id))
        
        for plt in self.penelitian_ids:
            sql = """
                update vit_skp_penelitian
                set name = %s, jumlah_peneliti_mandiri = %s, jumlah_peneliti_utama = %s, jumlah_peneliti_anggota = %s, ak_karya_ilmiah_jurnal = %s,  ak_jumlah_peneliti_mandiri = %s, ak_jumlah_peneliti_utama = %s, ak_jumlah_peneliti_anggota = %s, ak_jumlah = %s
                where id = %s and skp_id = %s
                """
            self.env.cr.execute(sql, (plt.name, plt.jumlah_peneliti_mandiri, plt.jumlah_peneliti_utama, plt.jumlah_peneliti_anggota, plt.ak_karya_ilmiah_jurnal, plt.ak_jumlah_peneliti_mandiri, plt.ak_jumlah_peneliti_utama, plt.ak_jumlah_peneliti_anggota, plt.ak_jumlah, plt.skp_penelitian_id.id, plt.skp_id.id))
            
        for abd in self.pengabdian_ids:
            sql = """
                update vit_skp_pengabdian
                set name = %s, jumlah_program = %s, ak_program = %s, ak_jumlah = %s
                where id = %s and skp_id = %s
                """
            self.env.cr.execute(sql, (abd.name, abd.jumlah_program, abd.ak_program, abd.ak_jumlah, abd.skp_pengabdian_id.id, abd.skp_id.id))
        
        for rkl in self.rekapitulasi_ids:
            sql = """
                update vit_skp_rekapitulasi_perkuliahan
                set name = %s, sks = %s, sks_riil = %s, ak_10_sks_pertama = %s, ak_sks_berikutnya = %s, ak_jumlah = %s, semester_id = %s
                where id = %s and skp_id = %s
                """
            self.env.cr.execute(sql, (rkl.name, rkl.sks, rkl.sks_riil, rkl.ak_10_sks_pertama, rkl.ak_sks_berikutnya, rkl.ak_jumlah, rkl.semester_id.id, rkl.skp_rekapitulasi_perkuliahan_id.id, rkl.skp_id.id))
        
        for rbk in self.rekapitulasi_mengembangkan_bahan_kuliah_ids:
            sql = """
                update vit_skp_rekapitulasi_mengembangkan_bahan_kuliah
                set name = %s, naskah = %s, ak = %s
                where id = %s and skp_id = %s
                """
            self.env.cr.execute(sql, (rbk.name, rbk.naskah, rbk.ak, rbk.skp_rekapitulasi_mengembangkan_bahan_kuliah_id.id, rbk.skp_id.id))
        
        for rjb in self.rekapitulasi_jabatan_pt_ids:
            sql = """
                update vit_skp_rekapitulasi_jabatan_pt
                set name = %s, satuan_hasil = %s, jumlah_angka_kredit = %s
                where id = %s and skp_id = %s
                """
            self.env.cr.execute(sql, (rjb.name, rjb.satuan_hasil, rjb.jumlah_angka_kredit, rjb.skp_rekapitulasi_jabatan_pt_id.id, rjb.skp_id.id))
        
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
        return super(mutasiskp, self).unlink()

    def action_print_pengukuran(self, ):
        pass


    def action_print_penilaian(self, ):
        pass


    def action_print_skp(self, ):
        pass


    def action_hitung_rekapitulasi(self, ):
        pass

    def action_reload(self, ):
        if self.pns_id.id == False and self.tahun_akademik_id.id == False:
            raise UserError("Isi kolom Pns dan Tahun Akademik")

        sql = "delete from vit_skp_perkuliahan_mut where mutasi_skp_id = %s"
        self.env.cr.execute(sql, (self.id,))
        sql = """
                insert into vit_skp_perkuliahan_mut (name, sks, jumlah_kelas, jumlah_dosen_pengampu, totak_sks_per_smt, semester_id, skp_id, skp_perkuliahan_id, mutasi_skp_id)
                select sp.name, sp.sks, sp.jumlah_kelas, sp.jumlah_dosen_pengampu, sp.totak_sks_per_smt, sem.id, skp.id, sp.id, %s
                from vit_skp skp
                left join vit_skp_perkuliahan sp on sp.skp_id = skp.id
                left join vit_semester sem on sp.semester_id = sem.id
                left join hr_employee pns on skp.pns_id = pns.id
                left join vit_tahun_akademik tak on skp.tahun_akademik_id = tak.id
                where pns.id = %s and tak.id = %s
                """
        # import pdb; pdb.set_trace()
        self.env.cr.execute(sql, (self.id, self.pns_id.id, self.tahun_akademik_id.id))

        sql1 = "delete from vit_skp_seminar_mut where mutasi_skp_id = %s"
        self.env.cr.execute(sql1, (self.id,))
        sql1 = """
                insert into vit_skp_seminar_mut (name, pelaksanaan, ak, semester_id, skp_id, skp_seminar_id, mutasi_skp_id)
                select smr.name, smr.pelaksanaan, smr.ak, sem.id, skp.id, smr.id, %s
                from vit_skp skp
                left join vit_skp_seminar smr on smr.skp_id = skp.id
                left join vit_semester sem on smr.semester_id = sem.id
                left join hr_employee pns on skp.pns_id = pns.id
                left join vit_tahun_akademik tak on skp.tahun_akademik_id = tak.id
                where pns.id = %s and tak.id = %s
                """
        # import pdb; pdb.set_trace()
        self.env.cr.execute(sql1, (self.id, self.pns_id.id, self.tahun_akademik_id.id))

        sql2 = "delete from vit_skp_kkn_pkn_pkl_mut where mutasi_skp_id = %s"
        self.env.cr.execute(sql2, (self.id,))
        sql2 = """
                insert into vit_skp_kkn_pkn_pkl_mut (name, semester_genap, semester_ganjil, jumlah, ak, jenis_kkn_id, skp_id, skp_kkn_pkn_pkl_id, mutasi_skp_id)
                select kkn.name, sema.id, semi.id, kkn.jumlah, kkn.ak, jk.id, skp.id, kkn.id, %s
                from vit_skp skp
                left join vit_skp_kkn_pkn_pkl kkn on kkn.skp_id = skp.id
                left join vit_semester sema on kkn.semester_genap = sema.id
                left join vit_semester semi on kkn.semester_ganjil = semi.id
                left join vit_jenis_kkn jk on kkn.jenis_kkn_id = jk.id
                left join hr_employee pns on skp.pns_id = pns.id
                left join vit_tahun_akademik tak on skp.tahun_akademik_id = tak.id
                where pns.id = %s and tak.id = %s
                """
        # import pdb; pdb.set_trace()
        self.env.cr.execute(sql2, (self.id, self.pns_id.id, self.tahun_akademik_id.id))

        sql3 = "delete from vit_skp_disertasi_mut where mutasi_skp_id = %s"
        self.env.cr.execute(sql3, (self.id,))
        sql3 = """
                insert into vit_skp_disertasi_mut (name, jumlah_lulusan_pembimbing_utama, jumlah_lulusan_pembimbing_pembantu, ak_pembimbing_utama, ak_pembimbing_pembantu, ak_total, jenis_disertasi_id, semester_id, skp_id, skp_disertasi_id, mutasi_skp_id)
                select dis.name, dis.jumlah_lulusan_pembimbing_utama, dis.jumlah_lulusan_pembimbing_pembantu, dis.ak_pembimbing_utama, dis.ak_pembimbing_pembantu, dis.ak_total, jd.id, sem.id, skp.id, dis.id, %s
                from vit_skp skp
                left join vit_skp_disertasi dis on dis.skp_id = skp.id
                left join vit_semester sem on dis.semester_id = sem.id
                left join vit_jenis_disertasi jd on dis.jenis_disertasi_id = jd.id
                left join hr_employee pns on skp.pns_id = pns.id
                left join vit_tahun_akademik tak on skp.tahun_akademik_id = tak.id
                where pns.id = %s and tak.id = %s
                """
        # import pdb; pdb.set_trace()
        self.env.cr.execute(sql3, (self.id, self.pns_id.id, self.tahun_akademik_id.id))

        sql4 = "delete from vit_skp_penguji_mut where mutasi_skp_id = %s"
        self.env.cr.execute(sql4, (self.id,))
        sql4 = """
                insert into vit_skp_penguji_mut (name, jumlah_mhs_ketua_penguji, jumlah_mhs_anggota_penguji, ak_ketua_penguji, ak_anggota_penguji, ak_total, semester_id, skp_id, skp_penguji_id, mutasi_skp_id)
                select uji.name, uji.jumlah_mhs_ketua_penguji, uji.jumlah_mhs_anggota_penguji, uji.ak_ketua_penguji, uji.ak_anggota_penguji, uji.ak_total, sem.id, skp.id, uji.id, %s
                from vit_skp skp
                left join vit_skp_penguji uji on uji.skp_id = skp.id
                left join vit_semester sem on uji.semester_id = sem.id
                left join hr_employee pns on skp.pns_id = pns.id
                left join vit_tahun_akademik tak on skp.tahun_akademik_id = tak.id
                where pns.id = %s and tak.id = %s
                """
        # import pdb; pdb.set_trace()
        self.env.cr.execute(sql4, (self.id, self.pns_id.id, self.tahun_akademik_id.id))

        sql5 = "delete from vit_skp_membina_mut where mutasi_skp_id = %s"
        self.env.cr.execute(sql5, (self.id,))
        sql5 = """
                insert into vit_skp_membina_mut (name, semester_genap, semester_ganjil, jumlah, ak, skp_id, skp_membina_id, mutasi_skp_id)
                select bna.name, sema.id, semi.id, bna.jumlah, bna.ak, skp.id, bna.id, %s
                from vit_skp skp
                left join vit_skp_membina bna on bna.skp_id = skp.id
                left join vit_semester sema on bna.semester_genap = sema.id
                left join vit_semester semi on bna.semester_ganjil = semi.id
                left join hr_employee pns on skp.pns_id = pns.id
                left join vit_tahun_akademik tak on skp.tahun_akademik_id = tak.id
                where pns.id = %s and tak.id = %s
                """
        # import pdb; pdb.set_trace()
        self.env.cr.execute(sql5, (self.id, self.pns_id.id, self.tahun_akademik_id.id))

        sql6 = "delete from vit_skp_mengembangkan_program_kuliah_mut where mutasi_skp_id = %s"
        self.env.cr.execute(sql6, (self.id,))
        sql6 = """
                insert into vit_skp_mengembangkan_program_kuliah_mut (name, semester_genap, semester_ganjil, jumlah, ak, skp_id, skp_mengembangkan_program_kuliah_id, mutasi_skp_id)
                select mpk.name, sema.id, semi.id, mpk.jumlah, mpk.ak, skp.id, mpk.id, %s
                from vit_skp skp
                left join vit_skp_mengembangkan_program_kuliah mpk on mpk.skp_id = skp.id
                left join vit_semester sema on mpk.semester_genap = sema.id
                left join vit_semester semi on mpk.semester_ganjil = semi.id
                left join hr_employee pns on skp.pns_id = pns.id
                left join vit_tahun_akademik tak on skp.tahun_akademik_id = tak.id
                where pns.id = %s and tak.id = %s
                """
        # import pdb; pdb.set_trace()
        self.env.cr.execute(sql6, (self.id, self.pns_id.id, self.tahun_akademik_id.id))

        sql7 = "delete from vit_skp_mengembangkan_bahan_kuliah_mut where mutasi_skp_id = %s"
        self.env.cr.execute(sql7, (self.id,))
        sql7 = """
                insert into vit_skp_mengembangkan_bahan_kuliah_mut (name, jumlah, ak_per_bahan_kuliah, ak_jumlah, semester_id, skp_id, skp_mengembangkan_bahan_kuliah_id, mutasi_skp_id)
                select mbk.name, mbk.jumlah, mbk.ak_per_bahan_kuliah, mbk.ak_jumlah, sem.id, skp.id, mbk.id, %s
                from vit_skp skp
                left join vit_skp_mengembangkan_bahan_kuliah mbk on mbk.skp_id = skp.id
                left join vit_semester sem on mbk.semester_id = sem.id
                left join hr_employee pns on skp.pns_id = pns.id
                left join vit_tahun_akademik tak on skp.tahun_akademik_id = tak.id
                where pns.id = %s and tak.id = %s
                """
        # import pdb; pdb.set_trace()
        self.env.cr.execute(sql7, (self.id, self.pns_id.id, self.tahun_akademik_id.id))

        sql8 = "delete from vit_skp_orasi_ilmiah_mut where mutasi_skp_id = %s"
        self.env.cr.execute(sql8, (self.id,))
        sql8 = """
                insert into vit_skp_orasi_ilmiah_mut (name, semester_genap, semester_ganjil, jumlah, ak, skp_id, skp_orasi_ilmiah_id, mutasi_skp_id)
                select oil.name, sema.id, semi.id, oil.jumlah, oil.ak, skp.id, oil.id, %s
                from vit_skp skp
                left join vit_skp_orasi_ilmiah oil on oil.skp_id = skp.id
                left join vit_semester sema on oil.semester_genap = sema.id
                left join vit_semester semi on oil.semester_ganjil = semi.id
                left join hr_employee pns on skp.pns_id = pns.id
                left join vit_tahun_akademik tak on skp.tahun_akademik_id = tak.id
                where pns.id = %s and tak.id = %s
                """
        # import pdb; pdb.set_trace()
        self.env.cr.execute(sql8, (self.id, self.pns_id.id, self.tahun_akademik_id.id))

        sql9 = "delete from vit_skp_jabatan_pt_mut where mutasi_skp_id = %s"
        self.env.cr.execute(sql9, (self.id,))
        sql9 = """
                insert into vit_skp_jabatan_pt_mut (name, hasil, satuan_hasil, angka_kredit, jumlah_angka_kredit, semester_id, skp_id, skp_jabatan_pt_id, mutasi_skp_id)
                select jab.name, jab.hasil, jab.satuan_hasil, jab.angka_kredit, jab.jumlah_angka_kredit, sem.id, skp.id, jab.id, %s
                from vit_skp skp
                left join vit_skp_jabatan_pt jab on jab.skp_id = skp.id
                left join vit_semester sem on jab.semester_id = sem.id
                left join hr_employee pns on skp.pns_id = pns.id
                left join vit_tahun_akademik tak on skp.tahun_akademik_id = tak.id
                where pns.id = %s and tak.id = %s
                """
        # import pdb; pdb.set_trace()
        self.env.cr.execute(sql9, (self.id, self.pns_id.id, self.tahun_akademik_id.id))

        sql10 = "delete from vit_skp_membimbing_dosen_mut where mutasi_skp_id = %s"
        self.env.cr.execute(sql10, (self.id,))
        sql10 = """
                insert into vit_skp_membimbing_dosen_mut (name, semester_genap, semester_ganjil, jumlah, ak, skp_id, skp_membimbing_dosen_id, mutasi_skp_id)
                select bim.name, sema.id, semi.id, bim.jumlah, bim.ak, skp.id, bim.id, %s
                from vit_skp skp
                left join vit_skp_membimbing_dosen bim on bim.skp_id = skp.id
                left join vit_semester sema on bim.semester_genap = sema.id
                left join vit_semester semi on bim.semester_ganjil = semi.id
                left join hr_employee pns on skp.pns_id = pns.id
                left join vit_tahun_akademik tak on skp.tahun_akademik_id = tak.id
                where pns.id = %s and tak.id = %s
                """
        # import pdb; pdb.set_trace()
        self.env.cr.execute(sql10, (self.id, self.pns_id.id, self.tahun_akademik_id.id))

        sql11 = "delete from vit_skp_detasering_mut where mutasi_skp_id = %s"
        self.env.cr.execute(sql11, (self.id,))
        sql11 = """
                insert into vit_skp_detasering_mut (name, semester_genap, semester_ganjil, jumlah, ak, skp_id, skp_detasering_id, mutasi_skp_id)
                select det.name, sema.id, semi.id, det.jumlah, det.ak, skp.id, det.id, %s
                from vit_skp skp
                left join vit_skp_detasering det on det.skp_id = skp.id
                left join vit_semester sema on det.semester_genap = sema.id
                left join vit_semester semi on det.semester_ganjil = semi.id
                left join hr_employee pns on skp.pns_id = pns.id
                left join vit_tahun_akademik tak on skp.tahun_akademik_id = tak.id
                where pns.id = %s and tak.id = %s
                """
        # import pdb; pdb.set_trace()
        self.env.cr.execute(sql11, (self.id, self.pns_id.id, self.tahun_akademik_id.id))

        sql12 = "delete from vit_skp_pengembangan_diri_mut where mutasi_skp_id = %s"
        self.env.cr.execute(sql12, (self.id,))
        sql12 = """
                insert into vit_skp_pengembangan_diri_mut (name, semester_genap, semester_ganjil, jumlah, ak, jumlah_ak, skp_id, skp_pengembangan_diri_id, mutasi_skp_id)
                select pd.name, sema.id, semi.id, pd.jumlah, pd.ak, pd.jumlah_ak, skp.id, pd.id, %s
                from vit_skp skp
                left join vit_skp_pengembangan_diri pd on pd.skp_id = skp.id
                left join vit_semester sema on pd.semester_genap = sema.id
                left join vit_semester semi on pd.semester_ganjil = semi.id
                left join hr_employee pns on skp.pns_id = pns.id
                left join vit_tahun_akademik tak on skp.tahun_akademik_id = tak.id
                where pns.id = %s and tak.id = %s
                """
        # import pdb; pdb.set_trace()
        self.env.cr.execute(sql12, (self.id, self.pns_id.id, self.tahun_akademik_id.id))

        sql12 = "delete from vit_skp_penelitian_mut where mutasi_skp_id = %s"
        self.env.cr.execute(sql12, (self.id,))
        sql12 = """
                insert into vit_skp_penelitian_mut (name, jumlah_peneliti_mandiri, jumlah_peneliti_utama, jumlah_peneliti_anggota, ak_karya_ilmiah_jurnal, ak_jumlah_peneliti_mandiri, ak_jumlah_peneliti_utama, ak_jumlah_peneliti_anggota, ak_jumlah, skp_id, skp_penelitian_id, mutasi_skp_id)
                select plt.name, plt.jumlah_peneliti_mandiri, plt.jumlah_peneliti_utama, plt.jumlah_peneliti_anggota, plt.ak_karya_ilmiah_jurnal, plt.ak_jumlah_peneliti_mandiri, plt.ak_jumlah_peneliti_utama, plt.ak_jumlah_peneliti_anggota, plt.ak_jumlah, skp.id, plt.id, %s
                from vit_skp skp
                left join vit_skp_penelitian plt on plt.skp_id = skp.id
                left join hr_employee pns on skp.pns_id = pns.id
                left join vit_tahun_akademik tak on skp.tahun_akademik_id = tak.id
                where pns.id = %s and tak.id = %s
                """
        # import pdb; pdb.set_trace()
        self.env.cr.execute(sql12, (self.id, self.pns_id.id, self.tahun_akademik_id.id))

        sql13 = "delete from vit_skp_pengabdian_mut where mutasi_skp_id = %s"
        self.env.cr.execute(sql13, (self.id,))
        sql13 = """
                insert into vit_skp_pengabdian_mut (name, jumlah_program, ak_program, ak_jumlah, skp_id, skp_pengabdian_id, mutasi_skp_id)
                select abd.name, abd.jumlah_program, abd.ak_program, abd.ak_jumlah, skp.id, abd.id, %s
                from vit_skp skp
                left join vit_skp_pengabdian abd on abd.skp_id = skp.id
                left join hr_employee pns on skp.pns_id = pns.id
                left join vit_tahun_akademik tak on skp.tahun_akademik_id = tak.id
                where pns.id = %s and tak.id = %s
                """
        # import pdb; pdb.set_trace()
        self.env.cr.execute(sql13, (self.id, self.pns_id.id, self.tahun_akademik_id.id))

        sql14 = "delete from vit_skp_rekapitulasi_perkuliahan_mut where mutasi_skp_id = %s"
        self.env.cr.execute(sql14, (self.id,))
        sql14 = """
                insert into vit_skp_rekapitulasi_perkuliahan_mut (name, sks, sks_riil, ak_10_sks_pertama, ak_sks_berikutnya, ak_jumlah, semester_id, skp_id, skp_rekapitulasi_perkuliahan_id, mutasi_skp_id)
                select rpk.name, rpk.sks, rpk.sks_riil, rpk.ak_10_sks_pertama, rpk.ak_sks_berikutnya, rpk.ak_jumlah, sem.id, skp.id, rpk.id, %s
                from vit_skp skp
                left join vit_skp_rekapitulasi_perkuliahan rpk on rpk.skp_id = skp.id
                left join vit_semester sem on rpk.semester_id = sem.id
                left join hr_employee pns on skp.pns_id = pns.id
                left join vit_tahun_akademik tak on skp.tahun_akademik_id = tak.id
                where pns.id = %s and tak.id = %s
                """
        # import pdb; pdb.set_trace()
        self.env.cr.execute(sql14, (self.id, self.pns_id.id, self.tahun_akademik_id.id))

        sql15 = "delete from vit_skp_rekapitulasi_mengembangkan_bahan_kuliah_mut where mutasi_skp_id = %s"
        self.env.cr.execute(sql15, (self.id,))
        sql15 = """
                insert into vit_skp_rekapitulasi_mengembangkan_bahan_kuliah_mut (name, naskah, ak, skp_id, skp_rekapitulasi_mengembangkan_bahan_kuliah_id, mutasi_skp_id)
                select rbk.name, rbk.naskah, rbk.ak, skp.id, rbk.id, %s
                from vit_skp skp
                left join vit_skp_rekapitulasi_mengembangkan_bahan_kuliah rbk on rbk.skp_id = skp.id
                left join hr_employee pns on skp.pns_id = pns.id
                left join vit_tahun_akademik tak on skp.tahun_akademik_id = tak.id
                where pns.id = %s and tak.id = %s
                """
        # import pdb; pdb.set_trace()
        self.env.cr.execute(sql15, (self.id, self.pns_id.id, self.tahun_akademik_id.id))

        sql16 = "delete from vit_skp_rekapitulasi_jabatan_pt_mut where mutasi_skp_id = %s"
        self.env.cr.execute(sql16, (self.id,))
        sql16 = """
                insert into vit_skp_rekapitulasi_jabatan_pt_mut (name, satuan_hasil, jumlah_angka_kredit, skp_id, skp_rekapitulasi_jabatan_pt_id, mutasi_skp_id)
                select rjb.name, rjb.satuan_hasil, rjb.jumlah_angka_kredit, skp.id, rjb.id, %s
                from vit_skp skp
                left join vit_skp_rekapitulasi_jabatan_pt rjb on rjb.skp_id = skp.id
                left join hr_employee pns on skp.pns_id = pns.id
                left join vit_tahun_akademik tak on skp.tahun_akademik_id = tak.id
                where pns.id = %s and tak.id = %s
                """
        # import pdb; pdb.set_trace()
        self.env.cr.execute(sql16, (self.id, self.pns_id.id, self.tahun_akademik_id.id))


class mutasi_skp_perkuliahan_mut(models.Model):
    _name = "vit.skp_perkuliahan_mut"
    _description = "vit.skp_perkuliahan_mut"

    name = fields.Char( required=True, string="Name",  help="")
    sks = fields.Integer( string="Sks",  help="")
    jumlah_kelas = fields.Integer( string="Jumlah kelas",  help="")
    jumlah_dosen_pengampu = fields.Integer( string="Jumlah dosen pengampu",  help="")
    totak_sks_per_smt = fields.Float( string="Total sks per smt",  help="")
    semester_id = fields.Many2one(comodel_name="vit.semester",  string="Semester",  help="")

    mutasi_skp_id = fields.Many2one(comodel_name="vit.mutasi_skp",  string="Mutasi Skp",  help="")
    skp_id = fields.Many2one(comodel_name="vit.skp",  string="Skp",  help="")
    skp_perkuliahan_id = fields.Many2one(comodel_name="vit.skp_perkuliahan",  string="Skp Perkuliahan",  help="")

class mutasi_skp_detasering_mut(models.Model):
    _name = "vit.skp_detasering_mut"
    _description = "vit.skp_detasering_mut"

    name = fields.Char( required=True, string="Name",  help="")
    semester_genap = fields.Integer( string="Semester genap",  help="")
    semester_ganjil = fields.Integer( string="Semester ganjil",  help="")
    jumlah = fields.Integer( string="Jumlah",  help="")
    ak = fields.Integer( string="Ak",  help="")

    mutasi_skp_id = fields.Many2one(comodel_name="vit.mutasi_skp",  string="Mutasi Skp",  help="")
    skp_id = fields.Many2one(comodel_name="vit.skp",  string="Skp",  help="")
    skp_detasering_id = fields.Many2one(comodel_name="vit.skp_detasering",  string="Skp Detasering",  help="")

class mutasi_skp_disertasi_mut(models.Model):
    _name = "vit.skp_disertasi_mut"
    _description = "vit.skp_disertasi_mut"

    name = fields.Char( required=True, string="Name",  help="")
    jumlah_lulusan_pembimbing_utama = fields.Integer( string="Jumlah lulusan pembimbing utama",  help="")
    jumlah_lulusan_pembimbing_pembantu = fields.Integer( string="Jumlah lulusan pembimbing pembantu",  help="")
    ak_pembimbing_utama = fields.Integer( string="Ak pembimbing utama",  help="")
    ak_pembimbing_pembantu = fields.Integer( string="Ak pembimbing pembantu",  help="")
    ak_total = fields.Integer( string="Ak total",  help="")
    jenis_disertasi_id = fields.Many2one(comodel_name="vit.jenis_disertasi",  string="Jenis disertasi",  help="")
    semester_id = fields.Many2one(comodel_name="vit.semester",  string="Semester",  help="")

    mutasi_skp_id = fields.Many2one(comodel_name="vit.mutasi_skp",  string="Mutasi Skp",  help="")
    skp_id = fields.Many2one(comodel_name="vit.skp",  string="Skp",  help="")
    skp_disertasi_id = fields.Many2one(comodel_name="vit.skp_disertasi",  string="Skp Disertasi",  help="")

class mutasi_skp_jabatan_pt(models.Model):
    _name = "vit.skp_jabatan_pt_mut"
    _description = "vit.skp_jabatan_pt_mut"

    name = fields.Char( required=True, string="Name",  help="")
    hasil = fields.Integer( string="Hasil",  help="")
    satuan_hasil = fields.Char( string="Satuan hasil",  help="")
    angka_kredit = fields.Integer( string="Angka kredit",  help="")
    jumlah_angka_kredit = fields.Integer( string="Jumlah angka kredit",  help="")
    semester_id = fields.Many2one(comodel_name="vit.semester",  string="Semester",  help="")

    mutasi_skp_id = fields.Many2one(comodel_name="vit.mutasi_skp",  string="Mutasi Skp",  help="")
    skp_id = fields.Many2one(comodel_name="vit.skp",  string="Skp",  help="")
    skp_jabatan_pt_id = fields.Many2one(comodel_name="vit.skp_jabatan_pt",  string="Skp Jabatan PT",  help="")

class mutasi_skp_kkn_pkn_pkl_mut(models.Model):
    _name = "vit.skp_kkn_pkn_pkl_mut"
    _description = "vit.skp_kkn_pkn_pkl_mut"

    name = fields.Char( required=True, string="Name",  help="")
    semester_genap = fields.Integer( string="Semester genap",  help="")
    semester_ganjil = fields.Integer( string="Semester ganjil",  help="")
    jumlah = fields.Integer( string="Jumlah",  help="")
    ak = fields.Integer( string="Ak",  help="")
    jenis_kkn_id = fields.Many2one(comodel_name="vit.jenis_kkn",  string="Jenis kkn",  help="")

    mutasi_skp_id = fields.Many2one(comodel_name="vit.mutasi_skp",  string="Mutasi Skp",  help="")
    skp_id = fields.Many2one(comodel_name="vit.skp",  string="Skp",  help="")
    skp_kkn_pkn_pkl_id = fields.Many2one(comodel_name="vit.skp_kkn_pkn_pkl",  string="Skp KKN",  help="")

class mutasi_skp_membimbing_dosen_mut(models.Model):
    _name = "vit.skp_membimbing_dosen_mut"
    _description = "vit.skp_membimbing_dosen_mut"

    name = fields.Char( required=True, string="Name",  help="")
    semester_genap = fields.Integer( string="Semester genap",  help="")
    semester_ganjil = fields.Integer( string="Semester ganjil",  help="")
    jumlah = fields.Integer( string="Jumlah",  help="")
    ak = fields.Integer( string="Ak",  help="")

    mutasi_skp_id = fields.Many2one(comodel_name="vit.mutasi_skp",  string="Mutasi Skp",  help="")
    skp_id = fields.Many2one(comodel_name="vit.skp",  string="Skp",  help="")
    skp_membimbing_dosen_id = fields.Many2one(comodel_name="vit.skp_membimbing_dosen",  string="Skp Membimbing dosen",  help="")

class mutasi_skp_membina_mut(models.Model):
    _name = "vit.skp_membina_mut"
    _description = "vit.skp_membina_mut"

    name = fields.Char( required=True, string="Name",  help="")
    semester_genap = fields.Integer( string="Semester genap",  help="")
    semester_ganjil = fields.Integer( string="Semester ganjil",  help="")
    jumlah = fields.Integer( string="Jumlah",  help="")
    ak = fields.Integer( string="Ak",  help="")

    mutasi_skp_id = fields.Many2one(comodel_name="vit.mutasi_skp",  string="Mutasi Skp",  help="")
    skp_id = fields.Many2one(comodel_name="vit.skp",  string="Skp",  help="")
    skp_membina_id = fields.Many2one(comodel_name="vit.skp_membina",  string="Skp Membina",  help="")

class mutasi_skp_mengembangkan_bahan_kuliah_mut(models.Model):
    _name = "vit.skp_mengembangkan_bahan_kuliah_mut"
    _description = "vit.skp_mengembangkan_bahan_kuliah_mut"

    name = fields.Char( required=True, string="Name",  help="")
    jumlah = fields.Integer( string="Jumlah",  help="")
    ak_per_bahan_kuliah = fields.Integer( string="Ak per bahan kuliah",  help="")
    ak_jumlah = fields.Integer( string="Ak jumlah",  help="")
    semester_id = fields.Many2one(comodel_name="vit.semester",  string="Semester",  help="")

    mutasi_skp_id = fields.Many2one(comodel_name="vit.mutasi_skp",  string="Mutasi Skp",  help="")
    skp_id = fields.Many2one(comodel_name="vit.skp",  string="Skp",  help="")
    skp_mengembangkan_bahan_kuliah_id = fields.Many2one(comodel_name="vit.skp_mengembangkan_bahan_kuliah",  string="Skp Mengembangkan bahan kuliah",  help="")

class mutasi_skp_mengembangkan_program_kuliah_mut(models.Model):
    _name = "vit.skp_mengembangkan_program_kuliah_mut"
    _description = "vit.skp_mengembangkan_program_kuliah_mut"

    name = fields.Char( required=True, string="Name",  help="")
    semester_genap = fields.Integer( string="Semester genap",  help="")
    semester_ganjil = fields.Integer( string="Semester ganjil",  help="")
    jumlah = fields.Integer( string="Jumlah",  help="")
    ak = fields.Integer( string="Ak",  help="")

    mutasi_skp_id = fields.Many2one(comodel_name="vit.mutasi_skp",  string="Mutasi Skp",  help="")
    skp_id = fields.Many2one(comodel_name="vit.skp",  string="Skp",  help="")
    skp_mengembangkan_program_kuliah_id = fields.Many2one(comodel_name="vit.skp_mengembangkan_program_kuliah",  string="Skp Mengembangkan program kuliah",  help="")

class mutasi_skp_orasi_ilmiah_mut(models.Model):
    _name = "vit.skp_orasi_ilmiah_mut"
    _description = "vit.skp_orasi_ilmiah_mut"

    name = fields.Char( required=True, string="Name",  help="")
    semester_genap = fields.Integer( string="Semester genap",  help="")
    semester_ganjil = fields.Integer( string="Semester ganjil",  help="")
    jumlah = fields.Integer( string="Jumlah",  help="")
    ak = fields.Integer( string="Ak",  help="")

    mutasi_skp_id = fields.Many2one(comodel_name="vit.mutasi_skp",  string="Mutasi Skp",  help="")
    skp_id = fields.Many2one(comodel_name="vit.skp",  string="Skp",  help="")
    skp_orasi_ilmiah_id = fields.Many2one(comodel_name="vit.skp_orasi_ilmiah",  string="Skp Orasi ilmiah",  help="")

class mutasi_skp_penelitian_mut(models.Model):
    _name = "vit.skp_penelitian_mut"
    _description = "vit.skp_penelitian_mut"

    name = fields.Char( required=True, string="Name",  help="")
    jumlah_peneliti_mandiri = fields.Integer( string="Jumlah peneliti mandiri",  help="")
    jumlah_peneliti_utama = fields.Integer( string="Jumlah peneliti utama",  help="")
    jumlah_peneliti_anggota = fields.Integer( string="Jumlah peneliti anggota",  help="")
    ak_karya_ilmiah_jurnal = fields.Integer( string="Ak karya ilmiah jurnal",  help="")
    ak_jumlah_peneliti_mandiri = fields.Integer( string="Ak jumlah peneliti mandiri",  help="")
    ak_jumlah_peneliti_utama = fields.Integer( string="Ak jumlah peneliti utama",  help="")
    ak_jumlah_peneliti_anggota = fields.Integer( string="Ak jumlah peneliti anggota",  help="")
    ak_jumlah = fields.Integer( string="Ak jumlah",  help="")

    mutasi_skp_id = fields.Many2one(comodel_name="vit.mutasi_skp",  string="Mutasi Skp",  help="")
    skp_id = fields.Many2one(comodel_name="vit.skp",  string="Skp",  help="")
    skp_penelitian_id = fields.Many2one(comodel_name="vit.skp_penelitian",  string="Skp Penelitian",  help="")

class mutasi_skp_pengabdian_mut(models.Model):
    _name = "vit.skp_pengabdian_mut"
    _description = "vit.skp_pengabdian_mut"

    name = fields.Char( required=True, string="Name",  help="")
    jumlah_program = fields.Integer( string="Jumlah program",  help="")
    ak_program = fields.Integer( string="Ak program",  help="")
    ak_jumlah = fields.Integer( string="Ak jumlah",  help="")

    mutasi_skp_id = fields.Many2one(comodel_name="vit.mutasi_skp",  string="Mutasi Skp",  help="")
    skp_id = fields.Many2one(comodel_name="vit.skp",  string="Skp",  help="")
    skp_pengabdian_id = fields.Many2one(comodel_name="vit.skp_pengabdian",  string="Skp Pengabdian",  help="")

class mutasi_skp_pengembangan_diri_mut(models.Model):
    _name = "vit.skp_pengembangan_diri_mut"
    _description = "vit.skp_pengembangan_diri_mut"

    name = fields.Char( required=True, string="Name",  help="")
    semester_genap = fields.Integer( string="Semester genap",  help="")
    semester_ganjil = fields.Integer( string="Semester ganjil",  help="")
    jumlah = fields.Integer( string="Jumlah",  help="")
    ak = fields.Integer( string="Ak",  help="")
    jumlah_ak = fields.Integer( string="Jumlah ak",  help="")

    mutasi_skp_id = fields.Many2one(comodel_name="vit.mutasi_skp",  string="Mutasi Skp",  help="")
    skp_id = fields.Many2one(comodel_name="vit.skp",  string="Skp",  help="")
    skp_pengembangan_diri_id = fields.Many2one(comodel_name="vit.skp_pengembangan_diri",  string="Skp Pengembangan diri",  help="")

class mutasi_skp_penguji_mut(models.Model):
    _name = "vit.skp_penguji_mut"
    _description = "vit.skp_penguji_mut"

    name = fields.Char( required=True, string="Name",  help="")
    jumlah_mhs_ketua_penguji = fields.Integer( string="Jumlah mhs ketua penguji",  help="")
    jumlah_mhs_anggota_penguji = fields.Integer( string="Jumlah mhs anggota penguji",  help="")
    ak_ketua_penguji = fields.Integer( string="Ak ketua penguji",  help="")
    ak_anggota_penguji = fields.Integer( string="Ak anggota penguji",  help="")
    ak_total = fields.Integer( string="Ak total",  help="")
    semester_id = fields.Many2one(comodel_name="vit.semester",  string="Semester",  help="")

    mutasi_skp_id = fields.Many2one(comodel_name="vit.mutasi_skp",  string="Mutasi Skp",  help="")
    skp_id = fields.Many2one(comodel_name="vit.skp",  string="Skp",  help="")
    skp_penguji_id = fields.Many2one(comodel_name="vit.skp_penguji",  string="Skp Penguji",  help="")

class mutasi_skp_rekapitulasi_jabatan_pt_mut(models.Model):
    _name = "vit.skp_rekapitulasi_jabatan_pt_mut"
    _description = "vit.skp_rekapitulasi_jabatan_pt_mut"

    name = fields.Char( required=True, string="Name",  help="")
    satuan_hasil = fields.Integer( string="Satuan hasil",  help="")
    jumlah_angka_kredit = fields.Integer( string="Jumlah angka kredit",  help="")

    mutasi_skp_id = fields.Many2one(comodel_name="vit.mutasi_skp",  string="Mutasi Skp",  help="")
    skp_id = fields.Many2one(comodel_name="vit.skp",  string="Skp",  help="")
    skp_rekapitulasi_jabatan_pt_id = fields.Many2one(comodel_name="vit.skp_rekapitulasi_jabatan_pt",  string="Skp Rekapitulasi Jabatan PT",  help="")

class mutasi_skp_rekapitulasi_mengembangkan_bahan_kuliah_mut(models.Model):
    _name = "vit.skp_rekapitulasi_mengembangkan_bahan_kuliah_mut"
    _description = "vit.skp_rekapitulasi_mengembangkan_bahan_kuliah_mut"

    name = fields.Char( required=True, string="Name",  help="")
    naskah = fields.Char( string="Naskah",  help="")
    ak = fields.Integer( string="Ak",  help="")
    
    mutasi_skp_id = fields.Many2one(comodel_name="vit.mutasi_skp",  string="Mutasi Skp",  help="")
    skp_id = fields.Many2one(comodel_name="vit.skp",  string="Skp",  help="")
    skp_rekapitulasi_mengembangkan_bahan_kuliah_id = fields.Many2one(comodel_name="vit.skp_rekapitulasi_mengembangkan_bahan_kuliah",  string="Skp Rekapitulasi mengembangkan bahan kuliah",  help="")

class mutasi_skp_rekapitulasi_perkuliahan_mut(models.Model):
    _name = "vit.skp_rekapitulasi_perkuliahan_mut"
    _description = "vit.skp_rekapitulasi_perkuliahan_mut"

    name = fields.Char( required=True, string="Name",  help="")
    sks = fields.Integer( string="Sks",  help="")
    sks_riil = fields.Integer( string="Sks riil",  help="")
    ak_10_sks_pertama = fields.Integer( string="Ak 10 sks pertama",  help="")
    ak_sks_berikutnya = fields.Integer( string="Ak sks berikutnya",  help="")
    ak_jumlah = fields.Integer( string="Ak jumlah",  help="")
    semester_id = fields.Many2one(comodel_name="vit.semester",  string="Semester",  help="")

    mutasi_skp_id = fields.Many2one(comodel_name="vit.mutasi_skp",  string="Mutasi Skp",  help="")
    skp_id = fields.Many2one(comodel_name="vit.skp",  string="Skp",  help="")
    skp_rekapitulasi_perkuliahan_id = fields.Many2one(comodel_name="vit.skp_rekapitulasi_perkuliahan",  string="Skp Rekapitulasi Perkuliahan",  help="")

class mutasi_skp_seminar_mut(models.Model):
    _name = "vit.skp_seminar_mut"
    _description = "vit.skp_seminar_mut"

    name = fields.Char( required=True, string="Name",  help="")
    pelaksanaan = fields.Integer( string="Pelaksanaan",  help="")
    ak = fields.Integer( string="Ak",  help="")
    semester_id = fields.Many2one(comodel_name="vit.semester",  string="Semester",  help="")

    mutasi_skp_id = fields.Many2one(comodel_name="vit.mutasi_skp",  string="Mutasi Skp",  help="")
    skp_id = fields.Many2one(comodel_name="vit.skp",  string="Skp",  help="")
    skp_seminar_id = fields.Many2one(comodel_name="vit.skp_seminar",  string="Skp Seminar",  help="")
