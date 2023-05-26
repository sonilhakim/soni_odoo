#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
import time
from odoo.exceptions import UserError, ValidationError
STATES=[('draft', 'Draft'), ('open', 'Open'), ('cancel', 'Cancel'), ('approved','Approved'), ('close','Closed')]

class purchase_order_garmen(models.Model):
    _name = "vit.purchase_order_garmen"
    _description = "vit.purchase_order_garmen"
    _order = 'date desc, id desc'
    _inherit = ['mail.thread']
        
    name            = fields.Char( readonly=True, required=True, default='New', string="No. OR", copy=False)
    state           = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",track_visibility='onchange',  help="")
    date            = fields.Date( string="Date", required=False, default=lambda self: time.strftime("%Y-%m-%d"), readonly=True, states={"draft" : [("readonly",False)]}, help="")
    # deadline_date   = fields.Date(string="Deadline Production", readonly=True, states={"draft" : [("readonly",False)]}, help="")
    time_production = fields.Char(string="Time Production", readonly=True, states={"draft" : [("readonly",False)]}, help="")
    total           = fields.Float( string="Total", help="")
    project         = fields.Text( string="Project Description", help="", readonly=True, states={"draft" : [("readonly",False)]} )
    po_buyer        = fields.Char( string="NO. PO Buyer", help="", readonly=True, states={"draft" : [("readonly",False)]})
    po_date         = fields.Date( string="Po date", help="", readonly=True, states={"draft" : [("readonly",False)]})
    total_price     = fields.Monetary( string="Total Price", help="")
    currency_id     = fields.Many2one('res.currency', related='company_id.currency_id', string="Currency", readonly=True)
    note            = fields.Text( string="Notes", readonly=True, states={"draft" : [("readonly",False)]},  help="")
    product_created = fields.Boolean( string='Product Style Created')

    user_id         = fields.Many2one("res.users", "User", default=lambda self: self.env.uid, track_visibility='onchange', readonly=True)
    company_id      = fields.Many2one( comodel_name="res.company",  string="Company", related='user_id.company_id', readonly=True,  help="")
    partner_id      = fields.Many2one(required=True, comodel_name="res.partner",  string="Buyer",  help="", readonly=True, states={"draft" : [("readonly",False)]})
    partner_invoice = fields.Many2one( comodel_name="res.partner",  string="Invoice Address",  help="", readonly=True, states={"draft" : [("readonly",False)]})
    partner_delivery= fields.Many2one( comodel_name="res.partner",  string="Delivery Address",  help="", readonly=True, states={"draft" : [("readonly",False)]})
    sph_id          = fields.Many2one( comodel_name="vit.marketing_sph_garmen",  string="No SPH",  help="")
    boq_line_ids    = fields.One2many(comodel_name="vit.boq_po_garmen_line",  inverse_name="po_id",  string="Boq lines",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    doc_line_ids    = fields.One2many(comodel_name="vit.document_po_garmen_line",  inverse_name="po_id",  string="Doc lines",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    po_payung_id    = fields.Many2one( comodel_name="vit.purchase_order_garmen", string="PO Payung", readonly=True)
    # spk             = fields.Char("No. SPK Pengukuran")
    or_count        = fields.Integer(string='Hitung OR', compute='_get_or')
    spk_count       = fields.Integer(string='Hitung SPK', compute='_get_spk')
    doc_count       = fields.Integer(string='Hitung Doc', compute='_get_doc')

    # _sql_constraints = [
    #     ('name', 'unique(name,company_id)',
    #      'Name of Order Receive must be unique per company'),
    # ]

    @api.multi
    def _cek_name(self):
        for po in self:
            # import pdb;pdb.set_trace()
            x = self.env['vit.purchase_order_garmen'].search([('name','=',po.name),('id','!=',po.id)])
            if x:
                return False

        return True

    _constraints = [(_cek_name, 'Name of Order Receive must be Unique!', ['name'])]
    
    @api.model
    def create(self, vals):
        if not vals.get('name', False) or vals['name'] == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('vit.purchase_order_garmen') or 'Error Number!!!'
        
        return super(purchase_order_garmen, self).create(vals)

    @api.onchange('boq_line_ids')
    def onchange_total_qty(self):
        for po in self:
            if po.boq_line_ids:
                po.total = sum(line.qty for line in po.boq_line_ids)
                po.total_price = sum(line.total_price for line in po.boq_line_ids)

    @api.multi
    def create_or(self):
        self.ensure_one()
        po_payung = self.env["vit.purchase_order_garmen"]
        cr = self.env.cr
        for po in self:
            line_ids = []
            for boq in po.boq_line_ids:
                # import pdb;pdb.set_trace()
                mat_data = []
                for mat in boq.material_ids:
                    mat_data.append((0, 0, {
                        "acc_no"   : mat.acc_no,
                        "material" : mat.material.id,
                        "spec"     : mat.spec,
                        "colour"   : mat.colour,
                        "qty"      : mat.qty,
                        "uom"      : mat.uom.id,
                        }))
                dsn_data = []
                for dsn in boq.design_ids:
                    dsn_data.append((0,0,{
                        'doc_name'   : dsn.doc_name,
                        'doc'        : dsn.doc,
                        'date'       : dsn.date,
                        'name'       : dsn.name,
                        }))
                line_ids.append((0,0,{
                    "name"          : boq.name,
                    "sample_id"     : boq.sample_id.id,
                    "product_id"    : boq.product_id.id,
                    "kain"          : boq.kain,
                    "uom_id"        : boq.uom_id.id,
                    "price"         : boq.price,
                    "tax_id"        : boq.tax_id.id,
                    "product_name"  : boq.product_name,
                    "material_ids"  : mat_data,
                    "design_ids"    : dsn_data
                    }))
            doc_ids = []
            for doc in po.doc_line_ids:
                doc_ids.append((0,0,{
                        'doc_name'   : doc.doc_name,
                        'doc'        : doc.doc,
                        'date'       : doc.date,
                        'name'       : doc.name,
                    }))
            
            data = {
                'name'           : po.name +'-'+ str(po.or_count + 1),
                'po_payung_id'   : po.id,
                'partner_id'     : po.partner_id.id ,
                'project'        : po.project,
                'note'           : po.note,
                'time_production': po.time_production,
                'date'           : po.date,
                'product_created': True,
                'boq_line_ids'   : line_ids,
                'doc_line_ids'   : doc_ids,
            }
            if po.name != po.name +'-'+ str(po.or_count + 1):
                po.create(data)
        
    def _get_or(self):
        for po in self:
            po_ids = self.env["vit.purchase_order_garmen"].search([('po_payung_id','=',po.id)])
            if po_ids:
                po.or_count = len(set(po_ids.ids))

    @api.multi
    def action_view_or(self):
        for po in self:
            po_ids = self.env["vit.purchase_order_garmen"].search([('po_payung_id','=',po.id)])
            action = self.env.ref('vit_marketing_po_garmen.action_vit_purchase_order_garmen').read()[0]
            if len(po_ids) > 1:
                action['domain'] = [('id', 'in', po_ids.ids)]
            elif len(po_ids) == 1:
                form_view = [(self.env.ref('vit_marketing_po_garmen.view_vit_purchase_order_garmen_form').id, 'form')]
                if 'views' in action:
                    action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
                else:
                    action['views'] = form_view
                action['res_id'] = po_ids.ids[0]
            else:
                action = {'type': 'ir.actions.act_window_close'}
            return action
    
    @api.multi 
    def action_draft(self):
        self.state = STATES[0][0]

    @api.multi 
    def action_confirm(self):
        for po in self:
            if not po.boq_line_ids or not po.doc_line_ids:
                raise UserError(_('BOQ dan Document harus diisi'))
            else:
                po.state = STATES[1][0]

    @api.multi 
    def action_cancel(self):        
        self.state = STATES[2][0]

    @api.multi 
    def create_spk_pengukuran(self):
        self.ensure_one()
        spk = self.env["vit.spk_pengukuran"]
        cr = self.env.cr
        for po in self:            
            sql = """SELECT pt.id
                    FROM vit_boq_po_garmen_line bl
                    LEFT JOIN product_template pt ON bl.product_id = pt.id
                    WHERE bl.po_id = %s
                    """
            cr.execute(sql, (po.id,))
            result = cr.fetchall()
            style_data = []
            for res in result:
                style_data.append((0, 0, {
                    "product_id": res[0],
                    }))
            data = {
                'partner_id'    : po.partner_id.id ,
                'project'       : po.project,
                'notes'         : po.note,
                'po_id'         : po.id,
                'spk_product_ids': style_data,
            }
            spk_id = spk.create(data)

    @api.multi 
    def create_product_jadi(self):
        for po in self:
            product_tmp = self.env['product.template']
            categ = self.env['product.category'].search([('name','=','Barang Jadi Uniform')])
            if not categ:
                raise UserError(_('Kategori Barang Jadi Uniform belum ada!'))
            i = 1
            for pb in po.boq_line_ids:
                default_code = po.sph_id.proposal_id.inquery_id.name + '-' + str(i)
                datas = {
                    'name'          : pb.name,
                    'type'          : 'product',
                    'categ_id'      : categ.id,
                    'uom_id'        : pb.uom_id.id,
                    'uom_po_id'     : pb.uom_id.id,
                    'list_price'    : pb.price,
                    'standard_price': 0.0,
                    'taxes_id'          : False,
                    'supplier_taxes_id' : False,
                    'tracking'      : 'serial',
                    'sale_ok'       : True,
                    'purchase_ok'   : True,
                    'company_id'    : po.company_id.id,
                    'partner_id'    : po.partner_id.id,
                    'inquery_id'    : po.sph_id.proposal_id.inquery_id.id,
                    'default_code'  : default_code,
                    'default_code_c': default_code,
                    'description'   : pb.product_name,
                }
                i += 1
                sql = """SELECT default_code
                    FROM product_template
                    WHERE categ_id = %s
                    """
                self.env.cr.execute(sql, (categ.id,))
                result = self.env.cr.fetchall()
                dc = []
                for pt in result:
                    dc.append(pt[0])
                # import pdb;pdb.set_trace()
                if default_code not in dc:
                    product = product_tmp.create(datas)                        
                    pb.write({'product_id': product.id})

        self.product_created = True


    @api.multi 
    def action_approved(self):
        self.state = STATES[3][0]

    @api.multi 
    def action_close(self):
        self.state = STATES[4][0]

    def _get_spk(self):
        for po in self:
            spk_ids = self.env["vit.spk_pengukuran"].search([('po_id','=',po.id)])
            if spk_ids:
                po.spk_count = len(set(spk_ids.ids))

    @api.multi
    def action_view_spk(self):
        for po in self:
            spk_ids = self.env["vit.spk_pengukuran"].search([('po_id','=',po.id)])
            action = self.env.ref('vit_spk_pengukuran.action_vit_spk_pengukuran').read()[0]
            if len(spk_ids) > 1:
                action['domain'] = [('id', 'in', spk_ids.ids)]
            elif len(spk_ids) == 1:
                form_view = [(self.env.ref('vit_spk_pengukuran.view_vit_spk_pengukuran_form').id, 'form')]
                if 'views' in action:
                    action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
                else:
                    action['views'] = form_view
                action['res_id'] = spk_ids.ids[0]
            else:
                action = {'type': 'ir.actions.act_window_close'}
            return action


    def _get_doc(self):
        for po in self:
            doc_ids = self.env["vit.document_po_garmen_line"].search([('po_id','=',po.id)])
            if doc_ids:
                po.doc_count = len(set(doc_ids.ids))

    @api.multi
    def action_view_doc(self):
        for po in self:
            doc_ids = self.env["vit.document_po_garmen_line"].search([('po_id','=',po.id)])
            action = self.env.ref('vit_marketing_po_garmen.action_vit_document_po_garmen_line').read()[0]
            action['domain'] = [('id', 'in', doc_ids.ids)]
            return action


    @api.multi
    def unlink(self):
        for rec in self:
            if rec.state != 'draft':
                raise UserError(_('Data yang bisa dihapus hanya yang berstatus draft!'))
        return super(purchase_order_garmen, self).unlink()

        