#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft','Draft'),('open','Proses'),('done','Selesai'),('reject','Ditolak')]
from odoo import models, fields, api, _
import time
from odoo.exceptions import UserError, Warning

class rekap_perguruan_tinggi(models.Model):
    _name = "vit.rekap_perguruan_tinggi"
    _inherit = ['vit.rekap_perguruan_tinggi','portal.mixin', 'mail.thread', 'mail.activity.mixin']

    name = fields.Char( required=True, default="Baru", readonly=True,  string="Name",  help="")
    date = fields.Date( string="Tanggal",  readonly=True, default=lambda self: time.strftime("%Y-%m-%d"), states={"draft" : [("readonly",False)]},  help="")
    tahun_akademik_id = fields.Many2one(comodel_name="vit.tahun_akademik",  string="Tahun akademik",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    rektor_id = fields.Many2one(comodel_name="hr.employee",  string="Rektor", related='institusi_id.rektor_id', readonly=True,  help="")
    nip_rektor = fields.Char( string="Nip rektor", related='rektor_id.nip', readonly=True, states={"draft" : [("readonly",True)]},  help="")
    alamat_perguruan_tinggi = fields.Char( string="Alamat perguruan tinggi", related='institusi_id.street',  readonly=True, states={"draft" : [("readonly",True)]},  help="")
    state = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",  help="")

    @api.model
    def create(self, vals):
        if not vals.get("name", False) or vals["name"] == "New":
            vals["name"] = self.env["ir.sequence"].next_by_code("vit.rekap_perguruan_tinggi") or "Error Number!!!"
        return super(rekap_perguruan_tinggi, self).create(vals)

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
        return super(rekap_perguruan_tinggi, self).unlink()

    @api.multi
    def action_reload(self, ):
        sql = "delete from vit_rekap_perguruan_tinggi_line where rekap_perguruan_tinggi_id = %s"
        self.env.cr.execute(sql, (self.id,))

        if not self.tahun_akademik_id:
            raise UserError(_("Tahun Akademik harus diisi") )
        else:
            # sql = """
            #     INSERT into vit_rekap_perguruan_tinggi_line (name, no_sertifikat, nama_dosen, rekap_perguruan_tinggi_id, status, semester_gasal_pd, semester_gasal_pl, semester_gasal_pg, semester_gasal_pk, semester_genap_pd, semester_genap_pl, semester_genap_pg, semester_genap_pk)                
            #     SELECT em.name, em.nomor_sertifikat, em.name, %s, %s,
            #         (SELECT SUM(pd.kinerja_sks)
            #         FROM vit_kinerja_bidang_pendidikan pd
            #         LEFT JOIN vit_bkd bkd ON pd.bkd_id = bkd.id
            #         LEFT JOIN vit_semester sm ON bkd.semester_id = sm.id
            #         WHERE bkd.employee_id = em.id AND bkd.state = 'done' AND sm.name = 'Ganjil')
            #         AS semester_gasal_pd,
            #         (SELECT SUM(pl.kinerja_sks)
            #         FROM vit_kinerja_bidang_penelitian pl
            #         LEFT JOIN vit_bkd bkd ON pl.bkd_id = bkd.id
            #         LEFT JOIN vit_semester sm ON bkd.semester_id = sm.id
            #         WHERE bkd.employee_id = em.id AND bkd.state = 'done' AND sm.name = 'Ganjil')
            #         AS semester_gasal_pl,
            #         (SELECT SUM(pb.kinerja_sks)
            #         FROM vit_kinerja_bidang_pengabdian pb
            #         LEFT JOIN vit_bkd bkd ON pb.bkd_id = bkd.id
            #         LEFT JOIN vit_semester sm ON bkd.semester_id = sm.id
            #         WHERE bkd.employee_id = em.id AND bkd.state = 'done' AND sm.name = 'Ganjil')
            #         AS semester_gasal_pg,
            #         (SELECT SUM(pk.kinerja_sks)
            #         FROM vit_kinerja_penunjang pk
            #         LEFT JOIN vit_bkd bkd ON pk.bkd_id = bkd.id
            #         LEFT JOIN vit_semester sm ON bkd.semester_id = sm.id
            #         WHERE bkd.employee_id = em.id AND bkd.state = 'done' AND sm.name = 'Ganjil')
            #         AS semester_gasal_pk,
            #         (SELECT SUM(pd.kinerja_sks)
            #         FROM vit_kinerja_bidang_pendidikan pd
            #         LEFT JOIN vit_bkd bkd ON pd.bkd_id = bkd.id
            #         LEFT JOIN vit_semester sm ON bkd.semester_id = sm.id
            #         WHERE bkd.employee_id = em.id AND bkd.state = 'done' AND sm.name = 'Genap')
            #         AS semester_genap_pd,
            #         (SELECT SUM(pl.kinerja_sks)
            #         FROM vit_kinerja_bidang_penelitian pl
            #         LEFT JOIN vit_bkd bkd ON pl.bkd_id = bkd.id
            #         LEFT JOIN vit_semester sm ON bkd.semester_id = sm.id
            #         WHERE bkd.employee_id = em.id AND bkd.state = 'done' AND sm.name = 'Genap')
            #         AS semester_genap_pl,
            #         (SELECT SUM(pb.kinerja_sks)
            #         FROM vit_kinerja_bidang_pengabdian pb
            #         LEFT JOIN vit_bkd bkd ON pb.bkd_id = bkd.id
            #         LEFT JOIN vit_semester sm ON bkd.semester_id = sm.id
            #         WHERE bkd.employee_id = em.id AND bkd.state = 'done' AND sm.name = 'Genap')
            #         AS semester_genap_pg,
            #         (SELECT SUM(pk.kinerja_sks)
            #         FROM vit_kinerja_penunjang pk
            #         LEFT JOIN vit_bkd bkd ON pk.bkd_id = bkd.id
            #         LEFT JOIN vit_semester sm ON bkd.semester_id = sm.id
            #         WHERE bkd.employee_id = em.id AND bkd.state = 'done' AND sm.name = 'Genap')
            #         AS semester_genap_pk                         
            #     FROM vit_bkd bkd
            #     LEFT JOIN hr_employee em ON bkd.employee_id = em.id
            #     LEFT JOIN vit_semester sm ON bkd.semester_id = sm.id
            #     WHERE bkd.tahun_akademik_id = %s AND bkd.state = %s
            #     GROUP BY em.id
            #     """            
            # self.env.cr.execute(sql, (self.id, 'done', self.tahun_akademik_id.id, 'done'))

            sql = """
                INSERT into vit_rekap_perguruan_tinggi_line (name, no_sertifikat, nama_dosen, rekap_perguruan_tinggi_id, status, semester_gasal_pd, semester_gasal_pl, semester_gasal_pg, semester_gasal_pk, semester_genap_pd, semester_genap_pl, semester_genap_pg, semester_genap_pk, kesimpulan, kewajiban_khusus)                
                SELECT em.name, em.nomor_sertifikat, em.name, %s, %s,
                    (SELECT SUM(kdl.kinerja)
                    FROM vit_kesimpulan_kinerja_dosen_line kdl
                    LEFT JOIN vit_kesimpulan_kinerja_dosen kkd ON kdl.kesimpulan_id = kkd.id
                    LEFT JOIN vit_semester sm ON kkd.semester_id = sm.id
                    WHERE kkd.dosen_id = em.id AND kkd.state = 'done' AND sm.name = 'Ganjil' AND kdl.name = 'Pendidikan')
                    AS semester_gasal_pd,
                    (SELECT SUM(kdl.kinerja)
                    FROM vit_kesimpulan_kinerja_dosen_line kdl
                    LEFT JOIN vit_kesimpulan_kinerja_dosen kkd ON kdl.kesimpulan_id = kkd.id
                    LEFT JOIN vit_semester sm ON kkd.semester_id = sm.id
                    WHERE kkd.dosen_id = em.id AND kkd.state = 'done' AND sm.name = 'Ganjil' AND kdl.name = 'Penelitian')
                    AS semester_gasal_pl,
                    (SELECT SUM(kdl.kinerja)
                    FROM vit_kesimpulan_kinerja_dosen_line kdl
                    LEFT JOIN vit_kesimpulan_kinerja_dosen kkd ON kdl.kesimpulan_id = kkd.id
                    LEFT JOIN vit_semester sm ON kkd.semester_id = sm.id
                    WHERE kkd.dosen_id = em.id AND kkd.state = 'done' AND sm.name = 'Ganjil' AND kdl.name = 'Pengabdian')
                    AS semester_gasal_pg,
                    ((SELECT SUM(kdl.kinerja)
                    FROM vit_kesimpulan_kinerja_dosen_line kdl
                    LEFT JOIN vit_kesimpulan_kinerja_dosen kkd ON kdl.kesimpulan_id = kkd.id
                    LEFT JOIN vit_semester sm ON kkd.semester_id = sm.id
                    WHERE kkd.dosen_id = em.id AND kkd.state = 'done' AND sm.name = 'Ganjil' AND kdl.name = 'Pengabdian + Penunjang')
                    -
                    (SELECT SUM(kdl.kinerja)
                    FROM vit_kesimpulan_kinerja_dosen_line kdl
                    LEFT JOIN vit_kesimpulan_kinerja_dosen kkd ON kdl.kesimpulan_id = kkd.id
                    LEFT JOIN vit_semester sm ON kkd.semester_id = sm.id
                    WHERE kkd.dosen_id = em.id AND kkd.state = 'done' AND sm.name = 'Ganjil' AND kdl.name = 'Pengabdian'))
                    AS semester_gasal_pk,
                    (SELECT SUM(kdl.kinerja)
                    FROM vit_kesimpulan_kinerja_dosen_line kdl
                    LEFT JOIN vit_kesimpulan_kinerja_dosen kkd ON kdl.kesimpulan_id = kkd.id
                    LEFT JOIN vit_semester sm ON kkd.semester_id = sm.id
                    WHERE kkd.dosen_id = em.id AND kkd.state = 'done' AND sm.name = 'Genap' AND kdl.name = 'Pendidikan')
                    AS semester_genap_pd,
                    (SELECT SUM(kdl.kinerja)
                    FROM vit_kesimpulan_kinerja_dosen_line kdl
                    LEFT JOIN vit_kesimpulan_kinerja_dosen kkd ON kdl.kesimpulan_id = kkd.id
                    LEFT JOIN vit_semester sm ON kkd.semester_id = sm.id
                    WHERE kkd.dosen_id = em.id AND kkd.state = 'done' AND sm.name = 'Genap' AND kdl.name = 'Penelitian')
                    AS semester_genap_pl,
                    (SELECT SUM(kdl.kinerja)
                    FROM vit_kesimpulan_kinerja_dosen_line kdl
                    LEFT JOIN vit_kesimpulan_kinerja_dosen kkd ON kdl.kesimpulan_id = kkd.id
                    LEFT JOIN vit_semester sm ON kkd.semester_id = sm.id
                    WHERE kkd.dosen_id = em.id AND kkd.state = 'done' AND sm.name = 'Genap' AND kdl.name = 'Pengabdian')
                    AS semester_genap_pg,
                    ((SELECT SUM(kdl.kinerja)
                    FROM vit_kesimpulan_kinerja_dosen_line kdl
                    LEFT JOIN vit_kesimpulan_kinerja_dosen kkd ON kdl.kesimpulan_id = kkd.id
                    LEFT JOIN vit_semester sm ON kkd.semester_id = sm.id
                    WHERE kkd.dosen_id = em.id AND kkd.state = 'done' AND sm.name = 'Genap' AND kdl.name = 'Pengabdian + Penunjang')
                    -
                    (SELECT SUM(kdl.kinerja)
                    FROM vit_kesimpulan_kinerja_dosen_line kdl
                    LEFT JOIN vit_kesimpulan_kinerja_dosen kkd ON kdl.kesimpulan_id = kkd.id
                    LEFT JOIN vit_semester sm ON kkd.semester_id = sm.id
                    WHERE kkd.dosen_id = em.id AND kkd.state = 'done' AND sm.name = 'Genap' AND kdl.name = 'Pengabdian'))
                    AS semester_genap_pk,
                    (CASE
                    WHEN 'Tidak memenuhi syarat UU' IN
                        ((SELECT kkd.kesimpulan_kinerja
                        FROM vit_kesimpulan_kinerja_dosen kkd
                        LEFT JOIN vit_semester sm ON kkd.semester_id = sm.id
                        WHERE kkd.dosen_id = em.id AND kkd.state = 'done' AND sm.name = 'Ganjil'),
                        (SELECT kkd.kesimpulan_kinerja
                        FROM vit_kesimpulan_kinerja_dosen kkd
                        LEFT JOIN vit_semester sm ON kkd.semester_id = sm.id
                        WHERE kkd.dosen_id = em.id AND kkd.state = 'done' AND sm.name = 'Genap'))
                    THEN 'Tidak memenuhi syarat UU'
                    ELSE 'Memenuhi syarat UU' END
                    )AS kesimpulan,
                    (CASE
                    WHEN 'Tidak memenuhi' IN
                        ((SELECT kkd.kesimpulan_khusus
                        FROM vit_kesimpulan_kinerja_dosen kkd
                        LEFT JOIN vit_semester sm ON kkd.semester_id = sm.id
                        WHERE kkd.dosen_id = em.id AND kkd.state = 'done' AND sm.name = 'Ganjil'),
                        (SELECT kkd.kesimpulan_khusus
                        FROM vit_kesimpulan_kinerja_dosen kkd
                        LEFT JOIN vit_semester sm ON kkd.semester_id = sm.id
                        WHERE kkd.dosen_id = em.id AND kkd.state = 'done' AND sm.name = 'Genap'))
                    THEN 'Tidak memenuhi'
                    ELSE 'Memenuhi' END
                    )AS kewajiban_khusus
                FROM vit_kesimpulan_kinerja_dosen kkd
                LEFT JOIN hr_employee em ON kkd.dosen_id = em.id
                LEFT JOIN vit_tahun_akademik ta ON kkd.tahun_akademik_id = ta.id
                WHERE ta.id = %s AND em.company_id = %s AND kkd.state = %s
                GROUP BY em.id
                """            
            self.env.cr.execute(sql, (self.id, 'done', self.tahun_akademik_id.id, self.institusi_id.id, 'done'))
        
