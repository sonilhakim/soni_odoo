from odoo import models, fields, api, exceptions, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.float_utils import float_is_zero, float_compare
from odoo.exceptions import ValidationError, RedirectWarning, UserError


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    request_detail_id   = fields.Many2one("vit.request_detail", "Request Detail")
    sample              = fields.Boolean( string="Sample")
    sample_room         = fields.Selection([('tebet', 'Tebet'),('cibinong', 'Cibinong')], string="Sample Room")

    @api.multi
    def button_mark_done(self):
        res = super(MrpProduction, self).button_mark_done()
        for mrp in self:
            if mrp.request_detail_id :
                self.env.cr.execute("update vit_request_detail set state=%s where id = %s",
                ( 'done_mo', mrp.request_detail_id.id,))
                self.env.cr.execute("update mrp_production set state=%s where id != %s and request_detail_id = %s",
                ( 'cancel', mrp.id, mrp.request_detail_id.id))
        return res