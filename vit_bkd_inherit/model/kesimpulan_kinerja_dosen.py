#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft','Draft'),('open','Proses'),('done','Selesai'),('reject','Ditolak')]
from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class kesimpulan_kinerja_dosen(models.Model):
    _name = "vit.kesimpulan_kinerja_dosen"
    _inherit = ['vit.kesimpulan_kinerja_dosen','portal.mixin', 'mail.thread', 'mail.activity.mixin']

    @api.model
    def year_selection(self):
        year = 2000 # replace 2000 with your a start year
        year_list = []
        while year != 2100: # replace 2030 with your end year
            year_list.append((str(year), str(year)))
            year += 1
        return year_list 

    name = fields.Char( required=True, default="Baru", readonly=True,  string="Name",  help="")
    nip = fields.Char( string="Nip", related="dosen_id.nip", readonly=True, states={"draft" : [("readonly",True)]},  help="")
    status_dosen_id = fields.Many2one(comodel_name="vit.status_dosen", related="dosen_id.status_dosen_id", string="Status dosen",  readonly=True, states={"draft" : [("readonly",True)]},  help="")
    jabatan_fungsional_id = fields.Many2one(comodel_name="vit.jabatan", related='dosen_id.jabatanf_id', string="Jabatan fungsional",  readonly=True, states={"draft" : [("readonly",True)]}, store=True, help="")
    jabatan_fungsional_name = fields.Char(related="jabatan_fungsional_id.name", string="Nama Jabatan fungsional",  readonly=True, store=True, help="")
    semester_id = fields.Many2one(comodel_name="vit.semester",  string="Semester",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    kesimpulan_kinerja = fields.Char( string="Kesimpulan",  help="")
    kesimpulan_khusus = fields.Char( string="Kesimpulan",  help="")
    line_khusus_ids = fields.One2many(comodel_name="vit.kesimpulan_kewajiban_khusus_line",  inverse_name="kesimpulan_id",  string="Line Khusus",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    state = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",  help="")

    asesor1_id = fields.Many2one(comodel_name="hr.employee",  string="Asesor1",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    asesor2_id = fields.Many2one(comodel_name="hr.employee",  string="Asesor2",  readonly=True, states={"draft" : [("readonly",False)]},  help="")

    periode_dari = fields.Selection( selection="year_selection", string="Periode Tahun dari")
    periode_sampai = fields.Char(compute="compute_sampai", string="Periode Tahun sampai")

    @api.model
    def create(self, vals):
        if not vals.get("name", False) or vals["name"] == "New":
            vals["name"] = self.env["ir.sequence"].next_by_code("vit.kesimpulan_kinerja_dosen") or "Error Number!!!"
        return super(kesimpulan_kinerja_dosen, self).create(vals)

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
        return super(kesimpulan_kinerja_dosen, self).unlink()

    @api.depends("periode_dari")
    def compute_sampai(self):
        if self.periode_dari:
            periode_sampai = int(self.periode_dari) + 2

            self.periode_sampai = str(periode_sampai)

    @api.multi
    def action_reload(self, ):
        sql = "delete from vit_kesimpulan_kinerja_dosen_line where kesimpulan_id = %s"
        self.env.cr.execute(sql, (self.id,))
        sql = "delete from vit_kesimpulan_kewajiban_khusus_line where kesimpulan_id = %s"
        self.env.cr.execute(sql, (self.id,))
        if not self.tahun_akademik_id or not self.dosen_id:
            raise UserError(_("Tahun Akademik dan nama dosen harus diisi") )
        else:
            sql = """
                UPDATE vit_kesimpulan_kinerja_dosen kd SET asesor1_id = em1.id, asesor2_id = em2.id, periode_dari = bkd.periode_dari
                FROM vit_bkd bkd
                LEFT JOIN hr_employee em1 ON bkd.asesor1_id = em1.id
                LEFT JOIN hr_employee em2 ON bkd.asesor2_id = em2.id
                WHERE kd.id = %s AND bkd.tahun_akademik_id = %s AND bkd.employee_id = %s AND bkd.status_dosen_id = %s AND bkd.semester_id = %s AND bkd.state = %s
                """
            cr=self.env.cr
            cr.execute(sql, ( self.id, self.tahun_akademik_id.id, self.dosen_id.id, self.status_dosen_id.id, self.semester_id.id, 'done'))
            # sql = """
            #     INSERT into vit_kesimpulan_kinerja_dosen_line (name, kesimpulan_id, kinerja)                
            #     SELECT em.name, %s,
            #         ( 
            #         (SELECT SUM(pd.kinerja_sks)
            #         FROM vit_kinerja_bidang_pendidikan pd
            #         LEFT JOIN vit_bkd bkd ON pd.bkd_id = bkd.id
            #         WHERE bkd.employee_id = em.id)
            #         +
            #         (SELECT SUM(pl.kinerja_sks)
            #         FROM vit_kinerja_bidang_penelitian pl
            #         LEFT JOIN vit_bkd bkd ON pl.bkd_id = bkd.id
            #         WHERE bkd.employee_id = em.id)
            #         +
            #         (SELECT SUM(pb.kinerja_sks)
            #         FROM vit_kinerja_bidang_pengabdian pb
            #         LEFT JOIN vit_bkd bkd ON pb.bkd_id = bkd.id
            #         WHERE bkd.employee_id = em.id)
            #         +
            #         (SELECT SUM(pk.kinerja_sks)
            #         FROM vit_kinerja_kewajiban_khusus pk
            #         LEFT JOIN vit_bkd bkd ON pk.bkd_id = bkd.id
            #         WHERE bkd.employee_id = em.id)
            #         ) AS kinerja                     
            #     FROM vit_bkd bkd
            #     LEFT JOIN hr_employee em ON bkd.employee_id = em.id
            #     WHERE bkd.tahun_akademik_id = %s AND bkd.employee_id = %s AND bkd.state = %s
            #     GROUP BY em.id
            #     """            
            # self.env.cr.execute(sql, (self.id, self.tahun_akademik_id.id, self.dosen_id.id, 'done'))
            
            sql = """
                INSERT into vit_kesimpulan_kinerja_dosen_line (name, syarat, kinerja, kesimpulan_id, kesimpulan)
                SELECT %s, sy.name, SUM(pd.kinerja_sks), %s,
                    (CASE WHEN SUM(pd.kinerja_sks) >= sy.min_sks
                     THEN 'Memenuhi'
                     ELSE 'Tidak memenuhi' 
                     END) AS kesimpulan
                FROM vit_bkd bkd                
                LEFT JOIN hr_employee em ON bkd.employee_id = em.id
                LEFT JOIN vit_kinerja_bidang_pendidikan pd ON pd.bkd_id = bkd.id
                LEFT JOIN vit_status_dosen sd ON bkd.status_dosen_id = sd.id
                LEFT JOIN vit_syarat_bkd sy ON sy.status_dosen_id = sd.id
                LEFT JOIN vit_semester sm ON bkd.semester_id = sm.id
                WHERE bkd.tahun_akademik_id = %s AND bkd.employee_id = %s AND bkd.status_dosen_id = %s AND bkd.semester_id = %s AND sy.pendidikan = %s AND bkd.state = %s
                GROUP BY em.id, sy.id
                """
            cr=self.env.cr
            cr.execute(sql, ('Pendidikan', self.id, self.tahun_akademik_id.id, self.dosen_id.id, self.status_dosen_id.id, self.semester_id.id, True, 'done'))
            
            sql1 = """
                INSERT into vit_kesimpulan_kinerja_dosen_line (name, syarat, kinerja, kesimpulan_id, kesimpulan)
                SELECT %s, sy.name, SUM(pl.kinerja_sks), %s,
                    (CASE WHEN SUM(pl.kinerja_sks) >= sy.min_sks
                     THEN 'Memenuhi'
                     ELSE 'Tidak memenuhi' 
                     END) AS kesimpulan
                FROM vit_bkd bkd                
                LEFT JOIN hr_employee em ON bkd.employee_id = em.id
                LEFT JOIN vit_kinerja_bidang_penelitian pl ON pl.bkd_id = bkd.id
                LEFT JOIN vit_status_dosen sd ON bkd.status_dosen_id = sd.id
                LEFT JOIN vit_syarat_bkd sy ON sy.status_dosen_id = sd.id
                LEFT JOIN vit_semester sm ON bkd.semester_id = sm.id
                WHERE bkd.tahun_akademik_id = %s AND bkd.employee_id = %s AND bkd.status_dosen_id = %s AND bkd.semester_id = %s AND sy.penelitian = %s AND bkd.state = %s
                GROUP BY em.id, sy.id
                """
            cr=self.env.cr
            cr.execute(sql1, ('Penelitian', self.id, self.tahun_akademik_id.id, self.dosen_id.id, self.status_dosen_id.id, self.semester_id.id, True, 'done'))

            sql2 = """
                INSERT into vit_kesimpulan_kinerja_dosen_line (name, syarat, kinerja, kesimpulan_id, kesimpulan)
                SELECT %s, sy.name, SUM(pb.kinerja_sks), %s,
                    (CASE WHEN SUM(pb.kinerja_sks) >= sy.min_sks
                     THEN 'Memenuhi'
                     ELSE 'Tidak memenuhi' 
                     END) AS kesimpulan
                FROM vit_bkd bkd                
                LEFT JOIN hr_employee em ON bkd.employee_id = em.id
                LEFT JOIN vit_kinerja_bidang_pengabdian pb ON pb.bkd_id = bkd.id
                LEFT JOIN vit_status_dosen sd ON bkd.status_dosen_id = sd.id
                LEFT JOIN vit_syarat_bkd sy ON sy.status_dosen_id = sd.id
                LEFT JOIN vit_semester sm ON bkd.semester_id = sm.id
                WHERE bkd.tahun_akademik_id = %s AND bkd.employee_id = %s AND bkd.status_dosen_id = %s AND bkd.semester_id = %s AND sy.pengabdian = %s AND bkd.state = %s
                GROUP BY em.id, sy.id
                """
            cr=self.env.cr
            cr.execute(sql2, ('Pengabdian', self.id, self.tahun_akademik_id.id, self.dosen_id.id, self.status_dosen_id.id, self.semester_id.id, True, 'done'))

            sql3 = """
                INSERT into vit_kesimpulan_kinerja_dosen_line (name, syarat, kinerja, kesimpulan, kesimpulan_id)
                SELECT %s, sy.name, 
                    (
                    (CASE WHEN 
                    (SELECT SUM(pd.kinerja_sks)
                    FROM vit_kinerja_bidang_pendidikan pd
                    LEFT JOIN vit_bkd bkd ON pd.bkd_id = bkd.id
                    WHERE bkd.employee_id = em.id AND bkd.tahun_akademik_id = ta.id AND bkd.semester_id = sm.id AND bkd.state = 'done')
                    IS NULL THEN 0 ELSE 
                    (SELECT SUM(pd.kinerja_sks)
                    FROM vit_kinerja_bidang_pendidikan pd
                    LEFT JOIN vit_bkd bkd ON pd.bkd_id = bkd.id
                    WHERE bkd.employee_id = em.id AND bkd.tahun_akademik_id = ta.id AND bkd.semester_id = sm.id AND bkd.state = 'done')
                    END)
                    + 
                    (CASE WHEN 
                    (SELECT SUM(pl.kinerja_sks)
                    FROM vit_kinerja_bidang_penelitian pl
                    LEFT JOIN vit_bkd bkd ON pl.bkd_id = bkd.id
                    WHERE bkd.employee_id = em.id AND bkd.tahun_akademik_id = ta.id AND bkd.semester_id = sm.id AND bkd.state = 'done')
                    IS NULL THEN 0 ELSE 
                    (SELECT SUM(pl.kinerja_sks)
                    FROM vit_kinerja_bidang_penelitian pl
                    LEFT JOIN vit_bkd bkd ON pl.bkd_id = bkd.id
                    WHERE bkd.employee_id = em.id AND bkd.tahun_akademik_id = ta.id AND bkd.semester_id = sm.id AND bkd.state = 'done') 
                    END)                    
                    ) AS kinerja,
                    (CASE WHEN (
                    (CASE WHEN 
                    (SELECT SUM(pd.kinerja_sks)
                    FROM vit_kinerja_bidang_pendidikan pd
                    LEFT JOIN vit_bkd bkd ON pd.bkd_id = bkd.id
                    WHERE bkd.employee_id = em.id AND bkd.tahun_akademik_id = ta.id AND bkd.semester_id = sm.id AND bkd.state = 'done')
                    IS NULL THEN 0 ELSE 
                    (SELECT SUM(pd.kinerja_sks)
                    FROM vit_kinerja_bidang_pendidikan pd
                    LEFT JOIN vit_bkd bkd ON pd.bkd_id = bkd.id
                    WHERE bkd.employee_id = em.id AND bkd.tahun_akademik_id = ta.id AND bkd.semester_id = sm.id AND bkd.state = 'done')
                    END)
                    + 
                    (CASE WHEN 
                    (SELECT SUM(pl.kinerja_sks)
                    FROM vit_kinerja_bidang_penelitian pl
                    LEFT JOIN vit_bkd bkd ON pl.bkd_id = bkd.id
                    WHERE bkd.employee_id = em.id AND bkd.tahun_akademik_id = ta.id AND bkd.semester_id = sm.id AND bkd.state = 'done')
                    IS NULL THEN 0 ELSE 
                    (SELECT SUM(pl.kinerja_sks)
                    FROM vit_kinerja_bidang_penelitian pl
                    LEFT JOIN vit_bkd bkd ON pl.bkd_id = bkd.id
                    WHERE bkd.employee_id = em.id AND bkd.tahun_akademik_id = ta.id AND bkd.semester_id = sm.id AND bkd.state = 'done') 
                    END)
                    ) >= sy.min_sks
                    THEN 'Memenuhi' ELSE 'Tidak memenuhi' END
                    ) AS kesimpulan,
                    %s
                FROM vit_bkd bkd                
                LEFT JOIN hr_employee em ON bkd.employee_id = em.id
                LEFT JOIN vit_tahun_akademik ta ON bkd.tahun_akademik_id = ta.id
                LEFT JOIN vit_semester sm ON bkd.semester_id = sm.id
                LEFT JOIN vit_status_dosen sd ON bkd.status_dosen_id = sd.id
                LEFT JOIN vit_syarat_bkd sy ON sy.status_dosen_id = sd.id
                WHERE ta.id = %s AND sm.id = %s AND em.id = %s AND sd.id = %s AND sy.pendidikan_penelitian = True AND bkd.state = 'done'
                GROUP BY em.id, sy.id, ta.id, sm.id
                """
            cr=self.env.cr
            cr.execute(sql3, ('Pendidikan + Penelitian', self.id, self.tahun_akademik_id.id, self.semester_id.id, self.dosen_id.id, self.status_dosen_id.id))

            sql4 = """
                INSERT into vit_kesimpulan_kinerja_dosen_line (name, syarat, kinerja, kesimpulan, kesimpulan_id)
                SELECT %s, sy.name, 
                    (
                    (CASE WHEN 
                    (SELECT SUM(pb.kinerja_sks)
                    FROM vit_kinerja_bidang_pengabdian pb
                    LEFT JOIN vit_bkd bkd ON pb.bkd_id = bkd.id
                    WHERE bkd.employee_id = em.id AND bkd.tahun_akademik_id = ta.id AND bkd.semester_id = sm.id AND bkd.state = 'done')
                    IS NULL THEN 0 ELSE 
                    (SELECT SUM(pb.kinerja_sks)
                    FROM vit_kinerja_bidang_pengabdian pb
                    LEFT JOIN vit_bkd bkd ON pb.bkd_id = bkd.id
                    WHERE bkd.employee_id = em.id AND bkd.tahun_akademik_id = ta.id AND bkd.semester_id = sm.id AND bkd.state = 'done') END)
                    + 
                    (CASE WHEN 
                    (SELECT SUM(pj.kinerja_sks)
                    FROM vit_kinerja_penunjang pj
                    LEFT JOIN vit_bkd bkd ON pj.bkd_id = bkd.id
                    WHERE bkd.employee_id = em.id AND bkd.tahun_akademik_id = ta.id AND bkd.semester_id = sm.id AND bkd.state = 'done')
                    IS NULL THEN 0 ELSE 
                    (SELECT SUM(pj.kinerja_sks)
                    FROM vit_kinerja_penunjang pj
                    LEFT JOIN vit_bkd bkd ON pj.bkd_id = bkd.id
                    WHERE bkd.employee_id = em.id AND bkd.tahun_akademik_id = ta.id AND bkd.semester_id = sm.id AND bkd.state = 'done') END)
                    ) AS kinerja,
                    (CASE WHEN (
                    (CASE WHEN (SELECT SUM(pb.kinerja_sks)
                    FROM vit_kinerja_bidang_pengabdian pb
                    LEFT JOIN vit_bkd bkd ON pb.bkd_id = bkd.id
                    WHERE bkd.employee_id = em.id AND bkd.tahun_akademik_id = ta.id AND bkd.semester_id = sm.id AND bkd.state = 'done')
                    IS NULL THEN 0 ELSE (SELECT SUM(pb.kinerja_sks)
                    FROM vit_kinerja_bidang_pengabdian pb
                    LEFT JOIN vit_bkd bkd ON pb.bkd_id = bkd.id
                    WHERE bkd.employee_id = em.id AND bkd.tahun_akademik_id = ta.id AND bkd.semester_id = sm.id AND bkd.state = 'done') END)
                    + 
                    (CASE WHEN (SELECT SUM(pj.kinerja_sks)
                    FROM vit_kinerja_penunjang pj
                    LEFT JOIN vit_bkd bkd ON pj.bkd_id = bkd.id
                    WHERE bkd.employee_id = em.id AND bkd.tahun_akademik_id = ta.id AND bkd.semester_id = sm.id AND bkd.state = 'done')
                    IS NULL THEN 0 ELSE (SELECT SUM(pj.kinerja_sks)
                    FROM vit_kinerja_penunjang pj
                    LEFT JOIN vit_bkd bkd ON pj.bkd_id = bkd.id
                    WHERE bkd.employee_id = em.id AND bkd.tahun_akademik_id = ta.id AND bkd.semester_id = sm.id AND bkd.state = 'done') END)
                    ) >= sy.min_sks
                    THEN 'Memenuhi' ELSE 'Tidak memenuhi' END
                    ) AS kesimpulan,
                    %s
                FROM vit_bkd bkd                
                LEFT JOIN hr_employee em ON bkd.employee_id = em.id
                LEFT JOIN vit_tahun_akademik ta ON bkd.tahun_akademik_id = ta.id
                LEFT JOIN vit_semester sm ON bkd.semester_id = sm.id
                LEFT JOIN vit_status_dosen sd ON bkd.status_dosen_id = sd.id
                LEFT JOIN vit_syarat_bkd sy ON sy.status_dosen_id = sd.id
                WHERE ta.id = %s AND sm.id = %s AND em.id = %s AND sd.id = %s AND sy.pengabdian_penunjang = True AND bkd.state = 'done'
                GROUP BY em.id, sy.id, ta.id,sm.id
                """
            cr=self.env.cr
            cr.execute(sql4, ('Pengabdian + Penunjang', self.id, self.tahun_akademik_id.id, self.semester_id.id, self.dosen_id.id, self.status_dosen_id.id))

            sql5 = """
                INSERT into vit_kesimpulan_kinerja_dosen_line (name, syarat, kinerja, kesimpulan, kesimpulan_id)
                SELECT %s, sy.name, 
                (
                    (CASE WHEN 
                        (SELECT SUM(pd.kinerja_sks)
                        FROM vit_kinerja_bidang_pendidikan pd
                        LEFT JOIN vit_bkd bkd ON pd.bkd_id = bkd.id
                        WHERE bkd.employee_id = em.id AND bkd.tahun_akademik_id = ta.id AND bkd.semester_id = sm.id AND bkd.state = 'done')
                        IS NULL THEN 0 ELSE 
                        (SELECT SUM(pd.kinerja_sks)
                        FROM vit_kinerja_bidang_pendidikan pd
                        LEFT JOIN vit_bkd bkd ON pd.bkd_id = bkd.id
                        WHERE bkd.employee_id = em.id AND bkd.tahun_akademik_id = ta.id AND bkd.semester_id = sm.id AND bkd.state = 'done')
                    END)
                    + 
                    (CASE WHEN 
                        (SELECT SUM(pl.kinerja_sks)
                        FROM vit_kinerja_bidang_penelitian pl
                        LEFT JOIN vit_bkd bkd ON pl.bkd_id = bkd.id
                        WHERE bkd.employee_id = em.id AND bkd.tahun_akademik_id = ta.id AND bkd.semester_id = sm.id AND bkd.state = 'done')
                        IS NULL THEN 0 ELSE 
                        (SELECT SUM(pl.kinerja_sks)
                        FROM vit_kinerja_bidang_penelitian pl
                        LEFT JOIN vit_bkd bkd ON pl.bkd_id = bkd.id
                        WHERE bkd.employee_id = em.id AND bkd.tahun_akademik_id = ta.id AND bkd.semester_id = sm.id AND bkd.state = 'done')
                    END)
                    +
                    (CASE WHEN 
                        (SELECT SUM(pb.kinerja_sks)
                        FROM vit_kinerja_bidang_pengabdian pb
                        LEFT JOIN vit_bkd bkd ON pb.bkd_id = bkd.id
                        WHERE bkd.employee_id = em.id AND bkd.tahun_akademik_id = ta.id AND bkd.semester_id = sm.id AND bkd.state = 'done')
                        IS NULL THEN 0 ELSE 
                        (SELECT SUM(pb.kinerja_sks)
                        FROM vit_kinerja_bidang_pengabdian pb
                        LEFT JOIN vit_bkd bkd ON pb.bkd_id = bkd.id
                        WHERE bkd.employee_id = em.id AND bkd.tahun_akademik_id = ta.id AND bkd.semester_id = sm.id AND bkd.state = 'done')
                    END)
                    + 
                    (CASE WHEN 
                        (SELECT SUM(pj.kinerja_sks)
                        FROM vit_kinerja_penunjang pj
                        LEFT JOIN vit_bkd bkd ON pj.bkd_id = bkd.id
                        WHERE bkd.employee_id = em.id AND bkd.tahun_akademik_id = ta.id AND bkd.semester_id = sm.id AND bkd.state = 'done')
                        IS NULL THEN 0 ELSE 
                        (SELECT SUM(pj.kinerja_sks)
                        FROM vit_kinerja_penunjang pj
                        LEFT JOIN vit_bkd bkd ON pj.bkd_id = bkd.id
                        WHERE bkd.employee_id = em.id AND bkd.tahun_akademik_id = ta.id AND bkd.semester_id = sm.id AND bkd.state = 'done') 
                    END)
                ) AS kinerja,
                (CASE WHEN 
                    (
                        (CASE WHEN 
                            (SELECT SUM(pd.kinerja_sks)
                            FROM vit_kinerja_bidang_pendidikan pd
                            LEFT JOIN vit_bkd bkd ON pd.bkd_id = bkd.id
                            WHERE bkd.employee_id = em.id AND bkd.tahun_akademik_id = ta.id AND bkd.semester_id = sm.id AND bkd.state = 'done')
                            IS NULL THEN 0 ELSE 
                            (SELECT SUM(pd.kinerja_sks)
                            FROM vit_kinerja_bidang_pendidikan pd
                            LEFT JOIN vit_bkd bkd ON pd.bkd_id = bkd.id
                            WHERE bkd.employee_id = em.id AND bkd.tahun_akademik_id = ta.id AND bkd.semester_id = sm.id AND bkd.state = 'done')
                        END)
                        + 
                        (CASE WHEN 
                            (SELECT SUM(pl.kinerja_sks)
                            FROM vit_kinerja_bidang_penelitian pl
                            LEFT JOIN vit_bkd bkd ON pl.bkd_id = bkd.id
                            WHERE bkd.employee_id = em.id AND bkd.tahun_akademik_id = ta.id AND bkd.semester_id = sm.id AND bkd.state = 'done')
                            IS NULL THEN 0 ELSE 
                            (SELECT SUM(pl.kinerja_sks)
                            FROM vit_kinerja_bidang_penelitian pl
                            LEFT JOIN vit_bkd bkd ON pl.bkd_id = bkd.id
                            WHERE bkd.employee_id = em.id AND bkd.tahun_akademik_id = ta.id AND bkd.semester_id = sm.id AND bkd.state = 'done') 
                        END)
                        +
                        (CASE WHEN 
                            (SELECT SUM(pb.kinerja_sks)
                            FROM vit_kinerja_bidang_pengabdian pb
                            LEFT JOIN vit_bkd bkd ON pb.bkd_id = bkd.id
                            WHERE bkd.employee_id = em.id AND bkd.tahun_akademik_id = ta.id AND bkd.semester_id = sm.id AND bkd.state = 'done')
                            IS NULL THEN 0 ELSE 
                            (SELECT SUM(pb.kinerja_sks)
                            FROM vit_kinerja_bidang_pengabdian pb
                            LEFT JOIN vit_bkd bkd ON pb.bkd_id = bkd.id
                            WHERE bkd.employee_id = em.id AND bkd.tahun_akademik_id = ta.id AND bkd.semester_id = sm.id AND bkd.state = 'done') 
                        END)
                        + 
                        (CASE WHEN 
                            (SELECT SUM(pj.kinerja_sks)
                            FROM vit_kinerja_penunjang pj
                            LEFT JOIN vit_bkd bkd ON pj.bkd_id = bkd.id
                            WHERE bkd.employee_id = em.id AND bkd.tahun_akademik_id = ta.id AND bkd.semester_id = sm.id AND bkd.state = 'done')
                            IS NULL THEN 0 ELSE 
                            (SELECT SUM(pj.kinerja_sks)
                            FROM vit_kinerja_penunjang pj
                            LEFT JOIN vit_bkd bkd ON pj.bkd_id = bkd.id
                            WHERE bkd.employee_id = em.id AND bkd.tahun_akademik_id = ta.id AND bkd.semester_id = sm.id AND bkd.state = 'done') 
                        END)
                    ) >= sy.min_sks
                    AND
                    (
                        (CASE WHEN 
                            (SELECT SUM(pd.kinerja_sks)
                            FROM vit_kinerja_bidang_pendidikan pd
                            LEFT JOIN vit_bkd bkd ON pd.bkd_id = bkd.id
                            WHERE bkd.employee_id = em.id AND bkd.tahun_akademik_id = ta.id AND bkd.semester_id = sm.id AND bkd.state = 'done')
                            IS NULL THEN 0 ELSE 
                            (SELECT SUM(pd.kinerja_sks)
                            FROM vit_kinerja_bidang_pendidikan pd
                            LEFT JOIN vit_bkd bkd ON pd.bkd_id = bkd.id
                            WHERE bkd.employee_id = em.id AND bkd.tahun_akademik_id = ta.id AND bkd.semester_id = sm.id AND bkd.state = 'done')
                        END)
                        + 
                        (CASE WHEN 
                            (SELECT SUM(pl.kinerja_sks)
                            FROM vit_kinerja_bidang_penelitian pl
                            LEFT JOIN vit_bkd bkd ON pl.bkd_id = bkd.id
                            WHERE bkd.employee_id = em.id AND bkd.tahun_akademik_id = ta.id AND bkd.semester_id = sm.id AND bkd.state = 'done')
                            IS NULL THEN 0 ELSE 
                            (SELECT SUM(pl.kinerja_sks)
                            FROM vit_kinerja_bidang_penelitian pl
                            LEFT JOIN vit_bkd bkd ON pl.bkd_id = bkd.id
                            WHERE bkd.employee_id = em.id AND bkd.tahun_akademik_id = ta.id AND bkd.semester_id = sm.id AND bkd.state = 'done') 
                        END)
                        +
                        (CASE WHEN 
                            (SELECT SUM(pb.kinerja_sks)
                            FROM vit_kinerja_bidang_pengabdian pb
                            LEFT JOIN vit_bkd bkd ON pb.bkd_id = bkd.id
                            WHERE bkd.employee_id = em.id AND bkd.tahun_akademik_id = ta.id AND bkd.semester_id = sm.id AND bkd.state = 'done')
                            IS NULL THEN 0 ELSE 
                            (SELECT SUM(pb.kinerja_sks)
                            FROM vit_kinerja_bidang_pengabdian pb
                            LEFT JOIN vit_bkd bkd ON pb.bkd_id = bkd.id
                            WHERE bkd.employee_id = em.id AND bkd.tahun_akademik_id = ta.id AND bkd.semester_id = sm.id AND bkd.state = 'done') 
                        END)
                        + 
                        (CASE WHEN 
                            (SELECT SUM(pj.kinerja_sks)
                            FROM vit_kinerja_penunjang pj
                            LEFT JOIN vit_bkd bkd ON pj.bkd_id = bkd.id
                            WHERE bkd.employee_id = em.id AND bkd.tahun_akademik_id = ta.id AND bkd.semester_id = sm.id AND bkd.state = 'done')
                            IS NULL THEN 0 ELSE 
                            (SELECT SUM(pj.kinerja_sks)
                            FROM vit_kinerja_penunjang pj
                            LEFT JOIN vit_bkd bkd ON pj.bkd_id = bkd.id
                            WHERE bkd.employee_id = em.id AND bkd.tahun_akademik_id = ta.id AND bkd.semester_id = sm.id AND bkd.state = 'done') 
                        END)
                    ) <= sy.max_sks
                    THEN 'Memenuhi' ELSE 'Tidak memenuhi' END
                ) AS kesimpulan,
                %s
                FROM vit_bkd bkd                
                LEFT JOIN hr_employee em ON bkd.employee_id = em.id
                LEFT JOIN vit_tahun_akademik ta ON bkd.tahun_akademik_id = ta.id
                LEFT JOIN vit_semester sm ON bkd.semester_id = sm.id
                LEFT JOIN vit_status_dosen sd ON bkd.status_dosen_id = sd.id
                LEFT JOIN vit_syarat_bkd sy ON sy.status_dosen_id = sd.id
                WHERE ta.id = %s AND sm.id = %s AND em.id = %s AND sd.id = %s AND sy.total_kinerja = True AND bkd.state = 'done'
                GROUP BY em.id, sy.id, ta.id, sm.id
                """
            cr=self.env.cr
            cr.execute(sql5, ('Total Kinerja', self.id, self.tahun_akademik_id.id, self.semester_id.id, self.dosen_id.id, self.status_dosen_id.id))
            
            sqlk = """
                INSERT into vit_kesimpulan_kewajiban_khusus_line (kewajiban_khusus_id, tahun, ceklist_asesor, kesimpulan_id)
                SELECT kk.id, kk.tahun, kk.ceklist_asesor, %s
                FROM vit_bkd bkd                
                LEFT JOIN hr_employee em ON bkd.employee_id = em.id
                LEFT JOIN vit_kinerja_kewajiban_khusus kk ON kk.bkd_id = bkd.id
                LEFT JOIN vit_status_dosen sd ON bkd.status_dosen_id = sd.id
                LEFT JOIN vit_semester sm ON bkd.semester_id = sm.id
                WHERE bkd.tahun_akademik_id = %s AND bkd.employee_id = %s AND bkd.status_dosen_id = %s AND bkd.semester_id = %s AND bkd.state = %s
                """
            cr=self.env.cr
            cr.execute(sqlk, ( self.id, self.tahun_akademik_id.id, self.dosen_id.id, self.status_dosen_id.id, self.semester_id.id, 'done'))
            
            kes = []
            for line in self.line_ids:                
                kes.append(line.kesimpulan)
                # import pdb; pdb.set_trace()
                if 'Tidak memenuhi' in kes:
                    self.kesimpulan_kinerja = 'Tidak memenuhi syarat UU'
                else:
                    self.kesimpulan_kinerja = 'Memenuhi syarat UU'

            kesk = []
            for lines in self.line_khusus_ids:                
                kesk.append(lines.ceklist_asesor)
                # import pdb; pdb.set_trace()
                if 'tidak_memenuhi' in kesk:
                    self.kesimpulan_khusus = 'Tidak memenuhi'
                else:
                    self.kesimpulan_khusus = 'Memenuhi'