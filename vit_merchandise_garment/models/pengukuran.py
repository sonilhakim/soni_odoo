from odoo import models, fields, api, _

class pengukuranmd(models.Model):
    _name = "vit.pengukuran"
    _inherit = "vit.pengukuran"


    @api.multi 
    def action_done(self):
        res = super(pengukuranmd, self).action_done()
        sql = "update vit_boq_po_garmen_line set pengukuran_id = '%s' where po_id = %s" % (self.id, self.spk_line_id.spk_id.po_id.id)
        self.env.cr.execute(sql)
        return res


