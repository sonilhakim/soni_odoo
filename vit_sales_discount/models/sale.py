from odoo import models, fields, api, _
from odoo.exceptions import UserError
import datetime
import sys
from odoo.addons import decimal_precision as dp
import logging
_logger = logging.getLogger(__name__)


class SaleOrderLineDiscount(models.Model):
    _inherit = 'sale.order.line'

    discount_val = fields.Float(string='Discount (Rp)', digits=dp.get_precision('Discount'), default=0.0)
    discount_amount = fields.Float(compute='_compute_amount', string='Discount (amount)', readonly=True, store=True)
    subtotal_amount = fields.Monetary(compute='_compute_amount', string='Subtotal Price', readonly=True, store=True)


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

    @api.depends('product_uom_qty', 'discount', 'discount_val', 'price_unit', 'tax_id')
    def _compute_amount(self):
        res = super(SaleOrderLineDiscount, self)._compute_amount()
        for line in self:
            if line.discount:
                line.discount_amount = (line.price_unit * (line.discount or 0.0) / 100.0) * line.product_uom_qty
            if line.discount_val:
                line.price_subtotal = line.price_subtotal - line.discount_val
            line.subtotal_amount = line.price_unit * line.product_uom_qty
        return res

    @api.multi
    def _prepare_invoice_line(self, qty):
        res = super(SaleOrderLineDiscount, self)._prepare_invoice_line(qty)
        self.ensure_one()
        product = self.product_id.with_context(force_company=self.company_id.id)
        account = product.property_account_income_id or product.categ_id.property_account_income_categ_id

        if not account and self.product_id:
            raise UserError(_('Please define income account for this product: "%s" (id:%d) - or for its category: "%s".') %
                (self.product_id.name, self.product_id.id, self.product_id.categ_id.name))

        fpos = self.order_id.fiscal_position_id or self.order_id.partner_id.property_account_position_id
        if fpos and account:
            account = fpos.map_account(account)

        if self.discount_val:
            res = {
                'name': self.name,
                'sequence': self.sequence,
                'origin': self.order_id.name,
                'account_id': account.id,
                'price_unit': self.price_unit,
                'quantity': qty,
                'discount_val': self.discount_val,
                'uom_id': self.product_uom.id,
                'product_id': self.product_id.id or False,
                'invoice_line_tax_ids': [(6, 0, self.tax_id.ids)],
                'account_analytic_id': self.order_id.analytic_account_id.id,
                'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)],
                'display_type': self.display_type,
            }
        return res

SaleOrderLineDiscount()

class SaleOrderDiscount(models.Model):
    _inherit = "sale.order"

    amount_undisc = fields.Monetary(string='Amount', store=True, readonly=True, compute='_amount_all')
    amount_disc = fields.Monetary(string='Discount', store=True, readonly=True, compute='_amount_all')
    discount_global_val = fields.Float(string='Discount Global (Rp)', digits=dp.get_precision('Discount'), states={'cancel': [('readonly', True)], 'done': [('readonly', True)]}, default=0.0)
    discount_global_persen = fields.Float(string='Discount Global (%)', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
    # global_discount_account = fields.Many2one('account.account', string="Global Discount Account")
    cara_bayar  = fields.Selection([('cash', 'Cash'), ('debit', 'Debit Card'), ('credit', 'Credit Card')], string='Cara Bayar')
    
    
    @api.depends('order_line.product_id','order_line.price_total','discount_global_val','discount_global_persen')
    def _amount_all(self):
        res = super(SaleOrderDiscount, self)._amount_all()
        for order in self:
            amount_undisc = amount_disc = 0.0
            amount_untaxed = order.amount_untaxed
            for line in order.order_line:
                amount_undisc += line.subtotal_amount
                if line.discount:
                    amount_disc += line.discount_amount
                    amount_untaxed = amount_undisc - amount_disc
                if line.discount_val:
                    amount_disc += line.discount_val
                    amount_untaxed = amount_undisc - amount_disc
            # if order.is_ongkos_muat:
            #     for line in order.order_line:
            #         ongkos_muat += line.product_uom_qty * line.product_id.weight * line.product_id.ongkos_muat                  
            if order.discount_global_val:
                amount_disc = amount_disc + order.discount_global_val
                amount_untaxed = amount_undisc - amount_disc
            if order.discount_global_persen:
                disc = order.amount_untaxed * (order.discount_global_persen/100)
                amount_disc = amount_disc + disc
                amount_untaxed = amount_undisc - amount_disc
            order.update({
                'amount_undisc': amount_undisc,
                'amount_disc': amount_disc,
                'amount_untaxed': amount_untaxed,
                # 'ongkos_muat': ongkos_muat,
                'amount_total': amount_untaxed + order.amount_tax,
            })

        return res

    @api.multi
    def _prepare_invoice(self):
        res = super(SaleOrderDiscount, self)._prepare_invoice()
        company_id = self.company_id.id
        journal_id = (self.env['account.invoice'].with_context(company_id=company_id or self.env.user.company_id.id)
            .default_get(['journal_id'])['journal_id'])
        if self.discount_global_val:
            res = {
                'name': (self.client_order_ref or '')[:2000],
                'origin': self.name,
                'type': 'out_invoice',
                'account_id': self.partner_invoice_id.property_account_receivable_id.id,
                'partner_shipping_id': self.partner_shipping_id.id,
                'journal_id': journal_id,
                'currency_id': self.pricelist_id.currency_id.id,
                'comment': self.note,
                'partner_id': self.partner_invoice_id.id,
                'payment_term_id': self.payment_term_id.id,
                'fiscal_position_id': self.fiscal_position_id.id or self.partner_invoice_id.property_account_position_id.id,
                'company_id': company_id,
                'user_id': self.user_id and self.user_id.id,
                'team_id': self.team_id.id,
                'transaction_ids': [(6, 0, self.transaction_ids.ids)],
                'discount_global_val' : self.discount_global_val,
                'amount_untaxed': self.amount_untaxed,
                'amount_total': self.amount_total,
                'cara_bayar' : self.cara_bayar,
            }
        if self.discount_global_persen:
            res = {
                'name': (self.client_order_ref or '')[:2000],
                'origin': self.name,
                'type': 'out_invoice',
                'account_id': self.partner_invoice_id.property_account_receivable_id.id,
                'partner_shipping_id': self.partner_shipping_id.id,
                'journal_id': journal_id,
                'currency_id': self.pricelist_id.currency_id.id,
                'comment': self.note,
                'partner_id': self.partner_invoice_id.id,
                'payment_term_id': self.payment_term_id.id,
                'fiscal_position_id': self.fiscal_position_id.id or self.partner_invoice_id.property_account_position_id.id,
                'company_id': company_id,
                'user_id': self.user_id and self.user_id.id,
                'team_id': self.team_id.id,
                'transaction_ids': [(6, 0, self.transaction_ids.ids)],
                'discount_global_persen' : self.discount_global_persen,
                'amount_untaxed': self.amount_untaxed,
                'amount_total': self.amount_total,
            }

        return res


SaleOrderDiscount()