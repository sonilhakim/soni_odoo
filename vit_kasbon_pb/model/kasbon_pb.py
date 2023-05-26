#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft','Draft'),('open',' Approval Manager'),('confirm','Approved'),('lunas','Lunas'),('cancel','Cancel'),('refuse','Ditolak')]
from odoo import models, fields, api, _
import time
from datetime import datetime, timedelta
from odoo.exceptions import UserError, Warning

class kasbon_pb(models.Model):

    _name = "vit.kasbon_pb"
    _description = "vit.kasbon_pb"
    _inherit = ['mail.thread']

    name            = fields.Char( required=True, default="New", readonly=True,  string="Name",  help="", )
    tanggal_pengajuan = fields.Date( string="Tanggal pengajuan", required=True, default=lambda self:time.strftime("%Y-%m-%d"), readonly=True, states={"draft" : [("readonly",False)]},  help="", )
    pinjaman        = fields.Float( string="Pinjaman", required=True, readonly=True, states={"draft" : [("readonly",False)]},  help="", )
    pencairan       = fields.Float( string="Pencairan",  help="", )
    angsuran        = fields.Float( string="Angsuran",  help="", )
    state           = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",  help="", )

    employee_id     = fields.Many2one(comodel_name="hr.employee",  string="Karyawan", required=True,  readonly=True, states={"draft" : [("readonly",False)]},  help="", )
    department_id   = fields.Many2one(comodel_name="hr.department",  string="Department",  related="employee_id.department_id", store=True,  help="", )
    user_id         = fields.Many2one(comodel_name="res.users",  string="User",  readonly=True, states={"draft" : [("readonly",False)]},  help="", )
    angsuran_ids    = fields.One2many(comodel_name="account.payment", string="Angsuran", inverse_name="kasbon_id")

    pencairan_count = fields.Integer(string='Hitung Pencairan', compute='_get_pen')
    angsuran_count  = fields.Integer(string='Hitung Angsuran', compute='_get_ang')

    notes = fields.Text(string='Keterangan')

    sama = fields.Boolean(string='sama', compute='compute_sama', store=True, help="jumlah Angsuran sama dengan jumlah Pencairan")
    not_fully_paid = fields.Boolean(string="belum lunas", compute='compute_bl')

    @api.model
    def create(self, vals):
        if not vals.get("name", False) or vals["name"] == "New":
            if vals["employee_id"]:
                karyawan = self.env['hr.employee'].browse(vals["employee_id"])
                vals["name"] = "Kasbon/" + karyawan.name + self.env["ir.sequence"].next_by_code("vit.kasbon_pb") or "Error Number!!!"
        return super(kasbon_pb, self).create(vals)

    @api.multi
    def button_confirm(self):
        self.state = STATES[1][0]

    @api.multi
    def button_confirm_manager(self):
        self.create_pencairan()
        self.state = STATES[2][0]

    @api.multi
    def button_cancel(self):
        self.state = STATES[4][0]

    @api.multi
    def button_refuse(self):
        self.state = STATES[5][0]

    @api.multi
    def button_draft(self):
        self.state = STATES[0][0]

    @api.multi
    def action_lunas(self):
        self.state = STATES[3][0]


    @api.multi
    def unlink(self):
        for me_id in self :
            if me_id.state != STATES[0][0]:
                raise UserError("Cannot delete non draft record!")
        return super(kasbon_pb, self).unlink()


    @api.multi
    def create_pencairan(self):
        partner = self.env['res.partner'].search([('id','=',self.employee_id.address_home_id.id)])
        partner.write({'supplier':True})

        product = self.env['product.product'].search([('name','ilike','kasbon')], limit=1)
        jurnal = self.env['account.journal'].search([('type','=','purchase')], limit=1)


        if product.property_account_expense_id:
            account = product.property_account_expense_id.id
        # elif product.categ_id.property_account_creditor_price_difference_categ:
        #     account = product.categ_id.property_account_creditor_price_difference_categ.id
        else:
            raise Warning(_("Settingan account product kasbon masih kosong !"))

        invoice_line = []
        invoice_line.append((0, 0 ,{'product_id':product.id, 
                                    'price_unit':self.pinjaman, 
                                    'name':'Kasbon '+ self.employee_id.name, 
                                    'quantity':1,
                                    'uom_id':product.uom_id.id, 
                                    'account_id':account}))

        invoice = self.env['account.invoice'].create({'partner_id':partner.id,
                                            'date_invoice': datetime.now().strftime("%Y-%m-%d"),
                                            'type': 'in_invoice',
                                            'journal_id': jurnal.id,
                                            'company_id': self.employee_id.company_id.id,
                                            'reference': self.name,
                                            'kasbon_id': self.id,
                                            'account_id': partner.property_account_payable_id.id,
                                            'invoice_line_ids': invoice_line,
                                           })

        return self.action_view_pencairan()
    
    def _get_pen(self):
        for kas in self:
            pen_ids = self.env["account.invoice"].search([('type','=','in_invoice'),('kasbon_id','=',kas.id)])
            if pen_ids:
                kas.pencairan_count = len(set(pen_ids.ids))

    @api.multi
    def action_view_pencairan(self):
        for kasbon in self:
            invoice_ids = self.env["account.invoice"].search([('kasbon_id','=',kasbon.id),('type','=','in_invoice')])
            action = self.env.ref('vit_kasbon_pb.action_bill_pencairan_kasbon').read()[0]
            if len(invoice_ids) > 1:
                action['domain'] = [('id', 'in', invoice_ids.ids)]
            elif len(invoice_ids) == 1:
                form_view = [(self.env.ref('vit_kasbon_pb.bill_pencairan_kasbon_form').id, 'form')]
                if 'views' in action:
                    action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
                else:
                    action['views'] = form_view
                action['res_id'] = invoice_ids.ids[0]
            else:
                action = {'type': 'ir.actions.act_window_close'}
            return action

    @api.depends('angsuran','pencairan')
    def compute_sama(self):
        for kas in self:
            if kas.angsuran == kas.pencairan and kas.angsuran != 0.0 and kas.pencairan != 0.0 and kas.pinjaman != kas.pencairan:
                kas.sama = True
            else:
                kas.sama = False


    def compute_bl(self):
        for kb in self:
            if kb.angsuran < kb.pencairan:
                kb.not_fully_paid = True

            else:
                kb.not_fully_paid = False

    