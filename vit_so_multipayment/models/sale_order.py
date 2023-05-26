from odoo import api,fields, models, _
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
from odoo.exceptions import UserError,ValidationError

class sale_order(models.Model):
    _inherit = 'sale.order'
    
    payment_ids = fields.Many2many('sale.payment',copy=False)
    payment_ids = fields.One2many(comodel_name='sale.payment', inverse_name="order_id")
    invoice_count = fields.Integer(string='# of Invoices', compute='_get_invoiced', readonly=True)

    
    @api.multi
    def action_view_invoice(self):
        invoice_ids = self.mapped('invoice_ids')
        invoice_ids  += self.env['account.invoice'].search([('sale_ids','=',self.id)])
        imd = self.env['ir.model.data']
        action = imd.xmlid_to_object('account.action_invoice_tree1')
        list_view_id = imd.xmlid_to_res_id('account.invoice_tree')
        form_view_id = imd.xmlid_to_res_id('account.invoice_form')
        
        result = {
            'name': action.name,
            'help': action.help,
            'type': action.type,
            'views': [[list_view_id, 'tree'], [form_view_id, 'form'], [False, 'graph'], [False, 'kanban'], [False, 'calendar'], [False, 'pivot']],
            'target': action.target,
            'context': action.context,
            'res_model': action.res_model,
        }
        if len(invoice_ids) > 1:
            result['domain'] = "[('id','in',%s)]" % invoice_ids.ids
        elif len(invoice_ids) == 1:
            result['views'] = [(form_view_id, 'form')]
            result['res_id'] = invoice_ids.ids[0]
        else:
            result = {'type': 'ir.actions.act_window_close'}
        return result
    
    @api.multi
    def create_multi_invoices(self):
        if not self.payment_ids:
            raise ValidationError(_("No Payment methods found!!"))
        inv_obj = self.env['account.invoice']
        inv_line_obj = self.env['account.invoice.line']
        invoices =[]
        @api.multi
        def line_name(self):
            name = "%s,"%self.name
            for product_name in self.order_line.mapped('product_id').mapped('name'):
                name += "%s,"%product_name
            return name
        for payment in self.payment_ids:
            invoice = inv_obj.create({
                    'partner_id':self.partner_id.id,
                    'payment_journal_id':payment.payment_journal_id.id,
                    'type':'out_invoice',
                    'company_id': self.company_id.id,
                    })
            line_data= {
                    'name':line_name(self),
                    'quantity':payment.qnty,
                    'sale_id':self.id,
                    'invoice_id':invoice.id
                    }
            invoice_line = self.env['account.invoice.line'].new(line_data)
            invoice_line._set_additional_fields(invoice)
            invoice_line.price_unit = payment.payment_amount/payment.qnty if payment.qnty >0 else 1
            invoice_line.account_id = invoice_line.with_context({'journal_id':invoice.journal_id.id,'type':'out_invoice'})._default_account()
            inv_line_obj.create(inv_line_obj._convert_to_write(invoice_line._cache))
            invoice.sale_ids += self
            invoices.append(invoice)
        invoice_ids = [inv.id for inv in invoices]
        self.invoice_ids += self.env['account.invoice'].browse(invoice_ids)
        print(len(self.invoice_ids.ids))
        self._cr.commit()
        return self.invoice_ids
    
        
    @api.depends('state', 'order_line.invoice_status')
    def _get_invoiced(self):
        "OVERRIDE"
        for order in self:
            invoice_ids = order.order_line.mapped('invoice_lines').mapped('invoice_id').filtered(lambda r: r.type in ['out_invoice', 'out_refund'])
            if order.id:
                inv_ids = self.env['account.invoice'].search([('sale_ids','in',self.ids)])
                for inv in inv_ids :
                    invoice_ids += inv
            # Search for invoices which have been 'cancelled' (filter_refund = 'modify' in
            # 'account.invoice.refund')
            # use like as origin may contains multiple references (e.g. 'SO01, SO02')
            refunds = invoice_ids.search([('origin', 'like', order.name)])
            invoice_ids |= refunds.filtered(lambda r: order.name in [origin.strip() for origin in r.origin.split(',')])
            # Search for refunds as well
            refund_ids = self.env['account.invoice'].browse()
            if invoice_ids:
                for inv in invoice_ids:
                    refund_ids += refund_ids.search([('type', '=', 'out_refund'), ('origin', '=', inv.number), ('origin', '!=', False), ('journal_id', '=', inv.journal_id.id)])

            line_invoice_status = [line.invoice_status for line in order.order_line]

            if order.state not in ('sale', 'done'):
                invoice_status = 'no'
            elif any(invoice_status == 'to invoice' for invoice_status in line_invoice_status):
                invoice_status = 'to invoice'
            elif all(invoice_status == 'invoiced' for invoice_status in line_invoice_status):
                invoice_status = 'invoiced'
            elif all(invoice_status in ['invoiced', 'upselling'] for invoice_status in line_invoice_status):
                invoice_status = 'upselling'
            else:
                invoice_status = 'no'

            order.update({
                'invoice_count': len(set(invoice_ids.ids + refund_ids.ids)),
                'invoice_ids': invoice_ids.ids + refund_ids.ids,
                'invoice_status': invoice_status
            })
    
class sale_payment(models.Model):
    _name = "sale.payment"

    order_id = fields.Many2one(comodel_name="sale.order", string="SO", required=False, )
    payment_amount = fields.Float("Amount")
    qnty = fields.Integer("Qty")
    payment_journal_id = fields.Many2one('account.journal',string="Bank Journal")
    