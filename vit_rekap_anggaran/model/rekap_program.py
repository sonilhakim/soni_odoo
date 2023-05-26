#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft','Draft'),('open','Verifikasi'), ('done','Disahkan')]
from odoo import models, fields, api, _
import time
import datetime
from odoo.exceptions import UserError, Warning

class rekap_program(models.Model):

    _name = "vit.rekap_program"
    _description = "vit.rekap_program"
    name = fields.Char( required=True, default="Baru", readonly=True,  string="Name",  help="")
    description = fields.Char( string="Description",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    date = fields.Date( string="Tanggal",  readonly=True, states={"draft" : [("readonly",False)]}, default=lambda self:time.strftime("%Y-%m-%d"), help="")
    state = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",  help="")


    tahun_id = fields.Many2one(comodel_name="account.fiscal.year", required=True, string="Tahun",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    periode_id = fields.Many2one(comodel_name="account.period", required=True, string="Periode",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    unit_id = fields.Many2one(comodel_name="vit.unit_kerja", required=True, string="Unit",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    program_line_ids = fields.One2many(comodel_name="vit.rekap_program_line",  inverse_name="program_rekap_id",  string="Anggaran program",  readonly=True, states={"draft" : [("readonly",False)]},  help="")

    @api.model
    def create(self, vals):
        if not vals.get("name", False) or vals["name"] == "New":
            vals["name"] = self.env["ir.sequence"].next_by_code("vit.rekap_program") or "Error Number!!!"
        return super(rekap_program, self).create(vals)

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
        return super(rekap_program, self).unlink()

    @api.multi
    def action_reload(self, ):
        sql = "delete from vit_rekap_program_line where program_rekap_id = %s"
        self.env.cr.execute(sql, (self.id,))
        sql = """
                insert into vit_rekap_program_line (category_id, anggaran, realisasi, sisa, program_rekap_id)
                select cat.id, sum(rkg.anggaran), sum(rkg.realisasi), sum(rkg.sisa), %s
                from anggaran_rka ang
                left join anggaran_rka_kegiatan rkg on rkg.rka_id = ang.id
                left join anggaran_category cat on rkg.category_id = cat.id
                left join account_fiscal_year fy on ang.tahun = fy.id
                left join account_period per on ang.period_id = per.id
                left join vit_unit_kerja uk on ang.unit_id = uk.id
                where rkg.anggaran != 0 and fy.id = %s and per.id = %s and uk.id = %s
                group by cat.id
                """
        self.env.cr.execute(sql, (self.id,self.tahun_id.id,self.periode_id.id,self.unit_id.id))
        
class rekap_program_line(models.Model):

    _name = "vit.rekap_program_line"
    _description = "vit.rekap_program_line"
    anggaran = fields.Float( string="Anggaran",  help="")
    realisasi = fields.Float( string="Realisasi",  help="")
    sisa = fields.Float( string="Sisa",  help="")
    category_id = fields.Many2one(comodel_name='anggaran.category', string="Program" )
    program_rekap_id = fields.Many2one(comodel_name="vit.rekap_program",  string="Rekap program",  help="")

