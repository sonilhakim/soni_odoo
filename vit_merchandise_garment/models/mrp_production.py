from odoo import models, fields, api, exceptions, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.float_utils import float_is_zero, float_compare
from odoo.exceptions import ValidationError, RedirectWarning, UserError


class MrpProductionMD(models.Model):
	_inherit = "mrp.production"

	worksheet 	   = fields.Boolean( string="Worksheet")
	boq_po_line_id = fields.Many2one("vit.boq_po_garmen_line", "Style List")
	partner_id     = fields.Many2one( comodel_name="res.partner",  string="Customer",  help="", readonly=True, states={"confirmed" : [("readonly",False)]})
	spec_type = fields.Selection([('Normal','Normal'), ('SP','SP')], string="Spec Type", default='Normal')


	@api.multi
	def button_plan(self):
		res = super(MrpProductionMD, self).button_plan()

		for wo in self.workorder_ids:
			wo.spec_type = self.spec_type

		return res


	@api.multi
	def button_mark_done(self):
		res = super(MrpProductionMD, self).button_mark_done()
		for mrp in self:
			if mrp.boq_po_line_id :
				# self.env.cr.execute("update vit_boq_po_garmen_line set state=%s where id = %s",
				# ( 'done_mo', mrp.boq_po_line_id.id,))
				self.env.cr.execute("update mrp_production set state=%s where id != %s and request_detail_id = %s",
				( 'cancel', mrp.id, mrp.boq_po_line_id.id))
		return res
