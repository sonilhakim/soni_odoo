#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft','Draft'),('open','Verifikasi'), ('done','Disahkan')]
from odoo import models, fields, api, _
import time
import datetime
from odoo.exceptions import UserError, Warning

class rekap_anggaran_program(models.Model):

    _name = "vit.rekap_anggaran_program"
    _description = "vit.rekap_anggaran_program"
    name = fields.Char( required=True, default="Baru", readonly=True,  string="Name",  help="")
    description = fields.Char( string="Description",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    date = fields.Date( string="Tanggal",  readonly=True, states={"draft" : [("readonly",False)]}, default=lambda self:time.strftime("%Y-%m-%d"), help="")
    state = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",  help="")


    tahun_id = fields.Many2one(comodel_name="account.fiscal.year", required=True, string="Tahun",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    periode_id = fields.Many2one(comodel_name="account.period", required=True, string="Periode",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    unit_id = fields.Many2one(comodel_name="vit.unit_kerja", required=True, string="Unit",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    anggaran_program_ids = fields.One2many(comodel_name="vit.anggaran_program",  inverse_name="rekap_anggaran_id",  string="Anggaran line",  readonly=True, states={"draft" : [("readonly",False)]},  help="")

    @api.model
    def create(self, vals):
        if not vals.get("name", False) or vals["name"] == "New":
            vals["name"] = self.env["ir.sequence"].next_by_code("vit.rekap_anggaran_program") or "Error Number!!!"
        return super(rekap_anggaran_program, self).create(vals)

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
        return super(rekap_anggaran_program, self).unlink()

    @api.multi
    def action_reload(self, ):
        sql = "delete from vit_anggaran_program where rekap_anggaran_id = %s"
        self.env.cr.execute(sql, (self.id,))
        sql = """
                insert into vit_anggaran_program (indikator, target_capaian, satuan_target, anggaran, realisasi, sisa, definitif, rekap_anggaran_id)
                select rkg.indikator, rkg.target_capaian, rkg.target_capaian_uom, rkg.anggaran, rkg.realisasi, rkg.sisa, rkg.definitif, %s
                from anggaran_rka ang
                left join anggaran_rka_kegiatan rkg on rkg.rka_id = ang.id
                left join account_fiscal_year fy on ang.tahun = fy.id
                left join account_period per on ang.period_id = per.id
                left join vit_unit_kerja uk on ang.unit_id = uk.id
                where rkg.anggaran != 0
                """
        if self.tahun_id:
            sql += " and fy.id = '%s' " %self.tahun_id.id
        if self.periode_id:
            sql += ' and per.id = %s ' %self.periode_id.id
        if self.unit_id:
            sql += ' and uk.id = %s ' %self.unit_id.id

        self.env.cr.execute(sql, (self.id,))
        # for rap in self:
        #     ap = rap.env['vit.anggaran_program']
            # anggaran = []
            # data = {}
            # anggaran_rka = rap.env['anggaran.rka'].search([('tahun','=',rap.tahun_id.id),('period_id','=',rap.periode_id.id),('unit_id','=',rap.unit_id.id)])
            # for rka in anggaran_rka:
            #     anggaran_rka_kegiatan = rka.env['anggaran.rka_kegiatan'].search([('rka_id','=',rka.id),('anggaran','!=',0)])
            #     for ark in anggaran_rka_kegiatan :

            #         data = {
            #             'program_id'      : ark.category_id.id,
            #             'target_capaian'  : ark.target_capaian ,
            #             'satuan_target'   : ark.target_capaian_uom,
            #             'anggaran'        : ark.anggaran,
            #             'realisasi'       : ark.realisasi,
            #             'sisa'            : ark.sisa,
            #             'definitif'       : ark.definitif, 
            #             'rekap_program_id': rap.id,
            #         }
            #         ap.create(data)
