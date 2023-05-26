from odoo import api, fields, models, _
import time
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

class ReviseConfirm(models.TransientModel):
    _name = 'anggaran.revise_wizard'
    _description = 'Konfirmasi Revisi'

    notes = fields.Char(string='Notes', required=True)

    def _get_active_rka(self):
        if self._context.get('active_model') == 'anggaran.rka':
            return self._context.get('active_id', False)
        return False
    
    rka_id = fields.Many2one(comodel_name="anggaran.rka", string="RKA", required=True,
                                 default=_get_active_rka)

    """
    :return:
    """

    @api.multi
    def confirm_button(self):
        self.ensure_one()

        self.rka_id.revised_notes       = self.notes
        self.rka_id.revised_date        = time.strftime("%Y-%m-%d %H:%M:%S")
        self.rka_id.revised_by_id       = self.env.uid
        self.rka_id.source_picking_id = False

        new_rec = self.rka_id.action_revised()
        
        rka_form = self.env.ref('anggaran.view_rka_form', False)

        return {
            'name': _('RKA'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'anggaran.rka',
            'res_id': new_rec.id,
            'views': [(rka_form.id, 'form')],
            'view_id': rka_form.id,
            'target': 'current',
        }
