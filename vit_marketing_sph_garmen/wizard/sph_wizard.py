# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2017  Odoo SA  (http://www.vitraining.com)
#    All Rights Reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import datetime
from odoo.exceptions import ValidationError, RedirectWarning, UserError
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.addons import decimal_precision as dp
import time
import base64



class SphWizard(models.TransientModel):
    _name = "marketing.sph.wizard"

    @api.model
    def _get_default_line(self):
        if self._context.get('active_id', False):
            sph_obj = self.env['vit.marketing_sph_garmen']
            sph = sph_obj.browse(self._context.get('active_id', False))
            line_ids = []
            sphlines = self.env['vit.boq_sph_garmen_line'].search([('sph_id','=',sph.id)])
            if sphlines :
                for sl in sphlines:
                    line_ids.append([0,0,{'name': sl.name,'qty':1.0,'uom':sl.uom_id.id,'boq_sph_id':sl.id}])
            return line_ids

    requester           = fields.Char( string="Request", required=True, help="" )
    recipient           = fields.Char( string="Recipient", required=True, help="" )
    due_date            = fields.Date(string="Due Date", required=True, help="")
    docwizar_ids        = fields.One2many(comodel_name="marketing.sphdoc.wizard",  inverse_name="spheizard_id",  string="Docs",  help="")
    linewizar_ids       = fields.One2many(comodel_name="marketing.sphline.wizard",  inverse_name="spheizard_id",  string="Lines", default=_get_default_line,  help="")


    @api.multi
    def create_request_design(self):
        #import pdb;pdb.set_trace()
        sph_id = self._context.get('active_id', False)
        if sph_id:
            sph_obj = self.env['vit.marketing_sph_garmen']
            sph = sph_obj.browse(sph_id)            
            request = self.env["vit.marketing_request"]
            line_ids = []
            for boq in self.linewizar_ids:
                line_ids.append((0,0,{
                        "name"       : boq.name,
                        "boq_sph_id" : boq.boq_sph_id.id,
                        "uom"        : boq.uom.id,
                        "qty"        : boq.qty,
                    }))
            doc_ids = []
            if not self.docwizar_ids:
                raise UserError(_('Dokumen Desain harus diisi !'))
            for doc in self.docwizar_ids:
                doc_ids.append((0,0,{
                        'doc_name'   : doc.doc_name,
                        'doc'        : doc.doc,
                        'date'       : doc.date,
                        'name'       : doc.name,
                    }))

            data = {
                'sph_id'        : sph.id,
                'partner_id'    : sph.partner_id.id ,
                'project'       : sph.project,
                'notes'         : sph.notes,
                'requester'     : self.requester,
                'recipient'     : self.recipient,
                'due_date'      : self.due_date,
                'line_request_ids' : line_ids,
                'doc_request_ids'  : doc_ids,
            }
            req_id = request.create(data)
            sph.write({'request' : req_id.name})
        return {'type': 'ir.actions.act_window_close'}

class SphdocWizard(models.TransientModel):
    _name = "marketing.sphdoc.wizard"

    name        = fields.Char( required=False, string="Description",  help="")
    doc         = fields.Binary( string="Document Name",  help="")
    doc_name    = fields.Char( string="Document Name",)
    date        = fields.Date( string="Date", required=False, default=lambda self: time.strftime("%Y-%m-%d"),  help="")

    spheizard_id= fields.Many2one(comodel_name="marketing.sph.wizard",  string="Sph Wizard",  help="")

class SphlineWizard(models.TransientModel):

    _name = "marketing.sphline.wizard"

    name            = fields.Char( required=True, string="Style",  help="")
    qty             = fields.Float( string="Qty", digits=dp.get_precision('Product Unit of Measure'), default=1.0,  help="")
    uom             = fields.Many2one(comodel_name="uom.uom", string="Satuan")
    boq_sph_id      = fields.Many2one( comodel_name="vit.boq_sph_garmen_line", string="BOQ", help="")
    spheizard_id    = fields.Many2one(comodel_name="marketing.sph.wizard",  string="Sph Wizard",  help="")
