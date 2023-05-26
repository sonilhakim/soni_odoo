from odoo import api, fields, models, _
import time
from odoo.exceptions import UserError
from odoo.tools import float_utils, float_compare
import logging
_logger = logging.getLogger(__name__)

KONVERSI_STATES =[('draft','Draft'),('confirmed','Confirmed')]

class ProductKonversi(models.Model):
	_name = 'product.konversi'

	name 		= fields.Char("Number", required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
	conv_date  	= fields.Date(string="Date", required=False, default=lambda self:time.strftime("%Y-%m-%d"), readonly=True, states={"draft" : [("readonly",False)]} )
	detail_ids 	= fields.One2many(comodel_name="konversi.detail", inverse_name="conv_id", string="Detail", required=False, readonly=True, states={"draft" : [("readonly",False)]} )
	state 		= fields.Selection(string="State", selection=KONVERSI_STATES, readonly=True, default=KONVERSI_STATES[0][0])

	@api.multi
	def action_confirm(self):
		for konv in self:
			adjust = konv.env['stock.inventory']
			conv_details = []
			sql = """select product_asal_id, location_id, lot_asal, qty_asal,
					product_tujuan_id, location_dest_id, lot_tujuan, qty_tujuan
					from konversi_detail
					where conv_id = (%s)""" %(konv.id)

			self.env.cr.execute(sql)
			res = self.env.cr.fetchall()
			
			for z in res:
				product_asal = self.env['product.product'].browse(z[0])
				location_asal = self.env['stock.location'].browse(z[1])
				qty_onhand_asal = 0.0
				sqla = """select quantity
					from stock_quant
					where product_id = %s and location_id = %s"""
				if z[2] != None:
					lot_asal = self.env['stock.production.lot'].browse(z[2])
					sqla += " and lot_id = %s " %lot_asal.id
				else:
					sqla += " and lot_id is null "

				self.env.cr.execute(sqla,(product_asal.id,location_asal.id))
				resa = self.env.cr.fetchall()
				for a in resa:
					qty_onhand_asal = a[0]				
				# import pdb; pdb.set_trace()
				conv_details.append((0,0,{
					'product_id'        : z[0],
					'location_id'       : z[1],
					'prod_lot_id'       : z[2],
					'product_qty'       : qty_onhand_asal - z[3],
					}))
				
				product_tujuan = self.env['product.product'].browse(z[4])
				location_tujuan = self.env['stock.location'].browse(z[5])
				qty_onhand_tujuan = 0.0
				sqlt = """select quantity
					from stock_quant
					where product_id = %s and location_id = %s"""
				if z[6] != None:
					lot_tujuan = self.env['stock.production.lot'].browse(z[6])
					sqlt += " and lot_id = %s " %lot_tujuan.id
				else:
					sqlt += " and lot_id is null "
				self.env.cr.execute(sqlt,(product_tujuan.id,location_tujuan.id))
				rest = self.env.cr.fetchall()
				for t in rest:
					qty_onhand_tujuan = t[0]
				
				conv_details.append((0,0,{
				'product_id'        : z[4],
				'location_id'       : z[5],
				'prod_lot_id'       : z[6],
				'product_qty'       : qty_onhand_tujuan + z[7],
				}))

			adjust_id = adjust.create({
					'name': konv.name,
					'date': konv.conv_date,
					'line_ids': conv_details,
					})
			s_adjust = adjust.browse(adjust_id.id)
			s_adjust.action_start()
			s_adjust.action_validate()
			inventory_lines = s_adjust.line_ids.filtered(lambda l: l.product_id.tracking in ['lot', 'serial'] and not l.prod_lot_id and l.theoretical_qty != l.product_qty)
			lines = s_adjust.line_ids.filtered(lambda l: float_compare(l.product_qty, 1, precision_rounding=l.product_uom_id.rounding) > 0 and l.product_id.tracking == 'serial' and l.prod_lot_id)
			if inventory_lines and not lines:
				wiz_lines = [(0, 0, {'product_id': product.id, 'tracking': product.tracking}) for product in inventory_lines.mapped('product_id')]
				wiz = s_adjust.env['stock.track.confirmation'].create({'inventory_id': s_adjust.id, 'tracking_line_ids': wiz_lines})
				wiz.action_confirm()	

			self.state = KONVERSI_STATES[1][0]

	@api.model
	def create(self, vals):
		vals['name'] = self.env['ir.sequence'].next_by_code('vit.konversi.product')
		result = super(ProductKonversi, self).create(vals)
		return result

class product_konversi(models.Model):
	_name = 'konversi.detail'

	product_asal_id 	= fields.Many2one('product.product', 'Product Asal', required=True)
	product_tujuan_id 	= fields.Many2one('product.product', 'Product Tujuan', required=True)
	location_id 		= fields.Many2one('stock.location', 'Lokasi Asal', required=False)
	location_dest_id 	= fields.Many2one('stock.location', 'Lokasi Tujuan', required=False)
	qty_asal			= fields.Float('Qty Asal', default=0.0, required=False)
	lot_asal 			= fields.Many2one('stock.production.lot', 'Lot/SN Asal')
	lot_tujuan 			= fields.Many2one('stock.production.lot', 'Lot/SN Tujuan')
	qty_tujuan			= fields.Float('Qty Tujuan', compute='compute_qty_tujuan', required=False, store=True)
	conv_id				= fields.Many2one(comodel_name="product.konversi", string="Konversi", required=False, store=True)
	product_tracking    = fields.Selection('Tracking', related='product_asal_id.tracking', readonly=True)

	@api.depends('qty_asal','product_tujuan_id')
	def compute_qty_tujuan(self):
		for det in self:
			if det.product_asal_id.product_tmpl_id != det.product_tujuan_id.product_tmpl_id:
					raise UserError(_('Product Template Tujuan Harus Sama Dengan Product Template Asal'))
			else :
				if (det.product_asal_id.conv_value!=0) and (det.product_tujuan_id.conv_value!=0):
					det.qty_tujuan = (det.product_tujuan_id.conv_value / det.product_asal_id.conv_value) * det.qty_asal
