from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.tools.float_utils import float_compare
from odoo.exceptions import UserError


class AccountBillDisc(models.Model):
    _inherit = 'account.invoice'

    discount_po_total = fields.Float(compute='_compute_discount_po', string='Discount Total', store=True, readonly=True)
    amount_po_subtotal = fields.Monetary(string='Amount', store=True, readonly=True, compute='_compute_discount_po', track_visibility='always')

    @api.multi
    @api.depends('invoice_line_ids.price_subtotal', 'invoice_line_ids.disc_po_amount')
    def _compute_discount_po(self):
        for inv in self:
            amount_undisc = amount_disc = 0.0
            for line in inv.invoice_line_ids:
                amount_undisc += line.subtotal_amount_po
                if line.disc_po_amount:
                    amount_disc += line.disc_po_amount
            inv.update({
                'amount_po_subtotal': amount_undisc,
                'discount_po_total': amount_disc,
            })

    def _prepare_invoice_line_from_po_line(self, line):
        res = super(AccountBillDisc, self)._prepare_invoice_line_from_po_line(line)
        if line.harga_discount:
            if line.product_id.purchase_method == 'purchase':
                qty = line.product_qty - line.qty_invoiced
            else:
                qty = line.qty_received - line.qty_invoiced
            if float_compare(qty, 0.0, precision_rounding=line.product_uom.rounding) <= 0:
                qty = 0.0
            taxes = line.taxes_id
            invoice_line_tax_ids = line.order_id.fiscal_position_id.map_tax(taxes, line.product_id, line.order_id.partner_id)
            invoice_line = self.env['account.invoice.line']
            date = self.date or self.date_invoice
            res = {
                'purchase_line_id': line.id,
                'name': line.order_id.name + ': ' + line.name,
                'origin': line.order_id.origin,
                'uom_id': line.product_uom.id,
                'product_id': line.product_id.id,
                'account_id': invoice_line.with_context({'journal_id': self.journal_id.id, 'type': 'in_invoice'})._default_account(),
                'price_unit': line.order_id.currency_id._convert(
                    line.price_unit, self.currency_id, line.company_id, date or fields.Date.today(), round=False),
                'quantity': qty,
                'discount': 0.0,
                'discount_bertingkat_id':line.discount_bertingkat_id.id,
                'disc_po_amount': line.harga_discount,
                'account_analytic_id': line.account_analytic_id.id,
                'analytic_tag_ids': line.analytic_tag_ids.ids,
                'invoice_line_tax_ids': invoice_line_tax_ids.ids
            }
            account = invoice_line.with_context(purchase_line_id=line.id).get_invoice_line_account('in_invoice', line.product_id, line.order_id.fiscal_position_id, self.env.user.company_id)
            if account:
                res['account_id'] = account.id
        return res

    
AccountBillDisc()


class AccountBillLineDisc(models.Model):
    _inherit = 'account.invoice.line'

    discount_bertingkat_id  = fields.Many2one('purchase.discount.bertingkat', 'Discount Bertingkat')
    disc_po_amount = fields.Float(string='Discount', )
    subtotal_amount_po = fields.Float(string='Subtotal Amount PO', compute='compute_sub_po', store=True)

    @api.onchange('discount_bertingkat_id')
    def onchange_disc_po_amount(self):
        self.ensure_one()

        discount_summary = 0.0
        discount_val = 0.0

        if self.quantity < 1 or self.price_unit < 1:
            discount_per_product = 0.0
            price_after_discount = self.price_unit
        else:
            # hitung discount bertingkat disini
            base_price = self.price_unit * self.quantity

            discount_model = self.env['purchase.discount.bertingkat'].search(
                [('id', '=', self.discount_bertingkat_id.id)])

            if discount_model:
                for discount in discount_model:
                    for discount_detail in discount.line_ids:
                        if discount_detail.calculate == "upper":
                            if discount_summary != 0.0:
                                discount_summary += discount_val * discount_detail.discount / 100
                                discount_val = base_price - discount_summary
                        else:
                            discount_summary += base_price * discount_detail.discount / 100
                            discount_val = base_price - discount_summary

            self.disc_po_amount = self.currency_id.round(discount_summary) 
        

    @api.one
    @api.depends('price_unit', 'disc_po_amount', 'invoice_line_tax_ids', 'quantity',
        'product_id', 'invoice_id.partner_id', 'invoice_id.currency_id', 'invoice_id.company_id',
        'invoice_id.date_invoice', 'invoice_id.date')
    def _compute_price(self):
        res = super(AccountBillLineDisc, self)._compute_price()
        for line in self:
            if line.disc_po_amount:
                line.price_subtotal = line.price_subtotal - line.disc_po_amount

        return res

    @api.depends('price_unit', 'quantity')
    def compute_sub_po(self):
        for line in self:
            if line.price_unit and line.quantity:
                line.subtotal_amount_po = line.price_unit * line.quantity


AccountBillLineDisc()