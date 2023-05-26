#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft','Draft'),('open','Diperiksa'),('done','Selesai'),('reject','Ditolak')]
from odoo import models, fields, api, _
import time
from datetime import date
from datetime import datetime
from datetime import timedelta
from dateutil import relativedelta
import calendar
import pytz
from odoo.exceptions import UserError, Warning

class MonitoringSkp(models.Model):

    _name = "vit.monitoring_skp"
    _description = "vit.monitoring_skp"
    name = fields.Char( required=True, default="Baru", readonly=True,  string="Name",  help="")
    state = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",  help="")
    tanggal = fields.Date( string="Tanggal",  readonly=True, states={"draft" : [("readonly",False)]}, default=lambda self:time.strftime("%Y-%m-%d"), help="")
    
    def action_print_pengukuran(self, ):
        pass


    def action_print_penilaian(self, ):
        pass


    def action_print_skp(self, ):
        pass


    def action_hitung_rekapitulasi(self, ):
        pass

    fakultas_id = fields.Many2one(comodel_name="vit.fakultas",  string="Fakultas",  help="")
    jurusan_id = fields.Many2one(comodel_name="vit.jurusan",  string="Jurusan",  help="")
    prodi_id = fields.Many2one(comodel_name="vit.program_studi",  string="Prodi",  help="")
    unit_kerja_id = fields.Many2one( comodel_name="vit.unit_kerja", string="Unit Kerja",  help="")
    tahun_akademik_id = fields.Many2one(comodel_name="vit.tahun_akademik",  string="Tahun akademik",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    mon_details = fields.One2many(comodel_name="vit.monitoring_detail", inverse_name="monitoring_id",  string="Kegiatan Detail", help="")
    
    @api.model
    def create(self, vals):
        if not vals.get("name", False) or vals["name"] == "New":
            vals["name"] = self.env["ir.sequence"].next_by_code("vit.monitoring_skp") or "Error Number!!!"
        return super(MonitoringSkp, self).create(vals)

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
        return super(MonitoringSkp, self).unlink()

    @api.multi
    def action_reload(self, ):
        sql = "delete from vit_monitoring_detail where monitoring_id = %s"
        self.env.cr.execute(sql, (self.id,))
        sql = """
                insert into vit_monitoring_detail (pns_id, pns_nip, nilai_prestasi_kerja, monitoring_id)
                select emp.id, emp.nip, pen.nilai_prestasi_kerja, %s
                from vit_penilaian_skp pen
                left join vit_tahun_akademik tak on pen.tahun_akademik_id = tak.id
                left join hr_employee emp on pen.pns_id = emp.id
                left join vit_fakultas fak on emp.fakultas_id = fak.id
                left join vit_jurusan jur on emp.jurusan_id = jur.id
                left join vit_program_studi pro on emp.program_studi_id = pro.id
                left join vit_unit_kerja uk on emp.unit_kerja_id = uk.id
                where pen.tahun_akademik_id = %s
                """
        if self.fakultas_id:
            sql += ' and emp.fakultas_id = %s ' %self.fakultas_id.id
        if self.jurusan_id:
            sql += ' and emp.jurusan_id = %s ' %self.jurusan_id.id
        if self.prodi_id:
            sql += ' and emp.program_studi_id = %s ' %self.prodi_id.id
        if self.unit_kerja_id:
            sql += ' and emp.unit_kerja_id = %s ' %self.unit_kerja_id.id
            
        self.env.cr.execute(sql, (self.id,self.tahun_akademik_id.id,))

    @api.multi
    def compute_capaian(self):
        for rec in self.mon_details:
            if rec.nilai_prestasi_kerja <= 75:
                rec.capaian = 'belum'
            else:
                rec.capaian = 'sudah'

            rec.capaian_persen = rec.nilai_prestasi_kerja


class Monitordetail(models.Model):

    _name = "vit.monitoring_detail"
    _description = "vit.monitoring_detail"

    pns_id = fields.Many2one(comodel_name="hr.employee",  string="Pns",  help="")
    pns_nip = fields.Char( string="Pns nip", help="")
    nilai_prestasi_kerja = fields.Float('Nilai Prestasi Kerja')
    capaian = fields.Selection(string="Capaian Kinerja Pegawai", 
                            selection=[('sudah', 'Sudah Tercapai'), 
                                        ('belum', 'Belum Tercapai')
                                        ])
    capaian_persen = fields.Float( string="Capaian Kinerja (%)")

    monitoring_id = fields.Many2one( comodel_name="vit.monitoring_skp", string="Monitoring SKP")

    