#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class account_asset(models.Model):
    _inherit = "account.asset.asset"

    kepemilikan = fields.Char(string="Kepemilikan",)
    nup = fields.Char(string="NUP")
    jenis_dokumen = fields.Char(string="Jenis Dokumen")
    jenis_sertifikat = fields.Char(string="Jenis Sertifikat")
    status_pengelolaan = fields.Char(string="Status Pengelolaan")

    luas_tanah = fields.Float(string="Luas Tanah Seluruhnya (M2)")
    luas_tanah_bangunan = fields.Float(string="Luas Tanah Untuk Bangunan (M2)")
    luas_tanah_lingkungan = fields.Float(string="Luas Tanah Untuk Sarana Lingkungan (M2)")
    luas_lahan_kosong = fields.Float(string="Luas Lahan Kosong (M2)")
    alamat = fields.Char(string="Alamat")
    alamat_lain = fields.Char(string="Alamat Lainnya")
    rt_rw = fields.Char(string="RT/RW")

    kelurahan_id = fields.Char(string="Kelurahan/Desa", required=False, )
    kecamatan_id = fields.Char(string="Kecamatan", required=False, )
    kota_id      = fields.Char(string="Kota/Kab", required=False, )
    state_id     = fields.Char(string='Provinsi')
    kode_pos = fields.Char(string="Kode Pos")

    luas_bangunan = fields.Float(string="Luas Bangunan")
    luas_dasar = fields.Float(string="Luas Dasar")
    jml_lantai = fields.Integer(string="Jumlah Lantai")

    jumlah_kib = fields.Float(string="Jumlah KIB")
    sbsk = fields.Float(string="SBSK")
    optimalisasi = fields.Float(string="Optimalisasi")
    status_sbsn = fields.Char(string="Status SBSN")

    no_bpkb = fields.Char(string="No BPKB")
    nomor_polisi = fields.Char(string="No Polisi")

    dates  = fields.Date(string="Tanggals", required=False, )

