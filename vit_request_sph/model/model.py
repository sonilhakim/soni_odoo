# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
import time
import datetime

class marketing_sph_garmen_req(models.Model):
    _inherit = "vit.marketing_sph_garmen"

    request_ids = fields.One2many(comodel_name="vit.marketing_request", inverse_name="sph_id", string="Sample Request",)

    @api.multi 
    def action_tender(self):
        for sph in self:
            req_states = []
            req_names = []
            for reqs in sph.request_ids.search([('sph_id','=',sph.id),('state','not in',['cancel','done'])]):
                req_names.append(reqs.name)
            for reqs2 in sph.request_ids:
                req_states.append(reqs2.state)
            for req in sph.request_ids:
                if req.state not in ['cancel','done']:
                    raise UserError(_('Request Design %s masih belum Done.') %(req_names))
                else:
                    if 'done' not in req_states:                    
                        raise UserError(_('Tidak ada Request Design yang Done.'))

            return super(marketing_sph_garmen_req, self).action_tender()