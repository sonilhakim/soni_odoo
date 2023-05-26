#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft','Draft'),('open','Diperiksa'),('done','Disetujui')]
from odoo import models, fields, api, _
import time
import datetime
from odoo.exceptions import UserError, Warning

class pbkd(models.Model):

    _name = "vit.permintaan_bkd"
    _description = "vit.permintaan_bkd"
    name = fields.Char( required=True, default="New", readonly=True,  string="Name",  help="")
    date = fields.Date( string="Date",  readonly=True, states={"draft" : [("readonly",False)]}, default=lambda self:time.strftime("%Y-%m-%d"), help="")    
    state = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",  help="")
    
    tahun_akademik_id = fields.Many2one(comodel_name="vit.tahun_akademik",  string="Tahun akademik",  readonly=True, states={"draft" : [("readonly",False)]},  help="")    
    fakultas_id = fields.Many2one(comodel_name="vit.fakultas",  string="Fakultas",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    jurusan_id = fields.Many2one(comodel_name="vit.jurusan",  string="Jurusan",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    program_studi_id = fields.Many2one(comodel_name="vit.program_studi",  string="Program studi",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    
    perm_details = fields.One2many(comodel_name="vit.permintaan_detail", inverse_name="perm_bkd_id",  string="Permintaan BKD Detail", help="")

    @api.model
    def create(self, vals):
        if not vals.get("name", False) or vals["name"] == "New":
            vals["name"] = self.env["ir.sequence"].next_by_code("vit.permintaan_bkd") or "Error Number!!!"
        return super(pbkd, self).create(vals)

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
        return super(pbkd, self).unlink()

    def action_reload(self, ):
        sql = "delete from vit_permintaan_detail where perm_bkd_id = %s"
        self.env.cr.execute(sql, (self.id,))
        sql = """
                insert into vit_permintaan_detail (bkd_id, date, employee_id, nip, nidn, bidang_ilmu, semester_id, status_dosen_id, state, perm_bkd_id)
                select bkd.id, bkd.date, bkd.employee_id, bkd.nip, bkd.nidn, bkd.bidang_ilmu, bkd.semester_id, bkd.status_dosen_id, bkd.state, %s
                from vit_bkd bkd
                where 1=1
                """
        if self.tahun_akademik_id:
            sql += ' and bkd.tahun_akademik_id = %s ' %self.tahun_akademik_id.id
        if self.fakultas_id:
            sql += ' and bkd.fakultas_id = %s ' %self.fakultas_id.id
        if self.jurusan_id:
            sql += ' and bkd.jurusan_id = %s ' %self.jurusan_id.id
        if self.program_studi_id:
            sql += ' and bkd.program_studi_id = %s ' %self.program_studi_id.id
            
        self.env.cr.execute(sql, (self.id,))


class permintaanbkd(models.Model):

    _name = "vit.permintaan_detail"
    _description = "vit.permintaan_detail"

    _rec_name = "bkd_id"

    bkd_id = fields.Many2one( comodel_name="vit.bkd", required=True, string="BKD",  help="")
    date = fields.Date( string="Date",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    nip = fields.Char( string="Nip",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    nidn = fields.Char( string="Nidn",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    bidang_ilmu = fields.Char( string="Bidang ilmu",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
   
    state = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",  help="")

    perm_bkd_id = fields.Many2one( comodel_name="vit.permintaan_bkd", string="Permintaan BKD",  help="")
    employee_id = fields.Many2one(comodel_name="hr.employee",  string="Dosen",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    semester_id = fields.Many2one(comodel_name="vit.semester",  string="Semester",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    status_dosen_id = fields.Many2one(comodel_name="vit.status_dosen",  string="Status dosen",  readonly=True, states={"draft" : [("readonly",False)]},  help="")    
