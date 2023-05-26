from odoo import tools
from odoo import fields,models,api
from odoo.tools.translate import _
from odoo.exceptions import UserError

PR_STATES =[('draft','Draft'),
    ('open','Confirmed'),
    ('validate','Validate'),
    ('onprogress','On Progress'), 
    ('done','Done'),
    ('reject','Rejected')]
PR_LINE_STATES =[('draft','Draft'),
    ('open','Confirmed'),
    ('validate','Validate'),
    ('onprogress','On Progress'), # Call for Bids in progress
    ('done','Done'),# Call for Bids = PO created / done
    ('reject','Rejected')]

class PurchaseRequestM(models.Model):
    _name           = "vit.product.request"
    _inherit        = "vit.product.request"

    partner_id = fields.Many2one("res.partner","Supplier", track_visibility='onchange',domain="[]")
    state = fields.Selection(PR_STATES,'Status',readonly=True,required=True, default='draft',track_visibility='onchange')
    
    @api.model
    def create(self,vals):
        res = super(PurchaseRequestM, self).create(vals)
        if res.merchandise_pr:            
            dept = self.env['hr.department'].browse(int(vals['department_id']))
            res.name = self.env['ir.sequence'].next_by_code('vit.product.request.modif') + '/' + dept.name or '/'

        return res

    @api.multi
    def action_validate(self):
        #set to "open" approved state
        body = _("PR confirmed")
        self.send_followers()
        self.update_line_state(PR_STATES[2][0])
        return self.write({'state':PR_STATES[2][0]})

    @api.multi
    def action_onprogress(self):
        #set to "onprogress" state
        body = _("PR on progress")
        self.send_followers()
        self.update_line_state(PR_STATES[3][0])
        return self.write({'state':PR_STATES[3][0]})

    @api.multi
    def action_done(self):
        #set to "done" state
        body = _("PR done")
        self.send_followers()
        self.update_line_state(PR_STATES[4][0])
        return self.write({'state':PR_STATES[4][0]})

    @api.multi
    def action_reject(self):
        #set to "reject" state
        body = _("PR reject")
        self.send_followers()
        self.update_line_state(PR_STATES[5][0])
        return self.write({'state':PR_STATES[5][0]})

class PurchaseRequestLine(models.Model):
    _name         = "vit.product.request.line"
    _inherit        = "vit.product.request.line"

    # allow = fields.Boolean("Allowance 1%", default=False)
    allowance_id = fields.Many2one("vit.product.request.allowance", "Allowance", default=False)
    allow_qty = fields.Float("Allow Qty", compute="compute_allow", store=True)
    quantity = fields.Float('Quantity', default=1.0)

    unit_price = fields.Float(string="Price Unit",  required=False)
    state = fields.Selection(PR_LINE_STATES,'Status',readonly=True,required=True, default='draft')

    @api.depends('quantity','allowance_id')
    def compute_allow(self):
        allow_qty = 0.0
        for line in self:
            if line.quantity and line.allowance_id:
                if line.allowance_id.amount_type == 'fixed':
                    allow_qty = line.allowance_id.amount
                else:
                    allow_qty = line.quantity * (line.allowance_id.amount/100)
                line.allow_qty = allow_qty

    @api.onchange('quantity','allowance_id')
    def _onchange_qty(self):
        for line in self:
            if line.quantity and line.allowance_id:
                line.product_qty = line.quantity + line.allow_qty
            else:
                line.product_qty = line.quantity


class PurchaseRequestAllowance(models.Model):
    _name = "vit.product.request.allowance"
    _description = "vit.product.request.allowance"

    name = fields.Char(string='Allowance Name', required=True)
    amount_type = fields.Selection(default='percent', string="Allowance Computation", required=True, oldname='type',
        selection=[('fixed', 'Fixed'), ('percent', 'Percentage')])
    active = fields.Boolean(default=True, help="Set active to false to hide the allowance without removing it.")
    amount = fields.Float(string='Amount', required=True)
