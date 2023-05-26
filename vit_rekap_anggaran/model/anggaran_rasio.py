#!/usr/bin/python
#-*- coding: utf-8 -*-
from odoo import models, fields, api, _
import time
from datetime import datetime, timedelta
import dateutil.parser
import pytz
from odoo.exceptions import UserError, Warning

STATES = [('draft','Draft'),('open','Verifikasi'), ('reject','Ditolak'), ('done','Disetujui')]

class anggaran_rasio(models.Model):

    _name = "vit.anggaran_rasio"
    _description = "vit.anggaran_rasio"

    name              = fields.Char( required=True, default="Baru", readonly=True,  string="Name",  help="")
    date              = fields.Date( string="Tanggal Dokumen",  readonly=True, states={"draft" : [("readonly",False)]}, default=lambda self:time.strftime("%Y-%m-%d"), help="")
    state             = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",  help="")

    tahun_id          = fields.Many2one(comodel_name="account.fiscal.year",  string="Tahun", required=True, readonly=True, states={"draft" : [("readonly",False)]},  help="")
    rasio_line_ids    = fields.One2many(comodel_name="vit.anggaran_rasio_line",  inverse_name="anggaran_rasio_id",  string="Rasio Anggaran",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    # ttd_id            = fields.Many2one(comodel_name="hr.employee",  string="Penandatangan", states={"lock" : [("readonly",True)]}, help="")
    # pos_ttd           = fields.Char(string="Posisi Penandatangan", states={"lock" : [("readonly",True)]}, help="")

    
    @api.model
    def create(self, vals):
        if not vals.get("name", False) or vals["name"] == "New":
            vals["name"] = self.env["ir.sequence"].next_by_code("vit.anggaran_rasio") or "Error Number!!!"
        return super(anggaran_rasio, self).create(vals)

    def action_confirm(self):
        self.state = STATES[1][0]

    def action_reject(self):
        self.state = STATES[2][0]

    def action_done(self):
        self.state = STATES[3][0]

    def action_draft(self):
        self.state = STATES[0][0]

    @api.multi
    def unlink(self):
        for me_id in self :
            if me_id.state != STATES[0][0]:
                raise UserError("Cannot delete non draft record!")
        return super(anggaran_rasio, self).unlink()

    @api.multi
    def action_reload(self, ):
        sql = "delete from vit_anggaran_rasio_line where anggaran_rasio_id = %s"
        self.env.cr.execute(sql, (self.id,))
        
        for rs in self:            
            lines = rs.env['vit.anggaran_rasio_line']
            data = {}
            anggaran_rka = rs.env['anggaran.rka'].search([('tahun','=',rs.tahun_id.id),('state','=','done')])
            for rka in anggaran_rka:
                anggaran_rka_lalu = rs.env['anggaran.rka'].search([('unit_id','=',rka.unit_id.id),('tahun','=',(rka.tahun.id - 1)),('state','in',('done','lock'))])
                real_lalu = 0.0
                for rka_l in anggaran_rka_lalu:
                    real_lalu =  rka_l.realisasi
                if real_lalu != 0.0:
                    data = {
                        'unit_id'       : rka.unit_id.id,
                        'realisasi_ini' : rka.realisasi,
                        'realisasi_lalu': real_lalu,
                        'pertumbuhan_rp': rka.realisasi - real_lalu,
                        'pertumbuhan_persen': ((rka.realisasi - real_lalu)/real_lalu)*100,
                        'anggaran_rasio_id' : rs.id,
                    }
                else:
                    data = {
                        'unit_id'       : rka.unit_id.id,
                        'realisasi_ini' : rka.realisasi,
                        'realisasi_lalu': 0,
                        'pertumbuhan_rp': rka.realisasi,
                        'pertumbuhan_persen': 0,
                        'anggaran_rasio_id' : rs.id,
                    }
                lines.create(data)

    # @api.multi
    # def print_rka(self):
    #     return self.env.ref('vit_rekap_anggaran.report_rka_uni').report_action(self)
    # @api.multi
    # def print_rka_detail(self):
    #     return self.env.ref('vit_rekap_anggaran.report_rka_uni_detail').report_action(self)

    # @api.multi
    # def get_current_date(self):
    #     date = ''
    #     for ra in self:
    #         now = datetime.now()
    #         user = ra.env['res.users'].browse(ra.env.uid)
    #         tz   = pytz.timezone(user.tz) or pytz.utc
    #         date_new = pytz.utc.localize(now).astimezone(tz)
    #         tgl    = datetime.strftime(date_new, '%d')
    #         bln    = datetime.strftime(date_new, '%m')
    #         thn    = datetime.strftime(date_new, '%Y')
    #         b = ''
    #         if bln == '01':
    #             b = 'Januari'
    #         if bln == '02':
    #             b = 'Februari'
    #         if bln == '03':
    #             b = 'Maret'
    #         if bln == '04':
    #             b = 'April'
    #         if bln == '05':
    #             b = 'Mei'
    #         if bln == '06':
    #             b = 'Juni'
    #         if bln == '07':
    #             b = 'Juli'
    #         if bln == '08':
    #             b = 'Agustus'
    #         if bln == '09':
    #             b = 'September'
    #         if bln == '10':
    #             b = 'Oktober'
    #         if bln == '11':
    #             b = 'November'
    #         if bln == '12':
    #             b = 'Desember'
    #         date = str(tgl) +" "+ b +" "+ str(thn)
    #     return date


class anggaran_rasio_line(models.Model):

    _name = "vit.anggaran_rasio_line"
    _description = "vit.anggaran_rasio_line"
    
    realisasi_ini = fields.Float( string="Realisasi Tahun ini",  help="")
    realisasi_lalu = fields.Float( string="Realisasi Tahun lalu",  help="")
    pertumbuhan_rp = fields.Float( string="Pertumbuhan (Rp)",  help="")
    pertumbuhan_persen = fields.Float( string="Pertumbuhan (%)",  help="")


    unit_id = fields.Many2one(comodel_name="vit.unit_kerja",  string="SUBSATKER",  help="")
    # rka_id = fields.Many2one(comodel_name="anggaran.rka",  string="RKA",  help="")
    anggaran_rasio_id = anggaran_rasio_id = fields.Many2one(comodel_name="vit.anggaran_rasio",  string="Anggaran Rasio",  help="")
