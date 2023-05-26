#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft','Draft'),('open','Verifikasi'), ('done','Disahkan')]
from odoo import models, fields, api, _
import time
import datetime
from odoo.exceptions import UserError, Warning

class rekapitulasi_anggaran_program_dan_kegiatan_unit(models.Model):

    _name = "vit.rekapitulasi_anggaran_program_dan_kegiatan_unit"
    _description = "vit.rekapitulasi_anggaran_program_dan_kegiatan_unit"
    name = fields.Char( required=True, default="Baru", readonly=True,  string="Name",  help="")
    description = fields.Char( string="Description",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    date = fields.Date( string="Tanggal",  readonly=True, states={"draft" : [("readonly",False)]}, default=lambda self:time.strftime("%Y-%m-%d"), help="")
    state = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",  help="")


    tahun_id = fields.Many2one(comodel_name="account.fiscal.year",  string="Tahun", required=True, readonly=True, states={"draft" : [("readonly",False)]},  help="")
    periode_id = fields.Many2one(comodel_name="account.period",  string="Periode", required=False, readonly=True, states={"draft" : [("readonly",False)]},  help="")
    unit_id = fields.Many2one(comodel_name="vit.unit_kerja",  string="SUBSATKER", required=True, readonly=True, states={"draft" : [("readonly",False)]},  help="")
    program_id = fields.Many2one(comodel_name="anggaran.program",  string="Program", required=False, readonly=True, states={"draft" : [("readonly",False)]},  help="")
    anggaran_ids = fields.One2many(comodel_name="vit.anggaran_detail",  inverse_name="rekapitulasi_id",  string="Anggaran",  readonly=True, states={"draft" : [("readonly",False)]},  help="")

    @api.model
    def create(self, vals):
        if not vals.get("name", False) or vals["name"] == "New":
            vals["name"] = self.env["ir.sequence"].next_by_code("vit.rekapitulasi_anggaran_program_dan_kegiatan_unit") or "Error Number!!!"
        return super(rekapitulasi_anggaran_program_dan_kegiatan_unit, self).create(vals)

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
        return super(rekapitulasi_anggaran_program_dan_kegiatan_unit, self).unlink()

    @api.multi
    def action_reload(self, ):
        sql = "delete from vit_anggaran_detail where rekapitulasi_id = %s"
        self.env.cr.execute(sql, (self.id,))
        # sql = """
        #         insert into vit_anggaran_detail (kegiatan_id, target_capaian, satuan_target, anggaran, realisasi, sisa, definitif, rekapitulasi_id)
        #         select keg.id, rkg.target_capaian, u.id, rkg.anggaran, rkg.realisasi, rkg.sisa, rkg.definitif, %s
        #         from anggaran_rka ang
        #         left join anggaran_rka_kegiatan rkg on rkg.rka_id = ang.id
        #         left join anggaran_kegiatan keg on rkg.kegiatan_id = keg.id
        #         left join anggaran_program prg on rkg.program_id = prg.id
        #         left join uom_uom u on rkg.target_capaian_uom = u.id
        #         left join account_fiscal_year fy on ang.tahun = fy.id
        #         left join account_period per on ang.period_id = per.id
        #         left join vit_unit_kerja uk on ang.unit_id = uk.id
        #         where rkg.anggaran != 0
        #         """
        # if self.tahun_id:
        #     sql += " and fy.id = '%s' " %self.tahun_id.id
        # if self.periode_id:
        #     sql += ' and per.id = %s ' %self.periode_id.id
        # if self.unit_id:
        #     sql += ' and uk.id = %s ' %self.unit_id.id
        # if self.program_id:
        #     sql += ' and keg.program_id = %s ' %self.program_id.id

        # self.env.cr.execute(sql, (self.id,))

        for rap in self:
            ap = rap.env['vit.anggaran_detail']
            # anggaran = []
            data = {}
            anggaran_rka = rap.env['anggaran.rka'].search([('tahun','=',rap.tahun_id.id),('unit_id','=',rap.unit_id.id)])
            for rka in anggaran_rka:
                anggaran_rka_kegiatan = rka.env['anggaran.rka_kegiatan'].search([('rka_id','=',rka.id),('anggaran','!=',0)])
                for ark in anggaran_rka_kegiatan :

                    data = {
                        'kegiatan'        : ark.indikator,
                        'target_capaian'  : ark.target_capaian ,
                        'satuan_target'   : ark.target_capaian_uom,
                        'anggaran'        : ark.anggaran,
                        'realisasi'       : ark.realisasi,
                        'sisa'            : ark.sisa,
                        'definitif'       : ark.definitif, 
                        'rekapitulasi_id': rap.id,
                    }
                    ap.create(data)
