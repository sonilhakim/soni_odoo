#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft','Draft'),('open','Verifikasi'), ('done','Disahkan')]
from odoo import models, fields, api, _
import time
from datetime import datetime, timedelta
import dateutil.parser
import pytz
from odoo.exceptions import UserError, Warning

class rekap_unit(models.Model):

    _name = "vit.rekap_unit"
    _description = "vit.rekap_unit"

    name              = fields.Char( required=True, default="Baru", readonly=True,  string="Name",  help="")
    description       = fields.Char( string="Description",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    date              = fields.Date( string="Tanggal",  readonly=True, states={"draft" : [("readonly",False)]}, default=lambda self:time.strftime("%Y-%m-%d"), help="")
    state             = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",  help="")
    total             = fields.Float('Total Anggaran', compute='_total_anggaran', store=True)


    tahun_id          = fields.Many2one(comodel_name="account.fiscal.year",  string="Tahun", required=True, readonly=True, states={"draft" : [("readonly",False)]},  help="")
    periode_id        = fields.Many2one(comodel_name="account.period",  string="Periode", required=False, readonly=True, states={"draft" : [("readonly",False)]},  help="")
    anggaran_unit_ids = fields.One2many(comodel_name="vit.anggaran_unit",  inverse_name="rekap_unit_id",  string="Anggaran unit",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    ttd_id            = fields.Many2one(comodel_name="hr.employee",  string="Penandatangan", states={"lock" : [("readonly",True)]}, help="")
    pos_ttd           = fields.Char(string="Posisi Penandatangan", states={"lock" : [("readonly",True)]}, help="")

    @api.depends('anggaran_unit_ids')
    def _total_anggaran(self):
        total = []
        for ru in self:
            for keg in ru.anggaran_unit_ids:
                total.append(keg.anggaran)
            ru.total = sum(total)

    @api.model
    def create(self, vals):
        if not vals.get("name", False) or vals["name"] == "New":
            vals["name"] = self.env["ir.sequence"].next_by_code("vit.rekap_unit") or "Error Number!!!"
        return super(rekap_unit, self).create(vals)

    def action_confirm(self):
        self.state = STATES[1][0]

    def action_done(self):
        self.state = STATES[2][0]

    def action_draft(self):
        self.state = STATES[0][0]

    @api.multi
    def unlink(self):
        for me_id in self :
            if me_id.state != STATES[0][0]:
                raise UserError("Cannot delete non draft record!")
        return super(rekap_unit, self).unlink()

    @api.multi
    def action_reload(self, ):
        sql = "delete from vit_anggaran_unit where rekap_unit_id = %s"
        self.env.cr.execute(sql, (self.id,))
        # sql = """
        #         insert into vit_anggaran_unit (unit_id, alokasi, anggaran, realisasi, sisa, definitif, rekap_unit_id)
        #         select uk.id, ang.alokasi, ang.anggaran, ang.realisasi, ang.sisa, ang.definitif, %s
        #         from anggaran_rka ang
        #         left join vit_unit_kerja uk on ang.unit_id = uk.id
        #         where ang.anggaran != 0 and ang.state != 'cancel'
        #         """
        # if self.tahun_id:
        #     sql += " and ang.tahun = '%s' " %self.tahun_id.id
        # if self.periode_id:
        #     sql += ' and ang.period_id = %s ' %self.periode_id.id

        # self.env.cr.execute(sql, (self.id,))

        for ru in self:
            au = ru.env['vit.anggaran_unit']
            data = {}
            anggaran_rka = ru.env['anggaran.rka'].search([('tahun','=',ru.tahun_id.id),('state','!=','cancel')])
            for rka in anggaran_rka:                
                data = {
                    'rka_id'        : rka.id,
                    'unit_id'       : rka.unit_id.id,
                    'alokasi'       : rka.alokasi ,
                    'anggaran'      : rka.anggaran,
                    'realisasi'     : rka.realisasi,
                    'sisa'          : rka.sisa,
                    'definitif'     : rka.definitif, 
                    'rekap_unit_id' : ru.id,
                }
                au.create(data)

    @api.multi
    def print_rka(self):
        return self.env.ref('vit_rekap_anggaran.report_rka_uni').report_action(self)
    @api.multi
    def print_rka_detail(self):
        return self.env.ref('vit_rekap_anggaran.report_rka_uni_detail').report_action(self)

    @api.multi
    def get_current_date(self):
        date = ''
        for ra in self:
            now = datetime.now()
            user = ra.env['res.users'].browse(ra.env.uid)
            tz   = pytz.timezone(user.tz) or pytz.utc
            date_new = pytz.utc.localize(now).astimezone(tz)
            tgl    = datetime.strftime(date_new, '%d')
            bln    = datetime.strftime(date_new, '%m')
            thn    = datetime.strftime(date_new, '%Y')
            b = ''
            if bln == '01':
                b = 'Januari'
            if bln == '02':
                b = 'Februari'
            if bln == '03':
                b = 'Maret'
            if bln == '04':
                b = 'April'
            if bln == '05':
                b = 'Mei'
            if bln == '06':
                b = 'Juni'
            if bln == '07':
                b = 'Juli'
            if bln == '08':
                b = 'Agustus'
            if bln == '09':
                b = 'September'
            if bln == '10':
                b = 'Oktober'
            if bln == '11':
                b = 'November'
            if bln == '12':
                b = 'Desember'
            date = str(tgl) +" "+ b +" "+ str(thn)
        return date
