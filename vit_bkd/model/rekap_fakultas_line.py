#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class rekap_fakultas_line(models.Model):

    _name = "vit.rekap_fakultas_line"
    _description = "vit.rekap_fakultas_line"
    name = fields.Char( required=True, string="Name",  help="")
    no_sertifikat = fields.Char( string="No sertifikat",  help="")
    nama_dosen = fields.Char( string="Nama dosen",  help="")
    semester_gasal_pd = fields.Integer( string="Semester gasal pd",  help="")
    semester_gasal_pl = fields.Integer( string="Semester gasal pl",  help="")
    semester_gasal_pg = fields.Integer( string="Semester gasal pg",  help="")
    semester_gasal_pk = fields.Integer( string="Semester gasal pk",  help="")
    semester_genap_pd = fields.Integer( string="Semester genap pd",  help="")
    semester_genap_pl = fields.Integer( string="Semester genap pl",  help="")
    semester_genap_pg = fields.Integer( string="Semester genap pg",  help="")
    semester_genap_pk = fields.Integer( string="Semester genap pk",  help="")
    kewajiban_khusus_prof = fields.Integer( string="Kewajiban khusus prof",  help="")
    status = fields.Char( string="Status",  help="")
    kesimpulan = fields.Char( string="Kesimpulan",  help="")


    rekap_fakultas_id = fields.Many2one(comodel_name="vit.rekap_fakultas",  string="Rekap fakultas",  help="")
