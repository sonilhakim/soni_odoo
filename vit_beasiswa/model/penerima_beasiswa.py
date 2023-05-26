#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft','Draft'),('open','Verifikasi'),('lolos_akademik','Lolos Akademik'),('done','Lolos PTN'),('reject','Ditolak')]
from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class penerima_beasiswa(models.Model):

    _name = "vit.penerima_beasiswa"
    _description = "vit.penerima_beasiswa"
    name = fields.Char( required=True, default="New", readonly=True,  string="Name",  help="")
    state = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",  help="")
    nama_siswa = fields.Char( string="Nama siswa",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    nomor_hp = fields.Char( string="Nomor hp",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    email = fields.Char( string="Email",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    nama_orang_tua = fields.Char( string="Nama orang tua",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    nomor_hp_orang_tua = fields.Char( string="Nomor hp orang tua",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    alamat = fields.Text( string="Alamat",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    asal_sekolah = fields.Char( string="Asal sekolah",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    nomor_rekening = fields.Char( string="Nomor rekening",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    nama_bank = fields.Char( string="Nama bank",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    upload_foto = fields.Binary( string="Upload foto",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    upload_kartu_keluarga = fields.Binary( string="Upload kartu keluarga",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    upload_buku_tabungan = fields.Binary( string="Upload buku tabungan",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    upload_ktp = fields.Binary( string="Upload ktp",  readonly=True, states={"draft" : [("readonly",False)]},  help="")


    institusi_id = fields.Many2one(comodel_name="res.company",  string="Institusi",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    prestasi_akademik_ids = fields.One2many(comodel_name="vit.prestasi_akademik",  inverse_name="penerima_beasiswa_id",  string="Prestasi akademik",  readonly=True, states={"draft" : [("readonly",False)]},  help="")

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
        return super(penerima_beasiswa, self).unlink()
