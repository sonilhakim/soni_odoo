from odoo import api, models


class FormStock(models.AbstractModel):
    _name = 'report.vit_report_rekap_inventory.form_stock_tmpl'

    @api.model
    def _compute_form_stock(self, data):
        sql = """SELECT mr.date_planned_start, pav.name,
                    (SELECT sum(smi.quantity_done)
                     FROM stock_move smi
                     LEFT JOIN stock_picking spi ON smi.picking_id = spi.id
                     LEFT JOIN stock_picking_type spti ON spi.picking_type_id = spti.id
                     WHERE spi.state = 'done' AND spti.is_production is True AND smi.product_id = pp.id
                    ) as terima,
                    (SELECT sum(smo.quantity_done)
                     FROM stock_move smo
                     LEFT JOIN stock_picking spo ON smo.picking_id = spo.id
                     LEFT JOIN stock_picking_type spto ON spo.picking_type_id = spto.id
                     WHERE spo.state = 'done' AND spto.code = 'outgoing' AND smo.product_id = pp.id
                     ) as keluar,
                    pp.qty_available
                FROM product_product pp
                LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
                LEFT JOIN product_attribute_value_product_product_rel pavr ON pavr.product_product_id = pp.id
                LEFT JOIN product_attribute_value pav ON pavr.product_attribute_value_id = pav.id
                LEFT JOIN product_product ppm ON ppm.product_tmpl_id = pt.id
                LEFT JOIN mrp_production mr ON mr.product_id = ppm.id
                WHERE pt.id = %s AND mr.id IS NOT NULL
                GROUP BY pav.name, pp.id, mr.date_planned_start
                """

        self.env.cr.execute(sql, (data['style_id'],))
        result = self.env.cr.fetchall()
        return result

    @api.model
    def _get_report_values(self, docids, data=None):
        self.model = 'product.product'
        wiz_rec = self.env[self._context.get('active_model', False)].browse(self._context.get('active_ids', False))
        result = self._compute_form_stock(data)
        docargs = {
            'doc_ids': wiz_rec.ids,
            'doc_model': 'form.stock.wizard',
            'data': data,
            'docs': wiz_rec,
            'data_dict': result,
        }
        return docargs
