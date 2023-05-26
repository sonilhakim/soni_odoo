from odoo import models, fields, api, exceptions, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.float_utils import float_is_zero, float_compare
from odoo.exceptions import ValidationError, RedirectWarning, UserError


class MrpProductionSA(models.Model):
    _inherit = "mrp.production"

    approval_line_id   = fields.Many2one("vit.sample_approval_line", "Sample Aproval Line")

    @api.multi
    def button_mark_done(self):
        res = super(MrpProductionSA, self).button_mark_done()
        for mrp in self:
            if mrp.approval_line_id :
                self.env.cr.execute("update vit_sample_approval_line set state=%s where id = %s",
                ( 'done_mo', mrp.approval_line_id.id,))
                self.env.cr.execute("update mrp_production set state=%s where id != %s and request_detail_id = %s",
                ( 'cancel', mrp.id, mrp.approval_line_id.id))
        return res