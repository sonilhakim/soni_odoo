from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError


class AccountInvoiceDisc(models.Model):
    _inherit = 'account.invoice'

    @api.model
    def _default_coa_disc(self):
        coa = self.env['account.account'].search([('name','=','Global Discount')])
        return coa

    amount_undisc = fields.Monetary(string='Amount', store=True, readonly=True, compute='_compute_amount')
    amount_disc = fields.Monetary(string='Discount', store=True, readonly=True, compute='_compute_amount')
    discount_global_val = fields.Float(string='Discount Global (Rp)', digits=dp.get_precision('Discount'), states={'draft': [('readonly', False)]}, default=0.0)
    discount_global_persen = fields.Float(string='Discount Global (%)', states={'draft': [('readonly', False)]}, default=0.0)
    global_discount_account = fields.Many2one('account.account', string="Global Discount Account", default=_default_coa_disc,)
    cara_bayar  = fields.Selection([('cash', 'Cash'), ('debit', 'Debit Card'), ('credit', 'Credit Card')], string='Cara Pembayaran')
    
    # @api.depends('invoice_line_ids.price_total','discount_global_val','discount_global_persen')
    # def _amount_discount(self):
    #     for inv in self:
    @api.multi
    @api.depends('invoice_line_ids.price_subtotal', 'tax_line_ids.amount', 'tax_line_ids.amount_rounding',
                 'currency_id', 'company_id', 'date_invoice', 'type', 'discount_global_val',
                 'discount_global_persen')
    def _compute_amount(self):
        for inv in self:
            res = super(AccountInvoiceDisc, inv)._compute_amount()
            amount_undisc = amount_disc = 0.0
            amount_untaxed = inv.amount_untaxed
            for line in inv.invoice_line_ids:
                amount_undisc += line.subtotal_amount
                if line.discount:
                    amount_disc += line.discount_amount
                    amount_untaxed = amount_undisc - amount_disc
                if line.discount_val:
                    amount_disc += line.discount_val
                    amount_untaxed = amount_undisc - amount_disc
            if inv.discount_global_val:
                amount_disc = amount_disc + inv.discount_global_val
                amount_untaxed = amount_undisc - amount_disc
            if inv.discount_global_persen:
                disc = inv.amount_untaxed * (inv.discount_global_persen/100)
                amount_disc = amount_disc + disc
                amount_untaxed = amount_undisc - amount_disc
            inv.update({
                'amount_undisc': amount_undisc,
                'amount_disc': amount_disc,
                'amount_untaxed': amount_untaxed,
                'amount_total': amount_untaxed + inv.amount_tax,
            })

    # @api.multi
    # def action_invoice_open(self):
    #     res = super(AccountInvoiceDisc, self).action_invoice_open()
    #     if self.discount_global_val:
    #         self.residual = self.residual - self.discount_global_val
    #     if self.discount_global_persen:
    #         self.residual = self.residual -  (self.discount_global_persen/100)

    #     return res

    @api.model
    def invoice_line_move_line_get(self):
        res = super(AccountInvoiceDisc, self).invoice_line_move_line_get()
        if self.discount_global_val > 0 or self.discount_global_persen > 0:
            name = "Global Discount"
            amount_discount = 0.0
            if self.discount_global_persen > 0:
                name = name + " (" + str(self.discount_global_persen) + "%)"
                amount_discount = self.amount_untaxed * (self.discount_global_persen/100)
            if self.discount_global_val > 0:
                amount_discount = self.discount_global_val
            name = name + " for " + (self.origin if self.origin else ("Invoice No " + str(self.id)))
            if not self.global_discount_account:
                raise UserError(_('Global Discount Account Harus Diisi!'))
            else:
                dict = {
                    'invl_id': self.number,
                    'type': 'src',
                    'name': name,
                    'price_unit': amount_discount,
                    'quantity': 1,
                    'price': -amount_discount,
                    'account_id': self.global_discount_account.id,
                    'invoice_id': self.id,
                }
                res.append(dict)

        return res

    # @api.multi
    # def write(self, vals):
    #     res = super(AccountInvoiceDisc, self).write(vals)
    #     for inv in self:
    #         sale = self.env['sale.order'].search([('name','=',inv.origin)])
    #         if sale.discount_global_val:
    #             # import pdb;pdb.set_trace()
    #             inv.discount_global_val = sale.discount_global_val
    #             inv.invoice_line_move_line_get()

    #         if sale.discount_global_persen:
    #             inv.discount_global_persen = sale.discount_global_persen
    #             inv.invoice_line_move_line_get()


    
AccountInvoiceDisc()


class AccountInvoiceLineDisc(models.Model):
    _inherit = 'account.invoice.line'

    discount_val = fields.Float(string='Discount (Rp)', digits=dp.get_precision('Discount'), default=0.0)
    discount_amount = fields.Float(compute='_compute_amount_discount', string='Discount (amount)', readonly=True, store=True)
    subtotal_amount = fields.Monetary(compute='_compute_amount_discount', string='Subtotal Price', readonly=True, store=True)


    @api.onchange('discount')
    def disc_onchange(self):
        for line in self:
            if line.discount:
                line.discount_val = 0.0

    @api.onchange('discount_val')
    def disc_onchangeval(self):
        for line in self:
            if line.discount_val:
                line.discount = 0.0

    @api.depends('quantity', 'discount', 'discount_val', 'price_unit')
    def _compute_amount_discount(self):
        for line in self:
            if line.discount:
                line.discount_amount = (line.price_unit * (line.discount or 0.0) / 100.0) * line.quantity
            
            line.subtotal_amount = line.price_unit * line.quantity

    @api.one
    @api.depends('price_unit', 'discount', 'invoice_line_tax_ids', 'quantity',
        'product_id', 'invoice_id.partner_id', 'invoice_id.currency_id', 'invoice_id.company_id',
        'invoice_id.date_invoice', 'invoice_id.date')
    def _compute_price(self):
        res = super(AccountInvoiceLineDisc, self)._compute_price()
        for line in self:
            if line.discount_val:
                line.price_subtotal = line.price_subtotal - line.discount_val

        return res

AccountInvoiceLineDisc()