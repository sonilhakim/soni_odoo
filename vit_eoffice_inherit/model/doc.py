#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft','Draft'),('open','Perlu Approval'),('read','Read'),('unread','Unread')]
from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning
import time

class doc(models.Model):
    _name = "vit.doc"
    _inherit = ["vit.doc", "mail.thread"]

    user_id = fields.Many2one(comodel_name="res.users",  required=True, default=lambda self: self.env.uid)
    subject = fields.Char( string="Subject", required=True)
    body = fields.Text( string="Body", required=True)
    date = fields.Date( string="Date",  required=True, default=lambda self: time.strftime("%Y-%m-%d"))

    @api.model
    def create(self, vals):
        if not vals.get("name", False) or vals["name"] == "New":
            vals["name"] = self.env["ir.sequence"].next_by_code("vit.doc") or "Error Number!!!"
        return super(doc, self).create(vals)

    def action_confirm(self):
        for doc in self:
            if not doc.to_user_ids:
                raise UserError(_("Pilih minimal satu tujuan surat") )       

        self.insert_history( 'Set to Need Approval')
        self.state = STATES[1][0]

    def action_done(self):
        self.state = STATES[2][0]

    def action_draft(self):
        self.insert_history( 'Set to Draft')
        self.state = STATES[0][0]

    def action_read(self):
        self.insert_history( 'Set to Read')
        self.state = STATES[2][0]

    @api.multi
    def unlink(self):
        for me_id in self :
            if me_id.state != STATES[0][0]:
                raise UserError("Cannot delete non draft record!")
        return super(doc, self).unlink()

    def action_send(self):
        partner_ids = [ to_user.user_id.partner_id.id for to_user in self.to_user_ids ]
        partner_ids += [ cc_user.user_id.partner_id.id for cc_user in self.cc_user_ids ]

        body = _("Anda mendapat Surat No:%s dari %s, silahkan dibuka") % (self.name, self.user_id.name)
        self.message_post(body=body, partner_ids=partner_ids)

        self.insert_history('Set to Unread')
        self.state=STATES[2][0]

    #########################################################################
    # read doc dan update status read di to_user_id dan cc_user_id
    # jika semua to_user_id sudah read maka update doc state = read 
    #########################################################################
    @api.multi
    def read(self, fields=None, load='_classic_read'):
        # if len(self) == 1:
        #     uid = self.env.uid
        #     # update status read utk to_user yang matching doc_id dan uid nya
        #     to_user_obj = self.env['eo.to_user']
        #     to_user_id  = to_user_obj.search([('doc_id','=',self.id), ('user_id','=',uid)], )
        #     if to_user_id:
        #         to_user_obj.write(to_user_id , {'read_status': True}, )
        #         self.insert_history('Read (to)')

        #     # update status read utk cc_user yang matching doc_id dan uid nya
        #     cc_user_obj = self.env['eo.cc_user']
        #     cc_user_id  = cc_user_obj.search([('doc_id','=',self.id), ('user_id','=',uid)], )
        #     if cc_user_id:
        #         cc_user_obj.write(cc_user_id , {'read_status': True}, )
        #         self.insert_history('Read (cc)')

        #     #update status doc = read jika semua to_user_ids sudah read_status=True
        #     st=''
        #     to_user_ids = to_user_obj.search([('doc_id','=',self.id)], )

        #     for to_user_id in to_user_obj.browse(to_user_ids, ):
        #         if to_user_id.read_status == True:
        #             st ='read'
        #         else:
        #             st = ''
        #             break
            
        #     if st=='read':
        #         self.write(ids, {'state':st}, )
        #         self.insert_history(ids[0], 'State updated to Read')

        #parent read
        res = super(doc, self).read(fields=fields, load=load)
        return res


    #########################################################################
    # replace tokens in body
    #########################################################################
    def replace_tokens(self):
        pass 

    #########################################################################
    # insert history
    #########################################################################
    def insert_history(self, name):
        uid= self.env.uid
        doc_history_obj = self.env['vit.doc_history']

        data = {
            'name'		: name ,
            'user_id'	: uid,
            'doc_id'	: self.id,
        }

        res = doc_history_obj.create(data, )
        return res 


    def action_reply(self):
        '''
        redirect to vit.doc form view with prefilled values 
        from the old doc
        '''

        uid = self.env.uid

        ######################################################################
        # get the old doc
        ######################################################################
        data = self

        ######################################################################
        # set defautl values for the redirect 
        ######################################################################
        context.update({
            'default_parent_id' : data.id,
            'default_user_id'   : uid,
            'default_to_user_ids' : [(0, 0, {'user_id': data.user_id.id })]
        })

        ######################################################################
        # history 
        ######################################################################
        self.insert_history( 'Replied')

        ######################################################################
        # return and show the view  
        ######################################################################
        return {
            'name': _('Reply Surat'),
            'view_type': 'form',
            "view_mode": 'form',
            'res_model': 'vit.doc',
            'type': 'ir.actions.act_window',
            'context': context,
        }

    def action_forward(self):
        pass