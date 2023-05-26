from odoo import api, models


class ReportStockAcc(models.AbstractModel):
    _name = 'report.vit_report_rekap_inventory.rekap_stock_acc_report_tmpl'

    @api.model
    def _compute_stock_acc(self, data):
        sql = """SELECT po.name, pt.default_code, pt.name, sm.quantity_done, um.name
                FROM stock_move sm
                LEFT JOIN stock_picking sp ON sm.picking_id = sp.id
                LEFT JOIN purchase_order po ON sp.origin = po.name
                LEFT JOIN product_product pp ON sm.product_id = pp.id
                LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
                LEFT JOIN product_category pc ON pt.categ_id = pc.id
                LEFT JOIN uom_uom um ON sm.product_uom = um.id
                LEFT JOIN stock_picking_type spt ON sp.picking_type_id = spt.id
                WHERE spt.name = %s AND pc.name = %s AND sp.state = %s
                """

        if data['date_from'] and data['date_to']:
            sql += " AND sp.date_done >= '%s' AND sp.date_done <= '%s' ORDER BY po.id " %(data['date_from'], data['date_to'])
        else:
            sql += "ORDER BY po.id"

        self.env.cr.execute(sql, ('Receipts', 'Accessories', 'done',))
        result = self.env.cr.fetchall()
        return result

    @api.model
    def _get_report_values(self, docids, data=None):
        self.model = 'stock.move'
        wiz_rec = self.env[self._context.get('active_model', False)].browse(self._context.get('active_ids', False))
        result = self._compute_stock_acc(data)
        docargs = {
            'doc_ids': wiz_rec.ids,
            'doc_model': 'rekap.stock.acc',
            'data': data,
            'docs': wiz_rec,
            'data_dict': result,
        }
        return docargs
