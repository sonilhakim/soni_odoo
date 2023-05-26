from odoo import models, fields, api, exceptions, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.float_utils import float_is_zero, float_compare
from odoo.exceptions import ValidationError, RedirectWarning, UserError


class StockMove_repws(models.Model):
    _inherit = 'stock.move'

    acc_no      = fields.Char( string="ACC NO", compute="_get_materials", store=True, help="")
    spec        = fields.Char( string="Spec", compute="_get_materials", store=True, help="")
    colour      = fields.Char( string="Col", compute="_get_materials", store=True, help="" )
    cons        = fields.Float( string="Cons", compute="_get_materials", store=True, help="")

    @api.depends('raw_material_production_id.boq_po_line_id')
    def _get_materials(self):
        for sm in self:
            if sm.raw_material_production_id.boq_po_line_id:
                sql = """SELECT ml.acc_no, ml.spec, ml.colour, ml.cons
                        FROM vit_or_material_list ml
                        LEFT JOIN vit_boq_po_garmen_line bl ON ml.boq_id = bl.id
                        LEFT JOIN vit_purchase_order_garmen po ON bl.po_id = po.id
                        LEFT JOIN product_product pp ON ml.material = pp.id
                        LEFT JOIN stock_move sm ON sm.product_id = pp.id
                        LEFT JOIN product_template pt ON bl.product_id = pt.id
                        WHERE bl.id = %s AND pt.id = %s AND sm.id = %s
                        """
                self.env.cr.execute(sql, (sm.raw_material_production_id.boq_po_line_id.id,sm.raw_material_production_id.product_tmpl_id.id,sm.id))
                result = self.env.cr.fetchall()
                for res in result:
                    sm.update({'acc_no':res[0],
                               'spec'  :res[1],
                               'colour':res[2],
                               'cons'  :res[3],
                            })

StockMove_repws()