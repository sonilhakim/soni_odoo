#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft','Rancangan'),('open','Proses'),('done','Valid')]
from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class capaian_kinerja_unit_kerja(models.Model):

    _name = "vit.capaian_kinerja_unit_kerja"
    _description = "vit.capaian_kinerja_unit_kerja"
    name = fields.Char( required=True, default="New", readonly=True,  string="Name",  help="")
    description = fields.Char( string="Description",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    state = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",  help="")


    capaian_unit_ids = fields.One2many(comodel_name="vit.capaian_kinerja_unit_kerja_detail",  inverse_name="capaian_unit_id",  string="Capaian unit",  readonly=True, states={"draft" : [("readonly",False)]},  help="")

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
        return super(capaian_kinerja_unit_kerja, self).unlink()

    @api.multi
    def action_reload(self, ):
        sql = "delete from vit_capaian_kinerja_unit_kerja_detail where capaian_unit_id = %s"
        self.env.cr.execute(sql, (self.id,))
        sql = """
                insert into vit_capaian_kinerja_unit_kerja_detail (unit_id, capaian_unit_id)
                select id, %s
                from vit_unit_kerja
                """
        self.env.cr.execute(sql, (self.id,))
